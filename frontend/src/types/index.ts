/**
 * TypeScript 类型定义
 *
 * 为什么需要类型定义？
 * 1. 类型安全：编译时发现错误
 * 2. 智能提示：IDE 自动补全
 * 3. 代码可读性：明确数据结构
 * 4. 重构友好：修改类型自动检查所有使用处
 */

/**
 * OCR 模式
 */
export interface OCRMode {
  id: string
  name: string
  description: string
  icon: string
}

/**
 * 上传的文件信息
 */
export interface UploadedFile {
  fileId: string
  filename: string
  filePath: string
  preview?: string  // 预览 URL
  size?: number
}

/**
 * WebSocket 消息类型
 */
export type WSMessageType = 'start' | 'progress' | 'complete' | 'error'

/**
 * WebSocket 消息
 */
export interface WSMessage {
  type: WSMessageType
  content?: string
  message?: string
}

/**
 * OCR 请求参数
 */
export interface OCRRequest {
  fileId: string
  mode: string
  cropMode: boolean
}

/**
 * OCR 结果
 */
export interface OCRResult {
  id: string
  filename: string
  mode: string
  content: string
  timestamp: number
  duration?: number
}
