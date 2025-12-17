import requests
import os

BASE_URL = "https://api.mangadex.org"
MANGA_ID = "f98660a1-d2e2-461c-960d-7bd13df8b76d"
MANGA_TITLE = "Myriad Realms Gatekeeper"

# -----------------------------
# Get chapter list
# -----------------------------
def getChapterInfo(lang=None):
    if lang is None:
        lang = ["en"]
    params = {"translatedLanguage[]": lang}
    r = requests.get(f"{BASE_URL}/manga/{MANGA_ID}/feed", params=params)
    r.raise_for_status()
    return r

# -----------------------------
# Download a single chapter
# -----------------------------
def downloadChapter(chapter_id, idx):
    r = requests.get(f"{BASE_URL}/at-home/server/{chapter_id}")
    r.raise_for_status()
    r_json = r.json()

    host = r_json["baseUrl"]
    chapter_hash = r_json["chapter"]["hash"]
    pages = r_json["chapter"]["data"]
    folder_path = f"data/{MANGA_TITLE}/chapter {idx}/"
    os.makedirs(folder_path, exist_ok=True)

    for page in pages:
        
        url = f"{host}/data/{chapter_hash}/{page}"
        r = requests.get(url)
        r.raise_for_status()
        with open(f"{folder_path}/{page}", "wb") as f:
            f.write(r.content)

    print(f"Downloaded {len(pages)} pages to {folder_path}.")

# -----------------------------
# MAIN
# -----------------------------
print("Getting Chapters...")
chapters = getChapterInfo()
chapter_ids = [chapter["id"] for chapter in chapters.json()["data"]]
print(chapter_ids)

print("Downloading first chapter...")
for idx,chapter_id in enumerate(chapter_ids):
    downloadChapter(chapter_id, idx)
