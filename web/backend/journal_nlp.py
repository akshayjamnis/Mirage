import re
from textblob import TextBlob

STRESS_WORDS = ["tired", "pressure", "deadline", "overwhelmed", "burnout"]
ANXIETY_WORDS = ["nervous", "worried", "panic", "fear", "anxious"]
DEPRESS_WORDS = ["sad", "hopeless", "empty", "cry", "lonely"]
SLEEP_WORDS = ["sleep", "insomnia", "rest", "dream"]
SOCIAL_WORDS = ["friend", "family", "talk", "support"]
ACTIVITY_WORDS = ["walk", "gym", "run", "exercise"]
WORK_WORDS = ["office", "boss", "job", "project", "meeting"]

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    return text

def keyword_score(text, keywords):
    return sum(text.count(word) for word in keywords)

def extract_features_from_journal(journal_text):
    text = clean_text(journal_text)
    sentiment = TextBlob(text).sentiment.polarity  # -1 to 1

    stress = keyword_score(text, STRESS_WORDS) + max(0, -sentiment * 5)
    anxiety = keyword_score(text, ANXIETY_WORDS) + max(0, -sentiment * 4)
    depression = keyword_score(text, DEPRESS_WORDS) + max(0, -sentiment * 6)
    sleep_quality = 10 - keyword_score(text, SLEEP_WORDS)
    social_support = keyword_score(text, SOCIAL_WORDS)
    physical_activity = keyword_score(text, ACTIVITY_WORDS)
    work_pressure = keyword_score(text, WORK_WORDS)

    return {
        "stress": min(10, int(stress)),
        "anxiety": min(10, int(anxiety)),
        "depression": min(10, int(depression)),
        "sleep_quality": max(0, min(10, int(sleep_quality))),
        "social_support": min(10, int(social_support)),
        "physical_activity": min(10, int(physical_activity)),
        "work_pressure": min(10, int(work_pressure))
    }
