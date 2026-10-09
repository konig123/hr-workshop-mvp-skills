#!/usr/bin/env python3
"""Build an editable bilingual storyboard HTML artifact.

Usage:
  python build_storyboard_html.py input-scenes.json output-folder
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DEFAULT_COLUMNS = {
    "en": [
        "Scene",
        "Time",
        "Goal",
        "Narration",
        "MiniMax TTS",
        "Visual",
        "On-Screen Text",
        "Asset",
        "Risk Check",
        "Descript Prompt (copy & paste)",
    ],
    "zh": [
        "\u5834\u666f",
        "\u6642\u9593",
        "\u76ee\u6a19",
        "\u65c1\u767d",
        "MiniMax \u5408\u6210\u7a3f",
        "\u756b\u9762",
        "\u87a2\u5e55\u6587\u5b57",
        "\u7d20\u6750",
        "\u98a8\u96aa\u6aa2\u67e5",
        "Descript \u63d0\u793a\u8a5e\uff08\u8907\u88fd\u8cbc\u4e0a\uff09",
    ],
}


HTML = r'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Video Storyboard</title>
  <style>
    :root { --header-bg: #5a8a8a; --header-text: #fff; --row-bg: #f0f0f0; --border: #ccc; --text: #222; --accent: #2a6b6b; --focus: #4a9; }
    * { box-sizing: border-box; }
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang TC", "Microsoft JhengHei", sans-serif; margin: 24px; color: var(--text); background: #fafafa; }
    h1 { font-size: 1.25rem; margin: 0 0 0.25rem; }
    .meta { font-size: 0.875rem; color: #555; margin-bottom: 0.75rem; }
    .meta a { color: var(--accent); }
    .toolbar { display: flex; flex-wrap: wrap; gap: 12px; align-items: center; margin-bottom: 1rem; }
    .lang-toggle { display: inline-flex; border: 1px solid var(--border); border-radius: 8px; overflow: hidden; background: #fff; }
    .lang-toggle button, .btn { border: 1px solid var(--border); background: #fff; padding: 7px 12px; cursor: pointer; font-size: 0.8125rem; }
    .lang-toggle button { border: none; padding: 8px 16px; }
    .lang-toggle button.active, .btn-primary { background: var(--header-bg); color: #fff; border-color: var(--header-bg); font-weight: 600; }
    .btn { border-radius: 6px; }
    .hint { font-size: 0.8125rem; color: #666; }
    .table-wrap { overflow-x: auto; border: 1px solid var(--border); border-radius: 8px; }
    table { border-collapse: collapse; width: 100%; min-width: 1600px; font-size: 0.8125rem; line-height: 1.45; }
    th { background: var(--header-bg); color: var(--header-text); font-weight: 600; text-align: left; padding: 10px 12px; border: 1px solid var(--border); vertical-align: top; }
    td { background: var(--row-bg); padding: 8px 10px; border: 1px solid var(--border); vertical-align: top; }
    tr:hover td { background: #e8e8e8; }
    .scene-label, .time-label { font-weight: 600; white-space: nowrap; }
    [contenteditable="true"] { min-height: 2.5em; outline: none; border-radius: 4px; padding: 4px; }
    [contenteditable="true"]:focus { background: #fff; box-shadow: inset 0 0 0 2px var(--focus); }
    .prompt-cell { min-width: 320px; max-width: 440px; }
    .prompt-box { font-family: ui-monospace, "SF Mono", Menlo, monospace; font-size: 0.72rem; line-height: 1.5; white-space: pre-wrap; word-break: break-word; background: #fff; border: 1px solid #bbb; border-radius: 6px; padding: 8px; min-height: 120px; max-height: 220px; overflow-y: auto; margin-bottom: 6px; outline: none; }
    .prompt-box:focus { border-color: var(--focus); box-shadow: 0 0 0 2px rgba(68, 170, 153, 0.25); }
    .copy-btn { font-size: 0.75rem; padding: 4px 10px; }
    .copy-btn.copied { background: #d4edda; border-color: #b7dfc3; }
    .toast { position: fixed; bottom: 24px; right: 24px; background: #333; color: #fff; padding: 10px 16px; border-radius: 8px; font-size: 0.875rem; opacity: 0; pointer-events: none; transition: opacity 0.2s; }
    .toast.show { opacity: 1; }
  </style>
</head>
<body>
  <h1 id="page-title"></h1>
  <p class="meta" id="page-meta"></p>
  <div class="toolbar">
    <div class="lang-toggle" role="group" aria-label="Language">
      <button type="button" id="btn-en" class="active">English</button>
      <button type="button" id="btn-zh">&#32321;&#39636;&#20013;&#25991;</button>
    </div>
    <button type="button" class="btn" id="btn-reset">Reset edits</button>
    <button type="button" class="btn btn-primary" id="btn-export">Export JSON</button>
    <span class="hint">Click any cell to edit. Changes save automatically in this browser.</span>
  </div>
  <div class="table-wrap"><table><thead id="table-head"></thead><tbody id="table-body"></tbody></table></div>
  <div class="toast" id="toast"></div>
  <script src="storyboard-data.js"></script>
  <script>
    const STORAGE_KEY = "video-storyboard-" + (window.STORYBOARD.meta.slug || "default") + "-v2";
    const FIELDS = ["goal", "narration", "ttsScript", "visual", "onScreen", "asset", "risk"];
    let lang = "en";
    let data = structuredClone(window.STORYBOARD);

    function loadSaved() { try { const raw = localStorage.getItem(STORAGE_KEY); if (raw) data = JSON.parse(raw); } catch (_) {} }
    function save() { localStorage.setItem(STORAGE_KEY, JSON.stringify(data)); }
    function text(el) { return el.innerText.replace(/\u00a0/g, " ").trim(); }
    function sceneLabel(id) { return lang === "en" ? "Scene " + id : "\u5834\u666f " + id; }

    function promptFor(scene, locale) {
      const c = scene[locale], en = locale === "en";
      return [
        en ? "Generate a professional video storyboard scene in Descript." : "\u8acb\u5728 Descript \u4e2d\u751f\u6210\u4e00\u6bb5\u5c08\u696d\u7684\u5f71\u7247\u5206\u93e1\u5834\u666f\u3002",
        "",
        en ? "SCENE: Scene " + scene.id : "\u5834\u666f\uff1a\u5834\u666f " + scene.id,
        en ? "DURATION: " + scene.time : "\u6642\u9577\uff1a" + scene.time,
        en ? "GOAL: " + c.goal : "\u76ee\u6a19\uff1a" + c.goal,
        "",
        en ? "VOICEOVER (read verbatim):" : "\u65c1\u767d\uff08\u8acb\u9010\u5b57\u6717\u8b80\uff09\uff1a",
        c.narration,
        "",
        en ? "MINIMAX TTS (send this text to T2A):" : "MiniMax \u5408\u6210\u7a3f\uff08\u9001\u53bb T2A\uff09\uff1a",
        c.ttsScript || "",
        "",
        en ? "VISUAL DIRECTION:" : "\u756b\u9762\u6307\u793a\uff1a",
        c.visual,
        "",
        en ? "ON-SCREEN TEXT:" : "\u87a2\u5e55\u6587\u5b57\uff1a",
        c.onScreen,
        "",
        en ? "ASSETS:" : "\u7d20\u6750\uff1a",
        c.asset,
        "",
        en ? "PRODUCTION NOTES:" : "\u88fd\u4f5c\u6ce8\u610f\u4e8b\u9805\uff1a",
        c.risk,
        "",
        en ? "STYLE: Clean corporate video, 16:9, 1080p, warm professional tone, subtle fade and highlight animations." : "\u98a8\u683c\uff1a\u7c21\u6f54\u5c08\u696d\u7684\u4f01\u696d\u5f71\u7247\uff0c16:9\u30011080p\uff0c\u8a9e\u6c23\u6eab\u6696\u5c08\u696d\uff0c\u6de1\u5165\u6de1\u51fa\u8207\u91cd\u9ede\u9ad8\u4eae\u52d5\u756b\u3002"
      ].join("\n");
    }

    function renderHeader() {
      document.documentElement.lang = lang === "en" ? "en" : "zh-Hant";
      document.getElementById("page-title").textContent = data.meta.title[lang] || data.meta.title.en;
      const label = lang === "en" ? "Source: " : "\u4f86\u6e90\uff1a";
      const note = lang === "en" ? "Transcript-backed storyboard" : "\u4f9d\u64da\u9010\u5b57\u7a3f\u6574\u7406\u7684\u5206\u93e1\u8868";
      document.getElementById("page-meta").innerHTML = label + '<a href="' + data.meta.source + '" target="_blank" rel="noopener">' + (data.meta.source || "source") + '</a> &middot; ' + note;
      document.getElementById("table-head").innerHTML = "<tr>" + data.columns[lang].map(h => "<th>" + h + "</th>").join("") + "</tr>";
    }

    function refreshPrompt(sceneId) {
      const scene = data.scenes.find(s => s.id === sceneId);
      const box = document.querySelector('.prompt-box[data-scene="' + sceneId + '"]');
      if (!scene || !box) return;
      const live = {};
      FIELDS.forEach(field => {
        const cell = document.querySelector('[data-scene="' + sceneId + '"][data-field="' + field + '"]');
        live[field] = cell ? text(cell) : scene[lang][field];
      });
      const temp = Object.assign({}, scene, { [lang]: Object.assign({}, scene[lang], live) });
      box.textContent = promptFor(temp, lang);
    }

    function renderBody() {
      const tbody = document.getElementById("table-body");
      tbody.innerHTML = "";
      data.scenes.forEach(scene => {
        const tr = document.createElement("tr");
        const sceneTd = document.createElement("td");
        sceneTd.className = "scene-label";
        sceneTd.textContent = sceneLabel(scene.id);
        tr.appendChild(sceneTd);

        const timeTd = document.createElement("td");
        timeTd.className = "time-label";
        timeTd.contentEditable = "true";
        timeTd.textContent = scene.time;
        timeTd.addEventListener("blur", () => { scene.time = text(timeTd); save(); refreshPrompt(scene.id); });
        timeTd.addEventListener("input", () => refreshPrompt(scene.id));
        tr.appendChild(timeTd);

        FIELDS.forEach(field => {
          const td = document.createElement("td");
          td.contentEditable = "true";
          td.dataset.scene = scene.id;
          td.dataset.field = field;
          td.textContent = scene[lang][field] || "";
          td.addEventListener("blur", () => { scene[lang][field] = text(td); save(); refreshPrompt(scene.id); });
          td.addEventListener("input", () => refreshPrompt(scene.id));
          tr.appendChild(td);
        });

        const promptTd = document.createElement("td");
        promptTd.className = "prompt-cell";
        const box = document.createElement("div");
        box.className = "prompt-box";
        box.dataset.scene = scene.id;
        box.contentEditable = "true";
        box.spellcheck = false;
        box.textContent = promptFor(scene, lang);
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "btn copy-btn";
        btn.textContent = lang === "en" ? "Copy prompt" : "\u8907\u88fd\u63d0\u793a\u8a5e";
        btn.addEventListener("click", () => {
          navigator.clipboard.writeText(box.textContent).then(() => {
            btn.classList.add("copied");
            btn.textContent = lang === "en" ? "Copied!" : "\u5df2\u8907\u88fd\uff01";
            setTimeout(() => { btn.classList.remove("copied"); btn.textContent = lang === "en" ? "Copy prompt" : "\u8907\u88fd\u63d0\u793a\u8a5e"; }, 1500);
          });
        });
        promptTd.appendChild(box);
        promptTd.appendChild(btn);
        tr.appendChild(promptTd);
        tbody.appendChild(tr);
      });
    }

    function setLang(next) {
      lang = next;
      document.getElementById("btn-en").classList.toggle("active", lang === "en");
      document.getElementById("btn-zh").classList.toggle("active", lang === "zh");
      renderHeader();
      renderBody();
    }

    document.getElementById("btn-en").addEventListener("click", () => setLang("en"));
    document.getElementById("btn-zh").addEventListener("click", () => setLang("zh"));
    document.getElementById("btn-reset").addEventListener("click", () => { localStorage.removeItem(STORAGE_KEY); data = structuredClone(window.STORYBOARD); renderHeader(); renderBody(); });
    document.getElementById("btn-export").addEventListener("click", () => {
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = "storyboard.json";
      a.click();
      URL.revokeObjectURL(a.href);
    });
    loadSaved(); renderHeader(); renderBody();
  </script>
</body>
</html>
'''


def normalize(data: dict) -> dict:
    data.setdefault("columns", DEFAULT_COLUMNS)
    data.setdefault("meta", {})
    data["meta"].setdefault("title", {"en": "Video Storyboard", "zh": "\u5f71\u7247\u5206\u93e1\u8868"})
    data["meta"].setdefault("source", "")
    data.setdefault("scenes", [])
    for index, scene in enumerate(data["scenes"], 1):
        scene.setdefault("id", index)
        scene.setdefault("time", "")
        for locale in ("en", "zh"):
            scene.setdefault(locale, {})
            for field in ("goal", "narration", "ttsScript", "visual", "onScreen", "asset", "risk"):
                scene[locale].setdefault(field, "")
    return data


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_json", type=Path)
    parser.add_argument("output_folder", type=Path)
    args = parser.parse_args()

    data = normalize(json.loads(args.input_json.read_text(encoding="utf-8")))
    args.output_folder.mkdir(parents=True, exist_ok=True)

    data_js = "window.STORYBOARD = " + json.dumps(data, ensure_ascii=True, indent=2) + ";\n"
    (args.output_folder / "storyboard-data.js").write_text(data_js, encoding="ascii")
    (args.output_folder / "storyboard.html").write_text(HTML, encoding="utf-8")

    for path in (args.output_folder / "storyboard-data.js", args.output_folder / "storyboard.html"):
        text = path.read_text(encoding="utf-8")
        if ("?" * 4) in text or "\ufffd" in text:
            raise SystemExit(f"Encoding corruption detected in {path}")

    print(f"Wrote {args.output_folder / 'storyboard.html'}")


if __name__ == "__main__":
    main()
