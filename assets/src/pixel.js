"use strict";
/**
 * Low-level pixel-art toolkit: a raw RGBA buffer plus primitives for
 * flat fills, dithered "glow" fills, Bresenham lines, and -- the piece
 * that actually makes this sprite-based rather than rectangle-based --
 * blit(), which stamps a hand-authored ASCII-art sprite grid onto the
 * buffer pixel by pixel.
 */

class PixelBuffer {
  constructor(width, height, bg) {
    this.width = width;
    this.height = height;
    this.data = new Uint8ClampedArray(width * height * 4);
    if (bg) this.clear(bg);
  }

  inBounds(x, y) {
    return x >= 0 && y >= 0 && x < this.width && y < this.height;
  }

  set(x, y, color) {
    if (!color) return;
    // Defensive rounding: a fractional coordinate (e.g. from an odd
    // dimension divided by 2) would otherwise still produce an integer
    // byte offset once multiplied by 4, silently writing into the wrong
    // RGBA channel of a neighboring pixel instead of failing loudly.
    x = Math.round(x);
    y = Math.round(y);
    if (!this.inBounds(x, y)) return;
    const i = (y * this.width + x) * 4;
    this.data[i] = color[0];
    this.data[i + 1] = color[1];
    this.data[i + 2] = color[2];
    this.data[i + 3] = color.length > 3 ? color[3] : 255;
  }

  get(x, y) {
    if (!this.inBounds(x, y)) return null;
    const i = (y * this.width + x) * 4;
    return [this.data[i], this.data[i + 1], this.data[i + 2], this.data[i + 3]];
  }

  clear(color) {
    for (let y = 0; y < this.height; y++) {
      for (let x = 0; x < this.width; x++) this.set(x, y, color);
    }
  }

  rect(x0, y0, x1, y1, color) {
    for (let y = y0; y <= y1; y++) {
      for (let x = x0; x <= x1; x++) this.set(x, y, color);
    }
  }

  hline(x0, x1, y, color) {
    for (let x = x0; x <= x1; x++) this.set(x, y, color);
  }

  vline(x, y0, y1, color) {
    for (let y = y0; y <= y1; y++) this.set(x, y, color);
  }

  /** Bresenham line -- used for cables, headphone bands, diagram edges. */
  line(x0, y0, x1, y1, color) {
    x0 = Math.round(x0); y0 = Math.round(y0);
    x1 = Math.round(x1); y1 = Math.round(y1);
    const dx = Math.abs(x1 - x0), sx = x0 < x1 ? 1 : -1;
    const dy = -Math.abs(y1 - y0), sy = y0 < y1 ? 1 : -1;
    let err = dx + dy;
    for (;;) {
      this.set(x0, y0, color);
      if (x0 === x1 && y0 === y1) break;
      const e2 = 2 * err;
      if (e2 >= dy) { err += dy; x0 += sx; }
      if (e2 <= dx) { err += dx; y0 += sy; }
    }
  }

  /** Filled ellipse via a simple squared-distance scan. */
  ellipse(cx, cy, rx, ry, color) {
    for (let y = -ry; y <= ry; y++) {
      for (let x = -rx; x <= rx; x++) {
        if ((x * x) / (rx * rx) + (y * y) / (ry * ry) <= 1) {
          this.set(cx + x, cy + y, color);
        }
      }
    }
  }

  ellipseOutline(cx, cy, rx, ry, color) {
    const steps = Math.max(16, (rx + ry) * 2);
    for (let i = 0; i < steps; i++) {
      const a = (i / steps) * Math.PI * 2;
      this.set(Math.round(cx + Math.cos(a) * rx), Math.round(cy + Math.sin(a) * ry), color);
    }
  }

  /** A partial elliptical arc (degrees, screen convention: 0=right,
   * 90=down) with real thickness -- used for the headphone headband so
   * it reads as a curved band instead of angular line segments. */
  arc(cx, cy, rx, ry, startDeg, endDeg, color, thickness = 1) {
    const steps = Math.max(20, Math.round((rx + ry) * 1.2));
    for (let i = 0; i <= steps; i++) {
      const deg = startDeg + ((endDeg - startDeg) * i) / steps;
      const rad = (deg * Math.PI) / 180;
      for (let t = 0; t < thickness; t++) {
        const x = cx + Math.cos(rad) * (rx - t);
        const y = cy + Math.sin(rad) * (ry - t);
        this.set(Math.round(x), Math.round(y), color);
      }
    }
  }

  /** Ordered dither fill between two colors -- the pixel-art stand-in
   * for a smooth gradient. */
  ditherRect(x0, y0, x1, y1, colorA, colorB, density = 2) {
    for (let y = y0; y <= y1; y++) {
      for (let x = x0; x <= x1; x++) {
        this.set(x, y, (x + y * 2) % density === 0 ? colorB : colorA);
      }
    }
  }

