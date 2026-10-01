import React from "react";
import { interpolate, useCurrentFrame } from "remotion";
import { SubtitleCue } from "../types";

interface SubtitleBarProps {
  cues: SubtitleCue[];
}

export const SubtitleBar: React.FC<SubtitleBarProps> = ({ cues }) => {
  const frame = useCurrentFrame();

  const activeCue = cues.find(
    (cue) => frame >= cue.from && frame < cue.to
  );

  if (!activeCue) {
    return null;
  }

  // Animate opacity during the first few frames of each cue
  const cueAge = frame - activeCue.from;
  const opacity = interpolate(cueAge, [0, 8], [0, 1], {
    extrapolateRight: "clamp",
    extrapolateLeft: "clamp",
  });
  const translateY = interpolate(cueAge, [0, 8], [6, 0], {
    extrapolateRight: "clamp",
    extrapolateLeft: "clamp",
  });

  return (
    <div
      style={{
        position: "absolute",
        bottom: 48,
        left: 0,
        right: 0,
        zIndex: 50,
        display: "flex",
        justifyContent: "center",
        pointerEvents: "none",
        padding: "0 64px",
      }}
    >
      <div
        style={{
          background: "rgba(18, 20, 29, 0.82)",
          backdropFilter: "blur(16px)",
          color: "#ffffff",
          padding: "16px 36px",
          borderRadius: 20,
          boxShadow: "0 10px 40px rgba(0, 0, 0, 0.25)",
          border: "1px solid rgba(255, 255, 255, 0.15)",
          textAlign: "center",
          maxWidth: 1200,
          opacity,
          transform: `translateY(${translateY}px)`,
        }}
      >
        <span
          style={{
            fontFamily:
              '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang TC", "Microsoft JhengHei", sans-serif',
            fontSize: 28,
            fontWeight: 600,
            lineHeight: 1.45,
            letterSpacing: "0.02em",
            textShadow: "0 2px 8px rgba(0,0,0,0.4)",
          }}
        >
          {activeCue.text}
        </span>
      </div>
    </div>
  );
};
