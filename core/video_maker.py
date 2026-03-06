#!/usr/bin/env python3
"""
Video Maker
Creates video from images + voiceover using MoviePy (FREE)
"""

import os
import requests
import random
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips

# Free image APIs
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_KEY", "")
PEXELS_API_KEY = os.getenv("PEXELS_KEY", "")

CHANNEL_KEYWORDS = {
    "ai_tech_tamil":  ["technology", "computer", "artificial intelligence", "coding"],
    "motivation":     ["success", "motivation", "sunrise", "achievement"],
    "facts_finance":  ["finance", "money", "investment", "business"],
    "eggy_world":     ["colorful", "cartoon", "children", "education"],
}

CHANNEL_COLORS = {
    "ai_tech_tamil":  {"bg": (10, 10, 40),    "text": (0, 200, 255)},
    "motivation":     {"bg": (40, 10, 10),    "text": (255, 200, 0)},
    "facts_finance":  {"bg": (10, 40, 10),    "text": (0, 255, 100)},
    "eggy_world":     {"bg": (255, 240, 200), "text": (255, 100, 0)},
}

VIDEO_WIDTH  = 1920
VIDEO_HEIGHT = 1080
FPS = 24


def fetch_image_unsplash(keyword: str, save_path: str) -> bool:
    """Fetch free image from Unsplash."""
    try:
        if not UNSPLASH_ACCESS_KEY:
            return False
        url = f"https://api.unsplash.com/photos/random?query={keyword}&orientation=landscape"
        headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            img_url = r.json()["urls"]["regular"]
            img_data = requests.get(img_url, timeout=15).content
            with open(save_path, "wb") as f:
                f.write(img_data)
            return True
    except Exception as e:
        print(f"Unsplash error: {e}")
    return False


def fetch_image_pexels(keyword: str, save_path: str) -> bool:
    """Fetch free image from Pexels."""
    try:
        if not PEXELS_API_KEY:
            return False
        url = f"https://api.pexels.com/v1/search?query={keyword}&per_page=5&orientation=landscape"
        headers = {"Authorization": PEXELS_API_KEY}
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            photos = r.json().get("photos", [])
            if photos:
                img_url = random.choice(photos)["src"]["large"]
                img_data = requests.get(img_url, timeout=15).content
                with open(save_path, "wb") as f:
                    f.write(img_data)
                return True
    except Exception as e:
        print(f"Pexels error: {e}")
    return False


