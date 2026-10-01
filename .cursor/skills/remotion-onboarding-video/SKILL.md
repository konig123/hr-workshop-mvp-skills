---
name: remotion-onboarding-video
description: Generate professional animated onboarding videos from presentation slides using Remotion and MiniMax Yue Cantonese TTS. Use when a user or workshop student wants to create an onboarding video from slide decks or images, needs automated Ken Burns camera animations, synchronized Cantonese voiceovers across 3 male and 3 female voices, preflight environment checks (Node, Remotion, MiniMax key), tiered durations (Express, Standard, Comprehensive), or custom slide replacements.
---

# Remotion 入職導向影片製作工作流程（Remotion Onboarding Video）

本技能為學員及機構提供標準化的「投影片轉動態入職影片」製作流程。結合 **Remotion 程式化動態渲染**（Ken Burns 鏡頭縮放、章節進度條、磨砂玻璃字幕）與 **MiniMax Yue 廣東話語音合成**，並具備環境自檢、金鑰防呆、多款男女聲選擇與時長分級功能。

---

## 核心工作步驟（Execution Workflow）

```
[步驟 1: 環境檢查] ──> [步驟 2: 金鑰防呆] ──> [步驟 3: 時長決定] ──> [步驟 4: 音色選擇] ──> [步驟 5: 素材替換提示] ──> [步驟 6: 語音合成與渲染]
```

---

### 步驟 1：環境前置檢查（Remotion Installation Check）

在執行任何代碼前，先檢查環境是否已安裝 Remotion。若未安裝，自動為學員安裝或建立專案：

```bash
python3 <skill-path>/scripts/check_env.py --project-dir ./remotion-onboarding
```

腳本會自動執行以下檢查：
1. **Node.js 及 npm**：確認環境具備 Node.js (v18+)。
2. **Remotion 專案與依賴套件**：若目錄不存在或未安裝，自動以 `npx create-video@latest --yes --blank --no-tailwind` 建立專案並補齊 `remotion` 及 `@remotion/cli`。
3. **學員提示**：學員無須手動在終端機輸入繁複指令，由 Agent 自動完成環境配置。

---

### 步驟 2：MiniMax 金鑰檢查與設定（API Key Check & .env.local）

廣東話旁白需呼叫 MiniMax T2A API。系統會自動搜尋環境變數與專案目錄中的金鑰：

1. 檢查 `process.env.MINIMAX_API_KEY` 或目錄下的 `.env.local`。
2. **若未找到金鑰**：
   - 系統會自動在專案根目錄建立 `.env.local` 模板：
     ```bash
     # MiniMax API Key for Cantonese Yue Speech Synthesis
     # 請在此填入你的 MiniMax API Key（由開放平台取得，例如：eyJhbGci...）
     MINIMAX_API_KEY=
     ```
   - **向學員提示**：「未檢測到 MiniMax API Key。已為你建立 `.env.local`，請開啟該檔案並貼上你的金鑰後儲存，即可繼續。」
3. 確認金鑰已填妥後才進入下一步。

---

### 步驟 3：決定影片長度分級（Duration Decision）

在生成影片前，使用 `AskQuestion` 讓學員決定預期的影片長度：

| 方案 | 預計長度 | 涵蓋場景與投影片 | 適合場景 |
|---|---|---|---|
| **精簡快報（Express）** | 約 30–40 秒 | 3 場（S01 歡迎 + S02 日程總覽 + S03 設備與支援） | 即時通訊群組（Slack/Teams）迎新通知、速報 |
| **標準入職（Standard，推薦）** | 約 55–65 秒 | 5 場（S01 歡迎 + S02 創辦人 + S03 團隊 + S04 導師 + S05 首週日程） | 新員工到職首日觀看、部門迎新模組 |
| **完整導向（Comprehensive）** | 約 100–120 秒 | 9 場（全套 15 張投影片：含設備寄送、合約表單、Remote 規範、HR 聯絡） | 完整自主培訓、遠距辦公全套指南 |

