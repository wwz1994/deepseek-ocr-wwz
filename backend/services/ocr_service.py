"""
OCR Service - 封装 DeepSeek-OCR 推理逻辑

设计思路：
1. 使用单例模式管理模型实例，避免重复加载模型（模型加载很耗时）
2. 支持异步流式输出，提升用户体验
3. 提供多种 OCR 模式支持
"""
import asyncio
import os
import sys
from typing import AsyncGenerator, Optional
from PIL import Image, ImageOps
import torch

# 添加 vllm 相关路径
sys.path.insert(0, '/home/user/DeepSeek-OCR/DeepSeek-OCR-master/DeepSeek-OCR-vllm')

from vllm import AsyncLLMEngine, SamplingParams
from vllm.engine.arg_utils import AsyncEngineArgs
from vllm.model_executor.models.registry import ModelRegistry

# 导入 DeepSeek-OCR 模型
from deepseek_ocr import DeepseekOCRForCausalLM
from process.ngram_norepeat import NoRepeatNGramLogitsProcessor
from process.image_process import DeepseekOCRProcessor

# 注册自定义模型
ModelRegistry.register_model("DeepseekOCRForCausalLM", DeepseekOCRForCausalLM)


class OCRService:
    """
    OCR 服务类 - 单例模式

    为什么使用单例？
    - 模型加载需要几十秒到几分钟
    - 模型占用大量 GPU 显存（几个 GB）
    - 整个应用生命周期只需要一个模型实例
    """
    _instance = None
    _engine = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OCRService, cls).__new__(cls)
        return cls._instance

    async def initialize(self, model_path: str = "deepseek-ai/DeepSeek-OCR"):
        """
        初始化模型引擎

        参数说明：
        - model_path: HuggingFace 模型路径或本地路径
        - block_size=256: vLLM 内存块大小，影响显存使用
        - max_model_len=8192: 最大序列长度，OCR 任务通常需要较长的输出
        - gpu_memory_utilization=0.75: GPU 显存使用率，留 25% 给其他操作
        """
        if self._initialized:
            return

        print("🚀 正在初始化 DeepSeek-OCR 模型...")

        # 配置环境变量
        os.environ['VLLM_USE_V1'] = '0'
        if torch.version.cuda == '11.8':
            os.environ["TRITON_PTXAS_PATH"] = "/usr/local/cuda-11.8/bin/ptxas"

        # 创建引擎配置
        engine_args = AsyncEngineArgs(
            model=model_path,
            hf_overrides={"architectures": ["DeepseekOCRForCausalLM"]},
            block_size=256,
            max_model_len=8192,
            enforce_eager=False,
            trust_remote_code=True,
            tensor_parallel_size=1,
            gpu_memory_utilization=0.75,
        )

        # 创建异步引擎
        self._engine = AsyncLLMEngine.from_engine_args(engine_args)
        self._initialized = True
        print("✅ 模型初始化完成！")

    def load_image(self, image_path: str) -> Optional[Image.Image]:
        """
        加载并预处理图片

        为什么需要 EXIF 转置？
        - 手机拍摄的照片包含 EXIF 旋转信息
        - PIL 默认不处理 EXIF，导致图片方向错误
        - ImageOps.exif_transpose 自动根据 EXIF 旋转图片
        """
        try:
            image = Image.open(image_path)
            # 根据 EXIF 信息自动旋转图片
            corrected_image = ImageOps.exif_transpose(image)
            return corrected_image.convert('RGB')
        except Exception as e:
            print(f"❌ 图片加载失败: {e}")
            return None

    async def process_image(
        self,
        image_path: str,
        mode: str = "free_ocr",
        crop_mode: bool = True
    ) -> AsyncGenerator[str, None]:
        """
        处理图片并流式返回结果

        为什么使用异步生成器（AsyncGenerator）？
        - OCR 识别过程可能需要几十秒
        - 流式输出让用户实时看到识别进度
        - 提升用户体验，避免长时间等待

        参数说明：
        - image_path: 图片路径
        - mode: OCR 模式（free_ocr, document_markdown, etc.）
        - crop_mode: 是否使用动态分辨率裁剪（提升大图识别效果）
        """
        if not self._initialized:
            raise RuntimeError("模型未初始化，请先调用 initialize()")

        # 加载图片
        image = self.load_image(image_path)
        if image is None:
            yield "ERROR: 图片加载失败"
            return

        # 根据模式选择提示词
        prompt = self._get_prompt(mode)

        # 处理图片特征
        if '<image>' in prompt:
            image_features = DeepseekOCRProcessor().tokenize_with_images(
                images=[image],
                bos=True,
                eos=True,
                cropping=crop_mode
            )
        else:
            image_features = ''

        # 配置采样参数
        logits_processors = [
            NoRepeatNGramLogitsProcessor(
                ngram_size=30,  # 30-gram 防止重复
                window_size=90,  # 90 token 窗口
                whitelist_token_ids={128821, 128822}  # 允许表格标签重复
            )
        ]

        sampling_params = SamplingParams(
            temperature=0.0,  # 贪心解码，保证稳定性
            max_tokens=8192,
            logits_processors=logits_processors,
            skip_special_tokens=False,
        )

        # 构建请求
        request = {
            "prompt": prompt,
            "multi_modal_data": {"image": image_features}
        } if image_features else {"prompt": prompt}

        # 流式生成
        request_id = f"ocr-{id(image)}"
        printed_length = 0

        async for request_output in self._engine.generate(
            request, sampling_params, request_id
        ):
            if request_output.outputs:
                full_text = request_output.outputs[0].text
                new_text = full_text[printed_length:]
                if new_text:
                    yield new_text
                    printed_length = len(full_text)

    def _get_prompt(self, mode: str) -> str:
        """
        根据模式返回对应的提示词

        为什么需要不同的提示词？
        - DeepSeek-OCR 是多模态大模型，通过提示词控制行为
        - 不同任务需要不同的输出格式
        - 例如：文档转 Markdown 需要保留结构，Free OCR 只提取文本
        """
        prompts = {
            "free_ocr": "<image>\nFree OCR.",
            "document_markdown": "<image>\n<|grounding|>Convert the document to markdown.",
            "ocr_grounding": "<image>\n<|grounding|>OCR this image.",
            "parse_figure": "<image>\nParse the figure.",
            "describe_image": "<image>\nDescribe this image in detail.",
        }
        return prompts.get(mode, prompts["free_ocr"])


# 全局单例实例
ocr_service = OCRService()
