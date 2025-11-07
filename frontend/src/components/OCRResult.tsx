/**
 * OCR 结果展示组件
 *
 * 功能：
 * 1. 实时显示 OCR 识别进度
 * 2. Markdown 格式渲染
 * 3. 代码高亮
 * 4. 复制和下载功能
 * 5. 识别时长统计
 *
 * 技术亮点：
 * - WebSocket 实时通信
 * - React Markdown 渲染
 * - 流式内容更新
 */
import React, { useState, useEffect, useRef } from 'react'
import ReactMarkdown from 'react-markdown'
import { Copy, Download, CheckCircle, Loader2, AlertCircle } from 'lucide-react'
import { cn, copyToClipboard, downloadText } from '@/lib/utils'
import type { UploadedFile, WSMessage } from '@/types'

interface OCRResultProps {
  file: UploadedFile | null
  mode: string
  onComplete?: () => void
}

type ProcessStatus = 'idle' | 'connecting' | 'processing' | 'complete' | 'error'

export const OCRResult: React.FC<OCRResultProps> = ({
  file,
  mode,
  onComplete
}) => {
  const [status, setStatus] = useState<ProcessStatus>('idle')
  const [content, setContent] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [startTime, setStartTime] = useState<number | null>(null)
  const [duration, setDuration] = useState<number | null>(null)
  const [copied, setCopied] = useState(false)

  const wsRef = useRef<WebSocket | null>(null)
  const contentRef = useRef<HTMLDivElement>(null)

  /**
   * 启动 OCR 识别
   *
   * WebSocket 通信流程：
   * 1. 建立连接
   * 2. 发送识别请求
   * 3. 接收实时结果
   * 4. 处理完成/错误
   */
  useEffect(() => {
    if (!file) {
      setStatus('idle')
      setContent('')
      setError(null)
      return
    }

    // 重置状态
    setContent('')
    setError(null)
    setStatus('connecting')
    setStartTime(Date.now())
    setDuration(null)

    // 创建 WebSocket 连接
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const wsUrl = `${protocol}//${window.location.host}/api/ws/ocr`
    const ws = new WebSocket(wsUrl)
    wsRef.current = ws

    ws.onopen = () => {
      console.log('✅ WebSocket 已连接')
      setStatus('processing')

      // 发送识别请求
      ws.send(JSON.stringify({
        file_id: file.fileId,
        mode: mode,
        crop_mode: true
      }))
    }

    ws.onmessage = (event) => {
      const message: WSMessage = JSON.parse(event.data)

      switch (message.type) {
        case 'start':
          setStatus('processing')
          break

        case 'progress':
          // 流式追加内容
          if (message.content) {
            setContent(prev => prev + message.content)
          }
          break

        case 'complete':
          setStatus('complete')
          setDuration(Date.now() - (startTime || Date.now()))
          onComplete?.()
          break

        case 'error':
          setStatus('error')
          setError(message.message || '识别失败')
          break
      }
    }

    ws.onerror = (error) => {
      console.error('❌ WebSocket 错误:', error)
      setStatus('error')
      setError('连接错误，请检查网络')
    }

    ws.onclose = () => {
      console.log('👋 WebSocket 已断开')
    }

    // 清理函数
    return () => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.close()
      }
    }
  }, [file, mode])

  /**
   * 自动滚动到底部
   */
  useEffect(() => {
    if (contentRef.current && status === 'processing') {
      contentRef.current.scrollTop = contentRef.current.scrollHeight
    }
  }, [content, status])

  /**
   * 复制内容
   */
  const handleCopy = async () => {
    const success = await copyToClipboard(content)
    if (success) {
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    }
  }

  /**
   * 下载内容
   */
  const handleDownload = () => {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-')
    const filename = `ocr-result-${timestamp}.md`
    downloadText(content, filename)
  }

  /**
   * 渲染状态指示器
   */
  const renderStatus = () => {
    switch (status) {
      case 'idle':
        return (
          <div className="text-center py-12 text-gray-500 dark:text-gray-400">
            <p>上传图片开始识别</p>
          </div>
        )

      case 'connecting':
        return (
          <div className="text-center py-12">
            <Loader2 className="w-10 h-10 animate-spin text-primary-500 mx-auto mb-3" />
            <p className="text-gray-600 dark:text-gray-400">正在连接...</p>
          </div>
        )

      case 'processing':
        return (
          <div className="flex items-center gap-2 text-sm text-primary-600 dark:text-primary-400 mb-4">
            <Loader2 className="w-4 h-4 animate-spin" />
            <span>识别中...</span>
            {startTime && (
              <span className="text-gray-500">
                {Math.round((Date.now() - startTime) / 1000)}s
              </span>
            )}
          </div>
        )

      case 'complete':
        return (
          <div className="flex items-center gap-2 text-sm text-green-600 dark:text-green-400 mb-4">
            <CheckCircle className="w-4 h-4" />
            <span>识别完成</span>
            {duration && (
              <span className="text-gray-500">
                耗时 {(duration / 1000).toFixed(1)}s
              </span>
            )}
          </div>
        )

      case 'error':
        return (
          <div className="flex items-center gap-2 text-sm text-red-600 dark:text-red-400 mb-4">
            <AlertCircle className="w-4 h-4" />
            <span>{error || '识别失败'}</span>
          </div>
        )
    }
  }

  return (
    <div className="flex flex-col h-full">
      {/* 头部 - 状态和操作 */}
      <div className="flex items-center justify-between mb-4">
        {renderStatus()}

        {content && status !== 'processing' && (
          <div className="flex items-center gap-2">
            <button
              onClick={handleCopy}
              className={cn(
                'px-3 py-1.5 rounded-lg text-sm font-medium transition-colors',
                'flex items-center gap-2',
                copied
                  ? 'bg-green-500 text-white'
                  : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600'
              )}
            >
              {copied ? (
                <>
                  <CheckCircle className="w-4 h-4" />
                  已复制
                </>
              ) : (
                <>
                  <Copy className="w-4 h-4" />
                  复制
                </>
              )}
            </button>

            <button
              onClick={handleDownload}
              className="px-3 py-1.5 rounded-lg text-sm font-medium transition-colors bg-primary-500 text-white hover:bg-primary-600 flex items-center gap-2"
            >
              <Download className="w-4 h-4" />
              下载
            </button>
          </div>
        )}
      </div>

      {/* 内容区域 */}
      {content && (
        <div
          ref={contentRef}
          className="flex-1 overflow-y-auto custom-scrollbar bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6"
        >
          <ReactMarkdown
            className="markdown-content"
            components={{
              // 自定义代码块样式
              code: ({node, inline, className, children, ...props}) => {
                return inline ? (
                  <code className={className} {...props}>
                    {children}
                  </code>
                ) : (
                  <code className={className} {...props}>
                    {children}
                  </code>
                )
              },
              // 自定义表格样式
              table: ({node, ...props}) => (
                <div className="overflow-x-auto">
                  <table {...props} />
                </div>
              )
            }}
          >
            {content}
          </ReactMarkdown>

          {/* 加载光标 */}
          {status === 'processing' && (
            <span className="inline-block w-2 h-5 bg-primary-500 animate-pulse ml-1"></span>
          )}
        </div>
      )}
    </div>
  )
}
