# -*- coding: utf-8 -*-
"""
抖音中长视频合集资产合成引擎
- 将 19 期 MP3 音频 + 1:1 高清排版插图 转换为符合抖音中长视频标准的 1080P MP4 视频
- 画布标准: 1920x1080 (16:9 横屏，抖音中长视频合集最佳画幅)
- 背景: 高斯模糊插图暗色打底 + 正中高保真封面插图 + 音频轨道无损混流
"""

import os, sys, subprocess, time
from audio_posts_data import EPISODES_DATA

VIDEO_OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "videos_douyin")
os.makedirs(VIDEO_OUT_DIR, exist_ok=True)

def generate_video_for_ep(ep_data, overwrite=False):
    ep_id = ep_data["ep_id"]
    audio_path = ep_data["audio_path"]
    cover_path = ep_data["cover_path"]
    out_mp4 = os.path.join(VIDEO_OUT_DIR, f"ep{ep_id}_douyin.mp4")

    if os.path.exists(out_mp4) and not overwrite:
        print(f"⏩ [第{ep_id}期] 视频已存在: {out_mp4}")
        return out_mp4

    print(f"🎬 正在合成 [第{ep_id}期] 抖音视频: {ep_data['title']}...")
    
    # 复杂滤镜: 
    # 1. 底图放大填满 1920x1080 并做高斯模糊 + 变暗处理 (背景氛围)
    # 2. 前景将 1:1 封面缩放到 1000x1000 居中叠加，并添加微阴影边缘
    filter_complex = (
        "[0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,gblur=sigma=25,eq=brightness=-0.18:contrast=1.1[bg];"
        "[0:v]scale=960:960[fg];"
        "[bg][fg]overlay=(W-w)/2:(H-h)/2"
    )

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", cover_path,
        "-i", audio_path,
        "-filter_complex", filter_complex,
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        out_mp4
    ]

    t0 = time.time()
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print(f"❌ 合成失败: {res.stderr[-300:]}")
        return None
        
    duration = time.time() - t0
    size_mb = os.path.getsize(out_mp4) / 1024 / 1024
    print(f"✅ [第{ep_id}期] 视频合成完成！耗时: {duration:.1f}s | 体积: {size_mb:.1f} MB -> {out_mp4}")
    return out_mp4

def generate_all_douyin_videos(ep_limit=None):
    episodes = EPISODES_DATA if ep_limit is None else EPISODES_DATA[:ep_limit]
    print(f"🚀 开始为 {len(episodes)} 个剧集生成抖音专属 1080P 中长视频...")
    
    generated = []
    for ep in episodes:
        v = generate_video_for_ep(ep)
        if v:
            generated.append(v)
            
    print(f"\n🎉 全部完成！共生成 {len(generated)} 个视频，存储于: {VIDEO_OUT_DIR}")
    return generated

if __name__ == "__main__":
    # 先合成第 00 期测试
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        generate_all_douyin_videos()
    else:
        generate_all_douyin_videos(ep_limit=1)
