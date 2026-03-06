#!/usr/bin/env python3
"""
🎬 YouTube AI Video Pipeline - Main Controller
Connects: Script → Voice → Video → Thumbnail → Upload
"""

import os
import json
import time
import schedule
import datetime
import requests
from core.script_generator import generate_script, CHANNEL_TOPICS
from core.voiceover import generate_voiceover
from core.video_maker import create_video
from core.thumbnail import create_thumbnail

# ─────────────────────────────────────────
# CONFIG — Edit these!
# ─────────────────────────────────────────
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID   = os.getenv("TELEGRAM_CHAT_ID", "")

CHANNELS_SCHEDULE = {
    "ai_tech_tamil":  ["08:00", "12:00", "18:00"],
    "motivation":     ["07:00", "15:00"],
    "facts_finance":  ["09:00", "14:00", "20:00"],
    "eggy_world":     ["10:00", "16:00"],
}

OUTPUT_DIR = "output_videos"

# ─────────────────────────────────────────

def send_telegram(msg: str):
    if not TELEGRAM_BOT_TOKEN:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": msg,
        "parse_mode": "Markdown"
    }, timeout=10)


def produce_video(channel: str) -> bool:
    """Full pipeline: Script → Voice → Video → Thumbnail"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    channel_dir = f"{OUTPUT_DIR}/{channel}"
    os.makedirs(channel_dir, exist_ok=True)

    print(f"\n{'═'*50}")
    print(f"🎬 Producing video for: {channel}")
    print(f"{'═'*50}")

    send_telegram(f"🎬 *Starting video production*\nChannel: `{channel}`")

    # Step 1: Generate Script
    print("📝 Step 1: Generating script...")
    data = generate_script(channel)
    script  = data["script"]
    title   = data["title"]
    topic   = data["topic"]
    print(f"✅ Script ready: {title}")

    # Step 2: Generate Voiceover
    print("🎙️ Step 2: Generating voiceover...")
    audio_path = f"{channel_dir}/{timestamp}_voice.mp3"
    if not generate_voiceover(script, channel, audio_path):
        send_telegram(f"❌ Voiceover failed for {channel}")
        return False

    # Step 3: Create Video
    print("🎬 Step 3: Creating video...")
    video_path = f"{channel_dir}/{timestamp}_video.mp4"
    if not create_video(script, channel, audio_path, video_path):
        send_telegram(f"❌ Video creation failed for {channel}")
        return False

    # Step 4: Create Thumbnail
    print("🖼️ Step 4: Creating thumbnail...")
    thumb_path = f"{channel_dir}/{timestamp}_thumb.jpg"
    create_thumbnail(title, channel, thumb_path)

    # Step 5: Upload to YouTube
    print("📤 Step 5: Uploading to YouTube...")
    from core.uploader import upload_video, set_thumbnail
    result = upload_video(
        video_path=video_path,
        title=data["title"],
        description=data["description"],
        tags=data["tags"],
        privacy="public"
    )
    if result["success"]:
        set_thumbnail(result["video_id"], thumb_path)
        send_telegram(f"""🎉 *Video Uploadedyoutube-ai-pipeline
📺 {channel}
🎯 {topic}
🔗 {result["video_url"]}""")
        print(f"✅ Live: {result['video_url']}")
    
    # Step 6: Save metadata
    meta = {
        "channel":    channel,
        "title":      title,
        "topic":      topic,
        "script":     script,
        "video":      video_path,
        "thumbnail":  thumb_path,
        "audio":      audio_path,
        "created_at": timestamp,
        "status":     "ready"
    }
    meta_path = f"{channel_dir}/{timestamp}_meta.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print(f"\n🎉 Video production complete!")
    print(f"   📹 Video:     {video_path}")
    print(f"   🖼️  Thumbnail: {thumb_path}")
    print(f"   📄 Metadata:  {meta_path}")

    send_telegram(f"""✅ *Video Ready!*

📺 Channel: `{channel}`
🎯 Topic: {topic}
📹 File: `{video_path}`
🕐 {datetime.datetime.now().strftime('%H:%M IST')}

_Ready for YouTube upload!_""")

    return True


def run_all_channels():
    """Produce one video for all channels."""
    print("\n🚀 Running full pipeline for all channels...")
    for channel in CHANNELS_SCHEDULE.keys():
        produce_video(channel)
        time.sleep(5)


def schedule_videos():
    """Schedule videos based on channel config."""
    for channel, times in CHANNELS_SCHEDULE.items():
        for t in times:
            schedule.every().day.at(t).do(produce_video, channel=channel)
            print(f"⏰ Scheduled {channel} at {t}")

    send_telegram("""🤖 *YouTube AI Pipeline Started!*

📺 Channels:
- 🤖 AI Tech Tamil
- 🧠 Motivation  
- 💰 Facts & Finance
- 🥚 Eggy's World

⏰ Auto producing videos daily!
_Videos saved to output\\_videos/_""")

    print("\n✅ All schedules set! Bot running...")
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            # Test single channel
            produce_video("ai_tech_tamil")
        elif sys.argv[1] == "all":
            # Run all channels once
            run_all_channels()
        elif sys.argv[1] == "schedule":
            # Run on schedule 24/7
            schedule_videos()
    else:
        # Default: test one video
        produce_video("ai_tech_tamil")