詳細場景腳本與投影片對應請參考 [references/durations.md](references/durations.md)。

---

### 步驟 4：選擇旁白音色（3 款男聲 + 3 款女聲）

本技能不硬編碼單一聲音，提供 **3 款男聲** 與 **3 款女聲** 供學員挑選。使用 `AskQuestion` 提供具體特質介紹：

#### 女聲音色
1. `female-chengshu`（**成熟幹練**，預設推薦）：沉穩、自信、清晰有權威，適合企業正式入職與制度解說。
2. `female-yujie`（**知性溫雅**）：平穩流暢、親和度高，適合專案工作流程導覽。
3. `female-shaonv`（**明快活力**）：熱情活潑、親切有朝氣，適合新創文化與輕鬆迎新。

#### 男聲音色
4. `male-qn-qingse`（**親切青年**，導師推薦）：陽光友善、平易近人，如同 Onboarding Buddy 或同儕分享。
5. `male-pure`（**沉靜專業**）：誠懇可靠、冷靜清晰，適合技術規範、工具配置與目標梳理。
6. `presenter_male`（**穩重主持**）：深沉大器、字正腔圓，適合創辦人致辭與企業使命宣導。

詳細音色特質與範例文句請參閱 [references/voices.md](references/voices.md)。

---

### 步驟 5：投影片素材載入與替換提示（Slide Assets Management）

1. **預設素材**：
   - 本技能內置一套完整的 **Team Awesome 入職簡報（共 15 張高清圖檔）**，位於技能的 `assets/slides/`。
   - 執行時會自動複製至 Remotion 專案的 `public/slides/` 作為預設素材。
2. **學員自訂替換提示**：
   - 必須主動向學員說明：
     > 「目前預設載入 Team Awesome 入職簡報（15 張圖檔）。如果你想使用自己公司的簡報，只需將自己的 16:9 投影片圖片（PNG/JPG）放入 `public/slides/` 資料夾並覆蓋即可，檔名建議按順序命名（如 `slide-01.png`）。」
   - 詳細替換指引與尺寸建議請參閱 [references/slide-replacement.md](references/slide-replacement.md)。

---

### 步驟 6：語音合成與時間軸同步

執行語音合成腳本，依據學員選擇的音色與時長分級產生廣東話音訊，並自動計算每場精確幀數：

```bash
python3 <skill-path>/scripts/generate_tts.py --voice-id <chosen_voice> --tier <express|standard|comprehensive> --project-dir ./remotion-onboarding
```

合成完成後，會輸出：
- 音訊檔案：`public/audio/S01-vo.mp3` 至 `Sxx-vo.mp3`
- 精確時長設定檔：`src/durations.json`

---

### 步驟 7：影片渲染與預覽

1. **渲染全片 MP4**：
   ```bash
   cd ./remotion-onboarding
   npx remotion render OnboardingVideo out/onboarding-video.mp4
   ```
2. **開啟 Remotion Studio 即時調校**：
   ```bash
   cd ./remotion-onboarding
   npm run dev
   ```
   瀏覽器會自動開啟可拖曳的時間軸介面，學員可即時預覽動畫、調整字體大小或微調轉場時長。

---

## 視覺與動畫設計規範（Remotion Design Rules）

- **嚴禁使用 CSS transitions 或 keyframe animations**：Remotion 離線渲染無法保證 CSS 動畫幀數一致。
- **必須使用 `useCurrentFrame()` 與 `interpolate()`**：所有鏡頭推拉、淡入淡出、元素平移必須由幀數直接驅動。
- **動態鏡頭（Ken Burns）**：透過 `transform: scale(...) translateX(...)` 營造電影級慢速平移，使靜態簡報生動自然。
- **頂部進度條（HeaderBar）**：包含組織標籤、章節計數器（如 `1 / 5`）與全片進度高亮。
- **浮動動態字幕（SubtitleBar）**：採用深色磨砂玻璃背景（`rgba(18, 20, 29, 0.82)`）與圓角設計，文字清晰不遮擋核心簡報內容。
