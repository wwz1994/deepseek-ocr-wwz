"""
FastAPI 主应用 - 后端入口

设计思路：
1. 使用 FastAPI 构建异步 Web 服务
2. 配置 CORS 允许前端跨域访问
3. 在启动时初始化 OCR 模型
4. 提供静态文件服务（用于访问上传的图片）
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from api.routes import router
from services.ocr_service import ocr_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理

    为什么需要 lifespan？
    - 在应用启动时初始化模型（耗时操作）
    - 在应用关闭时清理资源
    - 避免第一个请求时才加载模型（用户体验差）

    使用 asynccontextmanager：
    - yield 前的代码在启动时执行
    - yield 后的代码在关闭时执行
    """
    print("🚀 启动 DeepSeek-OCR 后端服务...")

    # 获取模型路径（优先使用环境变量）
    model_path = os.getenv("MODEL_PATH", "deepseek-ai/DeepSeek-OCR")
    print(f"📦 模型路径: {model_path}")

    # 初始化 OCR 服务
    await ocr_service.initialize(model_path)

    print("✅ 服务启动完成！")
    yield
    print("👋 服务正在关闭...")


# 创建 FastAPI 应用
app = FastAPI(
    title="DeepSeek-OCR API",
    description="DeepSeek-OCR 图像识别服务",
    version="1.0.0",
    lifespan=lifespan
)

# 配置 CORS - 允许跨域访问
"""
为什么需要 CORS？
- 前端和后端通常部署在不同端口或域名
- 浏览器的同源策略会阻止跨域请求
- 开发环境：前端 localhost:5173，后端 localhost:8000
- 生产环境：前端 example.com，后端 api.example.com

allow_origins=["*"]: 允许所有源（生产环境应该限制具体域名）
allow_credentials=True: 允许携带 Cookie
allow_methods=["*"]: 允许所有 HTTP 方法
allow_headers=["*"]: 允许所有请求头
"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应改为具体的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件目录
"""
为什么需要静态文件服务？
- 提供上传图片的访问路径
- 前端可以预览用户上传的图片
- 例如：http://localhost:8000/static/uploads/xxx.jpg
"""
app.mount(
    "/static",
    StaticFiles(directory="/home/user/DeepSeek-OCR/backend/static"),
    name="static"
)

# 注册路由
app.include_router(router, prefix="/api", tags=["OCR"])


@app.get("/")
async def root():
    """
    根路径 - 返回 API 信息
    """
    return {
        "name": "DeepSeek-OCR API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",  # Swagger UI 文档
        "model_initialized": ocr_service._initialized
    }


if __name__ == "__main__":
    """
    开发环境运行

    使用 uvicorn 运行 FastAPI：
    - host="0.0.0.0": 监听所有网络接口
    - port=8000: 端口号
    - reload=True: 代码修改自动重启（仅开发环境）
    - log_level="info": 日志级别
    """
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
