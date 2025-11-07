# DeepSeek-OCR 前端部署指南

本文档详细说明如何部署和运行 DeepSeek-OCR Web 应用。

## 📋 目录

- [系统要求](#系统要求)
- [快速开始](#快速开始)
- [开发环境部署](#开发环境部署)
- [生产环境部署](#生产环境部署)
- [故障排查](#故障排查)
- [性能优化](#性能优化)

---

## 🖥️ 系统要求

### 硬件要求

- **GPU**: NVIDIA GPU（推荐 A100/V100，最低 8GB 显存）
- **内存**: 最低 16GB RAM（推荐 32GB+）
- **存储**: 最低 50GB 可用空间
- **CPU**: 4 核心以上

### 软件要求

- **操作系统**: Ubuntu 20.04+ / CentOS 7+ / macOS
- **CUDA**: 11.8+ (如使用 GPU)
- **Docker**: 20.10+
- **Docker Compose**: 2.0+
- **NVIDIA Container Toolkit**: 最新版本（GPU 部署必需）
- **Node.js**: 18+ (仅开发环境)
- **Python**: 3.12+ (仅开发环境)

---

## 🚀 快速开始

### 方式一：Docker Compose 一键部署（推荐）

```bash
# 1. 克隆仓库
git clone https://github.com/deepseek-ai/DeepSeek-OCR.git
cd DeepSeek-OCR

# 2. 启动服务
docker-compose up -d

# 3. 查看日志
docker-compose logs -f

# 4. 访问应用
# 浏览器打开 http://localhost
```

**就是这么简单！** 🎉

---

## 💻 开发环境部署

适合本地开发和调试。

### 后端部署

```bash
# 1. 进入后端目录
cd backend

# 2. 创建 Python 虚拟环境
conda create -n deepseek-ocr python=3.12.9 -y
conda activate deepseek-ocr

# 3. 安装依赖
# 首先安装 PyTorch
pip install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu118

# 安装 vLLM（从项目根目录）
cd ..
pip install vllm-0.8.5+cu118-cp38-abi3-manylinux1_x86_64.whl

# 安装主项目依赖
pip install -r requirements.txt
pip install flash-attn==2.7.3 --no-build-isolation

# 安装后端 API 依赖
cd backend
pip install -r requirements.txt

# 4. 启动后端服务
python app.py

# 后端运行在 http://localhost:8000
# API 文档: http://localhost:8000/docs
```

### 前端部署

```bash
# 1. 进入前端目录
cd frontend

# 2. 安装依赖
npm install

# 3. 启动开发服务器
npm run dev

# 前端运行在 http://localhost:5173
```

### 环境变量配置

创建 `backend/.env` 文件：

```bash
# 模型路径（可以是 HuggingFace 路径或本地路径）
MODEL_PATH=deepseek-ai/DeepSeek-OCR

# GPU 设置
CUDA_VISIBLE_DEVICES=0

# 服务器设置
HOST=0.0.0.0
PORT=8000
```

---

## 🏭 生产环境部署

### 前提条件检查

```bash
# 1. 检查 NVIDIA 驱动
nvidia-smi

# 2. 检查 Docker GPU 支持
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu20.04 nvidia-smi

# 3. 检查 Docker Compose
docker-compose --version
```

### 部署步骤

#### 1. 克隆仓库

```bash
git clone https://github.com/deepseek-ai/DeepSeek-OCR.git
cd DeepSeek-OCR
```

#### 2. 配置环境变量

编辑 `docker-compose.yml`，根据实际情况修改：

```yaml
services:
  backend:
    environment:
      # 模型路径
      - MODEL_PATH=deepseek-ai/DeepSeek-OCR
      # GPU 编号
      - CUDA_VISIBLE_DEVICES=0

    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1  # GPU 数量
              capabilities: [gpu]
```

#### 3. 构建镜像

```bash
# 构建所有服务
docker-compose build

# 或分别构建
docker-compose build backend
docker-compose build frontend
```

#### 4. 启动服务

```bash
# 后台运行
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f backend
docker-compose logs -f frontend
```

#### 5. 健康检查

```bash
# 检查后端健康状态
curl http://localhost:8000/health

# 检查前端
curl http://localhost/
```

#### 6. 访问应用

浏览器打开: `http://your-server-ip`

### 使用 Nginx 反向代理（可选）

如果已有 Nginx 服务器，可以添加以下配置：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端
    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# HTTPS 配置（推荐）
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto https;
    }
}
```

---

## 🔧 管理命令

### Docker Compose 常用命令

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose stop

# 重启服务
docker-compose restart

# 停止并删除容器
docker-compose down

# 查看日志
docker-compose logs -f [service_name]

# 进入容器
docker-compose exec backend bash
docker-compose exec frontend sh

# 查看资源使用
docker stats

# 重新构建并启动
docker-compose up -d --build
```

### 更新部署

```bash
# 1. 拉取最新代码
git pull origin main

# 2. 重新构建
docker-compose build

# 3. 重启服务
docker-compose up -d

# 4. 清理旧镜像
docker image prune -f
```

---

## 🐛 故障排查

### 问题 1: 后端启动失败

**症状**: `docker-compose logs backend` 显示模型加载错误

**解决方案**:

```bash
# 检查 GPU 是否可用
docker-compose exec backend nvidia-smi

# 检查模型路径
docker-compose exec backend python -c "from transformers import AutoModel; print(AutoModel.from_pretrained('deepseek-ai/DeepSeek-OCR'))"

# 手动下载模型
docker-compose exec backend bash
pip install huggingface_hub
huggingface-cli download deepseek-ai/DeepSeek-OCR
```

### 问题 2: 前端无法连接后端

**症状**: 浏览器控制台显示网络错误

**解决方案**:

```bash
# 检查后端是否运行
curl http://localhost:8000/health

# 检查 Docker 网络
docker network ls
docker network inspect deepseek-ocr_ocr-network

# 重启服务
docker-compose restart
```

### 问题 3: WebSocket 连接失败

**症状**: OCR 识别无响应

**解决方案**:

```bash
# 检查 Nginx 配置
docker-compose exec frontend cat /etc/nginx/conf.d/default.conf

# 测试 WebSocket 连接
wscat -c ws://localhost/api/ws/ocr

# 查看后端日志
docker-compose logs -f backend | grep -i websocket
```

### 问题 4: 显存不足

**症状**: CUDA out of memory

**解决方案**:

编辑 `backend/services/ocr_service.py`:

```python
# 降低 GPU 显存使用率
engine_args = AsyncEngineArgs(
    ...
    gpu_memory_utilization=0.5,  # 从 0.75 降到 0.5
)
```

### 问题 5: 文件上传失败

**症状**: 上传后提示错误

**解决方案**:

```bash
# 检查上传目录权限
docker-compose exec backend ls -la /app/static/uploads

# 修复权限
docker-compose exec backend chmod 777 /app/static/uploads

# 检查磁盘空间
df -h
```

---

## ⚡ 性能优化

### 1. GPU 优化

```yaml
# docker-compose.yml
backend:
  deploy:
    resources:
      reservations:
        devices:
          - driver: nvidia
            count: all  # 使用所有可用 GPU
            capabilities: [gpu]
  environment:
    # 使用多 GPU
    - CUDA_VISIBLE_DEVICES=0,1
```

### 2. 模型优化

```python
# backend/services/ocr_service.py

# 使用 FP16 加速
engine_args = AsyncEngineArgs(
    ...
    dtype="float16",  # 或 "bfloat16"
)

# 增加并行请求数
engine_args = AsyncEngineArgs(
    ...
    max_num_seqs=16,  # 默认值，可根据显存调整
)
```

### 3. 前端优化

```bash
# 启用生产模式优化
cd frontend
npm run build

# 结果会更小、更快
ls -lh dist/
```

### 4. 缓存优化

```nginx
# frontend/nginx.conf

# 增加静态资源缓存时间
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 30d;
    add_header Cache-Control "public, immutable";
}
```

### 5. 并发优化

```yaml
# docker-compose.yml
backend:
  command: uvicorn app:app --host 0.0.0.0 --port 8000 --workers 2
  # 增加 worker 数量（注意 GPU 显存）
```

---

## 📊 监控

### 日志监控

```bash
# 实时日志
docker-compose logs -f

# 只看错误日志
docker-compose logs backend | grep -i error

# 保存日志到文件
docker-compose logs > logs.txt
```

### 资源监控

```bash
# 容器资源使用
docker stats

# GPU 使用情况
watch -n 1 nvidia-smi
```

### 性能指标

- **识别速度**: 应在 2-10 秒/页（取决于图片大小和 GPU）
- **内存使用**: 后端通常占用 8-16GB
- **GPU 利用率**: 识别时应接近 100%

---

## 🔐 安全建议

1. **使用 HTTPS**: 生产环境必须启用 SSL/TLS
2. **限制文件大小**: 在 Nginx 中设置 `client_max_body_size`
3. **添加认证**: 实现 JWT 或 OAuth 认证
4. **定期更新**: 保持依赖库最新
5. **防火墙**: 只开放必要端口

---

## 📞 获取帮助

- **GitHub Issues**: https://github.com/deepseek-ai/DeepSeek-OCR/issues
- **Discord**: https://discord.gg/Tc7c45Zzu5
- **文档**: https://github.com/deepseek-ai/DeepSeek-OCR

---

## 📄 许可证

本项目采用 MIT 许可证。详见 LICENSE 文件。
