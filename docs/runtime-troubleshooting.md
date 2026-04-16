# Runtime Troubleshooting

## Common failure cases

| Symptom | Likely cause | Suggested action |
|---|---|---|
| CUDA out-of-memory during PDF or batch runs | `MAX_CONCURRENCY`, `MAX_CROPS`, or page size is too aggressive for the GPU | Lower concurrency, test a smaller mode first, or split the workload |
| Blank or very short OCR output | The prompt does not match the task, or the input path is wrong | Re-check `PROMPT`, `INPUT_PATH`, and the selected script |
| The run finishes but nothing is saved | `OUTPUT_PATH` or `output_path` still points to a placeholder location | Set a writable directory before launching the script |
| Image OCR works but PDF OCR is unstable | Multi-page inputs produce a larger memory footprint and more preprocessing work | Reduce load, process fewer pages at a time, and verify disk space for intermediate artifacts |
| Results look flattened instead of structured | The run used `Free OCR.` instead of the markdown conversion prompt | Switch back to `<|grounding|>Convert the document to markdown.` for layout-aware output |

## Safe debugging sequence

1. Start with one local image and the Transformers script.
2. Move to the vLLM image script after the single-image path works.
3. Only then test PDF parsing or batch evaluation.

This order helps separate dependency issues from throughput-related failures.
