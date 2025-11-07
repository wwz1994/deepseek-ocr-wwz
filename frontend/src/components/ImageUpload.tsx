/**
 * 图片上传组件
 *
 * 功能：
 * 1. 支持拖拽上传
 * 2. 支持点击选择文件
 * 3. 支持粘贴上传
 * 4. 图片预览
 * 5. 上传进度显示
 *
 * 为什么使用 react-dropzone？
 * - 简化拖拽上传实现
 * - 自动处理文件验证
 * - 良好的用户体验
 */
import React, { useCallback, useState, useEffect } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, Image as ImageIcon, X, Loader2 } from 'lucide-react'
import { cn, formatFileSize } from '@/lib/utils'
import type { UploadedFile } from '@/types'

interface ImageUploadProps {
  onUploadSuccess: (file: UploadedFile) => void
  disabled?: boolean
}

export const ImageUpload: React.FC<ImageUploadProps> = ({
  onUploadSuccess,
  disabled = false
}) => {
  const [preview, setPreview] = useState<string | null>(null)
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [fileInfo, setFileInfo] = useState<{ name: string; size: number } | null>(null)

  /**
   * 上传文件到服务器
   */
  const uploadFile = async (file: File) => {
    setUploading(true)
    setError(null)

    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error('上传失败')
      }

      const data = await response.json()

      // 创建预览 URL
      const previewUrl = URL.createObjectURL(file)
      setPreview(previewUrl)
      setFileInfo({ name: file.name, size: file.size })

      // 通知父组件
      onUploadSuccess({
        fileId: data.file_id,
        filename: data.filename,
        filePath: data.file_path,
        preview: previewUrl,
        size: file.size,
      })
    } catch (err) {
      setError(err instanceof Error ? err.message : '上传失败')
      console.error('上传错误:', err)
    } finally {
      setUploading(false)
    }
  }

  /**
   * 文件拖拽处理
   */
  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      uploadFile(acceptedFiles[0])
    }
  }, [])

  /**
   * 配置 dropzone
   */
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg', '.bmp', '.webp']
    },
    multiple: false,
    disabled: disabled || uploading,
  })

  /**
   * 粘贴上传支持
   */
  useEffect(() => {
    const handlePaste = (e: ClipboardEvent) => {
      if (disabled || uploading) return

      const items = e.clipboardData?.items
      if (!items) return

      for (let i = 0; i < items.length; i++) {
        if (items[i].type.indexOf('image') !== -1) {
          const file = items[i].getAsFile()
          if (file) {
            uploadFile(file)
          }
          break
        }
      }
    }

    document.addEventListener('paste', handlePaste)
    return () => document.removeEventListener('paste', handlePaste)
  }, [disabled, uploading])

  /**
   * 清除预览
   */
  const clearPreview = () => {
    if (preview) {
      URL.revokeObjectURL(preview)
    }
    setPreview(null)
    setFileInfo(null)
    setError(null)
  }

  return (
    <div className="w-full">
      {/* 上传区域 */}
      {!preview ? (
        <div
          {...getRootProps()}
          className={cn(
            'border-2 border-dashed rounded-lg p-8 transition-all cursor-pointer',
            'flex flex-col items-center justify-center min-h-[300px]',
            isDragActive
              ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
              : 'border-gray-300 dark:border-gray-700 hover:border-primary-400 dark:hover:border-primary-600',
            (disabled || uploading) && 'opacity-50 cursor-not-allowed'
          )}
        >
          <input {...getInputProps()} />

          {uploading ? (
            <>
              <Loader2 className="w-12 h-12 text-primary-500 animate-spin mb-4" />
              <p className="text-lg font-medium text-gray-700 dark:text-gray-300">
                上传中...
              </p>
            </>
          ) : (
            <>
              <Upload className="w-12 h-12 text-gray-400 dark:text-gray-600 mb-4" />
              <p className="text-lg font-medium text-gray-700 dark:text-gray-300 mb-2">
                {isDragActive ? '放开以上传图片' : '拖拽图片到此处'}
              </p>
              <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">
                或点击选择文件 / Ctrl+V 粘贴
              </p>
              <p className="text-xs text-gray-400 dark:text-gray-500">
                支持 PNG、JPG、JPEG、BMP、WebP 格式
              </p>
            </>
          )}

          {error && (
            <div className="mt-4 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
              <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
            </div>
          )}
        </div>
      ) : (
        /* 预览区域 */
        <div className="relative rounded-lg border-2 border-gray-300 dark:border-gray-700 overflow-hidden">
          <img
            src={preview}
            alt="预览"
            className="w-full h-auto max-h-[500px] object-contain bg-gray-100 dark:bg-gray-800"
          />

          {/* 文件信息 */}
          <div className="absolute top-2 left-2 bg-black/70 text-white px-3 py-1.5 rounded-lg text-sm flex items-center gap-2">
            <ImageIcon className="w-4 h-4" />
            <span>{fileInfo?.name}</span>
            {fileInfo?.size && (
              <span className="text-gray-300">
                · {formatFileSize(fileInfo.size)}
              </span>
            )}
          </div>

          {/* 删除按钮 */}
          <button
            onClick={clearPreview}
            disabled={disabled}
            className="absolute top-2 right-2 p-2 bg-red-500 hover:bg-red-600 text-white rounded-lg transition-colors disabled:opacity-50"
          >
            <X className="w-5 h-5" />
          </button>
        </div>
      )}
    </div>
  )
}
