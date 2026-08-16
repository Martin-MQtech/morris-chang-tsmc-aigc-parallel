#!/usr/bin/env python3
"""
ReadShift 插图/封面生成脚本（gpt-image-2 · llm-token.cn OpenAI 兼容代理）

用法:
    python3 tools/make_images.py <prompt文件> <输出.png> [size] [model]

    python3 tools/make_images.py 设计资产/封面/cover-prompt.txt 设计资产/封面/封面.png 1024x1536
    python3 tools/make_images.py 设计资产/插图/p01.txt 设计资产/插图/p01.png 1536x1024

size 常用: 1024x1024 | 1024x1536(竖版 2:3, 书籍封面) | 1536x1024(横版 3:2, 章首图) | auto
model 默认 gpt-image-2（代理支持: gpt-image-1.5 / gpt-image-2 / gpt-image-2-4k / grok-imagine-image）
API key 取环境变量 OPENAI_API_KEY（llm-token.cn 代理密钥）。
"""
import base64
import json
import os
import sys
import time
import urllib.request

API_URL = "https://api.llm-token.cn/v1/images/generations"
API_KEY = os.environ.get("OPENAI_API_KEY", "")
DEFAULT_MODEL = "gpt-image-2"
DEFAULT_SIZE = "1536x1024"


def generate(prompt: str, out_path: str, size: str = DEFAULT_SIZE,
             model: str = DEFAULT_MODEL, retries: int = 3) -> None:
    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "n": 1,
        "size": size,
    }).encode("utf-8")

    last_err = None
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(API_URL, data=payload, headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {API_KEY}",
            })
            with urllib.request.urlopen(req, timeout=360) as r:
                data = json.loads(r.read().decode("utf-8"))
            if "error" in data:
                raise RuntimeError(data["error"].get("message", json.dumps(data["error"])))

            item = data["data"][0]
            b64 = item.get("b64_json") or ""
            url = item.get("url") or ""
            if b64:
                img = base64.b64decode(b64)
            elif url:
                with urllib.request.urlopen(url, timeout=120) as r2:
                    img = r2.read()
            else:
                raise RuntimeError("响应中无 b64_json 也无 url: " + json.dumps(item)[:200])

            os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
            with open(out_path, "wb") as f:
                f.write(img)
            print(f"✓ 已生成: {out_path} ({len(img) // 1024} KB)", flush=True)
            return
        except Exception as e:  # noqa: BLE001
            last_err = e
            print(f"  第 {attempt} 次失败: {e}", flush=True)
            if attempt < retries:
                time.sleep(4 * attempt)

    raise SystemExit(f"✗ 生成失败: {last_err}")


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        raise SystemExit(2)
    prompt_file, out_path = sys.argv[1], sys.argv[2]
    size = sys.argv[3] if len(sys.argv) > 3 else DEFAULT_SIZE
    model = sys.argv[4] if len(sys.argv) > 4 else DEFAULT_MODEL
    prompt = open(prompt_file, encoding="utf-8").read().strip()
    print(f"[{model} · {size}] {os.path.basename(prompt_file)} -> {out_path}", flush=True)
    generate(prompt, out_path, size=size, model=model)


if __name__ == "__main__":
    main()
