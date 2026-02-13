import json
import os

CONFIG_FILE = "categories.json"

DEFAULT_CATEGORIES = {
    "Text_Files": [".txt", ".md", ".rtf"],
    "PDFs": [".pdf"],
    "Word_Docs": [".docx", ".doc", ".odt"],
    "Spreadsheets": [".csv", ".xlsx", ".xls", ".ods"],
    "Photos": [".jpg", ".jpeg", ".png", ".bmp"],
    "Music": [".mp3", ".wav", ".flac"],
    "Videos": [".mp4", ".mkv", ".mov"],
    "Compressed": [".zip", ".tar", ".rar"],
    "Scripts": [".sh", ".py", ".js"]
}

def load_categories():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return DEFAULT_CATEGORIES

def save_categories(categories):
    with open(CONFIG_FILE, "w") as f:
        json.dump(categories, f, indent=4)

FILE_CATEGORIES = load_categories()
DEFAULT_FOLDER = "Others"