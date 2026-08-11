"use strict";
/**
 * Small desk-top and floor objects. Each is its own tiny sprite function
 * (per the brief: "if an object is a plant, design a plant sprite") --
 * none of these are a single rectangle.
 */

const palette = require("./palette");
const { pulse } = require("./pixel");
const layout = require("./layout");

const c = palette;

function shadow(buf, x0, x1, y) {
  buf.hline(x0, x1, y, c.shadowDesk);
}

function drawKeyboardAndMouse(buf) {
  const K = layout.KEYBOARD, M = layout.MOUSE;
  shadow(buf, K.x0 - 1, K.x1 + 1, K.y1 + 1);
  buf.rect(K.x0, K.y0, K.x1, K.y1, c.keyDark);
  buf.hline(K.x0, K.x1, K.y0, c.metalDarkHi);
  for (let kx = K.x0 + 2; kx < K.x1 - 1; kx += 3) buf.set(kx, K.y0 + 1, c.keyLight);

  buf.rect(M.x0, M.y0, M.x0 + 4, M.y0 + 6, c.mouseBody);
  buf.hline(M.x0, M.x0 + 4, M.y0, c.mouseHi);
  buf.set(M.x0 + 2, M.y0 + 2, c.keyLight);
}

/** A small round smart-speaker puck beside the keyboard -- a deliberately
 * circular silhouette among all the rectangular furniture. */
function drawSmartPuck(buf, frameIndex) {
  const cx = layout.KEYBOARD.x0 - 12, cy = layout.DESK.surfaceY - 4;
  shadow(buf, cx - 4, cx + 4, layout.DESK.surfaceY + 1);
  buf.ellipse(cx, cy, 4, 4, c.metalDark);
  buf.ellipse(cx, cy - 1, 4, 3, c.metalDarkHi);
  const glow = pulse(frameIndex, 20) > 0.5 ? c.pinkAccent : c.pinkAccentSoft;
  buf.ellipseOutline(cx, cy, 2, 2, glow);
}

function drawPlant(buf) {
  const { x0: px0, y0: py0 } = layout.DESK_ITEMS.plant;
  const bottom = layout.DESK.surfaceY;
  shadow(buf, px0 - 1, px0 + 9, bottom + 1);
  buf.rect(px0, py0 + 8, px0 + 8, bottom, c.plantPot);
  buf.hline(px0, px0 + 8, py0 + 8, c.plantPot);
  buf.rect(px0 + 1, py0 + 2, px0 + 3, py0 + 8, c.plantLeaf);
  buf.rect(px0 + 3, py0, px0 + 5, py0 + 8, c.plantLeafHi);
  buf.rect(px0 + 5, py0 + 3, px0 + 7, py0 + 8, c.plantLeaf);
}

function drawPenCup(buf) {
  const { x0: cx0, y0: cy0 } = layout.DESK_ITEMS.penCup;
  const bottom = layout.DESK.surfaceY;
  shadow(buf, cx0 - 1, cx0 + 7, bottom + 1);
  buf.rect(cx0, cy0, cx0 + 6, bottom, c.penCupBody);
  buf.hline(cx0, cx0 + 6, cy0, c.penCupHi);
  c.pens.forEach((pcolor, i) => {
    buf.line(cx0 + 1 + i * 2, cy0, cx0 + i * 2, cy0 - 7, pcolor);
  });
}

function drawNotebook(buf) {
  const { x0: nx0, y0: ny0 } = layout.DESK_ITEMS.notebook;
  const bottom = layout.DESK.surfaceY;
  shadow(buf, nx0 - 1, nx0 + 13, bottom + 1);
  buf.rect(nx0, ny0, nx0 + 12, bottom, c.notebookPage);
  buf.hline(nx0, nx0 + 12, ny0, c.notebookCover);
  buf.hline(nx0, nx0 + 12, ny0 + 1, c.notebookCover);
  for (let i = 0; i < 3; i++) buf.hline(nx0 + 2, nx0 + 9, ny0 + 3 + i * 2, c.notebookLine);
  for (let i = 0; i < 4; i++) buf.set(nx0 + 3 * i, ny0, c.notebookSpiral);
}

