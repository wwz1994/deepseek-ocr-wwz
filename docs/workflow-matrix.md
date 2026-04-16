# DeepSeek-OCR Workflow Matrix

Use this guide to pick the smallest entrypoint for the job you want to run.

| Workflow | Entrypoint | Best for | Output location |
|---|---|---|---|
| Single image with vLLM | `DeepSeek-OCR-master/DeepSeek-OCR-vllm/run_dpsk_ocr_image.py` | One `.jpg`, `.jpeg`, or `.png` file | `OUTPUT_PATH` from `DeepSeek-OCR-master/DeepSeek-OCR-vllm/config.py` |
| PDF with vLLM | `DeepSeek-OCR-master/DeepSeek-OCR-vllm/run_dpsk_ocr_pdf.py` | Multi-page document parsing | `OUTPUT_PATH` from `DeepSeek-OCR-master/DeepSeek-OCR-vllm/config.py` |
| Batch benchmark run | `DeepSeek-OCR-master/DeepSeek-OCR-vllm/run_dpsk_ocr_eval_batch.py` | Dataset-style evaluation over many images | `OUTPUT_PATH` from `DeepSeek-OCR-master/DeepSeek-OCR-vllm/config.py` |
| Single image with Transformers | `DeepSeek-OCR-master/DeepSeek-OCR-hf/run_dpsk_ocr.py` | Local debugging without the vLLM runtime | `output_path` in the script |

## Typical setup flow

1. Install the CUDA / PyTorch / vLLM dependencies from the root `README.md`.
2. Choose the matching entrypoint for your input shape.
3. Update `INPUT_PATH`, `OUTPUT_PATH`, and `PROMPT` before running the script.
4. Start with one image first, then scale up to PDFs or batch evaluation.

## Input reminders

- Use `run_dpsk_ocr_image.py` for image files.
- Use `run_dpsk_ocr_pdf.py` for `.pdf` inputs.
- Use the batch script only when your input directory already matches the benchmark layout you want to evaluate.
