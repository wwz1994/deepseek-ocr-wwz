/**
 * Vite 配置文件
 *
 * 为什么使用 Vite？
 * 1. 极速的开发服务器启动（使用 ESBuild）
 * 2. 热模块替换（HMR）- 代码修改即时生效
 * 3. 优化的生产构建（使用 Rollup）
 * 4. 原生 ES 模块支持
 */
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],

  // 路径别名配置
  // 使用 @ 代替 src，简化导入路径
  // 例如：import { cn } from '@/lib/utils' 而不是 '../../lib/utils'
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },

  // 开发服务器配置
  server: {
    port: 5173,
    host: '0.0.0.0',  // 允许外部访问

    // 配置代理，解决开发环境跨域问题
    // 前端请求 /api 会被转发到后端 http://localhost:8000
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      // WebSocket 代理
      '/ws': {
        target: 'ws://localhost:8000',
        ws: true,
      },
    },
  },

  // 生产构建配置
  build: {
    outDir: 'dist',
    sourcemap: false,  // 生产环境不生成 source map

    // 代码分割优化
    rollupOptions: {
      output: {
        manualChunks: {
          // 将 React 相关库打包到单独的 chunk
          'react-vendor': ['react', 'react-dom'],
          // 将 Markdown 相关库打包到单独的 chunk
          'markdown-vendor': ['react-markdown'],
        },
      },
    },
  },
})
