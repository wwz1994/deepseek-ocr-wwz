# 前端 Dockerfile - 多阶段构建
#
# 阶段1：构建阶段 - 编译 React 应用
# 阶段2：生产阶段 - 使用 Nginx 提供静态文件服务

# ========== 构建阶段 ==========
FROM node:18-alpine AS builder

WORKDIR /app

# 复制 package 文件
COPY package*.json ./

# 安装依赖
# 为什么使用 npm ci？
# - 比 npm install 更快
# - 基于 package-lock.json，确保一致性
# - 适合 CI/CD 环境
RUN npm ci

# 复制源代码
COPY . .

# 构建生产版本
# Vite 会优化代码：压缩、tree-shaking、code-splitting
RUN npm run build

# ========== 生产阶段 ==========
FROM nginx:alpine

# 复制自定义 Nginx 配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 从构建阶段复制编译好的文件
COPY --from=builder /app/dist /usr/share/nginx/html

# 暴露端口
EXPOSE 80

# Nginx 会自动启动
CMD ["nginx", "-g", "daemon off;"]
