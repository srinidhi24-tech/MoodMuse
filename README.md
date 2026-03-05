# MoodMuse – Emotion-Aware Mood Journal & Music Recommender

MoodMuse is a journaling web application that allows users to record daily thoughts and analyze emotional tone from their entries. Based on the detected mood, the application recommends songs using Spotify integration and visualizes mood trends over time.

## Features

* **Journal Entries** – Users can write and save daily journal entries.
* **Mood Detection** – Detects emotional tone from text using rule-based sentiment logic.
* **Music Recommendations** – Suggests songs through Spotify API based on detected mood.
* **Mood Analytics** – Displays mood distribution and emotional trends through charts.
* **Entry History** – Users can view previous journal entries and track emotional patterns.

## Tech Stack

* **Backend:** Python, Flask
* **Frontend:** HTML, CSS
* **Data Storage:** JSON file (`data.json`)
* **API Integration:** Spotify API
* **Visualization:** Chart.js

## Project Structure

```
MoodMuse
│
├── app
│   ├── __init__.py
│   ├── routes.py
│   ├── mood_engine.py
│   ├── data.json
│   │
│   ├── templates
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── journal.html
│   │   ├── entries.html
│   │   ├── calendar.html
│   │   └── stats.html
│   │
│   └── static
│       └── css
│           └── style.css
│
├── requirements.txt
├── run.py
└── README.md
```

## How It Works

1. User writes a journal entry.
2. The system analyzes the text using rule-based sentiment logic.
3. A mood category (happy, sad, calm, etc.) is identified.
4. The app fetches relevant songs using Spotify API.
5. Mood statistics are updated and visualized in the analytics dashboard.

## Future Improvements

* Machine learning–based sentiment analysis
* Advanced emotion detection models
* Personalized music recommendations
* Long-term mood prediction and insights
