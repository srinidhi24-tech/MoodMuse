import os
import re
import json
import random
from collections import Counter
from datetime import datetime
from textblob import TextBlob

try:
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
except ImportError:
    spotipy = None

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "").strip()
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "").strip()

if spotipy and SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET:
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET
        ))
    except Exception as e:
        print("Spotify init error:", e)
        sp = None
else:
    sp = None  


def analyze_mood(text: str) -> str:
    """Analyze mood from text via keywords; fallback by polarity."""
    polarity = TextBlob(text).sentiment.polarity
    cleaned_text = re.sub(r'[^\w\s]', '', text.lower())

    mood_keywords = {
        "Happy 😊": ["happy", "joyful", "excited", "cheerful", "delighted", "glad", "ecstatic"],
        "Sad 😔": ["sad", "unhappy", "depressed", "gloomy", "crying", "upset", "low"],
        "Neutral 😐": ["okay", "fine", "normal", "meh", "alright", "average"],
        "Confused 😵‍💫": ["confused", "unsure", "lost", "uncertain", "doubt", "mixed"],
        "Angry 😡": ["angry", "furious", "rage", "mad", "irritated", "annoyed"],
        "Crying 😭": ["crying", "tears", "sob", "weep", "wailing", "bawling"],
        "Chill 😌": ["chill", "relaxed", "calm", "peaceful", "serene", "laidback"],
        "Wholesome 🤗": ["grateful", "thankful", "blessed", "wholesome", "heartwarming", "kind"],
        "Stressed 😣": ["stressed", "pressure", "overwhelmed", "anxious", "tense", "exhausted"],
        "Anxious 😰": ["anxious", "nervous", "worried", "panic", "scared", "restless"],
        "Motivated 💪": ["motivated", "driven", "determined", "focused", "pumped", "goal", "ambition"],
        "Lazy 🛋️": ["lazy", "tired", "unmotivated", "sleepy", "sluggish", "lethargic", "procrastinate"],
        "Bored 😐": ["bored", "dull", "nothing", "idle", "uninspired", "monotonous", "meh"],
        "Hopeful 🌈": ["hopeful", "optimistic", "positive", "confident", "bright", "uplifting"],
        "Lonely 🥺": ["lonely", "alone", "isolated", "abandoned", "left out", "ignored"],
        "Productive ✅": ["productive", "accomplished", "efficient", "done", "completed", "focused", "progress"],
        "In Love 😍": ["love", "romantic", "crush", "affection", "infatuated", "adore", "sweetheart"],
        "Heartbroken 💔": ["heartbroken", "breakup", "lonely", "crushed", "rejected", "painful"]
    }

    for mood, keywords in mood_keywords.items():
        for word in keywords:
            if re.search(rf'\b{re.escape(word)}\b', cleaned_text):
                return mood

   
    if polarity > 0.5:
        return "Happy 😊"
    elif 0 < polarity <= 0.5:
        return "In Love 😍"
    elif polarity == 0:
        return "Neutral 😐"
    elif -0.3 < polarity < 0:
        return "Confused 😵‍💫"
    elif -0.5 < polarity <= -0.3:
        return "Sad 😔"
    else:
        return "Heartbroken 💔"



def get_songs_for_mood(mood: str, language: str = "english"):
    """
    Returns 5 Spotify track links for the mood and language if available.
    Otherwise returns reliable Spotify playlists (never broken).
    """
    mood_queries = {
        "Happy 😊": "happy upbeat feel-good",
        "Sad 😔": "sad emotional melancholy",
        "Neutral 😐": "calm chill relaxing",
        "Confused 😵‍💫": "ambient chill instrumental",
        "Angry 😡": "aggressive energetic workout",
        "Crying 😭": "heartbroken sad ballad",
        "Chill 😌": "chill lofi relaxing",
        "Wholesome 🤗": "feel-good wholesome positive",
        "Stressed 😣": "stress relief calm relax",
        "Anxious 😰": "soothing calm meditation",
        "Motivated 💪": "motivational hype gym",
        "Lazy 🛋️": "lazy mellow chill",
        "Bored 😐": "easygoing background chill",
        "Hopeful 🌈": "uplifting inspiring hopeful",
        "Lonely 🥺": "lonely acoustic mellow",
        "Productive ✅": "focus instrumental study",
        "In Love 😍": "romantic love soft",
        "Heartbroken 💔": "heartbreak emotional",
    }

    
    lang_bias = {
        "english": ("", "IN"),
        "hindi": ("genre:bollywood", "IN"),
        "tamil": ("genre:tamil", "IN"),
        "telugu": ("genre:telugu", "IN"),
        "kannada": ("genre:kannada", "IN"),
        "korean": ("genre:k-pop", "KR"),
        "spanish": ("genre:latin", "ES"),
    }
    genre_tag, market = lang_bias.get(language.lower(), ("", "IN"))

    playlist_fallbacks = {
        "Happy 😊": [
            "https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC",
            "https://open.spotify.com/playlist/37i9dQZF1DX3rxVfibe1L0",
            "https://open.spotify.com/playlist/37i9dQZF1DX9XIFQuFvzM4",
        ],
        "Sad 😔": [
            "https://open.spotify.com/playlist/37i9dQZF1DWVrtsSlLKzro",
            "https://open.spotify.com/playlist/37i9dQZF1DWSqBruwoIXkA",
            "https://open.spotify.com/playlist/37i9dQZF1DX7qK8ma5wgG1",
        ],
        "Neutral 😐": [
            "https://open.spotify.com/playlist/37i9dQZF1DX4WYpdgoIcn6",
            "https://open.spotify.com/playlist/37i9dQZF1DWZeKCadgRdKQ",
            "https://open.spotify.com/playlist/37i9dQZF1DX2PQDq3PdrHQ",
        ],
    }

   
    if sp:
        try:
            base = mood_queries.get(mood, "mood booster")
            query = f"{genre_tag} {base}".strip()

            results = sp.search(q=query, type="track", limit=15, market=market)
            tracks = results.get("tracks", {}).get("items", [])

           
            if not tracks:
                results = sp.search(q=base, type="track", limit=15)
                tracks = results.get("tracks", {}).get("items", [])

            if tracks:
                random.shuffle(tracks)
                return [t["external_urls"]["spotify"] for t in tracks[:5]]
        except Exception as e:
            print("Spotify search error:", e)


    return playlist_fallbacks.get(mood, [
        "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M"
    ])


DATA_FILE = "data.json"

def load_entries():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_entry(entry, mood, songs):
    data = load_entries()
    data.append({
        "entry": entry,
        "mood": mood,
        "songs": songs,
        "date": datetime.now().strftime("%Y-%m-%d")
    })
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_mood_stats():
    entries = load_entries()
    return Counter(e["mood"] for e in entries)

