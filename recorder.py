import requests
import re
import sys
import subprocess
import time

USERNAME = "viplalicer"

def get_live_url(username):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Referer': f'https://www.tiktok.com/@{username}/live'
    }
    url = f"https://www.tiktok.com/@{username}/live"
    try:
        r = requests.get(url, headers=headers, timeout=15)
        # Cari m3u8 flv stream URL di halaman
        match = re.search(r'"flv_pull_url":\{"FULL_HD1":"([^"]+)".*?\}', r.text)
        if not match:
            match = re.search(r'"hls_pull_url":"([^"]+)"', r.text)
        if not match:
            match = re.search(r'(https://[^\s"]+?\.m3u8[^\s"]*)', r.text)
            
        if match:
            stream_url = match.group(1).replace("\\u0026", "&")
            return stream_url
    except Exception as e:
        print(f"Error fetching room page: {e}")
    return None

if __name__ == "__main__":
    print(f"Mencari stream URL untuk @{USERNAME}...")
    stream_url = get_live_url(USERNAME)
    if not stream_url:
        print("Gagal mendapatkan M3U8/FLV stream URL via web page parser.")
        sys.exit(1)
        
    print(f"Stream URL ditemukan! Memulai perekaman 60 detik...")
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
