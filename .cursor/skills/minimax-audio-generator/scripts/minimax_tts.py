#!/usr/bin/env python3
"""
MiniMax Text-to-Speech (T2A) CLI Runner
Self-guarding: automatically detects MINIMAX_API_KEY in .env.local, .env, or environment.
Zero external dependencies (uses standard library urllib, json, os, pathlib).
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path


def find_api_key(explicit_key: str = None) -> str:
    """Finds API key from argument, .env.local, .env, or environment variables."""
    if explicit_key and explicit_key.strip() and not explicit_key.startswith("your_"):
        return explicit_key.strip()

    # Search current directory and up to 3 parent directories for .env.local or .env
    cwd = Path.cwd()
    search_dirs = [cwd] + list(cwd.parents)[:3]

    for d in search_dirs:
        for fname in [".env.local", ".env"]:
            env_file = d / fname
            if env_file.is_file():
                try:
                    for line in env_file.read_text(encoding="utf-8").splitlines():
                        line = line.strip()
                        if line.startswith("MINIMAX_API_KEY=") and not line.startswith("#"):
                            val = line.split("=", 1)[1].strip().strip('"').strip("'")
                            if val and not val.startswith("your_"):
                                return val
                except Exception:
                    continue

    env_val = os.environ.get("MINIMAX_API_KEY", "").strip()
    if env_val and not env_val.startswith("your_"):
        return env_val

    return ""


def generate_tts(
    text: str,
    output_path: Path,
    api_key: str,
    voice_id: str = "female-chengshu",
    model: str = "speech-2.8-hd",
    speed: float = 1.0,
    vol: float = 1.0,
    pitch: int = 0,
    language_boost: str = "auto",
) -> dict:
    """Calls MiniMax v1/t2a_v2 API, decodes hex payload, and writes MP3 file."""
    if not text or not text.strip():
        raise ValueError("Text to synthesize cannot be empty.")

    lang_map = {
        "yue": "Chinese,Yue",
        "cantonese": "Chinese,Yue",
        "zh": "Chinese",
        "mandarin": "Chinese",
        "en": "English",
        "english": "English",
        "auto": "auto",
    }
    resolved_lang = lang_map.get(language_boost.lower(), language_boost)

    payload = {
        "model": model,
        "text": text,
        "stream": False,
        "output_format": "hex",
        "voice_setting": {
            "voice_id": voice_id,
            "speed": speed,
            "vol": vol,
            "pitch": pitch,
        },
        "audio_setting": {
            "sample_rate": 32000,
            "bitrate": 128000,
            "format": "mp3",
            "channel": 1,
        },
    }

    if resolved_lang != "auto":
        payload["language_boost"] = resolved_lang

    url = "https://api.minimax.io/v1/t2a_v2"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            raw_data = resp.read().decode("utf-8")
            res_json = json.loads(raw_data)
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8") if e.fp else str(e)
        raise RuntimeError(f"HTTP Error {e.code} from MiniMax API: {err_msg}")
    except Exception as e:
        raise RuntimeError(f"Failed to connect to MiniMax API: {e}")

    base_resp = res_json.get("base_resp", {})
    if base_resp.get("status_code", 0) != 0:
        code = base_resp.get("status_code")
        msg = base_resp.get("status_msg", "Unknown error")
        raise RuntimeError(f"MiniMax API returned error {code}: {msg}")

    audio_hex = (res_json.get("data") or {}).get("audio", "")
    if not audio_hex:
        raise RuntimeError("No audio data returned from MiniMax.")

    audio_bytes = bytes.fromhex(audio_hex)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(audio_bytes)

    extra_info = res_json.get("extra_info", {})
    return {
        "output_path": str(output_path.resolve()),
        "file_size_bytes": len(audio_bytes),
        "audio_length_ms": extra_info.get("audio_length", 0),
        "word_count": extra_info.get("word_count", 0),
        "voice_id": voice_id,
        "model": model,
        "speed": speed,
    }


def main():
    parser = argparse.ArgumentParser(description="MiniMax T2A Voice Generator")
    parser.add_argument("--text", "-t", type=str, help="Text to convert into speech")
    parser.add_argument("--text-file", "-f", type=Path, help="Path to text file to read")
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path("public/audio/voiceover.mp3"),
        help="Destination path for generated MP3",
    )
    parser.add_argument(
        "--voice-id",
        type=str,
        default="female-chengshu",
        help="Voice ID (e.g. female-chengshu, male-pure, female-qn-qingse, or cloned voice)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="speech-2.8-hd",
        help="Model (speech-2.8-hd, speech-2.6-hd, or speech-01-turbo)",
    )
    parser.add_argument("--speed", type=float, default=1.0, help="Speech speed (0.5 to 2.0)")
    parser.add_argument("--vol", type=float, default=1.0, help="Volume (0.1 to 2.0)")
    parser.add_argument("--pitch", type=int, default=0, help="Pitch offset (-12 to 12)")
    parser.add_argument(
        "--language",
        type=str,
        default="auto",
        choices=["auto", "yue", "cantonese", "zh", "mandarin", "en", "english"],
        help="Language boost / hint",
    )
    parser.add_argument("--api-key", type=str, default="", help="Explicit MiniMax API key")
    parser.add_argument("--json", action="store_true", help="Output result as JSON")

    args = parser.parse_args()

    # Load text
    text = args.text
    if args.text_file:
        if not args.text_file.is_file():
            sys.exit(f"Error: Text file '{args.text_file}' not found.")
        text = args.text_file.read_text(encoding="utf-8")

    if not text:
        sys.exit("Error: Either --text or --text-file is required.")

    # Self-guarding key detection
    api_key = find_api_key(args.api_key)
    if not api_key:
        err_res = {
            "error": "KEY_NOT_FOUND",
            "message": "MINIMAX_API_KEY was not found. Please create .env.local with MINIMAX_API_KEY=your_key.",
        }
        if args.json:
            print(json.dumps(err_res))
        else:
            print(f"Error: {err_res['message']}", file=sys.stderr)
        sys.exit(1)

    try:
        res = generate_tts(
            text=text,
            output_path=args.output,
            api_key=api_key,
            voice_id=args.voice_id,
            model=args.model,
            speed=args.speed,
            vol=args.vol,
            pitch=args.pitch,
            language_boost=args.language,
        )
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            duration_s = res["audio_length_ms"] / 1000.0
            size_kb = res["file_size_bytes"] / 1024.0
            print(f"Audio successfully generated!")
            print(f"File:     {res['output_path']}")
            print(f"Duration: {duration_s:.2f} seconds ({res['audio_length_ms']} ms)")
            print(f"Size:     {size_kb:.1f} KB")
            print(f"Voice:    {res['voice_id']} (Speed: {res['speed']}x)")
    except Exception as e:
        if args.json:
            print(json.dumps({"error": "GENERATION_FAILED", "message": str(e)}))
        else:
            print(f"Generation failed: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
