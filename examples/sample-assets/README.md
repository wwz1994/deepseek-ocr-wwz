# Sample OCR Assets

This folder contains a tiny documentation-oriented sample you can use to compare prompt styles and saved output formats.

## Files

- `sample-document.svg`: a small text-heavy input image
- `sample-document.md`: an example markdown-style OCR result
- `sample-document.json`: a compact structured result you can diff in scripts

## Suggested workflow

1. Point your local script at `sample-document.svg`.
2. Run the markdown prompt first: `<image>\n<|grounding|>Convert the document to markdown.`
3. Save the generated result to a separate output directory and compare it with the sample files in this folder.
