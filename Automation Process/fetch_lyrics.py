import requests
import os
import time
import re

LYRICS_DIR = "lyrics"
os.makedirs(LYRICS_DIR, exist_ok=True)

songs = [
    {"title": "Lovers Rock",                                          "artist": "TV Girl"},
    {"title": "Raindance",                                            "artist": "Dave"},
    {"title": "Water",                                                "artist": "Tyla"},
    {"title": "Are You Bored Yet?",                                   "artist": "Wallows",    "filename": "are-you-bored-yet-(feat.-clairo)"},
    {"title": "Juna",                                                 "artist": "Clairo"},
    {"title": "Stay",                                                 "artist": "Rihanna"},
    {"title": "Let It Happen",                                        "artist": "Tame Impala"},
    {"title": "Why I Love You",                                       "artist": "Jay-Z"},
    {"title": "Lost Woman Found",                                     "artist": "Arca"},
    {"title": "Karma Police",                                         "artist": "Radiohead"},
    {"title": "Little Trouble Girl",                                  "artist": "Sonic Youth"},
    {"title": "I Don't Fuck With You",                                "artist": "Big Sean"},
    {"title": "A Pearl",                                              "artist": "Mitski"},
    {"title": "We Don't Count",                                       "artist": "Yves Tumor"},
    {"title": "Ain't It Funny",                                       "artist": "Danny Brown"},
    {"title": "Au Pays du Cocaine",                                   "artist": "Geese"},
    {"title": "Watching Him Fade Away",                               "artist": "Mac DeMarco"},
    {"title": "$0",                                                   "artist": "Cameron Winter"},
    {"title": "Real Love",                                            "artist": "Big Thief"},
    {"title": "The Way Things Go",                                    "artist": "Beabadoobee"},
    {"title": "Cherry-Coloured Funk",                                 "artist": "Cocteau Twins"},
    {"title": "Air Supply",                                           "artist": "Sweet Trip"},
    {"title": "Thinking Clean",                                       "artist": "Blood Orange"},
    {"title": "Sometimes I Believe in God (Sometimes I Believe in Me)", "artist": "Bassvictim"},
    {"title": "In My Room",                                           "artist": "Frank Ocean"},
]


def to_kebab(title):
    title = title.lower()
    title = re.sub(r"[^\w\s\$\(\)\-\'\.]", "", title)
    title = re.sub(r"\s+", "-", title.strip())
    return title


def fetch_lyrics(artist, title):
    url = f"https://api.lyrics.ovh/v1/{requests.utils.quote(artist)}/{requests.utils.quote(title)}"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            return data.get("lyrics", "").strip()
    except requests.RequestException as e:
        print(f"  Request error: {e}")
    return None


print(f"Fetching lyrics for {len(songs)} songs...\n")
success, failed = 0, []

for song in songs:
    title = song["title"]
    artist = song["artist"]
    filename = song.get("filename") or to_kebab(title)
    filepath = os.path.join(LYRICS_DIR, f"{filename}.txt")

    print(f"Fetching: {title} — {artist}")
    lyrics = fetch_lyrics(artist, title)

    if lyrics:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(lyrics)
        print(f"  Saved → {filepath}")
        success += 1
    else:
        print(f"  Not found")
        failed.append(f"{title} — {artist}")

    time.sleep(0.5)  # be polite to the API

print(f"\nDone: {success}/{len(songs)} fetched")
if failed:
    print(f"Not found ({len(failed)}):")
    for s in failed:
        print(f"  - {s}")
