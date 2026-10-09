import React from "react";
import { AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame } from "remotion";
import { HeaderBar } from "./components/HeaderBar";
import { SubtitleBar } from "./components/SubtitleBar";
import { Scene01Welcome } from "./scenes/Scene01Welcome";
import { Scene02Founders } from "./scenes/Scene02Founders";
import { Scene03Team } from "./scenes/Scene03Team";
import { Scene04Coach } from "./scenes/Scene04Coach";
import { Scene05Schedule } from "./scenes/Scene05Schedule";
import { SceneMeta } from "./types";

export const SCENES: SceneMeta[] = [
  {
    id: "S01",
    number: 1,
    title: "Welcome Lucy",
    subtitle: "Getting Started",
    durationFrames: 239,
    audioSrc: "audio/S01-vo.mp3",
    subtitles: [
      { from: 0, to: 80, text: "哈囉 Lucy！歡迎加入 Team Awesome。" },
      {
        from: 80,
        to: 239,
        text: "呢段簡介會帶你掌握第一星期嘅重要安排，等你可以輕鬆投入新工作。",
      },
    ],
  },
  {
    id: "S02",
    number: 2,
    title: "Meet the Founders",
    subtitle: "Leadership Team",
    durationFrames: 361,
    audioSrc: "audio/S02-vo.mp3",
    subtitles: [
      { from: 0, to: 110, text: "首先認識下我哋嘅三位創辦人：" },
      {
        from: 110,
        to: 250,
        text: "CEO Georgia、CTO Cameron，同埋 CFO Justin。",
      },
      { from: 250, to: 361, text: "佢哋帶領團隊持續突破同成長。" },
    ],
  },
  {
    id: "S03",
    number: 3,
    title: "Design Team",
    subtitle: "Team Structure",
    durationFrames: 308,
    audioSrc: "audio/S03-vo.mp3",
    subtitles: [
      { from: 0, to: 80, text: "跟住係你嘅設計團隊夥伴：" },
      {
        from: 80,
        to: 220,
        text: "Creative Director Avery，資深設計師 Teri 同 Liv，仲有 Clara、Enzo 同 Deb。",
      },
      { from: 220, to: 308, text: "大家隨時歡迎你交流！" },
    ],
  },
  {
    id: "S04",
    number: 4,
    title: "Your Coach",
    subtitle: "Teri Jackson",
    durationFrames: 285,
    audioSrc: "audio/S04-vo.mp3",
    subtitles: [
      {
        from: 0,
        to: 110,
        text: "第一星期同頭三個月，Teri 會擔任你嘅 Coach。",
      },
      {
        from: 110,
        to: 285,
        text: "除咗解答日常問題，佢仲會協助你訂立專業目標，一步步引導你適應工作。",
      },
    ],
  },
  {
    id: "S05",
    number: 5,
    title: "Week 1 Schedule",
    subtitle: "Roadmap",
    durationFrames: 420,
    audioSrc: "audio/S05-vo.mp3",
    subtitles: [
      { from: 0, to: 70, text: "嚟睇下第一星期嘅日程：" },
      {
        from: 70,
        to: 190,
        text: "頭兩日同團隊打招呼、同 Teri 做一對一面談，搞好 Email 同 Slack；",
      },
      {
        from: 190,
        to: 310,
        text: "第三四日有 HR 迎新同 Avery 面談，並提交表格；",
      },
      { from: 310, to: 420, text: "第五日就同 Teri 做週結 Check-in。" },
    ],
  },
];

export const TOTAL_FRAMES = SCENES.reduce(
  (acc, s) => acc + s.durationFrames,
  0
);

export const MainVideo: React.FC = () => {
  const currentFrame = useCurrentFrame();

  // Determine active scene for the HeaderBar
  let accumulated = 0;
  let activeScene = SCENES[0];
  for (const sc of SCENES) {
    if (
      currentFrame >= accumulated &&
      currentFrame < accumulated + sc.durationFrames
    ) {
      activeScene = sc;
      break;
    }
    accumulated += sc.durationFrames;
  }

  let sceneOffset = 0;

  return (
    <AbsoluteFill style={{ backgroundColor: "#ffffff" }}>
      {/* Dynamic persistent Header */}
      <HeaderBar
        currentScene={activeScene.number}
        totalScenes={SCENES.length}
        sceneTitle={activeScene.title}
        totalFrames={TOTAL_FRAMES}
      />

      {/* S01: Welcome */}
      {(() => {
        const offset = sceneOffset;
        sceneOffset += SCENES[0].durationFrames;
        return (
          <Sequence
            from={offset}
            durationInFrames={SCENES[0].durationFrames}
            name="S01-Welcome"
          >
            <Scene01Welcome />
            <Audio src={staticFile(SCENES[0].audioSrc)} />
            <SubtitleBar cues={SCENES[0].subtitles} />
          </Sequence>
        );
      })()}

      {/* S02: Founders */}
      {(() => {
        const offset = sceneOffset;
        sceneOffset += SCENES[1].durationFrames;
        return (
          <Sequence
            from={offset}
            durationInFrames={SCENES[1].durationFrames}
            name="S02-Founders"
          >
            <Scene02Founders />
            <Audio src={staticFile(SCENES[1].audioSrc)} />
            <SubtitleBar cues={SCENES[1].subtitles} />
          </Sequence>
        );
      })()}

      {/* S03: Team */}
      {(() => {
        const offset = sceneOffset;
        sceneOffset += SCENES[2].durationFrames;
        return (
          <Sequence
            from={offset}
            durationInFrames={SCENES[2].durationFrames}
            name="S03-Team"
          >
            <Scene03Team />
            <Audio src={staticFile(SCENES[2].audioSrc)} />
            <SubtitleBar cues={SCENES[2].subtitles} />
          </Sequence>
        );
      })()}

      {/* S04: Coach */}
      {(() => {
        const offset = sceneOffset;
        sceneOffset += SCENES[3].durationFrames;
        return (
          <Sequence
            from={offset}
            durationInFrames={SCENES[3].durationFrames}
            name="S04-Coach"
          >
            <Scene04Coach />
            <Audio src={staticFile(SCENES[3].audioSrc)} />
            <SubtitleBar cues={SCENES[3].subtitles} />
          </Sequence>
        );
      })()}

      {/* S05: Schedule */}
      {(() => {
        const offset = sceneOffset;
        sceneOffset += SCENES[4].durationFrames;
        return (
          <Sequence
            from={offset}
            durationInFrames={SCENES[4].durationFrames}
            name="S05-Schedule"
          >
            <Scene05Schedule />
            <Audio src={staticFile(SCENES[4].audioSrc)} />
            <SubtitleBar cues={SCENES[4].subtitles} />
          </Sequence>
        );
      })()}
    </AbsoluteFill>
  );
};
