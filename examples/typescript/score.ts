/** Pure deterministic rule shared by tests and an eventual game client. */
export function comboMultiplier(hits: number): number {
  if (!Number.isInteger(hits) || hits < 0) throw new RangeError('hits must be a nonnegative integer');
  return Math.min(1 + Math.max(0, hits - 1) * 0.1, 2);
}
