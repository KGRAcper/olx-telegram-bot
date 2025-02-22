import os
import time
import requests
from bs4 import BeautifulSoup
import telebot

# Pobranie tokenu bota z Rendera (zmienna środowiskowa)
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = "1466980597"  # Twoje Chat ID z Telegrama
bot = telebot.TeleBot(TOKEN)

# Słowa kluczowe do monitorowania
KEYWORDS = ["iphone 11", "bateria 86%"]

# Lista zapisanych linków, żeby unikać duplikatów
seen_ads = set()

def fetch_olx():
    url = "https://www.olx.pl/elektronika/telefony/q-iphone-11/"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    ads = soup.find_all("a", class_="css-rc5s2u")
    
    for ad in ads:
        title = ad.find("h6").text.lower()
        link = ad["href"]
        
        if any(keyword in title for keyword in KEYWORDS) and link not in seen_ads:
            seen_ads.add(link)
            send_telegram_message(title, link)

def send_telegram_message(title, link):
    message = f"🆕 Nowe ogłoszenie na OLX:\n**{title}**\n🔗 [Link do ogłoszenia]({link})"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
    }
    requests.post(url, data=data)

# Główna pętla - bot sprawdza OLX co 5 minut
while True:
    fetch_olx()
    time.sleep(300)  # Czekaj 5 minut
