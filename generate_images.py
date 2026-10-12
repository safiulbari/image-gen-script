#!/usr/bin/env python3
"""
Automated Batch Image Generator for Othe.app Prompts.

Reads prompts and profession names from a CSV file, generates images via
Google Gemini Image API (gemini-3-pro-image) or OpenAI (dall-e-3), saves each image into
an output folder named by profession, and updates the CSV file in real time
with a 'Completed' status.
"""

import os
import sys
import csv
import time
import re
import base64
import argparse
import logging
from pathlib import Path
from datetime import datetime

# Optional dotenv support
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("ImageGen")


def sanitize_filename(name: str) -> str:
    """
    Remove or replace filesystem-illegal characters for macOS/Windows/Linux.
    """
    sanitized = re.sub(r'[\\/*?:"<>|]', "_", name)
    sanitized = re.sub(r"\s+", " ", sanitized).strip()
    return sanitized or "untitled"


def parse_prompt(raw_prompt: str) -> tuple[str, str]:
    """
    Extract aspect ratio from Midjourney-style flags (e.g. '--ar 16:9')
    and strip out extra flags like '--style raw' for optimal image model input.
    """
    aspect_ratio = "16:9"
    ar_match = re.search(r"--ar\s+(\d+:\d+)", raw_prompt)
    if ar_match:
        aspect_ratio = ar_match.group(1)

    cleaned = re.sub(r"--[a-zA-Z0-9_-]+(\s+[a-zA-Z0-9_:.-]+)?", "", raw_prompt)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned, aspect_ratio


def generate_with_gemini(
    prompt: str,
    aspect_ratio: str,
    api_key: str,
    model: str = "gemini-3-pro-image",
) -> bytes:
    """
    Generate image using Google's official google-genai SDK.
    Uses multimodal generate_content with response_modalities=['IMAGE'].
    """
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        raise ImportError(
            "The 'google-genai' library is required. Install it using:\n"
            "pip install google-genai pillow"
        )

    client = genai.Client(api_key=api_key)

    # In Gemini Developer API mode, generateContent with response_modalities=['IMAGE'] is used
    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
            ),
        )

        for candidate in response.candidates:
            if candidate.content and candidate.content.parts:
                for part in candidate.content.parts:
                    if part.inline_data and part.inline_data.data:
                        raw_data = part.inline_data.data
                        if isinstance(raw_data, str):
                            return base64.b64decode(raw_data)
                        return raw_data

        raise RuntimeError("No image data found in Gemini response parts.")

    except Exception as e:
        err_str = str(e)
        if "limit: 0" in err_str:
            raise RuntimeError(
                "Gemini API Quota Error: Image generation models (gemini-3-pro-image) require a "
                "paid/pay-as-you-go billing account on Google AI Studio / Google Cloud. "
                "The free tier has a limit of 0 requests for image generation."
            ) from e
        raise


def generate_with_openai(
    prompt: str,
    aspect_ratio: str,
    api_key: str,
    model: str = "dall-e-3",
) -> bytes:
    """
    Generate image using OpenAI DALL-E 3.
    """
    try:
        from openai import OpenAI
    except ImportError:
        raise ImportError(
            "The 'openai' library is required. Install it using:\n"
            "pip install openai"
        )

    client = OpenAI(api_key=api_key)

    if aspect_ratio == "16:9":
        size = "1792x1024"
    elif aspect_ratio == "9:16":
        size = "1024x1792"
    else:
        size = "1024x1024"

    response = client.images.generate(
        model=model,
        prompt=prompt,
        size=size,
        response_format="b64_json",
        n=1,
    )

    return base64.b64decode(response.data[0].b64_json)


