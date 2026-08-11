"use strict";
/**
 * The developer sprite, viewed from behind. Built from a per-row
 * silhouette profile (each scanline's width/inset is a deliberate pixel
 * choice, the same technique real pixel-art sprites are authored with)
 * rather than a single flat rectangle, plus small hand-authored ear cups
 * and a real curved headphone band.
 *
 * Three typing poses (A / B / C) are exposed; the animation driver walks
 * A -> B -> C -> B -> A so the hands look like they're alternating keys
 * rather than robotically bobbing in lockstep.
 *
 * The character is scaled up from its originally-authored proportions
 * (W_SCALE / ROW_SCALE below) so it reads as the visual focal point of
 * the scene rather than a small silhouette lost against the monitor.
 */

const palette = require("./palette");

const W_SCALE = 1.45;
const ROW_SCALE = 1.15;

function s(v) {
  return Math.round(v * W_SCALE);
}

function drawEarCup(buf, cx, cy) {
  const c = palette;
  buf.ellipse(cx, cy, 4, 6, c.headphone);
  buf.ellipse(cx, cy - 5, 4, 3, c.headphoneHi);
  buf.ellipse(cx - 1, cy, 2, 4, [16, 16, 20]);
}

// Head silhouette profile: [insetLeft, insetRight, colorKey] per row,
// authored at a base size then scaled by row/width factors below.
const BASE_HEAD_PROFILE = [
  [9, 9, "hi"], [6, 6, "hi"], [3, 3, "hi"], [1, 1, "base"],
  [0, 0, "base"], [0, 0, "base"], [0, 0, "base"], [0, 0, "base"],
  [0, 0, "base"], [0, 0, "base"], [0, 0, "base"], [0, 0, "base"],
  [0, 0, "base"], [0, 0, "base"], [1, 1, "base"], [2, 2, "base"],
  [3, 3, "base"], [4, 4, "base"],
];

// Torso silhouette profile: [insetLeft, insetRight] per row (hoodie).
const BASE_TORSO_PROFILE = [
  [0, 0], [0, 0], [0, 0], [0, 0],
  [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1],
  [2, 2], [2, 2], [2, 2], [2, 2],
];

/** Scales a row-profile silhouette: stretches the row count and scales
 * each row's inset, preserving the authored taper shape instead of
 * naively stretching a bounding box. */
function scaleProfile(profile, wScale, rowScale) {
  const outLen = Math.max(1, Math.round(profile.length * rowScale));
  const out = [];
  for (let i = 0; i < outLen; i++) {
    const srcIdx = Math.min(profile.length - 1, Math.floor((i / outLen) * profile.length));
    const src = profile[srcIdx];
    const row = [Math.round(src[0] * wScale), Math.round(src[1] * wScale)];
    if (src.length > 2) row.push(src[2]);
    out.push(row);
  }
  return out;
}

const HEAD_PROFILE = scaleProfile(BASE_HEAD_PROFILE, W_SCALE, ROW_SCALE);
const TORSO_PROFILE = scaleProfile(BASE_TORSO_PROFILE, W_SCALE, ROW_SCALE);

function sEven(v) {
  const r = s(v);
  return r % 2 === 0 ? r : r + 1;
}

const HEAD_W = sEven(22);
const TORSO_W = sEven(46);
const ARM_CAP_H = 3;
const NECK_HALF_W = s(7);

// row offsets used by scene.js to position the chair relative to headTopY
const HEAD_ROWS = HEAD_PROFILE.length;
const NECK_ROWS = 3;
const TORSO_ROWS = TORSO_PROFILE.length;
const TORSO_TOP_OFFSET = HEAD_ROWS + NECK_ROWS;
const TORSO_BOTTOM_OFFSET = TORSO_TOP_OFFSET + TORSO_ROWS - 1;

/**
 * Draws the chair back behind the character: headrest posts, a backrest
 * crossbar and armrests, so real structure is visible around the torso.
 */
function drawChair(buf, cx, headTopY, torsoTopY, torsoBottomY) {
  const c = palette;
  const tX0 = cx - TORSO_W / 2, tX1 = cx + TORSO_W / 2;
  const headTop = headTopY - 4;

  buf.rect(tX0 - s(8), headTop, tX0 - s(3), torsoTopY, c.chair);
  buf.rect(tX1 + s(3), headTop, tX1 + s(8), torsoTopY, c.chair);
  buf.rect(tX0 - s(9), headTop + 1, tX0 - s(8), headTop + 8, c.chair);
  buf.rect(tX1 + s(8), headTop + 1, tX1 + s(9), headTop + 8, c.chair);

  buf.rect(tX0 - s(8), torsoTopY - 6, tX1 + s(8), torsoTopY + 4, c.chair);
  buf.rect(tX0 - s(8), torsoTopY - 6, tX1 + s(8), torsoTopY - 5, c.chairHi);
  buf.vline(tX0 + s(16), torsoTopY - 5, torsoTopY + 3, c.chairHi);

  const armY0 = torsoBottomY - 5, armY1 = torsoBottomY + 4;
  buf.rect(tX0 - s(13), armY0, tX0 - s(7), armY1, c.chair);
  buf.hline(tX0 - s(13), tX0 - s(7), armY0, c.chairHi);
  buf.rect(tX1 + s(7), armY0, tX1 + s(13), armY1, c.chair);
  buf.hline(tX1 + s(7), tX1 + s(13), armY0, c.chairHi);
}

