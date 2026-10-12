#!/usr/bin/env python3
"""
Generate an interactive HTML report listing all generated images with checkboxes.
The user can select images to delete/regenerate. Upon clicking "Export Selection",
 a JSON file `selected_for_regen.json` containing the selected keys will be downloaded.

Usage:
    python generate_report.py
"""
import json
import base64
from pathlib import Path
import re

# Workspace paths
WORKSPACE_DIR = Path("/Users/safiulbari/Documents/Office projects/othe.app images")
BASE_OUT_DIR = WORKSPACE_DIR / "images"
PROGRESS_FILE = BASE_OUT_DIR / "batch_progress.json"
REPORT_FILE = WORKSPACE_DIR / "report.html"

# Load progress data
if not PROGRESS_FILE.exists():
    raise FileNotFoundError(f"Progress file not found: {PROGRESS_FILE}")
with PROGRESS_FILE.open(encoding="utf-8") as f:
    progress = json.load(f)

# Helper to sanitize names (same as generate_all_gemini.py)
def sanitize_name(name: str) -> str:
    return re.sub(r"[/\\:*?\"<>|]", "-", name).strip() or "untitled"

rows_html = []
for key, data in progress.items():
    industry, profession = key.split("::", 1)
    safe_ind = sanitize_name(industry)
    safe_prof = sanitize_name(profession)
    img_path = BASE_OUT_DIR / safe_ind / f"{safe_prof}.png"
    if not img_path.exists():
        continue
    b64 = base64.b64encode(img_path.read_bytes()).decode("utf-8")
    img_data = f"data:image/png;base64,{b64}"
    rows_html.append(f"""
    <tr>
        <td><input type='checkbox' name='select' value='{key}'/></td>
        <td>{industry}</td>
        <td>{profession}</td>
        <td><img src='{img_data}' alt='{profession}' style='max-width:200px; max-height:120px;'/></td>
    </tr>
    """)

html_content = f"""
<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <title>Othe.app Image Selection Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        tr:hover {{ background-color: #f9f9f9; }}
    </style>
</head>
<body>
    <h1>Othe.app Image Selection Report</h1>
    <p>Select images to delete or regenerate and click "Export Selection".</p>
    <form id='selectionForm'>
        <table>
            <thead>
                <tr>
                    <th>Select</th>
                    <th>Industry</th>
                    <th>Profession</th>
                    <th>Preview</th>
                </tr>
            </thead>
            <tbody>
                {"\n".join(rows_html)}
            </tbody>
        </table>
        <br/>
        <button type='button' onclick='exportSelection()'>Export Selection</button>
    </form>
    <script>
        function exportSelection() {{
            const checked = document.querySelectorAll('input[name="select"]:checked');
            const selected = Array.from(checked).map(cb => cb.value);
            const blob = new Blob([JSON.stringify(selected, null, 2)], {{type: 'application/json'}});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'selected_for_regen.json';
            a.click();
            URL.revokeObjectURL(url);
        }}
    </script>
</body>
</html>
"""

REPORT_FILE.write_text(html_content, encoding='utf-8')
print(f"Report generated at {REPORT_FILE}")
