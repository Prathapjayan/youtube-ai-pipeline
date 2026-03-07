#!/usr/bin/env python3
"""
Background Music Generator - Creates ambient background music
"""
import numpy as np
import wave
import struct
import os
import random

def generate_background_music(duration: int, channel: str, output_path: str) -> bool:
    """Generate background music based on channel type."""
    try:
        sample_rate = 44100
        
        # Music styles per channel
        styles = {
            "ai_tech_tamil": {"tempo": 128, "mood": "electronic", "base_freq": 220},
            "facts_finance": {"tempo": 100, "mood": "corporate", "base_freq": 180},
            "motivation":    {"tempo": 140, "mood": "upbeat",     "base_freq": 260},
            "eggy_world":    {"tempo": 120, "mood": "playful",    "base_freq": 300},
        }
        style = styles.get(channel, styles["motivation"])
        
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        
        # Generate melody
        base  = style["base_freq"]
        music = np.zeros(len(t))
        
        # Layer multiple frequencies for rich sound
        freqs = [base, base*1.25, base*1.5, base*2.0]
        for i, freq in enumerate(freqs):
            vol = 0.3 / (i + 1)
            music += vol * np.sin(2 * np.pi * freq * t)
        
        # Add rhythm pulse
        beat_freq = style["tempo"] / 60
        rhythm = 0.1 * np.sin(2 * np.pi * beat_freq * t) ** 2
        music += rhythm
        
        # Fade in/out
        fade_samples = int(sample_rate * 1.5)
        music[:fade_samples]  *= np.linspace(0, 1, fade_samples)
        music[-fade_samples:] *= np.linspace(1, 0, fade_samples)
        
        # Normalize and lower volume (background)
        music = music / np.max(np.abs(music)) * 0.25
        music_int = (music * 32767).astype(np.int16)
        
        # Save as WAV
        with wave.open(output_path, 'w') as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(sample_rate)
            wav.writeframes(music_int.tobytes())
        
        print(f"✅ Background music created: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Music error: {e}")
        return False

if __name__ == "__main__":
    os.makedirs("test_output", exist_ok=True)
    generate_background_music(30, "ai_tech_tamil", "test_output/test_music.wav")