def create_text_image(text: str, channel: str, save_path: str,
                       width: int = VIDEO_WIDTH, height: int = VIDEO_HEIGHT):
    """Create a beautiful text slide image."""
    colors = CHANNEL_COLORS.get(channel, {"bg": (20, 20, 20), "text": (255, 255, 255)})

    img = Image.new("RGB", (width, height), color=colors["bg"])
    draw = ImageDraw.Draw(img)

    # Gradient overlay effect
    for i in range(height):
        alpha = int(30 * (i / height))
        draw.line([(0, i), (width, i)],
                  fill=(colors["bg"][0] + alpha,
                        colors["bg"][1] + alpha,
                        colors["bg"][2] + alpha))

    # Try to use a font, fallback to default
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 35)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Word wrap text
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + " " + word if current_line else word
        bbox = draw.textbbox((0, 0), test_line, font=font_large)
        if bbox[2] < width - 100:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    # Draw text centered
    total_height = len(lines) * 80
    start_y = (height - total_height) // 2

    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font_large)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = start_y + i * 80

        # Shadow effect
        draw.text((x + 3, y + 3), line, font=font_large, fill=(0, 0, 0))
        draw.text((x, y), line, font=font_large, fill=colors["text"])

    # Bottom watermark
    watermark = "Subscribe for more!"
    draw.text((width // 2 - 150, height - 60),
              watermark, font=font_small, fill=(150, 150, 150))

    img.save(save_path)
    return save_path


def create_video(script: str, channel: str,
                 audio_path: str, output_path: str) -> bool:
    """
    Create full video from script + audio.
    Splits script into scenes, creates image per scene.
    """
    try:
        os.makedirs("temp_frames", exist_ok=True)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Split script into scenes (by line)
        scenes = [s.strip() for s in script.split("\n") if s.strip()]
        if not scenes:
            scenes = [script]

        # Load audio to get duration
        audio = AudioFileClip(audio_path)
        total_duration = audio.duration
        scene_duration = total_duration / len(scenes)

        print(f"📹 Creating {len(scenes)} scenes, {scene_duration:.1f}s each")

        clips = []
        keywords = CHANNEL_KEYWORDS.get(channel, ["education"])

        for i, scene_text in enumerate(scenes):
            img_path = f"temp_frames/frame_{i}.jpg"

            # Try to get real image, fallback to text slide
            keyword = random.choice(keywords)
            fetched = fetch_image_unsplash(keyword, img_path)
            if not fetched:
                fetched = fetch_image_pexels(keyword, img_path)
            if not fetched:
                # Create text slide as fallback
                create_text_image(scene_text, channel, img_path)

            # Resize image to video dimensions
            img = Image.open(img_path).convert("RGB")
            img = img.resize((VIDEO_WIDTH, VIDEO_HEIGHT), Image.LANCZOS)

            # Overlay text on image
            draw = ImageDraw.Draw(img)
            colors = CHANNEL_COLORS.get(channel, {"bg": (0,0,0), "text": (255,255,255)})
            try:
                font = ImageFont.truetype(
                    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 45)
            except:
                font = ImageFont.load_default()

            # Text box at bottom
            box_y = VIDEO_HEIGHT - 180
            draw.rectangle([(0, box_y), (VIDEO_WIDTH, VIDEO_HEIGHT)],
                          fill=(0, 0, 0, 180))

            # Wrap and draw text
            words = scene_text.split()
            line = ""
            text_lines = []
            for word in words:
                test = line + " " + word if line else word
                bbox = draw.textbbox((0, 0), test, font=font)
                if bbox[2] < VIDEO_WIDTH - 60:
                    line = test
                else:
                    text_lines.append(line)
                    line = word
            if line:
                text_lines.append(line)

            for j, tl in enumerate(text_lines[:2]):
                draw.text((30, box_y + 20 + j * 55), tl,
                         font=font, fill=colors["text"])

            final_img_path = f"temp_frames/final_frame_{i}.jpg"
            img.save(final_img_path)

            clip = ImageClip(final_img_path).with_duration(scene_duration)
            clips.append(clip)

        # Combine all clips
        final_video = concatenate_videoclips(clips, method="compose")
        final_video = final_video.with_audio(audio)

        print(f"🎬 Rendering video: {output_path}")
        final_video.write_videofile(
            output_path,
            fps=FPS,
            codec="libx264",
            audio_codec="aac",
            logger=None
        )

        # Cleanup temp files
        import shutil
        shutil.rmtree("temp_frames", ignore_errors=True)

        print(f"✅ Video ready: {output_path}")
        return True

    except Exception as e:
        print(f"❌ Video creation error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Quick test
    test_script = """வணக்கம் நண்பர்களே!
இன்று AI பற்றி பேசப் போகிறோம்.
இந்த tool முற்றிலும் இலவசம்.
Like பண்ணுங்க Subscribe பண்ணுங்க!"""

    os.makedirs("test_output", exist_ok=True)

    # Generate test audio first
    from gtts import gTTS
    tts = gTTS(text=test_script, lang="ta", tld="co.in")
    tts.save("test_output/test_voice.mp3")

    # Create video
    create_video(
        script=test_script,
        channel="ai_tech_tamil",
        audio_path="test_output/test_voice.mp3",
        output_path="test_output/test_video.mp4"
    )