  /** Sparse overlay pattern -- used for glow/light bleed that shouldn't
   * erase the texture already drawn underneath it. */
  stipple(x0, y0, x1, y1, color, density = 3, phase = 0) {
    for (let y = y0; y <= y1; y++) {
      for (let x = x0; x <= x1; x++) {
        if ((x + y + phase) % density === 0) this.set(x, y, color);
      }
    }
  }

  /** Dithered ring halo around a point light. */
  ditherRing(cx, cy, rInner, rOuter, color) {
    for (let y = cy - rOuter; y <= cy + rOuter; y++) {
      for (let x = cx - rOuter; x <= cx + rOuter; x++) {
        const d2 = (x - cx) ** 2 + (y - cy) ** 2;
        if (d2 >= rInner * rInner && d2 <= rOuter * rOuter && (x + y) % 2 === 0) {
          this.set(x, y, color);
        }
      }
    }
  }

  /**
   * Stamp a hand-authored sprite onto the buffer. `rows` is an array of
   * equal-length strings; `colorMap` maps each character to an RGB color
   * (or omits it / maps to null for transparent). This is the mechanism
   * that lets objects be designed as real pixel-art shapes instead of
   * rectangles: every non-trivial sprite (character, chair, mug, plant,
   * books, trophy, figurine...) is authored this way.
   */
  blit(rows, colorMap, ox, oy, opts = {}) {
    const flipX = !!opts.flipX;
    const h = rows.length;
    for (let ry = 0; ry < h; ry++) {
      const row = rows[ry];
      const w = row.length;
      for (let rx = 0; rx < w; rx++) {
        const ch = row[flipX ? w - 1 - rx : rx];
        if (ch === "." || ch === " ") continue;
        const color = colorMap[ch];
        if (!color) continue;
        this.set(ox + rx, oy + ry, color);
      }
    }
  }
}

// ---------------------------------------------------------------------
// A hand-authored 3x5 pixel bitmap font. Real TrueType rendering breaks
// apart into illegible fragments at these pixel heights, so glyphs are
// drawn from fixed bit patterns instead.
// ---------------------------------------------------------------------

const FONT_3X5 = {
  A: ["010", "101", "111", "101", "101"],
  C: ["011", "100", "100", "100", "011"],
  D: ["110", "101", "101", "101", "110"],
  E: ["111", "100", "110", "100", "111"],
  F: ["111", "100", "110", "100", "100"],
  G: ["011", "100", "101", "101", "011"],
  H: ["101", "101", "111", "101", "101"],
  I: ["111", "010", "010", "010", "111"],
  K: ["101", "101", "110", "101", "101"],
  L: ["100", "100", "100", "100", "111"],
  M: ["101", "111", "111", "101", "101"],
  N: ["101", "111", "111", "111", "101"],
  O: ["010", "101", "101", "101", "010"],
  P: ["110", "101", "110", "100", "100"],
  R: ["110", "101", "110", "101", "101"],
  S: ["011", "100", "010", "001", "110"],
  T: ["111", "010", "010", "010", "010"],
  U: ["101", "101", "101", "101", "111"],
  V: ["101", "101", "101", "101", "010"],
  Y: ["101", "101", "010", "010", "010"],
  " ": ["000", "000", "000", "000", "000"],
  "/": ["001", "001", "010", "100", "100"],
  ".": ["000", "000", "000", "000", "010"],
};

function measurePixelText(text, scale = 1, spacing = 1) {
  const n = text.length;
  if (n === 0) return 0;
  return n * 3 * scale + (n - 1) * spacing * scale;
}

function drawPixelText(buf, x, y, text, color, opts = {}) {
  const scale = opts.scale || 1;
  const spacing = opts.spacing === undefined ? 1 : opts.spacing;
  const center = !!opts.center;
  const width = measurePixelText(text, scale, spacing);
  let cx = center ? x - Math.floor(width / 2) : x;
  for (const ch of text.toUpperCase()) {
    const glyph = FONT_3X5[ch] || FONT_3X5[" "];
    for (let ry = 0; ry < glyph.length; ry++) {
      const row = glyph[ry];
      for (let rx = 0; rx < row.length; rx++) {
        if (row[rx] === "1") {
          if (scale === 1) {
            buf.set(cx + rx, y + ry, color);
          } else {
            buf.rect(cx + rx * scale, y + ry * scale, cx + rx * scale + scale - 1, y + ry * scale + scale - 1, color);
          }
        }
      }
    }
    cx += 3 * scale + spacing * scale;
  }
  return width;
}

function pulse(frameIndex, period, lo = 0.3, hi = 1.0) {
  const t = (frameIndex % period) / period;
  return lo + (hi - lo) * (0.5 + 0.5 * Math.sin(t * Math.PI * 2));
}

module.exports = { PixelBuffer, drawPixelText, measurePixelText, pulse };
