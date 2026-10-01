#!/usr/bin/env python3
"""
Environment and Preflight Checker for Remotion Onboarding Video.

1. Checks Node.js and npm availability.
2. Checks Remotion installation in the target directory (auto-scaffolds or installs if missing).
3. Checks MINIMAX_API_KEY in environment or .env.local (creates template .env.local if missing).
4. Ensures slide assets exist in public/slides/ (copies defaults if missing).
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DEFAULT_SLIDES_DIR = SKILL_DIR / "assets" / "slides"


def check_node() -> bool:
    node = shutil.which("node")
    npm = shutil.which("npm")
    if not node or not npm:
        print("❌ 未檢測到 Node.js 或 npm，請先安裝 Node.js (v18+) 環境。")
        return False
    node_ver = subprocess.check_output([node, "-v"], text=True).strip()
    npm_ver = subprocess.check_output([npm, "-v"], text=True).strip()
    print(f"✅ Node.js: {node_ver}, npm: {npm_ver}")
    return True


def check_or_setup_remotion(project_dir: Path) -> bool:
    project_dir.mkdir(parents=True, exist_ok=True)
    pkg_json = project_dir / "package.json"

    if not pkg_json.exists():
        print(f"⚙️ 未在 {project_dir} 發現 Remotion 專案，正在自動建立基礎專案結構...")
        cmd = ["npx", "create-video@latest", "--yes", "--blank", "--no-tailwind", str(project_dir.name)]
        subprocess.run(cmd, cwd=project_dir.parent, check=True)
        # Install additional dependencies
        print("⚙️ 正在安裝 Remotion 相依套件...")
        subprocess.run(["npm", "install", "--loglevel=error"], cwd=project_dir, check=True)

    # Verify remotion is in package.json
    try:
        content = pkg_json.read_text(encoding="utf-8")
        if '"remotion"' not in content:
            print("⚙️ 正在補裝 Remotion 套件...")
            subprocess.run(["npm", "install", "remotion", "@remotion/cli", "--loglevel=error"], cwd=project_dir, check=True)
        print("✅ Remotion 專案相依套件已就緒。")
        return True
    except Exception as e:
        print(f"❌ 檢查或安裝 Remotion 時發生錯誤: {e}")
        return False


def check_or_setup_minimax_key(project_dir: Path) -> tuple[bool, str]:
    # 1. Check current environment variable
    if os.environ.get("MINIMAX_API_KEY"):
        val = os.environ["MINIMAX_API_KEY"].strip()
        if val:
            print("✅ 已於系統環境變數中檢測到 MINIMAX_API_KEY。")
            return True, val

    # 2. Check .env.local in project_dir or workspace
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
                        print(f"✅ 已在 {env_file} 中檢測到 MINIMAX_API_KEY。")
                        return True, val

    # 3. Not found -> Create template .env.local in project_dir
    target_env = project_dir / ".env.local"
    template_content = (
        "# MiniMax API Key for Cantonese Yue Speech Synthesis\n"
        "# 請在此填入你的 MiniMax API Key（由開放平台取得，例如：eyJhbGci...）\n"
        "MINIMAX_API_KEY=\n"
    )
    target_env.write_text(template_content, encoding="utf-8")
    print(f"⚠️ 未找到有效 MINIMAX_API_KEY。")
    print(f"📝 已為你自動建立設定檔：{target_env}")
    print(f"👉 請開啟該檔案填入你的 MINIMAX_API_KEY 後儲存。")
    return False, ""


def check_and_copy_slides(project_dir: Path) -> int:
    slides_dir = project_dir / "public" / "slides"
    slides_dir.mkdir(parents=True, exist_ok=True)

    existing_images = list(slides_dir.glob("*.png")) + list(slides_dir.glob("*.jpg"))
    if existing_images:
        print(f"✅ 檢測到已存在 {len(existing_images)} 張投影片圖片於 {slides_dir}。")
        return len(existing_images)

    # Copy defaults from skill assets
    if DEFAULT_SLIDES_DIR.exists():
        default_files = list(DEFAULT_SLIDES_DIR.glob("*.png"))
        if default_files:
            for f in default_files:
                shutil.copy(f, slides_dir / f.name)
            print(f"📦 已自動匯入 {len(default_files)} 張預設 Team Awesome 入職簡報至 {slides_dir}。")
            print("💡 溫馨提示：學員若要換成自己的投影片，可將圖片複製至 public/slides/ 覆蓋即可。")
            return len(default_files)

    print("⚠️ 未檢測到投影片素材，請將投影片圖片放入 public/slides/。")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Check Remotion and MiniMax environment.")
    parser.add_argument("--project-dir", type=Path, default=Path.cwd() / "remotion-onboarding", help="Path to Remotion project")
    args = parser.parse_args()

    project_dir = args.project_dir.resolve()
    print(f"🔍 正在檢查環境與專案設定：{project_dir}")

    if not check_node():
        sys.exit(1)

    remotion_ok = check_or_setup_remotion(project_dir)
    if not remotion_ok:
        sys.exit(1)

    key_ok, _ = check_or_setup_minimax_key(project_dir)
    slide_count = check_and_copy_slides(project_dir)

    print("\n--- 檢查總結 ---")
    print(f"• Remotion 安裝狀態: {'就緒' if remotion_ok else '失敗'}")
    print(f"• MiniMax API Key: {'已設定' if key_ok else '等待學員填寫 .env.local'}")
    print(f"• 投影片素材數量: {slide_count} 張")

    if not key_ok:
        print("\n👉 請先在 .env.local 填入 MINIMAX_API_KEY 再繼續生成影片！")
        sys.exit(2)
    else:
        print("\n🎉 環境全部就緒，可開始進行語音合成與影片渲染！")


if __name__ == "__main__":
    main()
