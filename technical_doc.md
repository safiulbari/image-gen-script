# Technical Documentation: Automated AI Image Generation Architecture & Pipeline

## 1. Overview & Purpose
This system provides an automated, resilient pipeline to batch-generate industry-authentic, SaaS-optimized background images (1920 × 1080) for 400+ professions. It combines:
- A local browser bridge daemon (**Kimi WebBridge**) interacting with Google Gemini (Imagen 3).
- An **Industry-Aware Environment & Demographic Engine** that generates customized Midjourney/Imagen prompts.
- A high-resolution **Canvas extraction engine** producing lossless 1080p images.
- A **Real-Time Visual Monitoring Dashboard** (`view.html` + `server.js` / Python HTTP) with interactive inspection and deletion capabilities.

---

## 2. Architecture & System Flow

```
┌────────────────────────────────────────────────────────┐
│ CSV Source: (Industry, Profession, Generated Prompt)    │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ Batch Controller (`generate_all_gemini.py`)           │
│  - Reads CSV & batch_progress.json                     │
│  - Checks existing disk files (skips completed)        │
│  - Manages prompt timeouts & retry policies            │
└──────────────────────────┬─────────────────────────────┘
                           │ HTTP POST /command
                           ▼
┌────────────────────────────────────────────────────────┐
│ Local Browser Bridge Daemon (`127.0.0.1:10086`)        │
│  - Connects to user's real Chrome/Edge session         │
│  - Dispatches actions: fill, click, evaluate           │
└──────────────────────────┬─────────────────────────────┘
                           │ DevTools / Content Script
                           ▼
┌────────────────────────────────────────────────────────┐
│ Google Gemini Web Application (Flash Medium Mode)      │
│  - Receives `Generate an image: <prompt>`              │
│  - Triggers Imagen 3 image synthesis                   │
│  - Displays `blob:https://gemini.google.com/...`       │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ Canvas Extraction & Upscale Engine                     │
│  - Draws rendered `<img>` to `<canvas>` (1920x1080)    │
│  - Applies high-quality bicubic smoothing              │
│  - Extracts lossless base64 DataURL                    │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ Output Filesystem:                                     │
│  - `images/{Industry}/{Profession}.png`                │
│  - `images/batch_progress.json`                        │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ Real-Time Dashboard (`view.html`, `app.js`, `server.js`)│
│  - Metrics & Gallery                                   │
│  - Full Image Preview Modal                            │
│  - Deletion & Regeneration endpoints                   │
└────────────────────────────────────────────────────────┘
```

---

## 3. Core Technologies & Dependencies

### Prerequisites
- **OS:** macOS (Apple Silicon / Intel) or Linux.
- **Python:** 3.9+ (Standard library: `urllib`, `json`, `csv`, `base64`, `re`, `subprocess`, `pathlib`).
- **macOS `sips`:** Built-in Scriptable Image Processing System for dimension validation.
- **Node.js (Optional):** Express server for `server.js` (or lightweight Python `http.server`).
- **Kimi WebBridge Daemon:** Local bridge binary connecting automated scripts to browser tabs.

---

## 4. Setup & Installation Guide

### Step 1: Install the WebBridge Daemon
The daemon connects automated scripts to your authenticated browser session without needing paid API keys:
```bash
curl -fsSL https://cdn.kimi.com/webbridge/install.sh | bash
```
Verify the daemon is running:
```bash
~/.kimi-webbridge/bin/kimi-webbridge status
```
Ensure your browser has the Kimi browser extension installed and enabled.

### Step 2: Directory Structure
```
project-root/
├── Othe.app image generation industry profession and prompt - Sheet1.csv
├── generate_all_gemini.py     # Main batch orchestration script
├── server.js                  # Node dashboard backend (optional API)
├── view.html                  # Dashboard frontend UI
├── app.js                     # Dashboard frontend logic & polling
└── images/                    # Output root
    ├── batch_progress.json    # Progress tracking database
    ├── Accounting & Finance/
    │   ├── Accountant.png
    │   ├── Auditor.png
    │   └── ...
    └── Production & Operations/
        └── ...
