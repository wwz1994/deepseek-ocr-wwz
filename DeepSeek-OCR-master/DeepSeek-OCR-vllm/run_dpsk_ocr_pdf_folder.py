import os
import fitz
import img2pdf
import io
import re
import glob
from tqdm import tqdm
import torch
from concurrent.futures import ThreadPoolExecutor
import sys
import gc

if torch.version.cuda == '11.8':
    os.environ["TRITON_PTXAS_PATH"] = "/usr/local/cuda-11.8/bin/ptxas"
os.environ['VLLM_USE_V1'] = '0'
os.environ["CUDA_VISIBLE_DEVICES"] = '0'


from config import MODEL_PATH, INPUT_PATH, OUTPUT_PATH, PROMPT, SKIP_REPEAT, MAX_CONCURRENCY, NUM_WORKERS, CROP_MODE

from PIL import Image, ImageDraw, ImageFont
import numpy as np
from deepseek_ocr import DeepseekOCRForCausalLM

from vllm.model_executor.models.registry import ModelRegistry

from vllm import LLM, SamplingParams
from process.ngram_norepeat import NoRepeatNGramLogitsProcessor
from process.image_process import DeepseekOCRProcessor

ModelRegistry.register_model("DeepseekOCRForCausalLM", DeepseekOCRForCausalLM)


# Reduced memory utilization to leave room for system overhead
llm = LLM(
    model=MODEL_PATH,
    hf_overrides={"architectures": ["DeepseekOCRForCausalLM"]},
    block_size=256,
    enforce_eager=False,
    trust_remote_code=True,
    max_model_len=8192,
    swap_space=0,
    max_num_seqs=MAX_CONCURRENCY,
    tensor_parallel_size=1,
    gpu_memory_utilization=0.7, # Reduced from 0.9 to 0.7
    disable_mm_preprocessor_cache=True
)

logits_processors = [NoRepeatNGramLogitsProcessor(ngram_size=15, window_size=60, whitelist_token_ids= {128821, 128822})] #window for fast；whitelist_token_ids: <td>,</td>

sampling_params = SamplingParams(
    temperature=0.0,
    max_tokens=8192,
    logits_processors=logits_processors,
    skip_special_tokens=False,
    include_stop_str_in_output=True,
    repetition_penalty=1.05,
)

# Drastically reduced batch size to preventing OOM
PAGE_BATCH_SIZE = 1
# Reduced worker count to save system RAM
SAFE_NUM_WORKERS = min(4, NUM_WORKERS)

class Colors:
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    RESET = '\033[0m'

