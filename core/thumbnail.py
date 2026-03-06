#!/usr/bin/env python3
"""
Thumbnail Generator
Creates YouTube thumbnails using Pillow (FREE)
"""

import os
from PIL import Image, ImageDraw, ImageFont

CHANNEL_STYLES = {
    "ai_tech_tamil": {
        "bg_color":    (5, 5, 30),
        "title_color": (0, 220, 255),
        "accent":      (255, 50, 50),
        "emoji":       "🤖",
    },
    "motivation": {
        "bg_color":    (30, 10, 5),
        "title_color": (255, 210, 0),
        "accent":      (255, 100, 0),
        "emoji":       "🔥",
    },
    "facts_finance": {
        "bg_color":    (5, 25, 5),
        "title_color": (0, 255, 120),
        "accent":      (255, 215, 0),
        "emoji":       "💰",
    },
    "eggy_world": {
        "bg_color":    (255, 245, 200),
        "title_color": (255, 80, 0),
        "accent":      (50, 180, 50),
        "emoji":       "🥚",
    },
}

THUMB_WIDTH  = 1280
THUMB_HEIGHT = 720


def create_thumbnail(title: str, channel: str, output_path: str) -> bool:
    """Create a YouTube thumbnail."""
    try:
        style = CHANNEL_STYLES.get(channel, CHANNEL_STYLES["motivation"])
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Base image
        img = Image.new("RGB", (THUMB_WIDTH, THUMB_HEIGHT), style["bg_color"])
        draw = ImageDraw.Draw(img)

        # Gradient background
        for i in range(THUMB_HEIGHT):
            ratio = i / THUMB_HEIGHT
            r = int(style["bg_color"][0] + (style["accent"][0] - style["bg_color"][0]) * ratio * 0.3)
            g = int(style["bg_color"][1] + (style["accent"][1] - style["bg_color"][1]) * ratio * 0.3)
            b = int(style["bg_color"][2] + (style["accent"][2] - style["bg_color"][2]) * ratio * 0.3)
            draw.line([(0, i), (THUMB_WIDTH, i)], fill=(r, g, b))

        # Accent bar left side
        draw.rectangle([(0, 0), (18, THUMB_HEIGHT)], fill=style["accent"])

        # Accent bar bottom
        draw.rectangle([(0, THUMB_HEIGHT - 18), (THUMB_WIDTH, THUMB_HEIGHT)],
                       fill=style["accent"])

        # Load fonts
        try:
            font_title = ImageFont.truetype(
                "/usr/share/fonts/truetype/lohit-tamil/Lohit-Tamil.ttf", 72)
            font_sub = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
            font_emoji = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 120)
        except:
            font_title = ImageFont.load_default()
            font_sub   = ImageFont.load_default()
            font_emoji = ImageFont.load_default()

        # Word wrap title
        words = title.split()
        lines = []
        current = ""
        for word in words:
            test = current + " " + word if current else word
            bbox = draw.textbbox((0, 0), test, font=font_title)
            if bbox[2] < THUMB_WIDTH - 200:
                current = test
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)

        # Draw title
        start_y = THUMB_HEIGHT // 2 - (len(lines) * 85) // 2
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font_title)
            x = (THUMB_WIDTH - bbox[2]) // 2
            y = start_y + i * 85
            # Shadow
            draw.text((x+4, y+4), line, font=font_title, fill=(0, 0, 0))
            # Main text
            draw.text((x, y), line, font=font_title, fill=style["title_color"])

        # Channel name bottom right
        ch_name = channel.replace("_", " ").upper()
        draw.text((THUMB_WIDTH - 350, THUMB_HEIGHT - 60),
                  ch_name, font=font_sub, fill=(180, 180, 180))

        img.save(output_path, quality=95)
        print(f"✅ Thumbnail saved: {output_path}")
        return True

    except Exception as e:
        print(f"❌ Thumbnail error: {e}")
        return False


if __name__ == "__main__":
    os.makedirs("test_output", exist_ok=True)
    channels = ["ai_tech_tamil", "motivation", "facts_finance", "eggy_world"]
    titles = [
        "ChatGPT Free Tips 2025 Tamil",
        "Success Secret Nobody Tells You",
        "India Economy Facts 2025",
        "Colors Learning with Eggy",
    ]
    for ch, title in zip(channels, titles):
        create_thumbnail(title, ch, f"test_output/thumb_{ch}.jpg")
    print("\nAll thumbnails created!")
