#!/usr/bin/env python3
"""
Voiceover Generator with Background Music
"""
from gtts import gTTS
import os
import subprocess
from core.music_generator import generate_background_music

def generate_voiceover(script: str, channel: str, output_path: str) -> bool:
    try:
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
        
        # Language per channel
        lang_map = {
            "ai_tech_tamil": "ta",
            "facts_finance": "ta", 
            "motivation":    "ta",
            "eggy_world":    "en"
        }
        lang = lang_map.get(channel, "ta")
        
        # Generate voice
        voice_path = output_path.replace(".mp3", "_voice_only.mp3")
        tts = gTTS(text=script, lang=lang, slow=False)
        tts.save(voice_path)
        
        # Generate background music
        music_path = output_path.replace(".mp3", "_music.wav")
        generate_background_music(60, channel, music_path)
        
        # Mix voice + music using ffmpeg
        result = subprocess.run([
            "ffmpeg", "-y",
            "-i", voice_path,
            "-i", music_path,
            "-filter_complex", "[0:a]volume=1.0[voice];[1:a]volume=0.15[music];[voice][music]amix=inputs=2:duration=first",
            "-codec:a", "libmp3lame",
            "-q:a", "2",
            output_path
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            # Cleanup temp files
            os.remove(voice_path)
            os.remove(music_path)
            print(f"✅ Voiceover + music saved: {output_path}")
        else:
            # Fallback - use voice only
            os.rename(voice_path, output_path)
            print(f"✅ Voiceover saved (no music): {output_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Voiceover error: {e}")
        return False

if __name__ == "__main__":
    os.makedirs("test_output", exist_ok=True)
    generate_voiceover("Hello this is a test", "ai_tech_tamil", "test_output/test_voice.mp3")
