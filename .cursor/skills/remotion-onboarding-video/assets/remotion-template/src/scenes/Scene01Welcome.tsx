import React from "react";
import {
  AbsoluteFill,
  Easing,
  Img,
  interpolate,
  staticFile,
  useCurrentFrame,
} from "remotion";

export const Scene01Welcome: React.FC = () => {
  const frame = useCurrentFrame();

  // Smooth Ken Burns zoom towards Lucy (right side)
  const scale = interpolate(frame, [0, 239], [1.0, 1.08], {
    easing: Easing.bezier(0.25, 0.1, 0.25, 1),
    extrapolateRight: "clamp",
  });

  const translateX = interpolate(frame, [0, 239], [0, -40], {
    easing: Easing.bezier(0.25, 0.1, 0.25, 1),
    extrapolateRight: "clamp",
  });

  // Badge animation
  const badgeOpacity = interpolate(frame, [15, 30], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const badgeTranslateY = interpolate(frame, [15, 30], [15, 0], {
    easing: Easing.out(Easing.cubic),
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ overflow: "hidden", backgroundColor: "#fdf8fb" }}>
      {/* Background slide with Ken Burns motion */}
      <div
        style={{
          width: "100%",
          height: "100%",
          transform: `scale(${scale}) translateX(${translateX}px)`,
          transformOrigin: "center center",
        }}
      >
        <Img
          src={staticFile("slides/slide-01-welcome-context.png")}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
          }}
        />
      </div>

      {/* Floating Accent Badge in whitespace */}
      <div
        style={{
          position: "absolute",
          bottom: 140,
          left: 64,
          opacity: badgeOpacity,
          transform: `translateY(${badgeTranslateY}px)`,
          background: "linear-gradient(135deg, #d82b7d 0%, #9873d9 100%)",
          color: "#ffffff",
          padding: "12px 24px",
          borderRadius: 14,
          boxShadow: "0 8px 25px rgba(216, 43, 125, 0.35)",
          display: "flex",
          alignItems: "center",
          gap: 12,
        }}
      >
        <span style={{ fontSize: 22 }}>✨</span>
        <div>
          <div
            style={{
              fontFamily:
                '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
              fontWeight: 800,
              fontSize: 18,
              letterSpacing: "0.02em",
            }}
          >
            Welcome Aboard, Lucy!
          </div>
          <div
            style={{
              fontFamily:
                '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
              fontSize: 13,
              opacity: 0.9,
            }}
          >
            Your First Week Navigation Guide
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
