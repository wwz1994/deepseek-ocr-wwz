# DeepSeek-OCR Web 前端

<div align="center">

![DeepSeek-OCR](https://img.shields.io/badge/DeepSeek-OCR-blue)
![React](https://img.shields.io/badge/React-18-61dafb)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178c6)
![Tailwind](https://img.shields.io/badge/Tailwind-3-38bdf8)

一个现代化的 DeepSeek-OCR Web 界面，支持实时流式输出和多种识别模式。

[在线演示](#) | [快速开始](#快速开始) | [功能特性](#功能特性) | [技术栈](#技术栈)

</div>

---

## ✨ 功能特性

### 🎯 核心功能

- **📤 多种上传方式**
  - 拖拽上传
  - 点击选择文件
  - Ctrl+V 粘贴上传
  - 实时预览

- **🔍 5 种识别模式**
  - 📝 自由 OCR - 纯文本提取
  - 📄 文档转 Markdown - 保留文档结构
  - 📍 带定位的 OCR - 标注位置信息
  - 📊 图表解析 - 解析图表数据
  - 🖼️ 图像描述 - 生成详细描述

- **⚡ 实时流式输出**
  - WebSocket 实时通信
  - 逐字显示识别进度
  - 识别时长统计
  - 错误实时反馈

- **📋 结果处理**
  - Markdown 格式渲染
  - 代码高亮显示
  - 一键复制结果
  - 下载为文件

- **🎨 现代化 UI**
  - 响应式设计（支持移动端）
  - 深色/浅色主题切换
  - 流畅动画效果
  - 直观的用户体验

---

## 🚀 快速开始

### 使用 Docker（推荐）

```bash
# 一键启动
docker-compose up -d

# 访问应用
open http://localhost
```

### 本地开发

#### 后端

```bash
# 1. 安装依赖
cd backend
pip install -r requirements.txt

# 2. 启动后端
python app.py
```

#### 前端

```bash
# 1. 安装依赖
cd frontend
npm install

# 2. 启动开发服务器
npm run dev

# 3. 访问应用
open http://localhost:5173
```

详细部署说明请参考 [DEPLOYMENT.md](./DEPLOYMENT.md)

---

## 🛠️ 技术栈

### 后端

| 技术 | 用途 | 为什么选择它 |
|------|------|-------------|
| **FastAPI** | Web 框架 | 高性能、异步支持、自动文档 |
| **vLLM** | 模型推理 | 极速推理、GPU 优化 |
| **WebSocket** | 实时通信 | 流式输出、低延迟 |
| **Uvicorn** | ASGI 服务器 | 生产级稳定性 |

### 前端

| 技术 | 用途 | 为什么选择它 |
|------|------|-------------|
| **React 18** | UI 框架 | 组件化、生态丰富 |
| **TypeScript** | 类型系统 | 类型安全、减少错误 |
| **Vite** | 构建工具 | 极速开发、优化构建 |
| **Tailwind CSS** | 样式框架 | 快速开发、响应式 |
| **React Markdown** | Markdown 渲染 | 支持 OCR 输出格式 |
| **Lucide React** | 图标库 | 现代、一致的图标 |

### 部署

| 技术 | 用途 |
|------|------|
| **Docker** | 容器化 |
| **Docker Compose** | 多容器编排 |
| **Nginx** | 反向代理、静态服务 |

---

## 📁 项目结构

```
DeepSeek-OCR/
├── backend/                    # 后端服务
│   ├── api/
│   │   └── routes.py          # API 路由
│   ├── services/
│   │   └── ocr_service.py     # OCR 核心服务
│   ├── static/
│   │   └── uploads/           # 上传文件存储
│   ├── app.py                 # FastAPI 主应用
│   ├── requirements.txt       # Python 依赖
│   └── Dockerfile            # 后端容器配置
│
├── frontend/                  # 前端应用
│   ├── src/
│   │   ├── components/       # React 组件
│   │   │   ├── ImageUpload.tsx      # 图片上传
│   │   │   ├── ModeSelector.tsx     # 模式选择
│   │   │   ├── OCRResult.tsx        # 结果展示
│   │   │   └── ThemeToggle.tsx      # 主题切换
│   │   ├── lib/
│   │   │   └── utils.ts      # 工具函数
│   │   ├── types/
│   │   │   └── index.ts      # 类型定义
│   │   ├── App.tsx           # 主应用组件
│   │   ├── main.tsx          # 入口文件
│   │   └── index.css         # 全局样式
│   ├── package.json          # Node 依赖
│   ├── vite.config.ts        # Vite 配置
│   ├── nginx.conf            # Nginx 配置
│   └── Dockerfile            # 前端容器配置
│
├── docker-compose.yml         # Docker Compose 配置
├── DEPLOYMENT.md             # 部署文档
└── FRONTEND_README.md        # 本文档
```

---

## 🎨 设计亮点

### 1. 流式输出设计

```typescript
// WebSocket 实时接收 OCR 结果
ws.onmessage = (event) => {
  const message = JSON.parse(event.data)

  if (message.type === 'progress') {
    // 逐字追加内容，实时展示
    setContent(prev => prev + message.content)
  }
}
```

**为什么这样设计？**
- ✅ 用户实时看到识别进度
- ✅ 避免长时间等待的焦虑感
- ✅ 类似 ChatGPT 的流畅体验

### 2. 模式选择设计

```tsx
// 卡片式模式选择，直观清晰
<ModeSelector
  modes={[
    { id: 'free_ocr', name: '自由 OCR', icon: '📝' },
    { id: 'document_markdown', name: '文档转 Markdown', icon: '📄' },
    // ...
  ]}
/>
```

**为什么这样设计？**
- ✅ 图标 + 文字，降低学习成本
- ✅ 卡片式布局，移动端友好
- ✅ 动态加载，便于扩展

### 3. 响应式布局

```css
/* 桌面端：左右分栏 */
.grid { grid-template-columns: 1fr 1fr; }

/* 移动端：上下堆叠 */
@media (max-width: 1024px) {
  .grid { grid-template-columns: 1fr; }
}
```

**为什么这样设计？**
- ✅ 桌面端充分利用屏幕空间
- ✅ 移动端优化触摸体验
- ✅ 自动适配不同设备

---

## 🔌 API 文档

### REST API

#### 1. 健康检查

```http
GET /api/health
```

响应:
```json
{
  "status": "healthy",
  "model_initialized": true
}
```

#### 2. 上传图片

```http
POST /api/upload
Content-Type: multipart/form-data

file: <binary>
```

响应:
```json
{
  "file_id": "uuid-here",
  "filename": "image.jpg",
  "file_path": "/path/to/file",
  "message": "上传成功"
}
```

#### 3. 获取支持的模式

```http
GET /api/modes
```

响应:
```json
{
  "modes": [
    {
      "id": "free_ocr",
      "name": "自由 OCR",
      "description": "纯文本提取",
      "icon": "📝"
    }
    // ...
  ]
}
```

### WebSocket API

#### OCR 识别

```
WS /api/ws/ocr
```

发送:
```json
{
  "file_id": "uuid-here",
  "mode": "document_markdown",
  "crop_mode": true
}
```

接收:
```json
// 开始识别
{ "type": "start", "message": "开始识别..." }

// 进度更新（多次）
{ "type": "progress", "content": "识别的文本片段..." }

// 识别完成
{ "type": "complete", "message": "识别完成" }

// 识别错误
{ "type": "error", "message": "错误信息" }
```

---

## 🎯 使用示例

### 示例 1: 识别文档

1. 上传文档图片（支持拖拽）
2. 选择"文档转 Markdown"模式
3. 等待识别完成（实时显示进度）
4. 复制或下载 Markdown 结果

### 示例 2: 提取表格

1. 上传包含表格的图片
2. 选择"带定位的 OCR"模式
3. 识别结果会包含表格的 Markdown 格式
4. 可直接粘贴到文档中使用

### 示例 3: 解析图表

1. 上传图表截图
2. 选择"图表解析"模式
3. 获得图表中的数据和说明
4. 用于数据分析或报告

---

## 🐛 常见问题

### Q: 上传后识别很慢？

**A**: 可能的原因：
- 图片过大（建议压缩到 5MB 以下）
- GPU 显存不足（查看后端日志）
- 网络延迟（检查 WebSocket 连接）

### Q: WebSocket 连接失败？

**A**: 检查：
1. 后端是否正常运行：`curl http://localhost:8000/health`
2. Nginx 配置是否正确（查看 `frontend/nginx.conf`）
3. 浏览器控制台错误信息

### Q: 识别结果不准确？

**A**: 尝试：
1. 使用"文档转 Markdown"模式（效果最好）
2. 确保图片清晰、光线充足
3. 启用"动态分辨率裁剪"选项

### Q: 如何自定义主题？

**A**: 编辑 `frontend/tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      primary: {
        500: '#your-color',
        // ...
      }
    }
  }
}
```

---

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 如何贡献

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 代码规范

- **TypeScript**: 使用严格模式
- **React**: 使用函数组件和 Hooks
- **样式**: 使用 Tailwind CSS
- **注释**: 重要逻辑添加中文注释

---

## 📊 性能指标

| 指标 | 值 |
|------|-----|
| 首屏加载时间 | < 1s |
| 文件上传速度 | 取决于网络 |
| OCR 识别速度 | 2-10s/页（A100） |
| 内存使用 | 前端 < 100MB，后端 8-16GB |
| 浏览器兼容性 | Chrome 90+, Firefox 88+, Safari 14+ |

---

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](./LICENSE) 文件。

---

## 🙏 致谢

- [DeepSeek AI](https://www.deepseek.com/) - 提供强大的 OCR 模型
- [vLLM](https://github.com/vllm-project/vllm) - 高性能推理引擎
- [React](https://react.dev/) - UI 框架
- [Tailwind CSS](https://tailwindcss.com/) - 样式框架

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给我们一个 Star！**

Made with ❤️ by DeepSeek AI

</div>
