from flask import render_template, request, jsonify, session, redirect, url_for
from app import app
from app.utils import analyze_mood, get_songs_for_mood, save_entry, load_entries, get_mood_stats

app.secret_key = "anything-super-secret"

@app.route("/")
def home():
    theme = session.get("theme", "default")
    return render_template("home.html", theme=theme)

@app.route("/journal", methods=["GET", "POST"])
def journal():
    theme = session.get("theme", "default")

    if request.method == "POST":
        entry = request.form.get("entry")
        language = request.form.get("language", "english")  # 🆕 get language

        mood = analyze_mood(entry)  # ✅ first analyze the mood
        songs = get_songs_for_mood(mood, language)  # ✅ then pass both mood + language

        mood_to_class = {
            "Happy 😊": "happy",
            "Sad 😔": "sad",
            "Neutral 😐": "neutral",
            "Confused 😵‍💫": "confused",
            "Heartbroken 💔": "heartbroken",
            "In Love 😍": "love",
            "Chill 😌": "chill",
            "Wholesome 🤗": "wholesome"
        }

        background_class = mood_to_class.get(mood, "neutral")

        save_entry(entry, mood, songs)  # store the journal

        return render_template(
            "journal.html",
            entry=entry,
            mood=mood,
            songs=songs,
            background_class=background_class,
            theme=theme
        )

    return render_template("journal.html", theme=theme)


@app.route("/entries")
def entries():
    theme = session.get("theme", "default")
    entries = load_entries()
    return render_template("entries.html", entries=entries, theme=theme)

@app.route("/stats")
def stats():
    theme = session.get("theme", "default")
    mood_stats = get_mood_stats()
    labels = list(mood_stats.keys())
    values = list(mood_stats.values())
    return render_template("stats.html", labels=labels, values=values, theme=theme)

@app.route("/calendar")
def calendar():
    theme = session.get("theme", "default")
    return render_template("calendar.html",  theme=session.get("theme", "default"))

@app.route("/mood-history")
def mood_history():
    entries = load_entries()
    mood_data = [{"date": e.get("date", ""), "mood": e.get("mood", "")} for e in entries]
    return jsonify(mood_data)

@app.route("/set-theme", methods=["POST"])
def set_theme():
    theme = request.form.get("theme", "default")
    session["theme"] = theme
    return redirect(url_for("home"))

