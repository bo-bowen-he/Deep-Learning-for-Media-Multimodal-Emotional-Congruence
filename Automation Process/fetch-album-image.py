import requests
import os

# ----------------------------------------------------------------
# Last.fm API Album Art Downloader
# Get your free API key at: https://www.last.fm/api/account/create
# Then replace YOUR_API_KEY below
# ----------------------------------------------------------------

API_KEY = "17a8cffd04012f63e34fc5f668e7736a"
OUTPUT_DIR = "album_art"
os.makedirs(OUTPUT_DIR, exist_ok=True)

songs = [
  { "title": "Lovers Rock", "artist": "TV Girl" },
  { "title": "Raindance", "artist": "Dave" },
  { "title": "Water", "artist": "Tyla" },
  { "title": "Are You Bored Yet?", "artist": "Wallows" },
  { "title": "Juna", "artist": "Clairo" },
  { "title": "Stay", "artist": "Rihanna" },
  { "title": "Let It Happen", "artist": "Tame Impala" },
  { "title": "Why I Love You", "artist": "Jay-Z" },
  { "title": "Lost Woman Found", "artist": "Arca" },
  { "title": "Karma Police", "artist": "Radiohead" },
  { "title": "Little Trouble Girl", "artist": "Sonic Youth" },
  { "title": "I Don't Fuck With You", "artist": "Big Sean" },
  { "title": "A Pearl", "artist": "Mitski" },
  { "title": "We Don't Count", "artist": "Yves Tumor ft. Nina" },
  { "title": "Ain't It Funny", "artist": "Danny Brown" },
  { "title": "Au Pays du Cocaine", "artist": "Geese" },
  { "title": "Watching Him Fade Away", "artist": "Mac DeMarco" },
  { "title": "$0", "artist": "Cameron Winter" },
  { "title": "Real Love", "artist": "Big Thief" },
  { "title": "The Way Things Go", "artist": "Beabadoobee" },
  { "title": "Cherry-Coloured Funk", "artist": "Cocteau Twins" },
  { "title": "Air Supply", "artist": "Sweet Trip" },
  { "title": "Thinking Clean", "artist": "Blood Orange" },
  { "title": "Sometimes I Believe in God (Sometimes I Believe in Me)", "artist": "Bassvictim" },
  { "title": "In My Room", "artist": "Frank Ocean" }
]

def get_album_art(title, artist):
    url = "https://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "track.getInfo",
        "api_key": API_KEY,
        "artist": artist,
        "track": title,
        "format": "json"
    }
    response = requests.get(url, params=params)
    data = response.json()

    try:
        images = data["track"]["album"]["image"]
        # Get the largest image (last in list)
        img_url = images[-1]["#text"]
        if img_url:
            return img_url
    except (KeyError, IndexError):
        pass

    # Fallback: search by artist
    params2 = {
        "method": "artist.getInfo",
        "api_key": API_KEY,
        "artist": artist,
        "format": "json"
    }
    r2 = requests.get(url, params=params2)
    d2 = r2.json()
    try:
        return d2["artist"]["image"][-1]["#text"]
    except (KeyError, IndexError):
        return None

def download_image(img_url, filename):
    r = requests.get(img_url, stream=True)
    if r.status_code == 200:
        with open(filename, "wb") as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
        return True
    return False

print(f"Downloading album art for {len(songs)} songs...\n")

success, failed = 0, []

for song in songs:
    title = song["title"]
    artist = song["artist"]
    safe_name = title.replace("/", "-").replace(".", "").replace("'", "")
    filepath = os.path.join(OUTPUT_DIR, f"{safe_name}.jpg")

    print(f"Fetching: {title} — {artist}")
    img_url = get_album_art(title, artist)

    if img_url:
        ok = download_image(img_url, filepath)
        if ok:
            print(f"  ✅ Saved to {filepath}")
            success += 1
        else:
            print(f"  ❌ Failed to download image")
            failed.append(title)
    else:
        print(f"  ⚠️  No image found")
        failed.append(title)

print(f"\n✅ Downloaded: {success}/{len(songs)}")
if failed:
    print(f"❌ Failed: {', '.join(failed)}")