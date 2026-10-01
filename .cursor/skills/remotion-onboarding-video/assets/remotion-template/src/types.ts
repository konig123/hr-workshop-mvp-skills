export interface SubtitleCue {
  from: number;
  to: number;
  text: string;
}

export interface SceneMeta {
  id: string;
  number: number;
  title: string;
  subtitle: string;
  durationFrames: number;
  audioSrc: string;
  subtitles: SubtitleCue[];
}
