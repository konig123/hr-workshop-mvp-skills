import React from "react";
import { interpolate, useCurrentFrame } from "remotion";

interface HeaderBarProps {
  currentScene: number;
  totalScenes: number;
  sceneTitle: string;
  totalFrames: number;
}

export const HeaderBar: React.FC<HeaderBarProps> = ({
  currentScene,
  totalScenes,
  sceneTitle,
  totalFrames,
}) => {
  const frame = useCurrentFrame();

  const progress = interpolate(frame, [0, totalFrames], [0, 100], {
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        position: "absolute",
        top: 0,
        left: 0,
        right: 0,
        zIndex: 50,
        display: "flex",
        flexDirection: "column",
        pointerEvents: "none",
      }}
    >
      {/* Top progress bar */}
      <div
        style={{
          width: "100%",
          height: 5,
          backgroundColor: "rgba(255, 255, 255, 0.4)",
          backdropFilter: "blur(4px)",
        }}
      >
        <div
          style={{
            height: "100%",
            width: `${progress}%`,
            background: "linear-gradient(90deg, #d82b7d 0%, #8c6cd9 100%)",
            boxShadow: "0 0 10px rgba(216, 43, 125, 0.6)",
          }}
        />
      </div>

      {/* Floating Header Badges - Sleek & Compact */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          padding: "14px 40px",
        }}
      >
        {/* Left: Organization Tag */}
        <div
          style={{
            display: "inline-flex",
            alignItems: "center",
            gap: 8,
            background: "rgba(255, 255, 255, 0.85)",
            backdropFilter: "blur(10px)",
            padding: "6px 16px",
            borderRadius: 999,
            boxShadow: "0 4px 16px rgba(0, 0, 0, 0.06)",
            border: "1px solid rgba(255, 255, 255, 0.7)",
          }}
        >
          <div
            style={{
              width: 10,
              height: 10,
              borderRadius: "50%",
              background: "#d82b7d",
            }}
          />
          <span
            style={{
              fontFamily:
                '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang TC", sans-serif',
              fontWeight: 700,
              fontSize: 14,
              letterSpacing: "0.02em",
              color: "#1f2937",
            }}
          >
            Team Awesome Onboarding
          </span>
        </div>

        {/* Right: Chapter Tracker */}
        <div
          style={{
            display: "inline-flex",
            alignItems: "center",
            gap: 8,
            background: "rgba(255, 255, 255, 0.85)",
            backdropFilter: "blur(10px)",
            padding: "6px 18px",
            borderRadius: 999,
            boxShadow: "0 4px 16px rgba(0, 0, 0, 0.06)",
            border: "1px solid rgba(255, 255, 255, 0.7)",
          }}
        >
          <span
            style={{
              fontFamily:
                '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang TC", sans-serif',
              fontWeight: 800,
              fontSize: 13,
              color: "#d82b7d",
            }}
          >
            {currentScene} / {totalScenes}
          </span>
          <span
            style={{
              width: 1,
              height: 12,
              backgroundColor: "rgba(0,0,0,0.15)",
            }}
          />
          <span
            style={{
              fontFamily:
                '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang TC", sans-serif',
              fontWeight: 600,
              fontSize: 13,
              color: "#4b5563",
            }}
          >
            {sceneTitle}
          </span>
        </div>
      </div>
    </div>
  );
};
