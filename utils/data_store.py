import os
import pandas as pd
from datetime import datetime, timedelta
import random

# ==========================================
# --- Data Store for Mood Logging ---
# ==========================================

LOG_FILE = "mood_logs.csv"

def get_log_filepath():
    """Gets the absolute path of the local CSV file in the current directory."""
    return os.path.abspath(LOG_FILE)


def init_data_store():
    """Initializes the CSV log file if it doesn't already exist."""
    path = get_log_filepath()
    if not os.path.exists(path):
        df = pd.DataFrame(columns=["timestamp", "score", "mood", "influencers", "notes"])
        df.to_csv(path, index=False)
        
        # Baseline entry
        append_mood_log(
            score=5.0,
            mood="neutral",
            influencers="Baseline",
            notes="EmpathyBot 2.0 system initialized.",
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )


def load_mood_logs():
    """Loads all mood logs from the CSV file as a Pandas DataFrame."""
    init_data_store()
    path = get_log_filepath()
    try:
        df = pd.read_csv(path)
        if df.empty:
            return pd.DataFrame(columns=["timestamp", "score", "mood", "influencers", "notes"])
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["score"] = pd.to_numeric(df["score"], errors="coerce").fillna(5.0)
        df["mood"] = df["mood"].astype(str)
        df["influencers"] = df["influencers"].fillna("")
        df["notes"] = df["notes"].fillna("")
        return df.sort_values(by="timestamp").reset_index(drop=True)
    except Exception as e:
        print(f"Error loading logs: {e}")
        return pd.DataFrame(columns=["timestamp", "score", "mood", "influencers", "notes"])


def append_mood_log(score, mood, influencers="", notes="", timestamp=None):
    """Appends a new mood log entry to the CSV database."""
    init_data_store()
    path = get_log_filepath()
    
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    elif isinstance(timestamp, datetime):
        timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        
    if isinstance(influencers, list):
        influencers = ", ".join(str(i).strip() for i in influencers if i)
    
    new_entry = pd.DataFrame([{
        "timestamp": timestamp,
        "score": float(score),
        "mood": str(mood).lower().strip(),
        "influencers": str(influencers).strip(),
        "notes": str(notes).strip()
    }])
    
    try:
        new_entry.to_csv(path, mode='a', header=not os.path.exists(path), index=False)
        return True
    except Exception as e:
        print(f"Error appending log: {e}")
        return False


def delete_mood_log(index_or_timestamp):
    """Deletes a single mood log by index or by timestamp string."""
    init_data_store()
    path = get_log_filepath()
    try:
        df = pd.read_csv(path)
        if isinstance(index_or_timestamp, int):
            if 0 <= index_or_timestamp < len(df):
                df = df.drop(index=index_or_timestamp).reset_index(drop=True)
                df.to_csv(path, index=False)
                return True
        else:
            ts_str = str(index_or_timestamp)
            df = df[df["timestamp"] != ts_str].reset_index(drop=True)
            df.to_csv(path, index=False)
            return True
    except Exception as e:
        print(f"Error deleting entry: {e}")
    return False


def populate_sample_data():
    """Populates realistic mock historical entries for the past 14 days."""
    sample_records = [
        {"days_ago": 13, "score": 6.5, "mood": "happy", "influencers": "Exercise/Sport, Sleep/Rest", "notes": "Went for a morning run and felt energized."},
        {"days_ago": 12, "score": 4.0, "mood": "anxious", "influencers": "Work/Study", "notes": "Heavy workload and upcoming deadlines created friction."},
        {"days_ago": 11, "score": 5.0, "mood": "neutral", "influencers": "Diet/Nutrition", "notes": "Routine day, caught up on chores."},
        {"days_ago": 10, "score": 3.0, "mood": "tired", "influencers": "Sleep/Rest, Work/Study", "notes": "Stayed up late debugging, need more rest."},
        {"days_ago": 9,  "score": 7.0, "mood": "happy", "influencers": "Mindfulness, Relationships", "notes": "Had dinner with good friends and practiced 10m meditation."},
        {"days_ago": 8,  "score": 7.5, "mood": "happy", "influencers": "Hobbies/Play, Exercise/Sport", "notes": "Played music and did light yoga."},
        {"days_ago": 7,  "score": 5.5, "mood": "neutral", "influencers": "Sleep/Rest", "notes": "Quiet Sunday preparing for the week."},
        {"days_ago": 6,  "score": 3.5, "mood": "anxious", "influencers": "Work/Study", "notes": "Monday morning stress spike, felt overwhelmed by inbox."},
        {"days_ago": 5,  "score": 4.5, "mood": "tired", "influencers": "Sleep/Rest", "notes": "Midweek slump, worked on pacing myself."},
        {"days_ago": 4,  "score": 6.0, "mood": "happy", "influencers": "Relationships, Mindfulness", "notes": "Walked in nature and had an honest talk with a friend."},
        {"days_ago": 3,  "score": 8.0, "mood": "happy", "influencers": "Hobbies/Play, Exercise/Sport", "notes": "Finished a creative project! Feeling accomplished."},
        {"days_ago": 2,  "score": 7.0, "mood": "happy", "influencers": "Sleep/Rest, Diet/Nutrition", "notes": "Great 8 hours of sleep, peaceful mood."},
        {"days_ago": 1,  "score": 5.5, "mood": "neutral", "influencers": "Work/Study", "notes": "Solid productive day without too much tension."},
        {"days_ago": 0,  "score": 8.5, "mood": "happy", "influencers": "Mindfulness, Relationships, Health", "notes": "Grateful and grounded today."}
    ]
    
    # Reset and write new data
    path = get_log_filepath()
    now = datetime.now()
    rows = []
    for rec in sample_records:
        ts = (now - timedelta(days=rec["days_ago"], hours=random.randint(1, 8))).strftime("%Y-%m-%d %H:%M:%S")
        rows.append({
            "timestamp": ts,
            "score": rec["score"],
            "mood": rec["mood"],
            "influencers": rec["influencers"],
            "notes": rec["notes"]
        })
    df_sample = pd.DataFrame(rows)
    df_sample = df_sample.sort_values(by="timestamp").reset_index(drop=True)
    df_sample.to_csv(path, index=False)
    return True


def clear_all_logs():
    """Resets the CSV file by clearing all entries."""
    path = get_log_filepath()
    if os.path.exists(path):
        try:
            os.remove(path)
        except Exception as e:
            print(f"Error deleting file: {e}")
    init_data_store()
