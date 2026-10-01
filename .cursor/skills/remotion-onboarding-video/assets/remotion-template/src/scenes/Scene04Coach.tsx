import React from "react";
import {
  AbsoluteFill,
  Easing,
  Img,
  interpolate,
  staticFile,
  useCurrentFrame,
} from "remotion";

export const Scene04Coach: React.FC = () => {
  const frame = useCurrentFrame();

  const scale = interpolate(frame, [0, 285], [1.0, 1.06], {
    easing: Easing.bezier(0.25, 0.1, 0.25, 1),
    extrapolateRight: "clamp",
  });

  const translateX = interpolate(frame, [0, 285], [0, 25], {
    easing: Easing.bezier(0.25, 0.1, 0.25, 1),
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ overflow: "hidden", backgroundColor: "#ffffff" }}>
      <div
        style={{
          width: "100%",
          height: "100%",
          transform: `scale(${scale}) translateX(${translateX}px)`,
          transformOrigin: "35% center",
        }}
      >
        <Img
          src={staticFile("slides/slide-04-coach-terry.png")}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
          }}
        />
      </div>
    </AbsoluteFill>
  );
};
