"use strict";
/**
 * Single source of truth for every zone's coordinates, shared by all
 * drawing modules. Canvas is a wide, asymmetric panorama: server rack +
 * window on the left, a two-monitor workstation with the developer
 * left-of-center, and a dense three-row shelf zone on the right -- no
 * mirrored window+character+shelf layout, no empty wall.
 */

const W = 300;
const H = 150;
const SCALE = 4;
const NUM_FRAMES = 30;
const FRAME_DELAY_MS = 130;

const WALL_FLOOR_Y = 110;

const WIN = { x0: 14, y0: 8, x1: 66, y1: 44 };

// narrow cable conduit running down the wall, filling the gap between the
// window/rack zone and the identity poster
const CONDUIT = { x0: 72, x1: 80, y0: 10, y1: 106 };

const POSTER = { x0: 88, y0: 6, x1: 196, y1: 28 };
const HANGING = { x0: 200, ceilingY: 6, nodeY: 26 };
const CLOCK = { cx: 228, cy: 40, r: 9 };
const DIAGRAM = { x0: 242, y0: 6, x1: 294, y1: 28 };

const RACK = { x0: 8, y0: 46, x1: 66, y1: 122 };

const SHELF = { x0: 240, x1: 296, plank1: 38, plank2: 62, plank3: 86 };

const DESK = { x0: 76, x1: 296, surfaceY: 104, frontBottom: 140 };

const MONITOR_CX = 158;
const MONITOR = { x0: 118, x1: 198, bezelY0: 34, bezelY1: 94 };
MONITOR.screenX0 = MONITOR.x0 + 3;
MONITOR.screenX1 = MONITOR.x1 - 3;
MONITOR.screenY0 = MONITOR.bezelY0 + 3;
MONITOR.screenY1 = MONITOR.bezelY1 - 3;

const MONITOR2 = { x0: 204, x1: 232, bezelY0: 60, bezelY1: 90 };
MONITOR2.screenX0 = MONITOR2.x0 + 2;
MONITOR2.screenX1 = MONITOR2.x1 - 2;
MONITOR2.screenY0 = MONITOR2.bezelY0 + 2;
MONITOR2.screenY1 = MONITOR2.bezelY1 - 2;

const KEYBOARD = { x0: MONITOR_CX - 13, x1: MONITOR_CX + 13, y0: 100, y1: 104 };
const MOUSE = { x0: KEYBOARD.x1 + 6, y0: 99 };

const CHAR = { cx: MONITOR_CX, headTopY: 57 };

const DESK_ITEMS = {
  plant: { x0: 80, y0: 86 },
  penCup: { x0: 92, y0: 90 },
  notebook: { x0: 102, y0: 95 },
  lamp: { x0: 236, y0: 100 },
  mug: { x0: 248, y0: 91 },
  devBoard: { x0: 258, y0: 95 },
  vectorDb: { x0: 268, y0: 86 },
  ramSticks: { x0: 282, y0: 90 },
};

const LED_COLORS = [
  [228, 78, 78], [88, 218, 128], [88, 158, 228], [228, 198, 88],
];

module.exports = {
  W, H, SCALE, NUM_FRAMES, FRAME_DELAY_MS,
  WALL_FLOOR_Y, WIN, CONDUIT, POSTER, HANGING, CLOCK, DIAGRAM, RACK, SHELF, DESK,
  MONITOR_CX, MONITOR, MONITOR2, KEYBOARD, MOUSE, CHAR, DESK_ITEMS, LED_COLORS,
};
