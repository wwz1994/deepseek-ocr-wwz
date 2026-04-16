# DeepSeek-OCR Output Formats

DeepSeek-OCR can be prompted in different ways depending on whether you want layout-aware markdown, plain OCR text, or figure-oriented descriptions.

## Prompt-to-output reference

| Prompt | Best for | Typical output |
|---|---|---|
| `<image>\n<|grounding|>Convert the document to markdown.` | Layout-aware document OCR | Markdown with headings, lists, tables, and inline formulas |
| `<image>\nFree OCR.` | Fast plain text extraction | Plain OCR text with minimal layout control |
| `<image>\nParse the figure.` | Charts or figure-heavy pages | Figure description or extracted labels |
| `<image>\nDescribe this image in detail.` | Non-document images | Free-form visual description |

## Example commands

### vLLM image run

```bash
cd DeepSeek-OCR-master/DeepSeek-OCR-vllm
python run_dpsk_ocr_image.py
```

Set `PROMPT='<image>\n<|grounding|>Convert the document to markdown.'` when you want markdown output.

### Transformers run

```bash
cd DeepSeek-OCR-master/DeepSeek-OCR-hf
python run_dpsk_ocr.py
```

The script writes results under the configured `output_path` when `save_results=True`.

## What to inspect in the output directory

- Markdown-style OCR runs should preserve document sections and table-like structure.
- Plain OCR runs should return fewer layout markers and more direct text.
- If you test multiple prompts on the same input, save them to separate output folders so you can compare formatting differences side by side.
