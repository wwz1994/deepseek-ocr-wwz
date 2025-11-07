/**
 * OCR 模式选择组件
 *
 * 功能：
 * 1. 展示可用的 OCR 模式
 * 2. 支持模式切换
 * 3. 显示模式说明
 * 4. 动态加载模式列表
 *
 * 设计思路：
 * - 使用卡片式布局，直观展示各个模式
 * - 选中状态高亮显示
 * - 响应式设计，移动端友好
 */
import React, { useEffect, useState } from 'react'
import { cn } from '@/lib/utils'
import type { OCRMode } from '@/types'
import { Loader2 } from 'lucide-react'

interface ModeSelectorProps {
  selectedMode: string
  onModeChange: (mode: string) => void
  disabled?: boolean
}

export const ModeSelector: React.FC<ModeSelectorProps> = ({
  selectedMode,
  onModeChange,
  disabled = false
}) => {
  const [modes, setModes] = useState<OCRMode[]>([])
  const [loading, setLoading] = useState(true)
  const [showAdvanced, setShowAdvanced] = useState(false)

  /**
   * 从服务器加载模式列表
   *
   * 为什么动态加载？
   * - 后端可能扩展新模式
   * - 集中管理模式配置
   * - 便于国际化和自定义
   */
  useEffect(() => {
    const loadModes = async () => {
      try {
        const response = await fetch('/api/modes')
        const data = await response.json()
        setModes(data.modes)
      } catch (error) {
        console.error('加载模式失败:', error)
        // 使用默认模式
        setModes([
          {
            id: 'free_ocr',
            name: '自由 OCR',
            description: '纯文本提取',
            icon: '📝'
          }
        ])
      } finally {
        setLoading(false)
      }
    }

    loadModes()
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <Loader2 className="w-8 h-8 animate-spin text-primary-500" />
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {/* 标题 */}
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
          识别模式
        </h3>
        <label className="flex items-center gap-2 text-sm">
          <input
            type="checkbox"
            checked={showAdvanced}
            onChange={(e) => setShowAdvanced(e.target.checked)}
            className="rounded"
          />
          <span className="text-gray-600 dark:text-gray-400">显示高级选项</span>
        </label>
      </div>

      {/* 模式列表 */}
      <div className="grid grid-cols-1 gap-3">
        {modes.map((mode) => (
          <button
            key={mode.id}
            onClick={() => onModeChange(mode.id)}
            disabled={disabled}
            className={cn(
              'p-4 rounded-lg border-2 text-left transition-all',
              'hover:shadow-md disabled:opacity-50 disabled:cursor-not-allowed',
              selectedMode === mode.id
                ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
                : 'border-gray-200 dark:border-gray-700 hover:border-primary-300 dark:hover:border-primary-700'
            )}
          >
            <div className="flex items-start gap-3">
              {/* 图标 */}
              <span className="text-2xl">{mode.icon}</span>

              {/* 内容 */}
              <div className="flex-1 min-w-0">
                <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-1">
                  {mode.name}
                </h4>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {mode.description}
                </p>
              </div>

              {/* 选中标记 */}
              {selectedMode === mode.id && (
                <div className="w-5 h-5 rounded-full bg-primary-500 flex items-center justify-center flex-shrink-0">
                  <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                </div>
              )}
            </div>
          </button>
        ))}
      </div>

      {/* 高级选项 */}
      {showAdvanced && (
        <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg animate-fade-in">
          <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-3">
            高级选项
          </h4>
          <div className="space-y-3 text-sm">
            <label className="flex items-center gap-2">
              <input
                type="checkbox"
                defaultChecked
                className="rounded"
              />
              <span className="text-gray-700 dark:text-gray-300">
                动态分辨率裁剪 (推荐)
              </span>
            </label>
            <p className="text-xs text-gray-500 dark:text-gray-400 ml-6">
              对大图进行智能裁剪，提升识别效果
            </p>
          </div>
        </div>
      )}
    </div>
  )
}
