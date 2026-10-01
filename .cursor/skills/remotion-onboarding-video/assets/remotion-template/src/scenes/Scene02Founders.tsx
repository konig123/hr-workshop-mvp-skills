import React from "react";
import {
  AbsoluteFill,
  Easing,
  Img,
  interpolate,
  staticFile,
  useCurrentFrame,
} from "remotion";

export const Scene02Founders: React.FC = () => {
  const frame = useCurrentFrame();

  // Dynamic camera panning across founders
  const panX = interpolate(
    frame,
    [0, 100, 140, 180, 230, 280, 361],
    [0, 0, 30, 0, -30, 0, 0],
    {
      easing: Easing.bezier(0.33, 1, 0.68, 1),
      extrapolateRight: "clamp",
    }
  );

  const scale = interpolate(
    frame,
    [0, 100, 140, 230, 280, 361],
    [1.0, 1.03, 1.05, 1.05, 1.02, 1.01],
    {
      easing: Easing.bezier(0.33, 1, 0.68, 1),
      extrapolateRight: "clamp",
    }
  );

  // Founder highlight tags active intervals
  const showGeorgia = frame >= 110 && frame < 165;
  const showCameron = frame >= 165 && frame < 220;
  const showJustin = frame >= 220 && frame < 275;

  return (
    <AbsoluteFill style={{ overflow: "hidden", backgroundColor: "#d82b7d" }}>
      <div
        style={{
          width: "100%",
          height: "100%",
          transform: `scale(${scale}) translateX(${panX}px)`,
          transformOrigin: "center 60%",
        }}
      >
        <Img
          src={staticFile("slides/slide-02-founders.png")}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
          }}
        />

        {/* Dynamic Glowing Spotlight Rings around Portrait Cards */}
        {showGeorgia && (
          <div
            style={{
              position: "absolute",
              left: "5.3%",
              top: "32.2%",
              width: "27.4%",
              height: "47%",
              borderRadius: 36,
              border: "5px solid #d82b7d",
              boxShadow:
                "0 0 30px rgba(216, 43, 125, 0.8), inset 0 0 15px rgba(216, 43, 125, 0.3)",
              pointerEvents: "none",
            }}
          />
        )}

        {showCameron && (
          <div
            style={{
              position: "absolute",
              left: "35.8%",
              top: "32.2%",
              width: "27.4%",
              height: "47%",
              borderRadius: 36,
              border: "5px solid #d82b7d",
              boxShadow:
                "0 0 30px rgba(216, 43, 125, 0.8), inset 0 0 15px rgba(216, 43, 125, 0.3)",
              pointerEvents: "none",
            }}
          />
        )}

        {showJustin && (
          <div
            style={{
              position: "absolute",
              left: "66.3%",
              top: "32.2%",
              width: "27.4%",
              height: "47%",
              borderRadius: 36,
              border: "5px solid #d82b7d",
              boxShadow:
                "0 0 30px rgba(216, 43, 125, 0.8), inset 0 0 15px rgba(216, 43, 125, 0.3)",
              pointerEvents: "none",
            }}
          />
        )}
      </div>
    </AbsoluteFill>
  );
};
