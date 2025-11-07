# 后端 Dockerfile
#
# 为什么使用多阶段构建？
# - 减小镜像体积
# - 分离构建环境和运行环境
# - 提高安全性

FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
# 为什么需要这些？
# - build-essential: 编译 Python 扩展需要
# - git: 某些 Python 包需要从 git 安装
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
# 使用 --no-cache-dir 减小镜像体积
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建上传目录
RUN mkdir -p /app/static/uploads

# 暴露端口
EXPOSE 8000

# 启动命令
# 为什么使用 uvicorn？
# - ASGI 服务器，支持 WebSocket
# - 高性能，异步处理
# - 生产级别的稳定性
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