function drawLamp(buf, frameIndex) {
  const { x0: lx0 } = layout.DESK_ITEMS.lamp;
  const bottom = layout.DESK.surfaceY;
  const baseY0 = bottom - 4;
  shadow(buf, lx0 - 1, lx0 + 11, bottom + 1);
  buf.rect(lx0, baseY0, lx0 + 10, bottom, c.metalDark);
  buf.hline(lx0, lx0 + 10, baseY0, c.metalDarkHi);

  const poleX = lx0 + 4;
  const poleTop = baseY0 - 34;
  buf.vline(poleX, poleTop, baseY0, c.metalDarkHi);
  buf.vline(poleX + 1, poleTop, baseY0, c.metalDarkHi);

  let ax = poleX, ay = poleTop;
  for (let i = 0; i < 7; i++) {
    buf.rect(ax, ay, ax + 1, ay + 1, c.metalDarkHi);
    ax += 2; ay -= 2;
  }
  const bulbX = ax + 1, bulbY = ay + 1;

  const glow = pulse(frameIndex, 22) > 0.5 ? c.warmGlow : c.warmGlowSoft;
  buf.ditherRing(bulbX, bulbY, 2, 7, glow);
  buf.rect(bulbX - 1, bulbY - 1, bulbX + 1, bulbY + 1, c.warmBulb);
}

function drawMug(buf, frameIndex) {
  const { x0: mx0, y0: my0 } = layout.DESK_ITEMS.mug;
  const bottom = layout.DESK.surfaceY;
  shadow(buf, mx0 - 1, mx0 + 9, bottom + 1);
  buf.rect(mx0, my0, mx0 + 7, bottom, c.mugBody);
  buf.hline(mx0, mx0 + 7, my0, c.mugHi);
  for (let a = -90; a <= 90; a += 15) {
    const rad = (a * Math.PI) / 180;
    buf.set(Math.round(mx0 + 8 + Math.cos(rad) * 3), Math.round(my0 + 4 + Math.sin(rad) * 3), c.mugBody);
  }
  for (let i = 0; i < 2; i++) {
    const wobble = Math.round(Math.sin((frameIndex + i * 4) / 3) * 1.5);
    const cycle = (frameIndex * 2 + i * 6) % 11;
    const sy = my0 - 2 - cycle;
    const sx = mx0 + 2 + i * 3 + wobble;
    const fade = 1 - cycle / 11;
    if (fade > 0.15) buf.set(sx, sy, c.steam);
  }
}

function drawDevBoard(buf, frameIndex) {
  const { x0: bx0, y0: by0 } = layout.DESK_ITEMS.devBoard;
  const bottom = layout.DESK.surfaceY;
  shadow(buf, bx0 - 1, bx0 + 11, bottom + 1);
  buf.rect(bx0, by0, bx0 + 10, bottom, c.devBoardBody);
  buf.rect(bx0 + 2, by0 + 1, bx0 + 5, by0 + 3, c.devBoardChip);
  for (let i = 0; i < 3; i++) buf.set(bx0 + 2 + i, by0 + 4, [58, 58, 66]);
  const on = frameIndex % 6 < 3;
  buf.set(bx0 + 8, by0 + 1, on ? layout.LED_COLORS[1] : [30, 70, 40]);
}

function drawVectorDb(buf, frameIndex) {
  const { x0: vx0, y0: vy0 } = layout.DESK_ITEMS.vectorDb;
  const bottom = layout.DESK.surfaceY;
  shadow(buf, vx0 - 1, vx0 + 13, bottom + 1);
  for (let i = 0; i < 3; i++) {
    const yy = vy0 + i * 4;
    buf.ellipse(vx0 + 6, yy + 2, 6, 2, c.vectorDb);
  }
  buf.rect(vx0, vy0 + 2, vx0 + 12, bottom - 2, c.vectorDb);
  buf.ellipse(vx0 + 6, vy0, 6, 2, c.vectorDbHi);
  const on = frameIndex % 10 < 6;
  buf.set(vx0 + 6, vy0 + 1, on ? layout.LED_COLORS[2] : [40, 70, 90]);
}

