/**
 * 主题切换组件
 *
 * 功能：
 * 1. 浅色/深色主题切换
 * 2. 保存用户偏好
 * 3. 响应系统主题变化
 *
 * 实现原理：
 * - 使用 localStorage 持久化用户选择
 * - 通过添加/移除 'dark' class 控制主题
 * - 支持系统主题自动匹配
 */
import React, { useEffect, useState } from 'react'
import { Moon, Sun } from 'lucide-react'

export const ThemeToggle: React.FC = () => {
  const [isDark, setIsDark] = useState(false)

  useEffect(() => {
    // 读取保存的主题或使用系统主题
    const savedTheme = localStorage.getItem('theme')
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches

    const shouldBeDark = savedTheme === 'dark' || (!savedTheme && systemPrefersDark)
    setIsDark(shouldBeDark)
    updateTheme(shouldBeDark)
  }, [])

  const updateTheme = (dark: boolean) => {
    if (dark) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }

  const toggleTheme = () => {
    const newTheme = !isDark
    setIsDark(newTheme)
    updateTheme(newTheme)
    localStorage.setItem('theme', newTheme ? 'dark' : 'light')
  }

  return (
    <button
      onClick={toggleTheme}
      className="p-2 rounded-lg bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
      title={isDark ? '切换到浅色模式' : '切换到深色模式'}
    >
      {isDark ? (
        <Sun className="w-5 h-5 text-yellow-500" />
      ) : (
        <Moon className="w-5 h-5 text-gray-700" />
      )}
    </button>
  )
}