/**
 * Draws the developer. `cx` is the horizontal center; `headTopY` is the
 * top row of the head; `keyboardY` is the row the hands rest on;
 * `keyboardX0/X1` bound the keys so the arms land on either side of them.
 * `pose` is 0 (neutral), 1 (left hand down) or 2 (right hand down).
 */
function drawCharacter(buf, opts) {
  const c = palette;
  const { cx, headTopY, keyboardY, keyboardX0, keyboardX1, pose, bob } = opts;

  const hx0 = cx - HEAD_W / 2, hx1 = cx + HEAD_W / 2;
  let y = headTopY + bob;
  for (const [inL, inR, colorKey] of HEAD_PROFILE) {
    const color = colorKey === "hi" ? c.hairHi : c.hair;
    buf.hline(hx0 + inL, hx1 - inR, y, color);
    y++;
  }
  const headBottomY = y - 1;
  // strand texture + a small asymmetric cowlick for a recognizable
  // hairstyle silhouette, not just a smooth dome
  buf.vline(hx0 + s(6), headTopY + bob + 5, headBottomY - 4, c.hairDark);
  buf.vline(hx1 - s(5), headTopY + bob + 5, headBottomY - 4, c.hairDark);
  buf.line(cx + s(3), headTopY + bob - 1, cx + s(6), headTopY + bob - 5, c.hairHi);
  buf.set(cx + s(5), headTopY + bob - 3, c.hairHi);

  // headphones: a real curved headband arc over the crown, plus rounded
  // ear cups tucked close to the head -- not two square blocks, and not
  // wide enough to crowd the monitor's status readout beside it
  const bandCx = cx, bandCy = headTopY + bob + s(9);
  const bandRx = HEAD_W / 2 + s(4), bandRy = s(15);
  buf.arc(bandCx, bandCy, bandRx, bandRy, 194, 346, c.headphone, 3);
  drawEarCup(buf, hx0 - 1, headTopY + bob + s(8));
  drawEarCup(buf, hx1 + 1, headTopY + bob + s(8));

  // neck
  const neckY0 = headBottomY + 1, neckY1 = neckY0 + NECK_ROWS - 1;
  buf.rect(cx - NECK_HALF_W, neckY0, cx + NECK_HALF_W, neckY1, c.skin);

  // torso (hoodie)
  const torsoY0 = neckY1 + 1;
  const tx0 = cx - TORSO_W / 2, tx1 = cx + TORSO_W / 2;
  y = torsoY0;
  for (const [inL, inR] of TORSO_PROFILE) {
    buf.hline(tx0 + inL, tx1 - inR, y, c.hoodie);
    y++;
  }
  const torsoY1 = y - 1;
  buf.rect(tx0, torsoY0, tx0 + s(5), torsoY1, c.hoodieShadow);
  buf.rect(tx1 - s(5), torsoY0, tx1, torsoY1, c.hoodieHi);
  buf.hline(tx0 + s(3), tx1 - s(3), torsoY0, c.hoodieHi);
  buf.hline(tx0 + s(16), tx1 - s(16), torsoY0 + 1, c.hoodieShadow);
  buf.set(tx0 + s(20), torsoY0 + 4, c.hoodieShadow);
  buf.set(tx1 - s(20), torsoY0 + 4, c.hoodieShadow);

  // small back-of-hoodie accent glyph -- a tiny circuit/node mark, the
  // same kind of personal-touch pop the reference gets from a patterned
  // pillow, without turning the character into a walking logo
  const gy = torsoY0 + 8;
  buf.line(cx - 2, gy, cx, gy + 3, c.purpleAccent);
  buf.line(cx + 2, gy, cx, gy + 3, c.purpleAccent);
  buf.set(cx - 2, gy, c.purpleAccent);
  buf.set(cx + 2, gy, c.purpleAccent);

  // arms: a wider shoulder cap tapering to a narrower forearm, ending in
  // a hand at the keyboard -- the elbow bend keeps them from reading as
  // straight bars
  const typingL = pose === 1 ? 1 : 0;
  const typingR = pose === 2 ? 1 : 0;
  const capW = s(8);
  for (const [kx0, kx1, typing] of [
    [keyboardX0, keyboardX0 + capW, typingL],
    [keyboardX1 - capW, keyboardX1, typingR],
  ]) {
    buf.rect(kx0, torsoY1, kx1, torsoY1 + ARM_CAP_H, c.hoodie);
    const fx0 = kx0 + 1, fx1 = kx1 - 1;
    const fy1 = keyboardY - 1 + typing;
    buf.rect(fx0, torsoY1 + ARM_CAP_H, fx1, fy1, c.hoodieShadow);
    buf.hline(fx0, fx1, Math.max(torsoY1 + ARM_CAP_H, fy1 - 2), c.hoodieHi);
    buf.rect(fx0, fy1 - 1, fx1, fy1, c.skin);
  }

  return { headBottomY, torsoY0, torsoY1 };
}

module.exports = {
  drawCharacter, drawChair, HEAD_W, TORSO_W,
  TORSO_TOP_OFFSET, TORSO_BOTTOM_OFFSET,
};
