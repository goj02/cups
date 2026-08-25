export function playSound(src) {
  const audio = new Audio(src);
  audio.volume = 0.7;
  audio.play().catch(() => {});
  return audio;
}

export function playLoop(src, volume = 0.5) {
  const audio = new Audio(src);
  audio.loop = true;
  audio.volume = volume;
  audio.play().catch(() => {});
  return audio;
}