def generate_placeholder_image(output_path: Path, title: str):
    """
    Generate a placeholder image for dry-run testing using Pillow.
    """
    try:
        from PIL import Image, ImageDraw
        img = Image.new("RGB", (1280, 720), color=(30, 41, 59))
        draw = ImageDraw.Draw(img)
        draw.text((40, 340), f"[DRY RUN PLACEHOLDER]\n{title}", fill=(241, 245, 249))
        img.save(output_path)
    except Exception:
        with open(output_path, "wb") as f:
            f.write(b"DRY_RUN_IMAGE_PLACEHOLDER")


def save_csv_atomic(csv_path: str, rows: list[dict], fieldnames: list[str]):
    """
    Save the CSV file atomically so no progress is corrupted or lost.
    """
    temp_path = f"{csv_path}.tmp"
    with open(temp_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temp_path, csv_path)


def process_dataset(
    csv_file: str,
    output_dir: str,
    provider: str,
    api_key: str | None,
    model: str | None,
    delay: float,
    limit: int | None,
    dry_run: bool,
    force: bool,
    include_industry: bool,
):
    csv_path = Path(csv_file)
    if not csv_path.exists():
        logger.error(f"CSV file not found: {csv_file}")
        sys.exit(1)

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    with open(csv_path, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        original_fieldnames = list(reader.fieldnames or [])
        rows = list(reader)

    fieldnames = list(original_fieldnames)
    if "Completed" not in fieldnames:
        fieldnames.append("Completed")
    if "Image_Path" not in fieldnames:
        fieldnames.append("Image_Path")

    total_rows = len(rows)
    logger.info(f"Loaded {total_rows} rows from {csv_file}")
    logger.info(f"Destination image folder: {out_dir.resolve()}")
    logger.info(f"Selected Provider: {provider.upper()} (Dry Run: {dry_run})")

    completed_count = 0
    skipped_count = 0
    failed_count = 0
    attempted_this_session = 0

    seen_filenames = {}

    for idx, row in enumerate(rows, start=1):
        if limit is not None and attempted_this_session >= limit:
            logger.info(f"Reached execution limit of {limit} rows. Stopping.")
            break

        profession = row.get("Profession", "").strip()
        industry = row.get("Industry", "").strip()
        prompt = row.get("Prompt", "").strip()
        is_completed = (row.get("Completed", "").strip().lower() in ("yes", "true", "1"))

        if not profession or not prompt:
            logger.warning(f"Row {idx}: Missing Profession or Prompt. Skipping.")
            continue

        safe_prof = sanitize_filename(profession)
        safe_ind = sanitize_filename(industry)

        if include_industry:
            base_filename = f"{safe_ind} - {safe_prof}"
        else:
            base_filename = safe_prof

        file_key = base_filename.lower()
        if file_key in seen_filenames and seen_filenames[file_key] != industry:
            base_filename = f"{base_filename} ({safe_ind})"
        seen_filenames[file_key] = industry

        ext = ".jpg" if provider == "gemini" else ".png"
        img_filename = f"{base_filename}{ext}"
        target_path = out_dir / img_filename

        if is_completed and target_path.exists() and not force:
            skipped_count += 1
            continue

        attempted_this_session += 1
        cleaned_prompt, aspect_ratio = parse_prompt(prompt)
        logger.info(
            f"[{idx}/{total_rows}] Generating: '{profession}' (Industry: '{industry}') -> {img_filename}"
        )

        max_retries = 2
        success = False

        for attempt in range(1, max_retries + 1):
            try:
                if dry_run:
                    generate_placeholder_image(target_path, f"{profession}\n({industry})")
                    time.sleep(0.1)
                elif provider == "gemini":
                    actual_model = model or "gemini-3-pro-image"
                    img_bytes = generate_with_gemini(
                        prompt=cleaned_prompt,
                        aspect_ratio=aspect_ratio,
                        api_key=api_key,
                        model=actual_model,
                    )
                    with open(target_path, "wb") as img_file:
                        img_file.write(img_bytes)
                elif provider == "openai":
                    actual_model = model or "dall-e-3"
                    img_bytes = generate_with_openai(
                        prompt=cleaned_prompt,
                        aspect_ratio=aspect_ratio,
                        api_key=api_key,
                        model=actual_model,
                    )
                    with open(target_path, "wb") as img_file:
                        img_file.write(img_bytes)
                else:
                    raise ValueError(f"Unknown provider: {provider}")

                success = True
                break

            except Exception as e:
                err_msg = str(e)
                logger.error(f"Attempt {attempt}/{max_retries} failed for '{profession}': {e}")
                if "limit: 0" in err_msg or "billing" in err_msg.lower():
                    # Stop immediately if billing is required rather than looping endlessly
                    logger.critical(
                        "Billing configuration error detected on your Gemini API key. Halting."
                    )
                    break
                if attempt < max_retries:
                    time.sleep(3)

        if success:
            row["Completed"] = "Yes"
            row["Image_Path"] = str(target_path)
            completed_count += 1
            logger.info(f"✓ Saved '{img_filename}' and updated CSV status.")
            
            save_csv_atomic(str(csv_path), rows, fieldnames)

            if delay > 0 and not dry_run:
                time.sleep(delay)
        else:
            failed_count += 1
            if "limit: 0" in locals().get("err_msg", "") or "billing" in locals().get("err_msg", "").lower():
                break

    logger.info("=" * 60)
    logger.info("Batch Processing Finished Summary:")
    logger.info(f"  Total records in CSV:   {total_rows}")
    logger.info(f"  Previously Completed:   {skipped_count}")
    logger.info(f"  Newly Generated:        {completed_count}")
    logger.info(f"  Failed / Stopped:       {failed_count}")
    logger.info(f"  Updated CSV:            {csv_path.resolve()}")
    logger.info(f"  Image Output Directory: {out_dir.resolve()}")
    logger.info("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Automate image generation from CSV prompts and track completion status."
    )
    parser.add_argument(
        "--csv",
        default="Othe.app image generation industry profession and prompt - Sheet1.csv",
        help="Path to the input CSV file",
    )
    parser.add_argument(
        "--output-dir",
        default="generated_images",
        help="Folder where generated images will be saved (default: generated_images)",
    )
    parser.add_argument(
        "--provider",
        choices=["gemini", "openai"],
        default="gemini",
        help="Image generation provider (gemini or openai, default: gemini)",
    )
    parser.add_argument(
        "--api-key",
        default=None,
        help="API Key for the provider (can also use GEMINI_API_KEY or OPENAI_API_KEY environment variable)",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Model name (default: 'gemini-3-pro-image' for Gemini, 'dall-e-3' for OpenAI)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=2.0,
        help="Delay in seconds between requests to avoid rate limits (default: 2.0)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Maximum number of images to attempt in this run (useful for testing)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the generation flow and generate placeholder images without consuming API credits",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-generate and overwrite even if marked Completed in CSV",
    )
    parser.add_argument(
        "--include-industry",
        action="store_true",
        help="Include industry name in the image filename (e.g., 'Industry - Profession.jpg')",
    )

    args = parser.parse_args()

    api_key = args.api_key
    if not args.dry_run:
        if args.provider == "gemini":
            api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
            if not api_key:
                logger.error(
                    "Missing Gemini API key! Provide it via --api-key, or set GEMINI_API_KEY in your environment / .env file."
                )
                sys.exit(1)
        elif args.provider == "openai":
            api_key = api_key or os.getenv("OPENAI_API_KEY")
            if not api_key:
                logger.error(
                    "Missing OpenAI API key! Provide it via --api-key, or set OPENAI_API_KEY in your environment / .env file."
                )
                sys.exit(1)

    process_dataset(
        csv_file=args.csv,
        output_dir=args.output_dir,
        provider=args.provider,
        api_key=api_key,
        model=args.model,
        delay=args.delay,
        limit=args.limit,
        dry_run=args.dry_run,
        force=args.force,
        include_industry=args.include_industry,
    )


if __name__ == "__main__":
    main()
