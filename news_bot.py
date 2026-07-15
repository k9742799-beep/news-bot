import requests
import feedparser
import json
import time
import google.generativeai as genai

# ---------- DETAILS ----------
GEMINI_API_KEY = "AIza..."  # ✍️ YAHAN APNI AIza SE START HONE WALI KEY DAALO
JSONBIN_ID = "6a56e8bbf5f4af5e29905588"
JSONBIN_KEY = "$2a$10$EjTzN3oMNJZXfd5fcqF1XOaVynZDhoQPOZfquAqzNRWNmZNQ7uVru"
RSS_URL = "https://news.google.com/rss/search?q=Asansol+West+Bengal&hl=en-IN&gl=IN&ceid=IN:en"

# ---------- SETUP GEMINI ----------
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# ---------- TRANSLATE ----------
def translate_news(news_item):
    prompt = f"""
    Translate this English news into fluent, journalistic Urdu. 
    End with: "ماخذ: {news_item['link']}"
    
    Title: {news_item['title']}
    Summary: {news_item['summary']}
    """
    response = model.generate_content(prompt)
    return response.text

# ---------- BAQI KOD (FETCH AUR SAVE) SAME HAI ----------
def get_news():
    feed = feedparser.parse(RSS_URL)
    news_list = []
    for entry in feed.entries[:5]:
        news_list.append({
            "title": entry.title,
            "link": entry.link,
            "summary": entry.summary
        })
    return news_list

def save_to_jsonbin(final_news):
    url = f"https://api.jsonbin.io/v3/b/{JSONBIN_ID}"
    headers = {
        "Content-Type": "application/json",
        "X-Master-Key": JSONBIN_KEY
    }
    requests.put(url, json={"news": final_news}, headers=headers)

def main():
    print("Fetching news...")
    raw_news = get_news()
    
    urdu_news = []
    for item in raw_news:
        print(f"Translating: {item['title']}")
        translated = translate_news(item)
        urdu_news.append({"content": translated})
    
    print("Saving to database...")
    save_to_jsonbin(urdu_news)
    print("✅ Success! Website updated with auto news.")

if __name__ == "__main__":
    main()
