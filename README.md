# Automated Image Generator for Othe.app

This tool reads prompts from your CSV file (`Othe.app image generation industry profession and prompt - Sheet1.csv`), generates high-quality images using the Gemini / Imagen 3 API (or OpenAI DALL-E), saves each image with its profession name into an output directory, and marks the CSV rows as `Completed` in real time.

---

## Features

- **Automated Batch Generation**: Processes all 414 rows from Column C (`Prompt`).
- **Profession-Based Naming**: Saves files as `<Profession>.jpg` (sanitizes invalid characters like `/` into `_`).
- **Duplicate Collision Handling**: For professions appearing in multiple industries, appends the industry name to prevent overwriting.
- **Real-Time CSV Tracking**: Adds `Completed` (`Yes`) and `Image_Path` columns immediately after each image is saved.
- **Fault-Tolerant & Resumable**: If interrupted or rate-limited, re-running the script automatically skips rows that are already completed.
- **Rate-Limiting & Retries**: Includes configurable delays between requests and exponential backoff for quota limits (HTTP 429).
- **Prompt Cleaning**: Automatically strips Midjourney-style tags (`--ar 16:9 --style raw`) while setting the native API aspect ratio to `16:9`.

---

## Quick Start

### 1. Configure Your API Key

Copy `.env.example` to `.env` and insert your Gemini API Key:

```bash
cp .env.example .env
```

Open `.env` and add:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```
*(You can get a free/standard Gemini API key at [Google AI Studio](https://aistudio.google.com/)).*

Alternatively, you can pass it directly to the command:
```bash
--api-key "AIzaSy..."
```

---

### 2. Run the Script

Use the virtual environment created in this project:

```bash
# Activate virtual environment
source .venv/bin/activate

# Run the batch generation
python generate_images.py
```

---

## Helpful Options & Examples

### Test First with `--dry-run` and `--limit`
Test 5 rows without calling the API:
```bash
python generate_images.py --dry-run --limit 5
```

### Run a Small Batch
Generate only the first 10 images to verify quality:
```bash
python generate_images.py --limit 10
```

### Custom Output Directory
Save images to a different folder:
```bash
python generate_images.py --output-dir "final_images"
```

### Adjust Delay Between Requests
If you encounter rate limits on standard tier:
```bash
python generate_images.py --delay 4.0
```

### Full Options Reference

| Flag | Description | Default |
|---|---|---|
| `--csv` | Path to input CSV | `Othe.app image generation industry profession and prompt - Sheet1.csv` |
| `--output-dir` | Folder to save images | `generated_images` |
| `--provider` | `gemini` or `openai` | `gemini` |
| `--model` | Model name | `imagen-3.0-generate-002` |
| `--api-key` | API Key (or use `.env`) | None |
| `--delay` | Delay in seconds between calls | `2.0` |
| `--limit` | Maximum images to generate | None (processes all) |
| `--dry-run` | Simulate run without API calls | Disabled |
| `--force` | Re-generate completed images | Disabled |
| `--include-industry` | Prefix filenames with industry | Disabled |
