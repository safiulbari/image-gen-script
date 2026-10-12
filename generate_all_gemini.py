#!/usr/bin/env python3
"""
Automated Batch Generator for all 414 Othe.app professions via Gemini Chat WebBridge.
Chat URL: https://gemini.google.com/app/d4426fa7629d8011
"""

import os
import sys
import csv
import time
import json
import base64
import urllib.request
import re
from pathlib import Path
from datetime import datetime

DAEMON_URL = "http://127.0.0.1:10086/command"
SESSION = "gemini-all-images"
TARGET_CHAT_KEY = "d4426fa7629d8011"

WORKSPACE_DIR = Path("/Users/safiulbari/Documents/Office projects/othe.app images")
CSV_PATH = WORKSPACE_DIR / "Othe.app image generation industry profession and prompt - Sheet1.csv"
BASE_OUT_DIR = WORKSPACE_DIR / "images"
PROGRESS_FILE = BASE_OUT_DIR / "batch_progress.json"

def sanitize_name(name: str) -> str:
    sanitized = re.sub(r'[/\\:*?"<>|]', "-", name).strip()
    return sanitized or "untitled"

def send_command(action, args=None, retries=3):
    payload = {"action": action, "session": SESSION}
    if args:
        payload["args"] = args
    
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                DAEMON_URL,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            if attempt == retries - 1:
                raise
            time.sleep(1)

def ensure_tab_attached():
    res = send_command("list_browser_tabs")
    if not res.get("ok"):
        raise RuntimeError(f"Failed to list browser tabs: {res.get('error')}")
    
    tabs = res.get("data", {}).get("tabs", [])
    target = None
    for t in tabs:
        if TARGET_CHAT_KEY in t.get("url", ""):
            target = t
            break
    
    if not target:
        for t in tabs:
            if "gemini.google.com/app" in t.get("url", ""):
                target = t
                break
                
    if not target:
        raise RuntimeError(f"No Gemini tab found matching {TARGET_CHAT_KEY} or gemini.google.com/app")
    
    tab_id = target["tabId"]
    att_res = send_command("attach_tab", {"tabId": tab_id})
    if not att_res.get("ok"):
        raise RuntimeError(f"Failed to attach to tab {tab_id}: {att_res.get('error')}")
    return tab_id

def eval_js(code: str):
    res = send_command("evaluate", {"code": code})
    if not res.get("ok"):
        return None
    val = res.get("data", {}).get("value")
    if isinstance(val, str) and (val.startswith("{") or val.startswith("[")):
        try:
            return json.loads(val)
        except Exception:
            return val
    return val

def fill_and_send(prompt: str):
    escaped_prompt = prompt.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")
    js_code = f"""
    (() => {{
        const editor = document.querySelector('rich-textarea p, rich-textarea div, div[contenteditable="true"]');
        if (!editor) return JSON.stringify({{ success: false, error: 'Editor not found' }});
        
        editor.focus();
        editor.innerText = `Generate an image: {escaped_prompt}`;
        editor.dispatchEvent(new Event('input', {{ bubbles: true }}));
        
        const btn = document.querySelector('button[aria-label="Send message"], button.send-button, mat-icon[data-mat-icon-name="send_spark"]');
        const sendBtn = btn ? (btn.closest('button') || btn) : null;
        
        if (!sendBtn || sendBtn.disabled || sendBtn.getAttribute('aria-disabled') === 'true') {{
            const keyEvent = new KeyboardEvent('keydown', {{ key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }});
            editor.dispatchEvent(keyEvent);
            return JSON.stringify({{ success: true, method: 'enter-key' }});
        }} else {{
            sendBtn.click();
            return JSON.stringify({{ success: true, method: 'button-click' }});
        }}
    }})()
    """
    res = eval_js(js_code)
    return res if isinstance(res, dict) else {}

def get_loaded_img_count():
    # Only count actual generated blob images to prevent false positives from UI icons
    js_code = """
    (() => {
        const imgs = document.querySelectorAll('img.image, img[src^="blob:"]');
        return imgs.length;
    })()
    """
    res = eval_js(js_code)
    try:
        return int(res) if res is not None else 0
    except Exception:
        return 0

