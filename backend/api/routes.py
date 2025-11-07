"""
API Routes - FastAPI 路由定义

设计思路：
1. REST API: 用于文件上传和基本操作
2. WebSocket: 用于实时流式输出 OCR 结果
3. CORS: 允许前端跨域访问
"""
import os
import uuid
from fastapi import APIRouter, UploadFile, File, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
import json

from services.ocr_service import ocr_service

router = APIRouter()

# 上传文件保存目录
UPLOAD_DIR = "/home/user/DeepSeek-OCR/backend/static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("/health")
async def health_check():
    """
    健康检查接口

    为什么需要？
    - 用于 Docker 容器健康检查
    - 用于负载均衡器探测服务状态
    - 返回模型是否已初始化
    """
    return {
        "status": "healthy",
        "model_initialized": ocr_service._initialized
    }


@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    """
    图片上传接口

    设计考虑：
    1. 使用 UUID 作为文件名，避免文件名冲突
    2. 验证文件类型，只接受图片格式
    3. 返回文件 ID，供后续 OCR 请求使用

    为什么分离上传和处理？
    - 上传快速完成，给用户即时反馈
    - 处理耗时，通过 WebSocket 异步进行
    - 支持同一张图片多次处理（不同模式）
    """
    # 验证文件类型
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="只支持图片文件")

    # 生成唯一文件名
    file_id = str(uuid.uuid4())
    file_extension = os.path.splitext(file.filename)[1] or '.jpg'
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}{file_extension}")

    # 保存文件
    try:
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件保存失败: {str(e)}")

    return {
        "file_id": file_id,
        "filename": file.filename,
        "file_path": file_path,
        "message": "上传成功"
    }


@router.websocket("/ws/ocr")
async def websocket_ocr(websocket: WebSocket):
    """
    WebSocket OCR 接口 - 实时流式输出

    为什么使用 WebSocket？
    1. 双向通信：服务器可以主动推送消息
    2. 长连接：避免 HTTP 轮询开销
    3. 低延迟：实时推送 OCR 识别结果

    消息格式：
    客户端 -> 服务器:
    {
        "file_id": "xxx",
        "mode": "free_ocr",
        "crop_mode": true
    }

    服务器 -> 客户端:
    {
        "type": "progress",  // progress | complete | error
        "content": "识别的文本...",
        "message": "状态消息"
    }
    """
    await websocket.accept()
    print("✅ WebSocket 客户端已连接")

    try:
        # 接收客户端请求
        data = await websocket.receive_text()
        request = json.loads(data)

        file_id = request.get("file_id")
        mode = request.get("mode", "free_ocr")
        crop_mode = request.get("crop_mode", True)

        if not file_id:
            await websocket.send_json({
                "type": "error",
                "message": "缺少 file_id 参数"
            })
            await websocket.close()
            return

        # 查找文件
        file_path = None
        for ext in ['.jpg', '.jpeg', '.png', '.bmp', '.webp']:
            potential_path = os.path.join(UPLOAD_DIR, f"{file_id}{ext}")
            if os.path.exists(potential_path):
                file_path = potential_path
                break

        if not file_path:
            await websocket.send_json({
                "type": "error",
                "message": "文件不存在"
            })
            await websocket.close()
            return

        # 发送开始消息
        await websocket.send_json({
            "type": "start",
            "message": "开始识别..."
        })

        # 流式处理 OCR
        async for text_chunk in ocr_service.process_image(
            file_path, mode, crop_mode
        ):
            if text_chunk.startswith("ERROR:"):
                await websocket.send_json({
                    "type": "error",
                    "message": text_chunk
                })
                break
            else:
                await websocket.send_json({
                    "type": "progress",
                    "content": text_chunk
                })

        # 发送完成消息
        await websocket.send_json({
            "type": "complete",
            "message": "识别完成"
        })

    except WebSocketDisconnect:
        print("⚠️ WebSocket 客户端断开连接")
    except Exception as e:
        print(f"❌ WebSocket 错误: {str(e)}")
        try:
            await websocket.send_json({
                "type": "error",
                "message": f"处理失败: {str(e)}"
            })
        except:
            pass
    finally:
        try:
            await websocket.close()
        except:
            pass


@router.get("/modes")
async def get_modes():
    """
    获取支持的 OCR 模式

    为什么需要这个接口？
    - 前端动态加载模式列表
    - 便于后续扩展新模式
    - 提供模式说明，帮助用户选择
    """
    return {
        "modes": [
            {
                "id": "free_ocr",
                "name": "自由 OCR",
                "description": "纯文本提取，不保留布局结构",
                "icon": "📝"
            },
            {
                "id": "document_markdown",
                "name": "文档转 Markdown",
                "description": "保留文档结构，转换为 Markdown 格式",
                "icon": "📄"
            },
            {
                "id": "ocr_grounding",
                "name": "带定位的 OCR",
                "description": "识别文本并标注位置信息",
                "icon": "📍"
            },
            {
                "id": "parse_figure",
                "name": "图表解析",
                "description": "解析图表、图形中的信息",
                "icon": "📊"
            },
            {
                "id": "describe_image",
                "name": "图像描述",
                "description": "生成详细的图像描述",
                "icon": "🖼️"
            }
        ]
    }