```

---

## 5. The Prompt Engineering Engine

To avoid repetitive characters and ensure domain-accurate visuals, prompts are constructed dynamically:

```
[Uniqueness Instruction] + [Authentic Setting] + [Tailored Profession] + [Demographic Profile] + [Domain Props] + [Lighting & Color Vibe] + [SaaS Composition Constraints]
```

### Prompt Construction Formula
```text
Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images.
Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi {SETTING}
tailored for a {PROFESSION} in the {INDUSTRY} industry, depicting {DIVERSE_PERSONA}.
Environment features {KEY_PROPS}, with an atmosphere that feels {COLOR_PALETTE_AND_VIBE}.
{LIGHTING_SPECIFICATION}.
Balanced composition, generous negative space designed for UI card and dashboard overlay,
low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism,
ultra-detailed textures, 8k resolution --ar 16:9 --style raw
```

### Rotating Demographic Engine (10 Profiles)
Prevents facial and character repetition across prompts:
1. Female, late 20s, field attire, 3/4 candid angle at workstation.
2. Male, early 30s, wireframe glasses, button-down, candid profile.
3. Female, mid-30s, authentic business wear, natural daylight.
4. Male, early 40s, tailored blazer, environmental wide shot.
5. Female, mid-20s, modern minimal outfit, over-the-shoulder view.
6. Male, late 20s, collar shirt, focused practical posture.
7. Female, early 30s, corporate kurti & wristwatch, modern desk.
8. Male, late 30s, glasses, side-angle workspace perspective.
9. Female, late 20s, smart casual, concentrated beside indoor plants.
10. Male, mid-20s, clean polo, diagonal desk perspective.

---

## 6. Image Extraction & 1080p Resolution Handling

Google Imagen 3 generates preview bitmaps inside a `<button class="image-button"><img class="image loaded" src="blob:...">`. Because blob URLs cannot be directly downloaded due to CORS/CSP policies, extraction is executed directly in the browser's JavaScript execution context:

```javascript
(() => {
    const imgs = document.querySelectorAll("model-response img.loaded");
    const lastImg = imgs[imgs.length - 1];
    if (!lastImg) return null;

    // Allocate exact 1920x1080 canvas
    const canvas = document.createElement("canvas");
    canvas.width = 1920;
    canvas.height = 1080;
    const ctx = canvas.getContext("2d");

    // Enable high-quality bicubic interpolation
    ctx.imageSmoothingEnabled = true;
    ctx.imageSmoothingQuality = "high";
    ctx.drawImage(lastImg, 0, 0, 1920, 1080);

    return canvas.toDataURL("image/png");
})()
```
The resulting Base64 string is decoded in Python and written directly to disk.

---

## 7. Monitoring & Dashboard Implementation

### Frontend (`view.html` & `app.js`)
- **Metric Cards:** Displays total, completed, pending counts, and progress percentage.
- **Cache-Busted Polling:** `fetch('images/batch_progress.json?_t=' + Date.now())` every 5 seconds.
- **Search & Filter:** Instant filter by generation status (`All`, `Generated`, `Pending`) or industry dropdown.
- **Preview Modal:** Allows clicking into any card to inspect full-res 1080p images with next/prev navigation.

### Backend (`server.js`)
Provides static file serving and a REST endpoint to safely delete and re-queue items:
```javascript
app.post('/delete_image', (req, res) => {
  const { key } = req.body; // e.g. "Commercial & Trade::Key Account Officer"
  // 1. Removes file from disk
  // 2. Removes key from batch_progress.json
  // 3. Allows next batch run to automatically re-generate
});
```

---

## 8. Gemini Model Optimization Guide

| Model Selection | Performance | Stability | Recommendation |
|---|---|---|---|
| **3.8 Flash (Medium)** | ~12–16s / image | Extremely High | **Recommended:** Fastest, adheres strictly to visual prompt without over-thinking or hallucinating. |
| **3.1 Pro (Medium)** | ~25–35s / image | Medium | Prone to text responses/hallucinations on complex descriptions. |
| **Pro (High Thinking)** | 50s+ / image | Low | Over-analyzes prompts and frequently triggers execution timeouts. |

---

## 9. Error Handling & Recovery Strategies

1. **Rate Limiting / Turn Limits:**
   - If a conversation thread reaches its turn limit (~150–200 prompts), the `Send message` button hides.
   - **Recovery:** Open a fresh chat in Gemini, update `TARGET_CHAT_KEY` in `generate_all_gemini.py`, and launch. It skips completed images instantly.
2. **Missing Element / Retries:**
   - Script performs 2 attempts per item with an exponential backoff.
   - If an item times out, it is logged as `failed` in `batch_progress.json` and the queue continues without freezing.
3. **Graceful Shutdown:**
   - Stopping the process does not corrupt `batch_progress.json`.
   - On restart, the script inspects both the file system and JSON database to pick up exactly where it stopped.