def extract_latest_image_1080p():
    # Target only generated blob images with 1920x1080 upscale canvas
    js_code = """
    (() => {
        const imgs = Array.from(document.querySelectorAll('img.image, img[src^="blob:"]'));
        if (imgs.length === 0) return JSON.stringify({ success: false, error: 'No generated images found' });
        
        const lastImg = imgs[imgs.length - 1];
        if (!lastImg.complete || lastImg.naturalWidth === 0) {
            return JSON.stringify({ success: false, error: 'Image not fully loaded yet' });
        }
        
        try {
            const canvas = document.createElement('canvas');
            canvas.width = 1920;
            canvas.height = 1080;
            const ctx = canvas.getContext('2d');
            ctx.imageSmoothingEnabled = true;
            ctx.imageSmoothingQuality = 'high';
            ctx.drawImage(lastImg, 0, 0, 1920, 1080);
            
            const dataUrl = canvas.toDataURL('image/png', 1.0);
            return JSON.stringify({
                success: true,
                dataUrl: dataUrl,
                naturalWidth: lastImg.naturalWidth,
                naturalHeight: lastImg.naturalHeight
            });
        } catch (e) {
            return JSON.stringify({ success: false, error: e.toString() });
        }
    })()
    """
    res = eval_js(js_code)
    return res if isinstance(res, dict) else {}

def load_progress():
    if PROGRESS_FILE.exists():
        try:
            return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}

def save_progress(progress):
    try:
        PROGRESS_FILE.write_text(json.dumps(progress, indent=2, ensure_ascii=False), encoding="utf-8")
    except Exception as e:
        print(f"Warning: failed to save progress: {e}")

def main():
    BASE_OUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print("Connecting to Gemini chat tab...")
    tab_id = ensure_tab_attached()
    print(f"Successfully attached to tab {tab_id} ({TARGET_CHAT_KEY})")

    with open(CSV_PATH, mode="r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    total = len(rows)
    print(f"Loaded {total} professions from CSV.")

    progress = load_progress()
    print(f"Previously tracked entries: {len(progress)} / {total}")

    for idx, row in enumerate(rows, 1):
        industry = row["Industry"].strip()
        profession = row["Profession"].strip()
        prompt = row["Prompt"].strip()

        safe_ind = sanitize_name(industry)
        safe_prof = sanitize_name(profession)

        out_folder = BASE_OUT_DIR / safe_ind
        out_folder.mkdir(parents=True, exist_ok=True)

        out_file = out_folder / f"{safe_prof}.png"
        item_key = f"{industry}::{profession}"

        # Resume check: if already completed and file exists on disk, skip
        if item_key in progress and progress[item_key].get("status") == "completed" and out_file.exists():
            continue

        print(f"\n==================================================")
        print(f"[{idx}/{total}] Processing: '{profession}'")
        print(f"Industry: '{industry}'")
        print(f"Target: {out_file}")
        print(f"==================================================")

        success = False
        max_attempts = 2

        for attempt in range(1, max_attempts + 1):
            try:
                ensure_tab_attached()
                initial_count = get_loaded_img_count()
                print(f"  Attempt {attempt}/{max_attempts} | Current generated images in thread: {initial_count}")

                fill_and_send(prompt)
                print("  Prompt submitted. Waiting for Imagen generation...")

                start_time = time.time()
                timeout = 160

                while time.time() - start_time < timeout:
                    time.sleep(5)
                    current_count = get_loaded_img_count()
                    if current_count > initial_count:
                        print("  New image element detected! Waiting 3s for render stabilization...")
                        time.sleep(3)
                        img_data = extract_latest_image_1080p()
                        if img_data.get("success") and img_data.get("dataUrl"):
                            data_url = img_data["dataUrl"]
                            header, b64_str = data_url.split(",", 1)
                            img_bytes = base64.b64decode(b64_str)

                            with open(out_file, "wb") as img_f:
                                img_f.write(img_bytes)

                            print(f"  SUCCESS! Image saved to {out_file} ({len(img_bytes)} bytes, 1920x1080)")
                            progress[item_key] = {
                                "status": "completed",
                                "timestamp": datetime.now().isoformat(),
                                "bytes": len(img_bytes),
                                "industry": industry,
                                "profession": profession,
                                "dimension": "1920x1080"
                            }
                            save_progress(progress)
                            success = True
                            break
                        else:
                            print(f"  Extraction not ready: {img_data.get('error')}. Retrying check...")
                    else:
                        elapsed = int(time.time() - start_time)
                        print(f"  Waiting... ({elapsed}s elapsed)")

                if success:
                    break
                else:
                    print(f"  Attempt {attempt} timed out waiting for image.")

            except Exception as e:
                print(f"  Error during attempt {attempt}: {e}")
                time.sleep(3)

        if not success:
            print(f"  FAILED to generate image for '{profession}' after {max_attempts} attempts.")
            progress[item_key] = {
                "status": "failed",
                "timestamp": datetime.now().isoformat(),
                "error": "Timeout or generation failure"
            }
            save_progress(progress)

        time.sleep(4)

    print("\nBatch generation execution finished!")

if __name__ == "__main__":
    main()
