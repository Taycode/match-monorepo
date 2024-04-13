export function getExperience(experience: string) {
  if (experience === "Entry-level") return [0, 1];
  if (experience === "Junior-level") return [1, 2];
  if (experience === "Mid-level") return [2, 4];
  return [4, 100];
}

export function getMatchScore(score: string) {
  if (score === "< 5.0") return [0, 5];
  if (score === "5.0-7.5") return [5, 7.5];
  if (score === "7.5-9.0") return [7.5, 9];
  return [9, 10];
}