/** A small desk speaker -- another quiet environmental detail. */
function drawSpeaker(buf) {
  const x0 = layout.DESK_ITEMS.notebook.x0 - 12;
  const bottom = layout.DESK.surfaceY;
  const y0 = bottom - 14;
  shadow(buf, x0 - 1, x0 + 7, bottom + 1);
  buf.rect(x0, y0, x0 + 6, bottom, c.speakerBody);
  buf.hline(x0, x0 + 6, y0, [46, 46, 56]);
  buf.ellipse(x0 + 3, y0 + 5, 2, 2, c.speakerCone);
  buf.ellipse(x0 + 3, y0 + 10, 2, 2, c.speakerCone);
}

/** Small stacked storage boxes beside the server rack. */
function drawStorageBoxes(buf) {
  const bx0 = layout.RACK.x1 + 2;
  const bottom = layout.RACK.y1;
  buf.rect(bx0, bottom - 10, bx0 + 12, bottom, c.boxBody);
  buf.hline(bx0, bx0 + 12, bottom - 10, c.boxTape);
  buf.vline(bx0 + 6, bottom - 10, bottom, c.boxTape);
  buf.rect(bx0 + 1, bottom - 18, bx0 + 10, bottom - 10, c.boxBody);
  buf.hline(bx0 + 1, bx0 + 10, bottom - 18, c.boxTape);
}

/** Small colorful "RAM stick" trio on the desk -- a quiet hardware accent. */
function drawRamSticks(buf) {
  const { x0, y0 } = layout.DESK_ITEMS.ramSticks;
  const bottom = layout.DESK.surfaceY;
  shadow(buf, x0 - 1, x0 + 9, bottom + 1);
  const colors = [c.iconAzure, c.iconSpark, c.tealNode];
  colors.forEach((col, i) => {
    const sx0 = x0 + i * 3;
    buf.rect(sx0, y0, sx0 + 2, bottom, [42, 42, 52]);
    buf.set(sx0 + 1, y0, col);
  });
}

/** A small NAS box tucked in front of the right desk leg -- balances the
 * server rack's foreground presence on the opposite side of the scene. */
function drawFloorNas(buf, frameIndex) {
  const x0 = layout.DESK.x1 - 22;
  const bottom = layout.DESK.frontBottom - 2;
  buf.rect(x0, bottom - 12, x0 + 14, bottom, c.metalCase);
  buf.hline(x0, x0 + 14, bottom - 12, c.metalDarkHi);
  for (let i = 0; i < 2; i++) {
    const on = (frameIndex + i * 3) % 9 < 5;
    const col = layout.LED_COLORS[i % layout.LED_COLORS.length];
    buf.set(x0 + 3 + i * 4, bottom - 8, on ? col : col.map((v) => Math.floor(v / 3)));
  }
  buf.hline(x0 + 2, x0 + 12, bottom - 4, [16, 17, 24]);
}

/** A slightly tilted stack of magazines/books leaning against the left
 * desk leg, with a pink sticky note poking out -- an organic, off-axis
 * silhouette and a splash of color low in the foreground. */
function drawLeaningBooks(buf) {
  const x0 = layout.DESK.x0 + 10, bottom = layout.DESK.frontBottom - 2;
  const heights = [14, 11, 8];
  const tilt = [0, 1, 2];
  const bookColors = [c.books[3], c.books[1], c.books[4]];
  heights.forEach((h, i) => {
    const bx = x0 + i * 2 + tilt[i];
    buf.rect(bx, bottom - h - i * 4, bx + 16, bottom - i * 4, bookColors[i]);
    buf.hline(bx, bx + 16, bottom - h - i * 4, [255, 255, 255]);
  });
  buf.rect(x0 + 3, bottom - heights[0] - 3, x0 + 9, bottom - heights[0] + 2, c.pinkAccent);
}

module.exports = {
  drawKeyboardAndMouse,
  drawSmartPuck,
  drawPlant,
  drawPenCup,
  drawNotebook,
  drawLamp,
  drawMug,
  drawDevBoard,
  drawVectorDb,
  drawSpeaker,
  drawLeaningBooks,
  drawStorageBoxes,
  drawRamSticks,
  drawFloorNas,
};
