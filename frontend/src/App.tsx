/**
 * 主应用组件
 *
 * 布局结构：
 * - 顶部导航栏（标题 + 主题切换）
 * - 主内容区：
 *   - 左侧：图片上传 + 模式选择
 *   - 右侧：OCR 结果展示
 *
 * 状态管理：
 * - uploadedFile: 上传的文件信息
 * - selectedMode: 选中的 OCR 模式
 *
 * 数据流：
 * 1. 用户上传图片 -> ImageUpload
 * 2. 文件信息传递给 OCRResult
 * 3. OCRResult 通过 WebSocket 获取识别结果
 * 4. 实时展示识别内容
 */
import { useState } from 'react'
import { ImageUpload } from '@/components/ImageUpload'
import { ModeSelector } from '@/components/ModeSelector'
import { OCRResult } from '@/components/OCRResult'
import { ThemeToggle } from '@/components/ThemeToggle'
import { Scan } from 'lucide-react'
import type { UploadedFile } from '@/types'

function App() {
  const [uploadedFile, setUploadedFile] = useState<UploadedFile | null>(null)
  const [selectedMode, setSelectedMode] = useState('document_markdown')
  const [processing, setProcessing] = useState(false)

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors">
      {/* 导航栏 */}
      <nav className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 sticky top-0 z-10">
        <div className="max-w-[1800px] mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            {/* Logo 和标题 */}
            <div className="flex items-center gap-3">
              <div className="p-2 bg-gradient-to-br from-primary-500 to-primary-600 rounded-lg">
                <Scan className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900 dark:text-gray-100">
                  DeepSeek-OCR
                </h1>
                <p className="text-xs text-gray-500 dark:text-gray-400">
                  强大的图像文字识别工具
                </p>
              </div>
            </div>

            {/* 右侧操作 */}
            <div className="flex items-center gap-3">
              <ThemeToggle />
              <a
                href="https://github.com/deepseek-ai/DeepSeek-OCR"
                target="_blank"
                rel="noopener noreferrer"
                className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-gray-100 transition-colors"
              >
                GitHub
              </a>
            </div>
          </div>
        </div>
      </nav>

      {/* 主内容区 */}
      <main className="max-w-[1800px] mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 h-[calc(100vh-120px)]">
          {/* 左侧 - 上传和设置 */}
          <div className="flex flex-col gap-6 overflow-y-auto custom-scrollbar">
            {/* 上传区域 */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
                上传图片
              </h2>
              <ImageUpload
                onUploadSuccess={(file) => {
                  setUploadedFile(file)
                  setProcessing(true)
                }}
                disabled={processing}
              />
            </div>

            {/* 模式选择 */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
              <ModeSelector
                selectedMode={selectedMode}
                onModeChange={(mode) => {
                  setSelectedMode(mode)
                  // 如果已经有上传的文件，切换模式会触发重新识别
                  if (uploadedFile) {
                    setUploadedFile({ ...uploadedFile })
                  }
                }}
                disabled={processing}
              />
            </div>

            {/* 使用说明 */}
            <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800 p-4">
              <h3 className="font-medium text-blue-900 dark:text-blue-100 mb-2">
                💡 使用提示
              </h3>
              <ul className="text-sm text-blue-800 dark:text-blue-200 space-y-1">
                <li>• 支持拖拽、点击选择、Ctrl+V 粘贴三种上传方式</li>
                <li>• 识别过程实时展示，可随时查看进度</li>
                <li>• 结果支持 Markdown 格式，可直接复制或下载</li>
                <li>• 推荐使用"文档转 Markdown"模式获得最佳效果</li>
              </ul>
            </div>
          </div>

          {/* 右侧 - 结果展示 */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6 flex flex-col overflow-hidden">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
              识别结果
            </h2>
            <OCRResult
              file={uploadedFile}
              mode={selectedMode}
              onComplete={() => setProcessing(false)}
            />
          </div>
        </div>
      </main>

      {/* 页脚 */}
      <footer className="text-center py-4 text-sm text-gray-500 dark:text-gray-400">
        <p>
          Powered by{' '}
          <a
            href="https://www.deepseek.com/"
            target="_blank"
            rel="noopener noreferrer"
            className="text-primary-600 dark:text-primary-400 hover:underline"
          >
            DeepSeek AI
          </a>
        </p>
      </footer>
    </div>
  )
}

export default App