def pdf_to_images_chunk(pdf_path, start_page, end_page, dpi=144, image_format="PNG"):
    """
    pdf2images for a specific range of pages
    """
    images = []

    try:
        pdf_document = fitz.open(pdf_path)
    except Exception as e:
        print(f"{Colors.RED}Error opening PDF {pdf_path}: {e}{Colors.RESET}")
        return []

    if pdf_document.needs_pass:
        print(f"{Colors.RED}PDF {pdf_path} is password protected.{Colors.RESET}")
        return []

    if pdf_document.page_count == 0:
        print(f"{Colors.YELLOW}PDF {pdf_path} has 0 pages.{Colors.RESET}")
        return []

    zoom = dpi / 72.0
    matrix = fitz.Matrix(zoom, zoom)

    # Ensure end_page does not exceed actual page count
    actual_end_page = min(end_page, pdf_document.page_count)

    for page_num in range(start_page, actual_end_page):
        try:
            page = pdf_document[page_num]

            pixmap = page.get_pixmap(matrix=matrix, alpha=False)
            Image.MAX_IMAGE_PIXELS = None

            if image_format.upper() == "PNG":
                img_data = pixmap.tobytes("png")
                img = Image.open(io.BytesIO(img_data))
            else:
                img_data = pixmap.tobytes("png")
                img = Image.open(io.BytesIO(img_data))
                if img.mode in ('RGBA', 'LA'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background

            images.append(img)
        except Exception as e:
            print(f"{Colors.YELLOW}Error processing page {page_num} of {pdf_path}: {e}{Colors.RESET}")
            continue

    pdf_document.close()
    return images

def pil_to_pdf_img2pdf(pil_images, output_path):

    if not pil_images:
        return

    image_bytes_list = []

    for img in pil_images:
        if img.mode != 'RGB':
            img = img.convert('RGB')

        img_buffer = io.BytesIO()
        img.save(img_buffer, format='JPEG', quality=95)
        img_bytes = img_buffer.getvalue()
        image_bytes_list.append(img_bytes)

    try:
        pdf_bytes = img2pdf.convert(image_bytes_list)
        with open(output_path, "wb") as f:
            f.write(pdf_bytes)

    except Exception as e:
        print(f"error: {e}")



def re_match(text):
    pattern = r'(<\|ref\|>(.*?)<\|/ref\|><\|det\|>(.*?)<\|/det\|>)'
    matches = re.findall(pattern, text, re.DOTALL)


    mathes_image = []
    mathes_other = []
    for a_match in matches:
        if '<|ref|>image<|/ref|>' in a_match[0]:
            mathes_image.append(a_match[0])
        else:
            mathes_other.append(a_match[0])
    return matches, mathes_image, mathes_other


def extract_coordinates_and_label(ref_text, image_width, image_height):


    try:
        label_type = ref_text[1]
        cor_list = eval(ref_text[2])
    except Exception as e:
        print(e)
        return None

    return (label_type, cor_list)


def draw_bounding_boxes(image, refs, jdx, pdf_base_name):

    image_width, image_height = image.size
    img_draw = image.copy()
    draw = ImageDraw.Draw(img_draw)

    overlay = Image.new('RGBA', img_draw.size, (0, 0, 0, 0))
    draw2 = ImageDraw.Draw(overlay)

    #     except IOError:
    font = ImageFont.load_default()

    img_idx = 0

    for i, ref in enumerate(refs):
        try:
            result = extract_coordinates_and_label(ref, image_width, image_height)
            if result:
                label_type, points_list = result

                color = (np.random.randint(0, 200), np.random.randint(0, 200), np.random.randint(0, 255))

                color_a = color + (20, )
                for points in points_list:
                    x1, y1, x2, y2 = points

                    x1 = int(x1 / 999 * image_width)
                    y1 = int(y1 / 999 * image_height)

                    x2 = int(x2 / 999 * image_width)
                    y2 = int(y2 / 999 * image_height)

                    if label_type == 'image':
                        try:
                            cropped = image.crop((x1, y1, x2, y2))
                            # Ensure directory exists
                            os.makedirs(f"{OUTPUT_PATH}/images", exist_ok=True)
                            save_name = f"{pdf_base_name}_{jdx}_{img_idx}.jpg"
                            cropped.save(f"{OUTPUT_PATH}/images/{save_name}")
                        except Exception as e:
                            print(e)
                            pass
                        img_idx += 1

                    try:
                        if label_type == 'title':
                            draw.rectangle([x1, y1, x2, y2], outline=color, width=4)
                            draw2.rectangle([x1, y1, x2, y2], fill=color_a, outline=(0, 0, 0, 0), width=1)
                        else:
                            draw.rectangle([x1, y1, x2, y2], outline=color, width=2)
                            draw2.rectangle([x1, y1, x2, y2], fill=color_a, outline=(0, 0, 0, 0), width=1)

                        text_x = x1
                        text_y = max(0, y1 - 15)

                        text_bbox = draw.textbbox((0, 0), label_type, font=font)
                        text_width = text_bbox[2] - text_bbox[0]
                        text_height = text_bbox[3] - text_bbox[1]
                        draw.rectangle([text_x, text_y, text_x + text_width, text_y + text_height],
                                    fill=(255, 255, 255, 30))

                        draw.text((text_x, text_y), label_type, font=font, fill=color)
                    except:
                        pass
        except:
            continue
    img_draw.paste(overlay, (0, 0), overlay)
    return img_draw


def process_image_with_refs(image, ref_texts, jdx, pdf_base_name):
    result_image = draw_bounding_boxes(image, ref_texts, jdx, pdf_base_name)
    return result_image


def process_single_image(image):
    """single image"""
    prompt_in = prompt
    cache_item = {
        "prompt": prompt_in,
        "multi_modal_data": {"image": DeepseekOCRProcessor().tokenize_with_images(images = [image], bos=True, eos=True, cropping=CROP_MODE)},
    }
    return cache_item


if __name__ == "__main__":

    # Check if INPUT_PATH is directory
    if not os.path.isdir(INPUT_PATH):
        print(f"{Colors.RED}INPUT_PATH '{INPUT_PATH}' is not a directory. Please set INPUT_PATH in config.py to a directory containing PDFs.{Colors.RESET}")
        exit(1)

    os.makedirs(OUTPUT_PATH, exist_ok=True)
    os.makedirs(f'{OUTPUT_PATH}/images', exist_ok=True)

    pdf_files = glob.glob(os.path.join(INPUT_PATH, "*.pdf"))
    if not pdf_files:
        print(f"{Colors.YELLOW}No PDF files found in {INPUT_PATH}{Colors.RESET}")
        exit(0)

    print(f'{Colors.GREEN}Found {len(pdf_files)} PDF files in {INPUT_PATH}{Colors.RESET}')

    prompt = PROMPT

    for pdf_file in tqdm(pdf_files, desc="Processing PDFs"):
        print(f'{Colors.BLUE}Processing {pdf_file} ...{Colors.RESET}')

        pdf_name = os.path.basename(pdf_file)
        pdf_base_name = os.path.splitext(pdf_name)[0]

        # Get total page count first
        try:
            doc_tmp = fitz.open(pdf_file)
            total_pages = doc_tmp.page_count
            doc_tmp.close()
        except Exception as e:
            print(f"{Colors.RED}Could not open PDF {pdf_file} to read page count: {e}{Colors.RESET}")
            continue

        if total_pages == 0:
            print(f"{Colors.YELLOW}PDF {pdf_file} has 0 pages. Skipping.{Colors.RESET}")
            continue

        # Prepare filenames
        mmd_det_path = os.path.join(OUTPUT_PATH, pdf_name.replace('.pdf', '_det.mmd'))
        mmd_path = os.path.join(OUTPUT_PATH, pdf_name.replace('.pdf', '.mmd'))
        pdf_out_path = os.path.join(OUTPUT_PATH, pdf_name.replace('.pdf', '_layouts.pdf'))

        # Clear existing files if they exist (since we append)
        if os.path.exists(mmd_det_path): os.remove(mmd_det_path)
        if os.path.exists(mmd_path): os.remove(mmd_path)
        # For the PDF layout, we can't easily append, so we accumulate images in memory
        # BUT for massive PDFs, accumulating 400 images in memory might also be an issue.
        # However, PIL images are smaller than the vllm context.
        # Let's keep the draw_images in memory for now, but be aware.
        # If the user crashes on PIL images, we'd need to save them to disk temporarily.

        draw_images = []
        jdx = 0

        # Process in chunks of 1 to minimize memory footprint
        for start_page in range(0, total_pages, PAGE_BATCH_SIZE):
            end_page = min(start_page + PAGE_BATCH_SIZE, total_pages)
            print(f"  Processing pages {start_page} to {end_page} of {total_pages}...")

            try:
                images = pdf_to_images_chunk(pdf_file, start_page, end_page)
            except Exception as e:
                print(f"{Colors.RED}Failed to process chunk {start_page}-{end_page} of {pdf_file}: {e}{Colors.RESET}")
                continue

            if not images:
                print(f"{Colors.YELLOW}No images extracted for chunk {start_page}-{end_page}{Colors.RESET}")
                continue

            with ThreadPoolExecutor(max_workers=SAFE_NUM_WORKERS) as executor:
                batch_inputs = list(tqdm(
                    executor.map(process_single_image, images),
                    total=len(images),
                    desc=f"    Pre-processing chunk",
                    leave=False
                ))

            outputs_list = llm.generate(
                batch_inputs,
                sampling_params=sampling_params
            )

            # Temporary accumulators for this chunk
            chunk_contents_det = ''
            chunk_contents = ''

            for output, img in zip(outputs_list, images):
                content = output.outputs[0].text

                if '<｜end▁of▁sentence｜>' in content: # repeat no eos
                    content = content.replace('<｜end▁of▁sentence｜>', '')
                else:
                    if SKIP_REPEAT:
                        continue

                page_num = f'\n<--- Page Split --->'

                chunk_contents_det += content + f'\n{page_num}\n'

                image_draw = img.copy()

                matches_ref, matches_images, mathes_other = re_match(content)

                result_image = process_image_with_refs(image_draw, matches_ref, jdx, pdf_base_name)

                # Accumulate result images for final PDF
                draw_images.append(result_image)

                for idx, a_match_image in enumerate(matches_images):
                    image_filename = f"{pdf_base_name}_{jdx}_{idx}.jpg"
                    content = content.replace(a_match_image, f'![](images/{image_filename})\n')

                for idx, a_match_other in enumerate(mathes_other):
                    content = content.replace(a_match_other, '').replace('\\coloneqq', ':=').replace('\\eqqcolon', '=:').replace('\n\n\n\n', '\n\n').replace('\n\n\n', '\n\n')

                chunk_contents += content + f'\n{page_num}\n'

                jdx += 1

            # Append text to files immediately
            with open(mmd_det_path, 'a', encoding='utf-8') as afile:
                afile.write(chunk_contents_det)

            with open(mmd_path, 'a', encoding='utf-8') as afile:
                afile.write(chunk_contents)

            # Explicit cleanup after each chunk
            del images
            del batch_inputs
            del outputs_list
            # Clear CUDA cache to prevent fragmentation/OOM
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            gc.collect()

        # Save the layout PDF at the end
        if draw_images:
            try:
                pil_to_pdf_img2pdf(draw_images, pdf_out_path)
            except Exception as e:
                print(f"{Colors.RED}Failed to save layout PDF: {e}{Colors.RESET}")

        # Cleanup final accumulators for this PDF
        del draw_images
        gc.collect()
