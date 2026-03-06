#!/usr/bin/env python3
"""
AI Script Generator
Generates video scripts for all 4 channels
Uses Ollama (free, runs on VPS) or simple templates
"""

import random
import json

CHANNEL_TOPICS = {
    "ai_tech_tamil": [
        "ChatGPT புதிய features 2025",
        "AI tools free ya use pannuvadhu eppadi",
        "Python automation beginners guide Tamil",
        "GitHub Copilot vs ChatGPT comparison",
        "Free AI image generators list 2025",
    ],
    "motivation": [
        "Success ku shortcut illai - real truth",
        "Elon Musk daily routine Tamil",
        "Morning habits of millionaires",
        "Failure nu oru success story",
        "Time management secrets Tamil",
    ],
    "facts_finance": [
        "India economy 2025 facts",
        "SIP investment basics Tamil",
        "World richest countries comparison",
        "Stock market beginners Tamil guide",
        "Crypto vs Gold vs Real estate 2025",
    ],
    "eggy_world": [
        "ABC Learning with Eggy",
        "123 Numbers fun Tamil",
        "Colors learning for kids",
        "Animals sounds learning",
        "Fruits and vegetables Tamil",
    ]
}

SCRIPT_TEMPLATES = {
    "ai_tech_tamil": """
நன்றி நண்பர்களே! இன்று நாம் {topic} பற்றி பார்க்கப் போகிறோம்.

{point1}

இது மிகவும் முக்கியமான விஷயம். {point2}

நீங்களும் இதை try பண்ணலாம். {point3}

Like பண்ணுங்க, Subscribe பண்ணுங்க! நன்றி!
""",
    "motivation": """
வணக்கம் நண்பர்களே! {topic} பற்றி இன்று பேசப் போகிறோம்.

{point1}

வெற்றிக்கு ஒரே ஒரு வழி தான் இருக்கு. {point2}

நீங்களும் இதை follow பண்ணுங்க. {point3}

உங்கள் கனவை நோக்கி தொடர்ந்து பயணியுங்கள்!
""",
    "facts_finance": """
வணக்கம்! இன்று {topic} பற்றிய சுவாரஸ்யமான facts பார்ப்போம்.

{point1}

இது உங்களுக்கு தெரியுமா? {point2}

இந்த தகவல் உங்கள் வாழ்க்கைக்கு உதவும். {point3}

Channel subscribe பண்ணுங்க மேலும் facts-க்கு!
""",
    "eggy_world": """
Hello friends! Today Eggy will teach us about {topic}!

{point1}

Can you repeat after Eggy? {point2}

Very good! You are so smart! {point3}

See you next time with Eggy! Bye bye!
"""
}

POINTS_BANK = {
    "ai_tech_tamil": [
        "இந்த tool முற்றிலும் இலவசம்",
        "நீங்கள் இதை laptop-லயே use பண்ணலாம்",
        "இதனால் உங்கள் time மிச்சமாகும்",
        "Beginners கூட easily கற்றுக்கொள்ளலாம்",
        "இது future-ல் மிகவும் useful ஆகும்",
    ],
    "motivation": [
        "ஒவ்வொரு தோல்வியும் ஒரு பாடம்",
        "Consistency தான் உண்மையான secret",
        "உங்கள் mindset மாற்றுங்கள்",
        "Small steps lead to big success",
        "Never give up on your dreams",
    ],
    "facts_finance": [
        "இந்த விஷயம் 90% பேருக்கு தெரியாது",
        "Compound interest என்பது magic",
        "Early investment மிகவும் முக்கியம்",
        "Risk management தெரிந்துகொள்ளுங்கள்",
        "Diversification is the key",
    ],
    "eggy_world": [
        "Let us learn together!",
        "This is so much fun!",
        "You are doing great!",
        "Keep practicing every day!",
        "Learning is wonderful!",
    ]
}

def generate_script(channel: str, topic: str = None) -> dict:
    """Generate a video script for given channel."""
    if topic is None:
        topic = random.choice(CHANNEL_TOPICS.get(channel, ["General Topic"]))

    template = SCRIPT_TEMPLATES.get(channel, SCRIPT_TEMPLATES["motivation"])
    points = POINTS_BANK.get(channel, [])

    selected_points = random.sample(points, min(3, len(points)))

    script = template.format(
        topic=topic,
        point1=selected_points[0] if len(selected_points) > 0 else "",
        point2=selected_points[1] if len(selected_points) > 1 else "",
        point3=selected_points[2] if len(selected_points) > 2 else "",
    )

    return {
        "channel": channel,
        "topic": topic,
        "script": script.strip(),
        "title": f"{topic} | Tamil",
        "description": f"{topic} பற்றிய முழுமையான வீடியோ. Like & Subscribe!",
        "tags": ["tamil", "education", channel, topic]
    }

if __name__ == "__main__":
    # Test all channels
    for ch in CHANNEL_TOPICS.keys():
        result = generate_script(ch)
        print(f"\n{'='*50}")
        print(f"Channel: {ch}")
        print(f"Topic: {result['topic']}")
        print(f"Script:\n{result['script']}")
