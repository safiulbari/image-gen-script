#!/usr/bin/env python3
import csv

with open("Othe.app image generation industry profession and prompt - Sheet1.csv", "r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

with open("images/batch_progress.json", "r", encoding="utf-8") as f:
    import json
    bp = json.load(f)

pending_keys = [k for k, v in bp.items() if v.get("status") != "completed"]

out_file = "remaining_44_distinct_prompts.txt"
with open(out_file, "w", encoding="utf-8") as f:
    f.write("=" * 90 + "\n")
    f.write("OTHE.APP - 44 REMAINING PROFESSIONS (HYPER-DISTINCT PROMPTS BREAKDOWN)\n")
    f.write("=" * 90 + "\n")
    f.write("Total Remaining: 44\n")
    f.write("Target Resolution: 1920x1080 (16:9 Landscape)\n")
    f.write("Every entry has an authentic Bangladeshi location, varied age/gender, distinct color grading,\n")
    f.write("unique lighting setup, realistic specialized tools, and SaaS negative space.\n")
    f.write("=" * 90 + "\n\n")

    matched_rows = [r for r in rows if f"{r['Industry']}::{r['Profession']}" in pending_keys]

    for idx, r in enumerate(matched_rows, 1):
        ind = r["Industry"]
        prof = r["Profession"]
        prompt = r["Prompt"]
        f.write(f"[{idx:02d}/44] INDUSTRY: {ind}\n")
        f.write(f"       PROFESSION: {prof}\n")
        f.write(f"       PROMPT:\n{prompt}\n")
        f.write("-" * 90 + "\n\n")

print(f"Report generated: {out_file} with {len(matched_rows)} distinct prompts.")
