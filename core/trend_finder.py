#!/usr/bin/env python3
"""
Viral Topic Finder Bot
Finds trending topics daily for FutureFables AI
Sends to Telegram automatically
"""

import os
import requests
import datetime
import random

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID   = os.getenv("TELEGRAM_CHAT_ID", "")

# Trending topic categories
VIRAL_TOPICS = {
    "animal_attacks": [
        "Lion attacks tourist 2025",
        "Crocodile vs hippo fight",
        "Most dangerous snake attacks",
        "Elephant attack compilation",
        "Shark attack caught on camera",
    ],
    "ai_technology": [
        "AI robot does impossible things 2025",
        "ChatGPT vs Gemini vs Claude comparison",
        "Robots replacing humans jobs 2025",
        "Tesla robot walking update",
        "AI generates realistic video 2025",
    ],
    "world_facts": [
        "Countries with highest salary 2025",
        "Most expensive cities in world",
        "Richest people in Asia 2025",
        "Smallest countries in world facts",
        "Most powerful passports 2025",
    ],
    "future_technology": [
        "Flying cars ready for 2025",
        "Brain computer interface update",
        "Quantum computer breakthrough",
        "Space tourism latest news",
        "Underwater city project 2025",
    ],
}

FINANCE_TOPICS_TAMIL = [
    "₹500 SIP invest பண்ணி ₹1 crore ஆக்குவது எப்படி?",
    "Credit card secrets யாரும் சொல்லாதது",
    "Nifty 50 என்றால் என்ன? Beginners guide",
    "Gold vs Bitcoin vs Real estate 2025 Tamil",
    "Dubai எப்படி rich ஆனது? Real story",
    "India 2030 economy prediction Tamil",
    "Stock market crash - என்ன பண்றது?",
    "Passive income ideas India 2025 Tamil",
    "Mutual fund vs Fixed deposit comparison",
    "How to become crorepati in 10 years Tamil",
    "Singapore vs India salary comparison",
    "Warren Buffett investment secrets Tamil",
    "Crypto tax India 2025 - what you need to know",
    "Real estate investment tips India Tamil",
    "Emergency fund என்றால் என்ன? How to build?",
]

def get_daily_topics() -> dict:
    """Get today's content plan."""
    today = datetime.datetime.now()
    day_of_week = today.strftime("%A")

    # Pick topics based on day
    viral_category = random.choice(list(VIRAL_TOPICS.keys()))
    viral_topic    = random.choice(VIRAL_TOPICS[viral_category])
    finance_topic  = random.choice(FINANCE_TOPICS_TAMIL)

    return {
        "date":          today.strftime("%d %B %Y"),
        "day":           day_of_week,
        "viral_topic":   viral_topic,
        "viral_category": viral_category,
        "finance_topic": finance_topic,
        "upload_times": {
            "finance": "10:00 AM",
            "viral":   "04:00 PM",
        }
    }


def generate_seo_title(topic: str, video_type: str) -> dict:
    """Generate SEO optimized title, description, tags."""

    if video_type == "finance":
        titles = [
            f"{topic} | Tamil Wealth Guide",
            f"{topic} - Must Watch Tamil",
            f"{topic} | FutureFables AI",
        ]
        tags = [
            "tamil finance", "wealth tamil", "investment tamil",
            "money tips tamil", "stock market tamil", "sip tamil",
            "mutual fund tamil", "passive income tamil", "tamil wealth",
            "futurefables", topic.lower()
        ]
        description = f"""🔥 {topic}

இந்த video-ல் நாம் பார்க்கப் போவது:
✅ Complete explanation in Tamil
✅ Real examples with numbers  
✅ Practical tips you can use today
✅ Common mistakes to avoid

👉 Subscribe பண்ணுங்க மேலும் videos-க்கு!
👉 Bell icon click பண்ணுங்க!

#TamilFinance #WealthTamil #InvestmentTamil #FutureFablesAI
"""

    else:  # viral
        titles = [
            f"{topic} | Shocking Facts",
            f"{topic} - You Won't Believe This!",
            f"{topic} | FutureFables AI",
        ]
        tags = [
            "viral", "shocking", "amazing facts", "future technology",
            "ai technology", "world facts", "futurefables",
            topic.lower(), "must watch", "incredible"
        ]
        description = f"""🔥 {topic}

Amazing content you've never seen before!
✅ Shocking facts
✅ Mind blowing moments
✅ Latest updates 2025

👉 Subscribe for more amazing content!
👉 Don't miss our daily videos!

#Viral #AmazingFacts #FutureFablesAI #MustWatch
"""

    return {
        "title":       random.choice(titles),
        "description": description.strip(),
        "tags":        tags,
    }


def send_daily_plan():
    """Send daily content plan to Telegram."""
    topics = get_daily_topics()

    finance_seo = generate_seo_title(topics["finance_topic"], "finance")
    viral_seo   = generate_seo_title(topics["viral_topic"], "viral")

    msg = f"""
📅 *DAILY CONTENT PLAN*
{topics['date']} — {topics['day']}

━━━━━━━━━━━━━━━━━━━━
💰 *FINANCE VIDEO* (10:00 AM)
━━━━━━━━━━━━━━━━━━━━
🎯 Topic: {topics['finance_topic']}
📌 Title: {finance_seo['title']}
⏱ Length: 10-15 minutes
📊 Expected: High watch time

━━━━━━━━━━━━━━━━━━━━
🔥 *VIRAL VIDEO* (04:00 PM)
━━━━━━━━━━━━━━━━━━━━
🎯 Topic: {topics['viral_topic']}
📌 Title: {viral_seo['title']}
⏱ Length: 3-5 minutes
📊 Expected: High views + subs

━━━━━━━━━━━━━━━━━━━━
🎯 *TODAY'S TARGET*
- Views goal: 500+
- Subs goal: +10
- Watch hours: +5 hrs

_FutureFables AI — Growing to 1000 subs!_ 🚀
"""
    send_telegram(msg.strip())
    return topics


def send_telegram(msg: str):
    if not TELEGRAM_BOT_TOKEN:
        print(msg)
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={
            "chat_id":    TELEGRAM_CHAT_ID,
            "text":       msg,
            "parse_mode": "Markdown"
        }, timeout=10)
        print("✅ Daily plan sent to Telegram!")
    except Exception as e:
        print(f"❌ Telegram error: {e}")


if __name__ == "__main__":
    print("🔍 Generating daily content plan...")
    topics = send_daily_plan()
    print(f"\n✅ Today's finance topic: {topics['finance_topic']}")
    print(f"✅ Today's viral topic:   {topics['viral_topic']}")
