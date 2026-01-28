import json
from datetime import datetime

FILE = "history.json"

def save_history(original, translated, src, tgt):
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        data = []

    data.append({
        "date": str(datetime.now()),
        "source_lang": src,
        "target_lang": tgt,
        "original": original,
        "translated": translated
    })

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_history():
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []
