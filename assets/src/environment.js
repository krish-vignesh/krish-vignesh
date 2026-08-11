"use strict";
/**
 * Background, left-zone server rack, right-zone shelf, and the desk
 * carcass. Furniture panels stay rectangular (real desks and racks are
 * rectangular) but every surface carries its own small sprite-level
 * detail -- vents, seams, LEDs, book spines, cable runs -- so the scene
 * doesn't read as a handful of big flat blocks.
 */

const palette = require("./palette");
const { drawPixelText, pulse } = require("./pixel");
const layout = require("./layout");

const c = palette;

// --- small hand-authored sprites --------------------------------------

const ROBOT_FIGURINE = [
  ".##.",
  "####",
  "#EE#",
  "####",
  ".##.",
];
const ROBOT_COLORS = { "#": [150, 150, 160], E: [90, 220, 170] };

const TROPHY = [
  ".###.",
  "#####",
  ".###.",
  "..#..",
  ".###.",
];
const TROPHY_COLORS = { "#": c.trophyCup };

function drawBackground(buf) {
  const { W, H, WALL_FLOOR_Y } = layout;
  buf.rect(0, 0, W - 1, WALL_FLOOR_Y - 1, c.bgWallTop);
  buf.rect(0, 0, W - 1, 9, c.bgWallShadow);
  for (let x = 3; x < W - 3; x += 42) {
    buf.vline(x, 10, WALL_FLOOR_Y - 1, c.bgPanelLine);
  }
  buf.ditherRect(68, 12, 118, 54, c.bgWallTop, c.bgMoonlight, 5);

  buf.hline(0, W - 1, WALL_FLOOR_Y - 2, c.baseboardHi);
  buf.rect(0, WALL_FLOOR_Y - 1, W - 1, WALL_FLOOR_Y + 1, c.baseboard);

  buf.rect(0, WALL_FLOOR_Y + 2, W - 1, H - 1, c.floor);
  for (let x = 6; x < W - 2; x += 17) {
    buf.vline(x, WALL_FLOOR_Y + 2, H - 1, c.floorPlank);
  }

  const rugY0 = H - 11, rugY1 = H - 1;
  buf.rect(66, rugY0, W - 8, rugY1, c.rug);
  buf.hline(66, W - 8, rugY0, c.rugBorder);
  for (let x = 72; x < W - 8; x += 7) {
    buf.set(x, rugY0 + 3, c.rugPattern);
    buf.set(x, rugY0 + 6, c.rugPattern);
  }
}

const CITY_WINDOW_SPOTS = [
  [4, 3], [10, 6], [17, 2], [24, 7], [31, 4], [38, 8], [45, 3],
];
const STARS = [
  [18, 10, 0], [30, 7, 1], [42, 13, 2], [48, 9, 0], [23, 17, 1],
  [37, 19, 2], [16, 15, 0], [33, 15, 1],
];

function drawWindow(buf, frameIndex) {
  const { WIN } = layout;
  buf.rect(WIN.x0 - 2, WIN.y0 - 2, WIN.x1 + 2, WIN.y1 + 2, c.frameWood);
  buf.hline(WIN.x0 - 2, WIN.x1 + 2, WIN.y0 - 2, c.frameWoodHi);

  const lowBand = WIN.y0 + Math.round((WIN.y1 - WIN.y0) * 0.55);
  buf.rect(WIN.x0, WIN.y0, WIN.x1, lowBand, c.skyTop);
  buf.rect(WIN.x0, lowBand, WIN.x1, WIN.y1, c.skyLow);

  const mx = WIN.x0 + 10, my = WIN.y0 + 9, mr = 6;
  buf.ellipse(mx, my, mr, mr, c.moon);
  buf.ellipse(mx + 2, my - 1, mr - 1, mr - 1, c.moonShadow);

  for (const [sx, sy, seed] of STARS) {
    const wx = WIN.x0 + sx, wy = WIN.y0 + sy;
    if (wx >= WIN.x1 || wy >= lowBand) continue;
    const on = (frameIndex + seed * 5) % 18 < 13;
    buf.set(wx, wy, on ? c.starBright : c.starDim);
  }

  const span = WIN.x1 - WIN.x0 + 16;
  const cx = WIN.x0 - 12 + Math.floor((frameIndex / layout.NUM_FRAMES) * span);
  const cy = WIN.y0 + 6;
  for (const [dx, dy, w] of [[0, 0, 7], [3, -1, 5], [7, 0, 6]]) {
    const x0 = Math.max(cx + dx, WIN.x0), x1 = Math.min(cx + dx + w, WIN.x1);
    if (x1 > x0) buf.rect(x0, cy + dy, x1, cy + dy + 1, c.cloud);
  }

  const heights = [9, 15, 7, 18, 11, 16, 8];
  const bw = (WIN.x1 - WIN.x0) / heights.length;
  heights.forEach((h, i) => {
    const x0 = Math.floor(WIN.x0 + i * bw), x1 = Math.floor(WIN.x0 + (i + 1) * bw) - 1;
    buf.rect(x0, WIN.y1 - h, x1, WIN.y1, c.skyline);
  });
  CITY_WINDOW_SPOTS.forEach(([cwx, cwy], i) => {
    const wx = WIN.x0 + cwx, wy = WIN.y1 - cwy;
    if (wy <= WIN.y0) return;
    const on = (Math.floor(frameIndex / 2) + i * 3) % 9 < 6;
    buf.set(wx, wy, on ? c.cityWindowOn : c.cityWindowOff);
  });

  const midX = Math.floor((WIN.x0 + WIN.x1) / 2);
  buf.vline(midX, WIN.y0, WIN.y1, c.frameWood);
  buf.hline(WIN.x0, WIN.x1, lowBand, c.frameWood);
}

function drawIdentityPoster(buf) {
  const p = layout.POSTER;
  buf.rect(p.x0, p.y0, p.x1, p.y1, c.frameWood);
  buf.rect(p.x0 + 2, p.y0 + 2, p.x1 - 2, p.y1 - 2, c.posterBg);
  const cx = Math.floor((p.x0 + p.x1) / 2);
  drawPixelText(buf, cx, p.y0 + 4, "VIGNESH KRISHNA", c.posterText, { center: true });
  drawPixelText(buf, cx, p.y0 + 13, "AI / ML / DL ENGINEER", c.posterAccent, { center: true });
}

function drawArchitecturePoster(buf) {
  const d = layout.DIAGRAM;
  buf.rect(d.x0, d.y0, d.x1, d.y1, c.diagramFrame);
  buf.rect(d.x0 + 2, d.y0 + 2, d.x1 - 2, d.y1 - 2, c.diagramBg);
  const nodes = [
    [d.x0 + 7, d.y0 + 6], [d.x0 + 22, d.y0 + 6],
    [d.x0 + 14, d.y0 + 15], [d.x0 + 29, d.y0 + 15],
  ];
  for (const [a, b] of [[0, 2], [1, 2], [2, 3]]) {
    buf.line(nodes[a][0], nodes[a][1], nodes[b][0], nodes[b][1], c.tealNodeLine);
  }
  for (const [nx, ny] of nodes) buf.rect(nx - 1, ny - 1, nx + 1, ny + 1, c.tealNode);
}

const SHELF_BOOK_HEIGHTS = [10, 8, 11, 8, 9, 7];

function shelfSpineX(index) {
  const S = layout.SHELF;
  let x = S.x0 + 2;
  for (let i = 0; i < SHELF_BOOK_HEIGHTS.length; i++) {
    if (i === index) return x;
    x += 6;
  }
  return x;
}

// small stacked "RAM stick" trio -- a colorful desk/shelf accent
function drawRamSticks(buf, x0, bottomY) {
  const colors = [c.iconAzure, c.iconSpark, c.tealNode];
  colors.forEach((col, i) => {
    const y0 = bottomY - 9 - i;
    buf.rect(x0, y0, x0 + 9, bottomY - i * 3, [40, 40, 50]);
    buf.hline(x0, x0 + 9, y0, col);
  });
}

// tiny coiled cable prop
function drawCableCoil(buf, cx, cy) {
  buf.ellipseOutline(cx, cy, 4, 3, [60, 60, 68]);
  buf.ellipseOutline(cx, cy, 2, 2, [40, 40, 48]);
}

// small NAS/router box with its own status light
function drawMiniNas(buf, x0, bottomY, frameIndex) {
  buf.rect(x0, bottomY - 8, x0 + 10, bottomY, c.metalDark);
  buf.hline(x0, x0 + 10, bottomY - 8, c.metalDarkHi);
  for (let i = 0; i < 2; i++) buf.hline(x0 + 2, x0 + 6, bottomY - 5 + i * 2, [16, 17, 24]);
  const on = (frameIndex + 2) % 8 < 5;
  buf.set(x0 + 8, bottomY - 6, on ? c.ledGreen : [30, 70, 40]);
}

function drawShelves(buf, frameIndex) {
  const S = layout.SHELF;
  const planks = [S.plank1, S.plank2, S.plank3];
  for (const plankY of planks) {
    buf.rect(S.x0, plankY, S.x1, plankY + 2, c.woodShelf);
    buf.hline(S.x0, S.x1, plankY, c.woodShelfHi);
    buf.hline(S.x0, S.x1, plankY + 3, c.bgPanelLine);
    // faint under-shelf LED strip accent
    const glow = pulse(frameIndex + plankY, 16) > 0.55 ? c.tealNodeLine : [30, 46, 46];
    buf.hline(S.x0 + 2, S.x1 - 2, plankY + 2, glow);
  }

  // row 1 (top): a book, robot figurine, trophy, tiny succulent
  let x = S.x0 + 2;
  buf.rect(x, S.plank1 - 9, x + 5, S.plank1 - 1, c.books[0]);
  buf.hline(x, x + 5, S.plank1 - 9, [255, 255, 255]);
  x += 7;

  buf.blit(ROBOT_FIGURINE, ROBOT_COLORS, x, S.plank1 - 9);
  x += 7;

  buf.blit(TROPHY, TROPHY_COLORS, x, S.plank1 - 9);
  buf.rect(x + 1, S.plank1 - 4, x + 3, S.plank1 - 1, c.trophyBase);
  x += 8;

  buf.rect(x, S.plank1 - 5, x + 5, S.plank1 - 1, c.plantPot);
  buf.rect(x + 1, S.plank1 - 9, x + 2, S.plank1 - 5, c.plantLeaf);
  buf.rect(x + 3, S.plank1 - 10, x + 4, S.plank1 - 5, c.plantLeafHi);

  // row 2 (middle): varied book spines carrying the technology glyphs
  SHELF_BOOK_HEIGHTS.forEach((h, i) => {
    const bx = shelfSpineX(i);
    const color = c.books[(i + 2) % c.books.length];
    buf.rect(bx, S.plank2 - h, bx + 5, S.plank2 - 1, color);
    buf.hline(bx, bx + 5, S.plank2 - h, [255, 255, 255]);
    buf.vline(bx, S.plank2 - h, S.plank2 - 1, [0, 0, 0]);
  });

  // row 3 (bottom): hardware clutter -- coiled cable, RAM sticks, mini NAS
  drawCableCoil(buf, S.x0 + 8, S.plank3 - 5);
  drawRamSticks(buf, S.x0 + 18, S.plank3 - 1);
  drawMiniNas(buf, S.x0 + 34, S.plank3 - 1, frameIndex);
}

function drawShelfDiagramScreen(buf, frameIndex) {
  /** A neural-network mini-display: three layers of nodes, fully wired --
   * a different visual language from the LangGraph screen so the two
   * don't read as duplicates of each other. */
  const S = layout.SHELF;
  const tx0 = S.x0 + 26, ty0 = S.plank1 - 22;
  const tx1 = tx0 + 16, ty1 = ty0 + 22;
  buf.rect(tx0, ty0, tx1, ty1, c.metalDark);
  buf.rect(tx0 + 1, ty0 + 1, tx1 - 1, ty1 - 5, [12, 16, 28]);

  const glow = pulse(frameIndex, 14);
  const litColor = (base) => base.map((v) => Math.floor(v * (0.5 + glow * 0.5)));
  const layer1 = [ty0 + 4, ty0 + 9, ty0 + 14];
  const layer2 = [ty0 + 6, ty0 + 12];
  const x1 = tx0 + 3, x2 = tx0 + 8, x3 = tx0 + 13;
  for (const y1 of layer1) {
    for (const y2 of layer2) buf.line(x1, y1, x2, y2, c.diagramFrame);
  }
  for (const y2 of layer2) buf.line(x2, y2, x3, ty0 + 9, c.diagramFrame);
  for (const y of layer1) buf.set(x1, y, litColor(c.tealNode));
  for (const y of layer2) buf.set(x2, y, litColor(c.purpleAccent));
  buf.set(x3, ty0 + 9, litColor(c.ledYellow));
  buf.hline(tx0 + 2, tx1 - 2, ty1 - 3, [60, 60, 68]);
}

function drawTechnologyGlyphs(buf) {
  const ax = shelfSpineX(0), ay = layout.SHELF.plank2 - 3;
  buf.rect(ax, ay, ax + 1, ay + 1, c.iconPyBlue);
  buf.rect(ax + 1, ay + 1, ax + 2, ay + 2, c.iconPyYellow);

  const azX = shelfSpineX(1), azY = layout.SHELF.plank2 - 4;
  buf.set(azX + 1, azY, c.iconAzure);
  buf.set(azX + 2, azY, c.iconAzure);
  buf.set(azX + 2, azY - 1, c.iconAzure);
  buf.set(azX + 3, azY - 1, c.iconAzure);

  const spX = shelfSpineX(3), spY = layout.SHELF.plank2 - 4;
  buf.set(spX + 3, spY - 2, c.iconSpark);
  buf.set(spX + 2, spY - 1, c.iconSpark);
  buf.set(spX + 3, spY, c.iconSpark);
  buf.set(spX + 2, spY + 1, c.iconSpark);

  const fbX = shelfSpineX(4), fbY = layout.SHELF.plank2 - 5;
  buf.set(fbX + 1, fbY, c.iconFabric);
  buf.set(fbX + 3, fbY, c.iconFabric);
  buf.set(fbX + 2, fbY + 1, c.iconFabric);
  buf.set(fbX + 1, fbY + 2, c.iconFabric);
  buf.set(fbX + 3, fbY + 2, c.iconFabric);
}

function drawConduit(buf, frameIndex) {
  /** A vertical cable conduit running down the wall between the window
   * zone and the identity poster, so that gap isn't bare wall. */
  const K = layout.CONDUIT;
  buf.rect(K.x0, K.y0, K.x1, K.y1, c.metalCase);
  buf.vline(K.x0, K.y0, K.y1, c.metalDarkHi);
  for (let y = K.y0 + 4; y < K.y1 - 4; y += 10) {
    const on = (frameIndex + y) % 12 < 7;
    const col = layout.LED_COLORS[Math.floor(y / 10) % layout.LED_COLORS.length];
    buf.set(K.x0 + 3, y, on ? col : col.map((v) => Math.floor(v / 3)));
  }
}

function drawTrailingVine(buf) {
  /** A trailing plant hanging off the shelf edge -- curved drooping
   * leaves instead of another upright potted silhouette. */
  const S = layout.SHELF;
  const x0 = S.x0 + 4, y0 = S.plank1;
  buf.rect(x0 - 2, y0 - 4, x0 + 6, y0, c.plantPot);
  buf.hline(x0 - 2, x0 + 6, y0 - 4, c.plantPot);
  const vines = [
    [x0, y0, x0 - 3, y0 + 10, x0 - 1, y0 + 18],
    [x0 + 2, y0, x0 + 5, y0 + 8, x0 + 3, y0 + 16],
    [x0 + 4, y0, x0 + 7, y0 + 12, x0 + 5, y0 + 20],
  ];
  for (const [ax, ay, bx, by, cx2, cy2] of vines) {
    buf.line(ax, ay, bx, by, c.plantLeaf);
    buf.line(bx, by, cx2, cy2, c.plantLeafHi);
    buf.set(cx2, cy2, c.plantLeafHi);
  }
}

function drawHangingMobile(buf, frameIndex) {
  /** A small mobile of two connected nodes dangling from the ceiling --
   * a whimsical depth layer between the poster and the shelf zone. */
  const M = layout.HANGING;
  const sway = Math.round(Math.sin(frameIndex / layout.NUM_FRAMES * Math.PI * 2) * 2);
  const x0 = M.x0 + sway;
  buf.vline(x0, M.ceilingY, M.nodeY, [40, 40, 50]);
  const x1 = x0 + 10, y1 = M.nodeY + 6;
  buf.line(x0, M.nodeY, x1, y1, [40, 40, 50]);
  buf.rect(x0 - 2, M.nodeY - 2, x0 + 2, M.nodeY + 2, c.tealNode);
  buf.rect(x1 - 2, y1 - 2, x1 + 2, y1 + 2, c.purpleAccent);
}

function drawWallClock(buf, frameIndex) {
  const K = layout.CLOCK;
  buf.ellipse(K.cx, K.cy, K.r, K.r, c.frameWood);
  buf.ellipse(K.cx, K.cy, K.r - 2, K.r - 2, c.diagramBg);
  const angle = (frameIndex / layout.NUM_FRAMES) * Math.PI * 2;
  buf.line(K.cx, K.cy, K.cx + Math.round(Math.cos(angle) * (K.r - 4)), K.cy + Math.round(Math.sin(angle) * (K.r - 4)), c.tealNode);
  buf.line(K.cx, K.cy, K.cx + Math.round(Math.cos(angle * 0.3) * (K.r - 6)), K.cy + Math.round(Math.sin(angle * 0.3) * (K.r - 6)), c.posterText);
  buf.set(K.cx, K.cy, c.ledYellow);
}

function drawServerRack(buf, frameIndex) {
  const R = layout.RACK;
  buf.rect(R.x0, R.y0, R.x1, R.y1, c.metalCase);
  buf.hline(R.x0, R.x1, R.y0, c.metalDarkHi);
  buf.rect(R.x0, R.y1 - 4, R.x1, R.y1, c.metalLegShadow);

  const unitTop = R.y0 + 3, unitBottom = R.y1 - 8, nUnits = 4;
  const unitH = Math.floor((unitBottom - unitTop - (nUnits - 1)) / nUnits);

  for (let u = 0; u < nUnits; u++) {
    const uy0 = unitTop + u * (unitH + 1), uy1 = uy0 + unitH;
    buf.rect(R.x0 + 2, uy0, R.x1 - 2, uy1, c.metalDark);
    for (let vx = R.x0 + 4; vx < R.x0 + 22; vx += 3) {
      buf.set(vx, uy0 + Math.floor(unitH / 2), [16, 17, 24]);
    }
    for (let i = 0; i < 3; i++) {
      const lx = R.x1 - 15 + i * 4;
      const on = (Math.floor(frameIndex / 2) + u * 2 + i) % 5 < 3;
      const base = layout.LED_COLORS[(u + i) % layout.LED_COLORS.length];
      const color = on ? base : base.map((v) => Math.floor(v / 3));
      buf.set(lx, uy0 + Math.floor(unitH / 2), color);
    }
  }

  const barX0 = R.x0 + 4;
  const barW = Math.floor(10 + 9 * pulse(frameIndex, 10, 0, 1));
  buf.hline(barX0, barX0 + 20, unitTop - 2, [16, 17, 24]);
  buf.hline(barX0, barX0 + barW, unitTop - 2, layout.LED_COLORS[1]);

  const dx = R.x0 + 6, dy = R.y1 - 20;
  buf.rect(dx, dy + 2, dx + 8, dy + 4, c.iconDocker);
  for (let i = 0; i < 3; i++) buf.rect(dx + 1 + i * 2, dy, dx + 2 + i * 2, dy + 1, c.iconDocker);

  // tiny asset-tag sticker, a believable server-room detail -- sits in
  // the clear gap between the vent dashes and the LED column
  const qx = R.x0 + 26, qy = unitTop + 2;
  buf.rect(qx, qy, qx + 6, qy + 6, [220, 220, 220]);
  for (let i = 0; i < 3; i++) {
    for (let j = 0; j < 3; j++) {
      if ((i + j) % 2 === 0) buf.rect(qx + 1 + i * 2, qy + 1 + j * 2, qx + 2 + i * 2, qy + 2 + j * 2, [20, 20, 20]);
    }
  }

  const swY0 = R.y1 - 6;
  buf.rect(R.x0 - 6, swY0, R.x0 + 20, R.y1 - 1, c.metalCase);
  for (let i = 0; i < 5; i++) {
    const on = (frameIndex + i * 2) % 8 < 5;
    const base = layout.LED_COLORS[i % layout.LED_COLORS.length];
    buf.set(R.x0 - 4 + i * 4, swY0 + 2, on ? base : base.map((v) => Math.floor(v / 3)));
  }

  buf.line(R.x1, R.y1 - 3, R.x1 + 8, R.y1 - 3, [16, 16, 22]);
  buf.line(R.x1 + 8, R.y1 - 3, layout.DESK.x0 + 2, layout.DESK.surfaceY + 6, [16, 16, 22]);
  buf.line(R.x1, R.y1 - 7, R.x1 + 12, R.y1 - 7, [16, 16, 22]);
  buf.line(R.x1 + 12, R.y1 - 7, layout.DESK.x0 + 2, layout.DESK.surfaceY + 10, [16, 16, 22]);
}

function drawDesk(buf, part) {
  const D = layout.DESK;
  if (part === "top") {
    buf.rect(D.x0, D.surfaceY - 4, D.x1, D.surfaceY - 1, c.woodDeskTop);
    buf.hline(D.x0, D.x1, D.surfaceY - 4, c.woodDeskTopHi);
    return;
  }

  buf.rect(D.x0, D.surfaceY, D.x0 + 7, D.frontBottom, c.metalLeg);
  buf.rect(D.x1 - 7, D.surfaceY, D.x1, D.frontBottom, c.metalLeg);
  buf.rect(D.x0, D.frontBottom - 2, D.x0 + 7, D.frontBottom, c.metalLegShadow);
  buf.rect(D.x1 - 7, D.frontBottom - 2, D.x1, D.frontBottom, c.metalLegShadow);

  buf.rect(D.x0 + 52, D.surfaceY, D.x1 - 52, D.frontBottom, c.woodDeskFront);
  buf.hline(D.x0 + 52, D.x1 - 52, D.surfaceY, c.woodDeskFrontShadow);
  for (let lx = D.x0 + 64; lx < D.x1 - 52; lx += 24) {
    buf.vline(lx, D.surfaceY + 4, D.frontBottom - 4, c.woodDeskFrontLine);
  }
  // subtle dither shading so the open panel doesn't read as one flat
  // brown block, plus a soft cast-shadow pool under where the character
  // and keyboard sit
  buf.ditherRect(D.x0 + 56, D.surfaceY + 6, D.x0 + 96, D.frontBottom - 6, c.woodDeskFront, c.woodDeskFrontShadow, 5);
  buf.ditherRect(D.x1 - 96, D.surfaceY + 6, D.x1 - 56, D.frontBottom - 6, c.woodDeskFront, c.woodDeskFrontShadow, 5);
  buf.ellipse(Math.floor((D.x0 + D.x1) / 2), D.surfaceY + 3, 30, 4, c.woodDeskFrontShadow);

  // two gently curved cables draped over the front edge -- an organic,
  // non-rectangular silhouette breaking up the panel
  for (const cableX of [D.x0 + 100, D.x1 - 132]) {
    let px0 = cableX, py0 = D.surfaceY;
    const pts = [[cableX, D.surfaceY], [cableX + 3, D.surfaceY + 10], [cableX - 1, D.surfaceY + 20], [cableX + 2, D.surfaceY + 30]];
    for (const [px, py] of pts) {
      buf.line(px0, py0, px, py, c.metalDrawerSeam);
      px0 = px; py0 = py;
    }
  }

  for (const [dx0, dx1] of [[D.x0 + 9, D.x0 + 50], [D.x1 - 50, D.x1 - 9]]) {
    for (const [dy0, dy1] of [[D.surfaceY + 2, D.surfaceY + 16], [D.surfaceY + 18, D.surfaceY + 32]]) {
      buf.rect(dx0, dy0, dx1, dy1, c.metalDrawer);
      buf.hline(dx0, dx1, dy0, c.metalDrawerHi);
      buf.vline(dx0, dy0, dy1, c.metalDrawerSeam);
      buf.vline(dx1, dy0, dy1, c.metalDrawerSeam);
      const hx = Math.floor((dx0 + dx1) / 2), hy = Math.floor((dy0 + dy1) / 2);
      buf.hline(hx - 4, hx + 4, hy, c.metalHandle);
    }
  }
}

module.exports = {
  drawBackground,
  drawWindow,
  drawIdentityPoster,
  drawArchitecturePoster,
  drawShelves,
  drawShelfDiagramScreen,
  drawTechnologyGlyphs,
  drawServerRack,
  drawDesk,
  drawConduit,
  drawHangingMobile,
  drawWallClock,
  drawTrailingVine,
  shelfSpineX,
};
