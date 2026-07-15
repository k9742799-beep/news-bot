import requests
import feedparser
import json
import time
import google.generativeai as genai

# ---------- APNI DETAILS YAHAN DAALO ----------
GEMINI_API_KEY = "apni_gemini_pro_key_yahan_daalo"
JSONBIN_ID = "apna_jsonbin_id_yahan_daalo"
JSONBIN_KEY = "apni_jsonbin_master_key_yahan_daalo"
RSS_URL = "https://news.google.com/rss/search?q=Asansol+West+Bengal&hl=en-IN&gl=IN&ceid=IN:en"

# ---------- SETUP GEMINI ----------
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# ---------- NEWS FETCH ----------
def get_news():
    feed = feedparser.parse(RSS_URL)
    news_list = []
    for entry in feed.entries[:5]:  # Sirf 5 latest news
        news_list.append({
            "title": entry.title,
            "link": entry.link,
            "summary": entry.summary
        })
    return news_list

# ---------- GEMINI TRANSLATE ----------
def translate_news(news_item):
    prompt = f"""
    Translate this English news into fluent, journalistic Urdu. 
    End with: "ماخذ: {news_item['link']}"
    
    Title: {news_item['title']}
    Summary: {news_item['summary']}
    """
    response = model.generate_content(prompt)
    return response.text

# ---------- JSONBIN PAR SAVE ----------
def save_to_jsonbin(final_news):
    url = f"https://api.jsonbin.io/v3/b/{JSONBIN_ID}"
    headers = {
        "Content-Type": "application/json",
        "X-Master-Key": JSONBIN_KEY
    }
    # JSONBin par purani news ko replace kar do
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
