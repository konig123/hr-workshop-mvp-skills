import React from "react";
import {
  AbsoluteFill,
  Img,
  interpolate,
  staticFile,
  useCurrentFrame,
} from "remotion";

export const Scene05Schedule: React.FC = () => {
  const frame = useCurrentFrame();

  // Phase 1: 0-70f Overview (slide-05)
  // Phase 2: 70-190f Days 1-2 (slide-06)
  // Phase 3: 190-310f Days 3-4 (slide-07)
  // Phase 4: 310-420f Day 5 Wrap-up (slide-08)

  const opacity05 = interpolate(frame, [0, 65, 75], [1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const opacity06 = interpolate(frame, [65, 75, 185, 195], [0, 1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const opacity07 = interpolate(frame, [185, 195, 305, 315], [0, 1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const opacity08 = interpolate(frame, [305, 315, 420], [0, 1, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ overflow: "hidden", backgroundColor: "#fbf6fa" }}>
      {/* Slide 05 - Overview */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          opacity: opacity05,
        }}
      >
        <Img
          src={staticFile("slides/slide-05-week-one-overview.png")}
          style={{ width: "100%", height: "100%", objectFit: "cover" }}
        />
      </div>

      {/* Slide 06 - Days 1-2 */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          opacity: opacity06,
        }}
      >
        <Img
          src={staticFile("slides/slide-06-days-1-2.png")}
          style={{ width: "100%", height: "100%", objectFit: "cover" }}
        />
      </div>

      {/* Slide 07 - Days 3-4 */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          opacity: opacity07,
        }}
      >
        <Img
          src={staticFile("slides/slide-07-days-3-4.png")}
          style={{ width: "100%", height: "100%", objectFit: "cover" }}
        />
      </div>

      {/* Slide 08 - Day 5 */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          opacity: opacity08,
        }}
      >
        <Img
          src={staticFile("slides/slide-08-day-5-wrapup.png")}
          style={{ width: "100%", height: "100%", objectFit: "cover" }}
        />
      </div>
    </AbsoluteFill>
  );
};
