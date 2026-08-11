"use strict";
/**
 * Composes one low-resolution frame from all the sprite modules, in
 * back-to-front order.
 */

const { PixelBuffer } = require("./pixel");
const palette = require("./palette");
const layout = require("./layout");
const env = require("./environment");
const devices = require("./devices");
const { drawMonitor, drawSecondaryMonitor } = require("./monitor");
const { drawCharacter, drawChair, TORSO_TOP_OFFSET, TORSO_BOTTOM_OFFSET } = require("./character");

const POSE_SEQUENCE = [0, 1, 2, 1, 0]; // A -> B -> C -> B -> A

function poseForFrame(frameIndex) {
  const step = Math.max(1, Math.floor(layout.NUM_FRAMES / POSE_SEQUENCE.length));
  return POSE_SEQUENCE[Math.floor(frameIndex / step) % POSE_SEQUENCE.length];
}

function composeFrame(frameIndex) {
  const buf = new PixelBuffer(layout.W, layout.H, palette.bgWallTop);

  env.drawBackground(buf);
  env.drawWindow(buf, frameIndex);
  env.drawConduit(buf, frameIndex);
  env.drawIdentityPoster(buf);
  env.drawHangingMobile(buf, frameIndex);
  env.drawWallClock(buf, frameIndex);
  env.drawArchitecturePoster(buf);
  env.drawServerRack(buf, frameIndex);
  devices.drawStorageBoxes(buf);
  env.drawShelves(buf, frameIndex);
  env.drawTrailingVine(buf);
  env.drawShelfDiagramScreen(buf, frameIndex);
  env.drawTechnologyGlyphs(buf);

  env.drawDesk(buf, "top");
  drawMonitor(buf, frameIndex);
  drawSecondaryMonitor(buf, frameIndex);

  // the chair is behind the desk, so it's drawn before anything sitting
  // on the desk surface -- otherwise a grown armrest can paint over a
  // desk item drawn "underneath" it
  drawChair(
    buf, layout.CHAR.cx, layout.CHAR.headTopY,
    layout.CHAR.headTopY + TORSO_TOP_OFFSET,
    layout.CHAR.headTopY + TORSO_BOTTOM_OFFSET
  );

  devices.drawKeyboardAndMouse(buf);
  devices.drawSmartPuck(buf, frameIndex);
  devices.drawPlant(buf);
  devices.drawPenCup(buf);
  devices.drawNotebook(buf);
  devices.drawSpeaker(buf);
  devices.drawLamp(buf, frameIndex);
  devices.drawMug(buf, frameIndex);
  devices.drawDevBoard(buf, frameIndex);
  devices.drawVectorDb(buf, frameIndex);
  devices.drawRamSticks(buf);

  const bob = frameIndex % 10 < 5 ? 0 : -1;
  drawCharacter(buf, {
    cx: layout.CHAR.cx,
    headTopY: layout.CHAR.headTopY,
    keyboardY: layout.KEYBOARD.y1,
    keyboardX0: layout.KEYBOARD.x0,
    keyboardX1: layout.KEYBOARD.x1,
    pose: poseForFrame(frameIndex),
    bob,
  });

  env.drawDesk(buf, "front");
  devices.drawFloorNas(buf, frameIndex);
  devices.drawLeaningBooks(buf);

  return buf;
}

module.exports = { composeFrame };
