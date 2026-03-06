#!/usr/bin/env python3
"""
Voiceover Generator
Tamil + English using gTTS (100% FREE)
"""

import os
from gtts import gTTS

CHANNEL_LANGUAGE = {
    "ai_tech_tamil":  {"lang": "ta", "tld": "co.in"},
    "motivation":     {"lang": "ta", "tld": "co.in"},
    "facts_finance":  {"lang": "ta", "tld": "co.in"},
    "eggy_world":     {"lang": "en", "tld": "co.in"},
}

def generate_voiceover(text: str, channel: str, output_path: str) -> bool:
    """Generate voiceover audio from text."""
    try:
        lang_config = CHANNEL_LANGUAGE.get(channel, {"lang": "ta", "tld": "co.in"})
        
        # Clean text for TTS
        text = text.replace("*", "").replace("#", "").strip()
        
        tts = gTTS(
            text=text,
            lang=lang_config["lang"],
            tld=lang_config["tld"],
            slow=False
        )
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        tts.save(output_path)
        print(f"✅ Voiceover saved: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Voiceover error: {e}")
        return False

if __name__ == "__main__":
    # Test voiceover
    test_text = "வணக்கம் நண்பர்களே! இன்று AI பற்றி பேசப் போகிறோம்!"
    os.makedirs("test_output", exist_ok=True)
    generate_voiceover(test_text, "ai_tech_tamil", "test_output/test_voice.mp3")
    print("Test complete! Check test_output/test_voice.mp3")
