/**
 * Tailwind CSS 配置
 *
 * 为什么使用 Tailwind CSS？
 * 1. 实用优先：通过组合 class 快速构建 UI
 * 2. 响应式：内置响应式设计工具类
 * 3. 深色模式：原生支持主题切换
 * 4. 体积小：PurgeCSS 自动移除未使用的样式
 */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      // 自定义颜色
      colors: {
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
        },
      },
      // 自定义动画
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
    },
  },
  plugins: [],
  // 深色模式配置
  darkMode: 'class',
}
