import requests
import feedparser
import json
import time

# ---------- DETAILS (SIRF API KEY CHANGE KARO) ----------
PERPLEXITY_API_KEY = "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"   # ✅ Ye key daal di
JSONBIN_ID = "6a56e8bbf5f4af5e29905588"
JSONBIN_KEY = "$2a$10$EjTzN3oMNJZXfd5fcqF1XOaVynZDhoQPOZfquAqzNRWNmZNQ7uVru"
RSS_URL = "https://news.google.com/rss/search?q=Asansol+West+Bengal&hl=en-IN&gl=IN&ceid=IN:en"

# ---------- PERPLEXITY API CALL ----------
def translate_news(news_item):
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }
    prompt = f"""
    Translate this English news into fluent, journalistic Urdu. 
    End with: "ماخذ: {news_item['link']}"
    
    Title: {news_item['title']}
    Summary: {news_item['summary']}
    """
    data = {
        "model": "llama-3.1-sonar-small-128k-online",
        "messages": [
            {"role": "system", "content": "You are a professional Urdu translator."},
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    return result["choices"][0]["message"]["content"]

# ---------- NEWS FETCH ----------
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

# ---------- JSONBIN PAR SAVE ----------
def save_to_jsonbin(final_news):
    url = f"https://api.jsonbin.io/v3/b/{JSONBIN_ID}"
    headers = {
        "Content-Type": "application/json",
        "X-Master-Key": JSONBIN_KEY
    }
    requests.put(url, json={"news": final_news}, headers=headers)

# ---------- MAIN LOGIC ----------
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
