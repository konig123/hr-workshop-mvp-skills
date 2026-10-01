#!/usr/bin/env python3
"""
MiniMax Yue Cantonese TTS Generator for Remotion Onboarding Video.

Supports:
- 3 Female voices: female-chengshu, female-yujie, female-shaonv
- 3 Male voices: male-qn-qingse, male-pure, presenter_male
- 3 Duration tiers: express (~35s), standard (~60s), comprehensive (~110s)
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

VOICE_CATALOG = {
    # Female voices
    "female-chengshu": {
        "name": "成熟幹練女聲",
        "description": "沉穩、自信、清晰，適合企業正式入職、管理層致辭、制度講解",
        "gender": "female"
    },
    "female-yujie": {
        "name": "知性溫雅女聲",
        "description": "平穩、條理分明、親和度高，適合專案導向與工作流程講解",
        "gender": "female"
    },
    "female-shaonv": {
        "name": "明快活力女聲",
        "description": "輕快、熱情活潑、親切有朝氣，適合新創文化與輕鬆迎新",
        "gender": "female"
    },
    # Male voices
    "male-qn-qingse": {
        "name": "親切青年男聲",
        "description": "陽光、友善隨和、無距離感，如同入職導師（Buddy）指引",
        "gender": "male"
    },
    "male-pure": {
        "name": "沉靜專業男聲",
        "description": "誠懇可靠、冷靜清晰，適合技術架構、辦公設備與目標導引",
        "gender": "male"
    },
    "presenter_male": {
        "name": "穩重主持男聲",
        "description": "深沉大器、字正腔圓，適合創辦人致辭與企業使命宣導",
        "gender": "male"
    }
}

SCRIPTS_BY_TIER = {
    "express": [
        {
            "id": "S01",
            "name": "歡迎加入",
            "text": "哈囉！<#0.35#>歡迎加入 team awesome。<#0.35#>呢段速報會帶你掌握首週最重要嘅幾個焦點安排，等你可以輕鬆展開新旅程。<#0.35#>"
        },
        {
            "id": "S02",
            "name": "首週日程概覽",
            "text": "第一星期嘅日程好清晰：<#0.35#>頭兩日做好系統開通同一對一面談，第三四日參加 H R 迎新，第五日做週結 check-in。<#0.35#>"
        },
        {
            "id": "S03",
            "name": "設備與支援管道",
            "text": "公司 laptop 已在寄送途中。<#0.35#>有任何問題隨時搵 H R 同事，祝你有個愉快充實嘅新開始！<#0.35#>"
        }
    ],
    "standard": [
        {
            "id": "S01",
            "name": "歡迎 Lucy",
            "text": "哈囉 lucy！<#0.35#>歡迎加入 team awesome。<#0.35#>呢段簡介會帶你掌握第一星期嘅重要安排，等你可以輕鬆投入新工作。<#0.35#>"
        },
        {
            "id": "S02",
            "name": "認識創辦人",
            "text": "首先認識下我哋嘅三位創辦人：<#0.35#>C E O georgia、<#0.35#>C T O cameron，<#0.35#>同埋 C F O justin。<#0.35#>佢哋帶領團隊持續突破同成長。<#0.35#>"
        },
        {
            "id": "S03",
            "name": "設計團隊架構",
            "text": "跟住係你嘅設計團隊夥伴：<#0.35#>creative director avery，資深設計師 teri 同 liv，仲有 clara、enzo 同 deb。<#0.35#>大家隨時歡迎你交流！<#0.35#>"
        },
        {
            "id": "S04",
            "name": "專屬導師指導",
            "text": "第一星期同頭三個月，<#0.35#>teri 會擔任你嘅 coach。<#0.35#>除咗解答日常問題，佢仲會協助你訂立專業目標，一步步引導你適應工作。<#0.35#>"
        },
        {
            "id": "S05",
            "name": "第一週日程規劃",
            "text": "嚟睇下第一星期嘅日程：<#0.35#>頭兩日同團隊打招呼、同 teri 做一對一面談，搞好 email 同 slack；<#0.35#>第三四日有 H R 迎新同 avery 面談，並提交表格；<#0.35#>第五日就同 teri 做週結 check-in。<#0.35#>"
        }
    ],
    "comprehensive": [
        {
            "id": "S01",
            "name": "歡迎 Lucy",
            "text": "哈囉 lucy！<#0.35#>歡迎加入 team awesome。<#0.35#>呢段簡介會帶你掌握第一星期嘅重要安排，等你可以輕鬆投入新工作。<#0.35#>"
        },
        {
            "id": "S02",
            "name": "認識創辦人",
            "text": "首先認識下我哋嘅三位創辦人：<#0.35#>C E O georgia、<#0.35#>C T O cameron，<#0.35#>同埋 C F O justin。<#0.35#>佢哋帶領團隊持續突破同成長。<#0.35#>"
        },
        {
            "id": "S03",
            "name": "設計團隊架構",
            "text": "跟住係你嘅設計團隊夥伴：<#0.35#>creative director avery，資深設計師 teri 同 liv，仲有 clara、enzo 同 deb。<#0.35#>大家隨時歡迎你交流！<#0.35#>"
        },
        {
            "id": "S04",
            "name": "專屬導師指導",
            "text": "第一星期同頭三個月，<#0.35#>teri 會擔任你嘅 coach。<#0.35#>除咗解答日常問題，佢仲會協助你訂立專業目標，一步步引導你適應工作。<#0.35#>"
        },
        {
            "id": "S05",
            "name": "第一週日程規劃",
            "text": "嚟睇下第一星期嘅日程：<#0.35#>頭兩日同團隊打招呼、同 teri 做一對一面談，搞好 email 同 slack；<#0.35#>第三四日有 H R 迎新同 avery 面談，並提交表格；<#0.35#>第五日就同 teri 做週結 check-in。<#0.35#>"
        },
        {
            "id": "S06",
            "name": "辦公設備與平台",
            "text": "工具方面：<#0.35#>公司 laptop 會喺三日內寄到你屋企；<#0.35#>H R 亦會寄出 email 邀請你登入 slack 同團隊各個工作平台。<#0.35#>"
        },
        {
            "id": "S07",
            "name": "文件與表單簽署",
            "text": "文件方面，請記得交齊 final contract、<#0.35#>P T O 年假協議、laptop 同電話使用協議，以及健康證明畀 H R 同事。<#0.35#>"
        },
        {
            "id": "S08",
            "name": "工作期望與請假制度",
            "text": "關於工作期望：<#0.35#>我哋實行 remote-first，工作時間彈性，每日美國東部時間 9 點至 3 點保留四個鐘開會協作。<#0.35#>請假只需通知主管，請超過一星期就要提前申請。<#0.35#>大家互相尊重、坦誠溝通。<#0.35#>"
        },
        {
            "id": "S09",
            "name": "結語與求助管道",
            "text": "祝你喺 team awesome 展開精彩嘅新旅程！<#0.35#>有任何問題，隨時搵我哋嘅 H R team lead tria 或者 H R associate austin，我哋隨時幫到你！<#0.35#>"
        }
    ]
}


def load_api_key(project_dir: Path) -> str:
    if os.environ.get("MINIMAX_API_KEY"):
        val = os.environ["MINIMAX_API_KEY"].strip()
        if val:
            return val

    search_dirs = [
        project_dir,
        project_dir.parent,
        Path.cwd(),
        Path("/Users/km/Desktop/Desktop - km’s MacBook Pro/craw/Novum"),
    ]
    for d in search_dirs:
        env_file = d / ".env.local"
        if env_file.exists():
            for line in env_file.read_text(encoding="utf-8").splitlines():
                if line.startswith("MINIMAX_API_KEY="):
                    val = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if val:
                        return val
    raise SystemExit("❌ 未找到 MINIMAX_API_KEY，請在 .env.local 填入 API Key。")


def minimax_tts(text: str, voice_id: str, speed: float, api_key: str) -> bytes:
    payload = {
        "model": "speech-2.8-hd",
        "text": text,
        "stream": False,
        "language_boost": "Chinese,Yue",
        "output_format": "hex",
        "voice_setting": {
            "voice_id": voice_id,
            "speed": speed,
            "vol": 1.0,
            "pitch": 0,
        },
        "audio_setting": {
            "sample_rate": 32000,
            "bitrate": 128000,
            "format": "mp3",
            "channel": 1
        },
    }
    req = urllib.request.Request(
        "https://api.minimax.io/v1/t2a_v2",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    if (data.get("base_resp") or {}).get("status_code") != 0:
        raise RuntimeError(data.get("base_resp"))
    return bytes.fromhex(data["data"]["audio"])


def probe_duration(path: Path) -> float:
    return float(
        subprocess.check_output(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(path),
            ],
            text=True,
        ).strip()
    )


def main():
    parser = argparse.ArgumentParser(description="Generate MiniMax Yue Cantonese TTS for onboarding video.")
    parser.add_argument("--voice-id", default="female-chengshu", help="MiniMax voice ID (e.g. female-chengshu, male-qn-qingse)")
    parser.add_argument("--tier", choices=["express", "standard", "comprehensive"], default="standard", help="Duration tier")
    parser.add_argument("--speed", type=float, default=1.1, help="Speech rate (default: 1.1x)")
    parser.add_argument("--project-dir", type=Path, default=Path.cwd() / "remotion-onboarding", help="Path to Remotion project")
    args = parser.parse_args()

    project_dir = args.project_dir.resolve()
    audio_dir = project_dir / "public" / "audio"
    src_dir = project_dir / "src"

    audio_dir.mkdir(parents=True, exist_ok=True)
    src_dir.mkdir(parents=True, exist_ok=True)

    key = load_api_key(project_dir)
    voice_info = VOICE_CATALOG.get(args.voice_id, {"name": args.voice_id, "description": "自訂音色"})
    scenes = SCRIPTS_BY_TIER[args.tier]

    print(f"🎙️ 正在以【{voice_info['name']}】({args.voice_id}) 生成【{args.tier}】模式旁白語音（共 {len(scenes)} 場）...")

    durations = {}
    for sc in scenes:
        sid = sc["id"]
        out_file = audio_dir / f"{sid}-vo.mp3"
        print(f"  • 合成 {sid}（{sc['name']}）...", end="", flush=True)
        audio_bytes = minimax_tts(sc["text"], args.voice_id, args.speed, key)
        out_file.write_bytes(audio_bytes)
        dur = probe_duration(out_file)
        durations[sid] = {
            "name": sc["name"],
            "duration": round(dur, 2),
            "frames": int(round((dur + 0.5) * 30)),
            "text": sc["text"]
        }
        print(f" 完成：{dur:.2f} 秒（{durations[sid]['frames']} 幀）")

    dur_json = src_dir / "durations.json"
    dur_json.write_text(json.dumps(durations, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    total_sec = sum(d["duration"] for d in durations.values())
    total_frames = sum(d["frames"] for d in durations.values())

    print(f"\n✅ 語音合成全部完成！總時長約 {total_sec:.1f} 秒（共 {total_frames} 幀）。")
    print(f"📁 語音檔已存入：{audio_dir}")
    print(f"📄 時間長度資料已寫入：{dur_json}")


if __name__ == "__main__":
    main()
