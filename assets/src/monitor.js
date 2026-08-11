"use strict";
/**
 * The hero monitor: a real RAG pipeline (SOURCE -> RETRIEVE -> RANK ->
 * GENERATE) rendered as small connected node sprites with flowing
 * particles, plus a live bar chart and a status readout -- placed in the
 * screen regions that stay clear of the character's head rather than
 * stacked behind it.
 */

const palette = require("./palette");
const { drawPixelText, measurePixelText, pulse } = require("./pixel");
const layout = require("./layout");

const c = palette;

const STAGES = [
  ["SRC", c.ledBlue],
  ["RET", c.tealNode],
  ["RNK", c.ledYellow],
  ["GEN", c.purpleNode],
];

function drawMonitor(buf, frameIndex) {
  const M = layout.MONITOR;

  const glow = pulse(frameIndex, 18) > 0.65 ? c.cyanGlowStrong : c.cyanGlowSoft;
  buf.stipple(M.x0 - 3, M.bezelY0 - 3, M.x1 + 3, M.bezelY1, glow, 3);

  buf.rect(M.x0, M.bezelY0, M.x1, M.bezelY1, c.metalDark);
  buf.hline(M.x0, M.x1, M.bezelY0, c.metalDarkHi);

  const flicker = frameIndex % 17 === 0;
  const screenBg = flicker ? c.screenBg.map((v) => Math.max(0, v - 3)) : c.screenBg;
  buf.rect(M.screenX0, M.screenY0, M.screenX1, M.screenY1, screenBg);

  const ledX = M.x1 - 3, ledY = M.bezelY1 - 2;
  if (frameIndex % 16 < 13) buf.set(ledX, ledY, c.ledGreen);

  const neckX0 = layout.MONITOR_CX - 4, neckX1 = layout.MONITOR_CX + 4;
  buf.rect(neckX0, M.bezelY1, neckX1, M.bezelY1 + 6, c.metalCase);
  buf.rect(layout.MONITOR_CX - 12, M.bezelY1 + 6, layout.MONITOR_CX + 12, M.bezelY1 + 8, c.metalCase);
  buf.hline(layout.MONITOR_CX - 12, layout.MONITOR_CX + 12, M.bezelY1 + 6, c.metalDarkHi);

  // --- RAG pipeline row, pinned to the guaranteed-clear top strip -----
  const pipeY = M.screenY0 + 2;
  const nodeW = 12;
  const span = M.screenX1 - M.screenX0 - 6;
  const xs = STAGES.map((_, i) => M.screenX0 + 3 + Math.round((i * (span - nodeW)) / (STAGES.length - 1)));

  for (let i = 0; i < STAGES.length - 1; i++) {
    buf.hline(xs[i] + nodeW, xs[i + 1], pipeY + 2, [50, 70, 80]);
  }
  STAGES.forEach(([label, color], i) => {
    buf.rect(xs[i], pipeY, xs[i] + nodeW, pipeY + 5, color);
    drawPixelText(buf, xs[i] + 1, pipeY + 1, label, c.screenBg);
  });

  const totalSpan = xs[xs.length - 1] - xs[0];
  for (let p = 0; p < 2; p++) {
    const prog = (frameIndex * 3 + p * Math.floor(totalSpan / 2)) % totalSpan;
    buf.set(xs[0] + Math.floor(nodeW / 2) + prog, pipeY + 2, c.tealParticle);
  }

  // the character's head sits below the pipeline; graph + status live in
  // the clear bands to either side of it
  const bandY0 = pipeY + 9;

  const barX0 = M.screenX0 + 3;
  const barBase = bandY0 + 16;
  for (let i = 0; i < 4; i++) {
    const bh = 3 + ((frameIndex + i * 5) % 13);
    const bx = barX0 + i * 3;
    buf.vline(bx, barBase - bh, barBase, c.tealNode);
    buf.vline(bx + 1, barBase - bh, barBase, c.tealNode);
  }
  buf.hline(barX0 - 1, barX0 + 11, barBase + 1, c.screenGrid);

  const codes = ["SRCH", "READ", "AGNT", "DONE"];
  const code = codes[Math.floor(frameIndex / 7) % codes.length];
  const statusX = M.screenX1 - 3 - measurePixelText(code);
  drawPixelText(buf, statusX, bandY0, code, c.tealNode);
  if (frameIndex % 8 < 4) buf.rect(M.screenX1 - 3, bandY0, M.screenX1 - 2, bandY0 + 4, c.cyanCursor);
  const confW = 4 + ((frameIndex * 2) % 14);
  buf.hline(statusX, statusX + confW, bandY0 + 7, c.purpleNode);

  return { pipeY, bandY0 };
}

/**
 * A smaller secondary screen beside the hero monitor, showing a
 * LangGraph-style node graph -- "multiple monitors" plus the
 * LangGraph/AI-agent easter egg, as its own distinct pixel-art object
 * rather than a duplicate of the main screen.
 */
function drawSecondaryMonitor(buf, frameIndex) {
  const M2 = layout.MONITOR2;
  buf.rect(M2.x0, M2.bezelY0, M2.x1, M2.bezelY1, c.metalDark);
  buf.hline(M2.x0, M2.x1, M2.bezelY0, c.metalDarkHi);
  buf.rect(M2.screenX0, M2.screenY0, M2.screenX1, M2.screenY1, [12, 16, 28]);

  const standCx = Math.floor((M2.x0 + M2.x1) / 2);
  buf.rect(standCx - 3, M2.bezelY1, standCx + 3, layout.DESK.surfaceY, c.metalCase);
  buf.rect(standCx - 8, layout.DESK.surfaceY - 2, standCx + 8, layout.DESK.surfaceY, c.metalCase);

  const glow = pulse(frameIndex, 12);
  const lit = (base) => base.map((v) => Math.floor(v * (0.55 + glow * 0.45)));
  const cx0 = M2.screenX0, cy0 = M2.screenY0;
  const nodes = [[cx0 + 3, cy0 + 3], [cx0 + 15, cy0 + 3], [cx0 + 3, cy0 + 13], [cx0 + 15, cy0 + 13]];
  const edges = [[0, 1], [0, 2], [1, 3], [2, 3]];
  for (const [a, b] of edges) buf.line(nodes[a][0], nodes[a][1], nodes[b][0], nodes[b][1], c.tealNodeLine);
  nodes.forEach(([nx, ny], i) => {
    buf.rect(nx - 1, ny - 1, nx + 1, ny + 1, i === Math.floor(frameIndex / 5) % 4 ? lit(c.purpleNode) : lit(c.tealNode));
  });

  const ledOn = (frameIndex + 3) % 10 < 6;
  buf.set(M2.x1 - 2, M2.bezelY1 - 2, ledOn ? c.ledBlue : [30, 50, 70]);
}

module.exports = { drawMonitor, drawSecondaryMonitor };
