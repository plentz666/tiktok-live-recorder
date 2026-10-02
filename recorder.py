import asyncio
import subprocess
import time
import sys
from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent

USERNAME = "viplalicer"
client = TikTokLiveClient(unique_id=USERNAME)

@client.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    print(f"[-] Terhubung ke Room ID: {client.room_id}")
    # Ambil URL Stream FLV / M3U8 langsung dari data Webcast Room
    stream_url = None
    if client.room_info and 'stream_url' in client.room_info:
        s_info = client.room_info['stream_url']
        if 'rtmp_pull_url' in s_info:
            stream_url = s_info['rtmp_pull_url']
        elif 'flv_pull_url' in s_info:
            # Ambil FULL_HD1 atau HD1
            flv_map = s_info['flv_pull_url']
            stream_url = flv_map.get('FULL_HD1') or flv_map.get('HD1') or list(flv_map.values())[0] if flv_map else None

    if not stream_url:
        print("[!] Gagal mendapatkan stream URL dari Webcast Room Info.")
        await client.disconnect()
        sys.exit(1)

    print(f"[-] Stream URL didapatkan! Memulai FFmpeg selama 60 detik...")
    cmd = [
        "ffmpeg", "-y",
        "-headers", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n",
        "-i", stream_url,
        "-t", "60",
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "28", "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-movflags", "+faststart",
        "rekaman_viplalicer.mp4"
    ]
    subprocess.run(cmd)
    print("[-] Rekam selesai.")
    await client.disconnect()

async def main():
    try:
        await client.start()
    except Exception as e:
        print(f"[!] Error TikTokLive: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
