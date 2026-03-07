#!/usr/bin/env python3
"""
AI-Powered Script Generator using Claude API
Generates unique Tamil/English scripts every time - no repetition!
"""

import random
import requests
import json
import os

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

CHANNEL_TOPICS = {
    "ai_tech_tamil": [
        "ChatGPT tips 2026", "Free AI tools", "AI image generation",
        "Python automation", "GitHub Copilot", "AI video making",
        "Midjourney prompts", "Google Gemini features", "Claude AI uses",
        "AI for students", "Machine learning basics", "AI money making"
    ],
    "facts_finance": [
        "SIP investment", "Nifty 50 basics", "Credit card tips",
        "India economy 2026", "Stock market basics", "Mutual funds",
        "Gold vs Bitcoin", "Real estate India", "Tax saving tips",
        "Emergency fund", "Passive income ideas", "Crypto basics India"
    ],
    "motivation": [
        "Morning routine success", "Study motivation", "Discipline habits",
        "Success mindset", "Time management", "Focus techniques",
        "Overthinking solutions", "Confidence building", "Goal setting",
        "Productivity hacks", "Positive thinking", "Fear overcome"
    ],
    "eggy_world": [
        "Animals sounds", "Colors learning", "Numbers fun",
        "Alphabets song", "Fruits names", "Vegetables learning",
        "Body parts", "Days of week", "Weather learning", "Transport"
    ]
}

CHANNEL_STYLE = {
    "ai_tech_tamil": {
        "lang": "Tamil mixed with English tech terms",
        "tone": "excited, informative, youth-friendly",
        "cta": "Like pannunga, Subscribe pannunga, notification bell press pannunga!"
    },
    "facts_finance": {
        "lang": "Tamil with English finance terms",
        "tone": "professional, trustworthy, helpful",
        "cta": "Share pannunga, Subscribe pannunga, comment pannunga!"
    },
    "motivation": {
        "lang": "Tamil inspirational language",
        "tone": "energetic, inspiring, emotional",
        "cta": "Unga friends ku share pannunga, Together grow aaguvom!"
    },
    "eggy_world": {
        "lang": "Simple English for kids",
        "tone": "fun, cheerful, educational",
        "cta": "Watch again! Learn with Eggy!"
    }
}

def generate_script_with_ai(channel: str, topic: str) -> str:
    """Generate unique script using Claude AI API."""
    style = CHANNEL_STYLE.get(channel, CHANNEL_STYLE["motivation"])
    
    prompt = f"""Create a YouTube Shorts script for topic: "{topic}"

Channel style: {style['tone']}
Language: {style['lang']}
Duration: 30-45 seconds when spoken

Requirements:
- Start with a HOOK (surprising fact or question) in first 3 seconds
- 3-4 key points about the topic
- End with: {style['cta']}
- Make it UNIQUE and ENGAGING
- No repetition, fresh content every time
- Format as natural speech, not bullet points

Write ONLY the script text, nothing else."""

    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            },
            json={
                "model": "claude-haiku-4-5-20261001",
                "max_tokens": 500,
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=30
        )
        data = response.json()
        if "content" in data and len(data["content"]) > 0:
            return data["content"][0]["text"].strip()
    except Exception as e:
        print(f"AI API error: {e}")
    
    return generate_fallback_script(channel, topic)

def generate_fallback_script(channel: str, topic: str) -> str:
    """Fallback script if API fails."""
    scripts = [
        f"Did you know? {topic} is changing everything in 2026! Here are 3 things you must know. First, this affects your daily life directly. Second, you can use this to earn money. Third, starting today will change your future. Don't miss this opportunity!",
        f"Stop what you're doing! {topic} - this is the most important thing you'll learn today. Many people don't know this secret. But after watching this, you will be ahead of everyone. Save this video and share with friends!",
        f"In just 30 seconds, I'll tell you everything about {topic}. This information took me months to learn. But you'll get it for free right now. Are you ready? Let's go!"
    ]
    return random.choice(scripts)

def generate_script(channel: str) -> dict:
    """Generate complete video script with metadata."""
    topics = CHANNEL_TOPICS.get(channel, CHANNEL_TOPICS["motivation"])
    
    # Pick random topic - avoid recent repeats
    topic = random.choice(topics)
    
    print(f"🤖 Generating AI script for: {topic}")
    
    # Generate unique script with AI
    script = generate_script_with_ai(channel, topic)
    
    # Generate scenes from script
    sentences = [s.strip() for s in script.replace('!', '.').replace('?', '.').split('.') if s.strip()]
    scenes = sentences[:5] if len(sentences) >= 5 else sentences + ["Subscribe for more!"] * (5 - len(sentences))
    
    # Generate catchy title
    title_styles = [
        f"{topic} - இதை யாரும் சொல்லல! #Shorts",
        f"{topic} | Must Watch 2026 #Shorts",
        f"🔥 {topic} | Tamil #Shorts",
        f"{topic} - Full Guide Tamil #Shorts",
        f"⚡ {topic} secrets revealed #Shorts"
    ]
    title = random.choice(title_styles)
    
    # Tags
    base_tags = ["tamil", "shorts", "viral", "2026", channel, topic]
    channel_tags = {
        "ai_tech_tamil": ["ai", "technology", "chatgpt", "tamil tech"],
        "facts_finance": ["finance", "investment", "money", "tamil finance"],
        "motivation": ["motivation", "success", "inspiration", "tamil motivation"],
        "eggy_world": ["kids", "learning", "education", "children"]
    }
    tags = base_tags + channel_tags.get(channel, [])
    
    return {
        "channel": channel,
        "topic": topic,
        "script": script,
        "scenes": scenes,
        "title": title[:100],
        "description": f"{topic} பற்றிய முக்கியமான தகவல்கள். Tamil la complete guide. Like & Subscribe! #tamil #shorts #{channel}",
        "tags": tags
    }

if __name__ == "__main__":
    for ch in CHANNEL_TOPICS.keys():
        result = generate_script(ch)
        print(f"\n{'='*50}")
        print(f"Channel: {ch}")
        print(f"Topic: {result['topic']}")
        print(f"Title: {result['title']}")
        print(f"Script:\n{result['script'][:200]}...")
