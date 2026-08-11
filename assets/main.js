"use strict";
/**
 * Entry point: renders every low-resolution frame from src/scene.js,
 * upscales each with nearest-neighbor sampling (via canvas with
 * imageSmoothingEnabled = false) for authentic blocky pixel-art edges,
 * and writes assets/ai-engineer.gif + assets/preview.png.
 *
 * Run from the repository root:
 *   node assets/main.js
 */

const fs = require("fs");
const path = require("path");
const { createCanvas } = require("canvas");
const GIFEncoder = require("gif-encoder-2");

const layout = require("./src/layout");
const { composeFrame } = require("./src/scene");

const GIF_PATH = path.join(__dirname, "ai-engineer.gif");
const PREVIEW_PATH = path.join(__dirname, "preview.png");

const FINAL_W = layout.W * layout.SCALE;
const FINAL_H = layout.H * layout.SCALE;

function bufferToLowResCanvas(buf) {
  const canvas = createCanvas(buf.width, buf.height);
  const ctx = canvas.getContext("2d");
  const imageData = ctx.createImageData(buf.width, buf.height);
  imageData.data.set(buf.data);
  ctx.putImageData(imageData, 0, 0);
  return canvas;
}

function upscale(lowResCanvas) {
  const canvas = createCanvas(FINAL_W, FINAL_H);
  const ctx = canvas.getContext("2d");
  ctx.imageSmoothingEnabled = false;
  ctx.drawImage(lowResCanvas, 0, 0, layout.W, layout.H, 0, 0, FINAL_W, FINAL_H);
  return canvas;
}

function main() {
  console.log(`Rendering ${layout.NUM_FRAMES} frames at ${layout.W}x${layout.H} -> ${FINAL_W}x${FINAL_H}...`);

  const frames = [];
  for (let i = 0; i < layout.NUM_FRAMES; i++) {
    const buf = composeFrame(i);
    frames.push(upscale(bufferToLowResCanvas(buf)));
  }

  const encoder = new GIFEncoder(FINAL_W, FINAL_H, "neuquant", false);
  encoder.start();
  encoder.setRepeat(0);
  encoder.setDelay(layout.FRAME_DELAY_MS);
  encoder.setQuality(5);
  for (const canvas of frames) {
    encoder.addFrame(canvas.getContext("2d"));
  }
  encoder.finish();

  fs.writeFileSync(GIF_PATH, encoder.out.getData());
  console.log(`Saved GIF: ${GIF_PATH}`);

  fs.writeFileSync(PREVIEW_PATH, frames[0].toBuffer("image/png"));
  console.log(`Saved preview PNG: ${PREVIEW_PATH}`);

  const gifStats = fs.statSync(GIF_PATH);
  console.log(`\nFinal GIF: ${FINAL_W}x${FINAL_H}, ${layout.NUM_FRAMES} frames, ${(gifStats.size / 1024).toFixed(1)} KB`);
}

main();
