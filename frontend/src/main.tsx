/**
 * React 应用入口文件
 *
 * 职责：
 * 1. 导入全局样式
 * 2. 渲染根组件
 * 3. 挂载到 DOM
 */
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
