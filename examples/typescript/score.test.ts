import { test } from 'node:test';
import assert from 'node:assert/strict';
import { comboMultiplier } from './score.ts';

test('first hit and no hit have baseline damage', () => {
  assert.equal(comboMultiplier(0), 1);
  assert.equal(comboMultiplier(1), 1);
});
test('consecutive hits increase damage up to the cap', () => {
  assert.equal(comboMultiplier(5), 1.4);
  assert.equal(comboMultiplier(11), 2);
  assert.equal(comboMultiplier(100), 2);
});
test('reject malformed inputs at the contract boundary', () => {
  for (const value of [-1, 1.5, NaN, Infinity]) assert.throws(() => comboMultiplier(value), RangeError);
});
