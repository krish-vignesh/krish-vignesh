"""
Generates assets/ai-engineer.gif: "AI Engineer Command Center" -- an
original pixel-art nighttime workspace rendered at low resolution and
upscaled with nearest-neighbor sampling for authentic blocky pixel-art
edges. Three asymmetric zones share one continuous desk/floor: a server
rack on the left, the developer at a hero RAG-pipeline monitor in the
center, and a books-and-devices shelf on the right.

Run from the repository root:
    python assets/create_animation.py
"""

import math
import os
from PIL import Image, ImageDraw

# ---------------------------------------------------------------------------
# Canvas / output constants
# ---------------------------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GIF_PATH = os.path.join(SCRIPT_DIR, "ai-engineer.gif")
PREVIEW_PATH = os.path.join(SCRIPT_DIR, "preview.png")

LOW_W, LOW_H = 240, 135          # low-res pixel-art canvas
SCALE = 4                        # nearest-neighbor upscale factor
FINAL_W, FINAL_H = LOW_W * SCALE, LOW_H * SCALE

NUM_FRAMES = 28
FRAME_DURATION_MS = 140

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------

WALL_BG = (21, 23, 48)
WALL_BG_SHADOW = (16, 17, 38)
WALL_PANEL_LINE = (17, 19, 40)
WALL_MOONLIGHT = (36, 38, 70)
FLOOR = (30, 20, 30)
FLOOR_PLANK = (36, 24, 34)
BASEBOARD = (48, 40, 54)
BASEBOARD_HI = (62, 52, 66)
RUG_COLOR = (54, 36, 56)
RUG_BORDER = (74, 50, 76)
RUG_PATTERN = (46, 30, 48)

WINDOW_FRAME = (94, 82, 68)
WINDOW_FRAME_HI = (124, 108, 88)
SKY = (14, 14, 40)
SKY_LOW = (24, 21, 56)
STAR_BRIGHT = (232, 232, 202)
STAR_DIM = (138, 138, 120)
MOON = (230, 220, 180)
MOON_SHADOW = (200, 188, 150)
CLOUD = (44, 42, 82)
SKYLINE = (11, 10, 28)
CITY_WINDOW_ON = (234, 200, 120)
CITY_WINDOW_OFF = (40, 36, 58)

POSTER_FRAME = (146, 124, 84)
POSTER_BG = (20, 18, 40)
POSTER_TEXT = (232, 234, 226)
POSTER_ACCENT = (120, 230, 190)

DIAGRAM_FRAME = (90, 96, 110)
DIAGRAM_BG = (16, 18, 30)
DIAGRAM_NODE = (110, 170, 210)
DIAGRAM_LINE = (60, 90, 110)

SHELF_WOOD = (104, 70, 46)
SHELF_WOOD_HI = (130, 92, 62)
BOOK_COLORS = [
    (196, 90, 90), (90, 156, 200), (222, 182, 92),
    (120, 188, 140), (168, 120, 198), (92, 198, 188),
]
TROPHY_CUP = (210, 190, 110)
TROPHY_BASE = (150, 110, 70)

DESK_TOP = (118, 78, 48)
DESK_TOP_HI = (142, 98, 62)
DESK_FRONT = (84, 54, 32)
DESK_FRONT_SHADOW = (64, 40, 24)
DESK_FRONT_LINE = (96, 62, 38)
DESK_LEG = (58, 36, 22)
DESK_LEG_SHADOW = (42, 24, 14)
DRAWER_FRONT = (76, 48, 28)
DRAWER_FRONT_HI = (96, 62, 38)
DRAWER_SEAM = (56, 34, 20)
DRAWER_HANDLE = (204, 182, 130)
SHADOW_ON_DESK = (70, 44, 26)
SHADOW_ON_FLOOR = (22, 15, 22)

MONITOR_BEZEL = (24, 24, 30)
MONITOR_BEZEL_HI = (40, 40, 48)
MONITOR_STAND = (32, 32, 38)
MONITOR_LED = (100, 235, 150)
SCREEN_BG = (6, 11, 18)
SCREEN_GRID = (14, 22, 30)
NODE_SOURCE = (90, 170, 230)
NODE_RETRIEVE = (120, 220, 190)
NODE_RANK = (230, 200, 100)
NODE_GENERATE = (200, 130, 220)
PIPE_LINE = (50, 70, 80)
PIPE_PARTICLE = (150, 240, 210)
GRAPH_LINE = (110, 230, 190)
CURSOR_COLOR = (130, 245, 180)
GLOW_TEAL = (32, 56, 62)
GLOW_TEAL_SOFT = (24, 38, 46)

CHAIR = (26, 26, 36)
CHAIR_HI = (42, 42, 54)

HAIR = (38, 27, 24)
HAIR_HI = (58, 42, 36)
HAIR_DARK = (26, 18, 16)
SKIN = (214, 168, 138)
HOODIE = (54, 86, 126)
HOODIE_SHADOW = (36, 60, 92)
HOODIE_HI = (76, 114, 154)
HEADPHONE = (30, 30, 36)
HEADPHONE_HI = (52, 52, 60)

MUG_BODY = (198, 82, 70)
MUG_HI = (222, 112, 98)
STEAM = (205, 205, 214)

KEY_DARK = (18, 18, 24)
KEY_LIGHT = (58, 58, 68)
MOUSE_BODY = (26, 26, 34)
MOUSE_HI = (46, 46, 56)

PLANT_POT = (114, 66, 46)
PLANT_LEAF = (68, 148, 90)
PLANT_LEAF_HI = (94, 178, 114)

PEN_CUP_BODY = (62, 62, 74)
PEN_CUP_HI = (84, 84, 98)
PEN_COLORS = [(220, 90, 90), (90, 180, 220), (230, 200, 90)]

NOTEBOOK_COVER = (176, 60, 64)
NOTEBOOK_PAGE = (222, 214, 190)
NOTEBOOK_LINE = (150, 142, 120)
NOTEBOOK_SPIRAL = (170, 170, 178)

LAMP_BODY = (46, 46, 54)
LAMP_HI = (66, 66, 76)
LAMP_BULB = (255, 214, 140)
LAMP_GLOW = (86, 66, 40)
LAMP_GLOW_SOFT = (58, 46, 32)

TABLET_BODY = (30, 30, 38)
TABLET_SCREEN = (14, 30, 40)
NODE_COLOR = (120, 220, 190)
NODE_LINE = (60, 120, 110)

RACK_BODY = (30, 32, 40)
RACK_BODY_HI = (46, 48, 58)
RACK_UNIT = (20, 22, 30)
RACK_VENT = (14, 15, 22)
LED_COLORS = [(230, 80, 80), (90, 220, 130), (90, 160, 230), (230, 200, 90)]
CABLE_COLOR = (16, 16, 22)
SWITCH_BODY = (26, 28, 36)

VDB_COLOR = (120, 170, 220)
VDB_HI = (160, 200, 235)
DEVBOARD_BODY = (30, 62, 42)
DEVBOARD_CHIP = (18, 18, 22)

ICON_PY_BLUE = (70, 130, 200)
ICON_PY_YELLOW = (220, 200, 90)
ICON_DOCKER = (80, 170, 220)
ICON_AZURE = (90, 160, 230)
ICON_SPARK = (230, 140, 70)
ICON_FABRIC = (200, 120, 200)

# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

WALL_FLOOR_Y = 96

WINDOW_X0, WINDOW_Y0, WINDOW_X1, WINDOW_Y1 = 12, 8, 62, 44

POSTER_X0, POSTER_Y0, POSTER_X1, POSTER_Y1 = 66, 6, 166, 27

DIAGRAM_X0, DIAGRAM_Y0, DIAGRAM_X1, DIAGRAM_Y1 = 198, 8, 234, 30

RACK_X0, RACK_Y0, RACK_X1, RACK_Y1 = 10, 44, 56, 108

SHELF_X0, SHELF_X1 = 196, 236
SHELF_PLANK_1_Y = 40
SHELF_PLANK_2_Y = 68

DESK_SURFACE_Y = 90
DESK_FRONT_BOTTOM = 124
DESK_X0, DESK_X1 = 64, 236

MONITOR_CX = 142
MONITOR_X0, MONITOR_X1 = 104, 180
MONITOR_BEZEL_Y0, MONITOR_BEZEL_Y1 = 28, 82
SCREEN_X0, SCREEN_X1 = MONITOR_X0 + 3, MONITOR_X1 - 3
SCREEN_Y0, SCREEN_Y1 = MONITOR_BEZEL_Y0 + 3, MONITOR_BEZEL_Y1 - 3

KEYBOARD_X0, KEYBOARD_X1 = 130, 154
KEYBOARD_Y0, KEYBOARD_Y1 = 86, 90

CHAR_HEAD_X0, CHAR_HEAD_X1 = 130, 154
CHAR_HEAD_Y0, CHAR_HEAD_Y1 = 50, 68
CHAR_NECK_Y1 = 71
CHAR_TORSO_X0, CHAR_TORSO_X1 = 120, 164
CHAR_TORSO_Y0, CHAR_TORSO_Y1 = 71, 84
CHAR_ARM_Y1 = KEYBOARD_Y1

MOUSE_X0, MOUSE_Y0 = 158, 85

PLANT_X0, PLANT_Y0 = 76, 76
PENCUP_X0, PENCUP_Y0 = 94, 80
NOTEBOOK_X0, NOTEBOOK_Y0 = 104, 84
LAMP_BASE_X0, LAMP_BASE_Y0 = 168, 88
MUG_X0, MUG_Y0 = 182, 79
DEVBOARD_X0, DEVBOARD_Y0 = 196, 84
VDB_X0, VDB_Y0 = 214, 76

# ---------------------------------------------------------------------------
# A hand-authored 3x5 pixel bitmap font -- system TrueType fonts break up
# into illegible fragments at these pixel heights, so glyphs are drawn
# from fixed bit patterns to keep the sign genuinely "pixel art".
# ---------------------------------------------------------------------------

PIXEL_FONT_3X5 = {
    "A": ["010", "101", "111", "101", "101"],
    "C": ["011", "100", "100", "100", "011"],
    "D": ["110", "101", "101", "101", "110"],
    "E": ["111", "100", "110", "100", "111"],
    "F": ["111", "100", "110", "100", "100"],
    "G": ["011", "100", "101", "101", "011"],
    "H": ["101", "101", "111", "101", "101"],
    "I": ["111", "010", "010", "010", "111"],
    "K": ["101", "101", "110", "101", "101"],
    "L": ["100", "100", "100", "100", "111"],
    "M": ["101", "111", "111", "101", "101"],
    "N": ["101", "111", "111", "111", "101"],
    "O": ["010", "101", "101", "101", "010"],
    "P": ["110", "101", "110", "100", "100"],
    "R": ["110", "101", "110", "101", "101"],
    "S": ["011", "100", "010", "001", "110"],
    "T": ["111", "010", "010", "010", "010"],
    "U": ["101", "101", "101", "101", "111"],
    "V": ["101", "101", "101", "101", "010"],
    "Y": ["101", "101", "010", "010", "010"],
    " ": ["000", "000", "000", "000", "000"],
    "/": ["001", "001", "010", "100", "100"],
    ".": ["000", "000", "000", "000", "010"],
    ">": ["100", "010", "001", "010", "100"],
}


# ---------------------------------------------------------------------------
# Low-level pixel helpers
# ---------------------------------------------------------------------------

def rect(img, x0, y0, x1, y1, color):
    ImageDraw.Draw(img).rectangle([x0, y0, x1, y1], fill=color)


def px(img, x, y, color):
    img.putpixel((x, y), color)


def measure_pixel_text(text, scale=1, spacing=1):
    n = len(text)
    if n == 0:
        return 0
    return n * 3 * scale + (n - 1) * spacing * scale


def draw_pixel_text(img, x, y, text, color, scale=1, spacing=1, center=False):
    width = measure_pixel_text(text, scale, spacing)
    if center:
        x = x - width // 2
    cx = x
    for ch in text.upper():
        glyph = PIXEL_FONT_3X5.get(ch, PIXEL_FONT_3X5[" "])
        for ry, row in enumerate(glyph):
            for rx, bit in enumerate(row):
                if bit == "1":
                    gx, gy = cx + rx * scale, y + ry * scale
                    if scale == 1:
                        px(img, gx, gy, color)
                    else:
                        rect(img, gx, gy, gx + scale - 1, gy + scale - 1, color)
        cx += 3 * scale + spacing * scale
    return width


def pulse(frame_idx, period, lo=0.3, hi=1.0):
    t = (frame_idx % period) / period
    return lo + (hi - lo) * (0.5 + 0.5 * math.sin(t * 2 * math.pi))


def dither_rect(img, x0, y0, x1, y1, base_color, glow_color, density=2):
    """Fill a rect with an ordered pixel-dither mix of two colors -- the
    pixel-art way to fake a soft glow/gradient without smooth blending."""
    for yy in range(y0, y1 + 1):
        for xx in range(x0, x1 + 1):
            if (xx + yy * 2) % density == 0:
                px(img, xx, yy, glow_color)
            else:
                px(img, xx, yy, base_color)


def stipple(img, x0, y0, x1, y1, color, density=3, phase=0):
    """Overlay a sparse pixel pattern onto whatever is already drawn --
    used for glow/light bleed so it doesn't erase the texture beneath it."""
    for yy in range(y0, y1 + 1):
        for xx in range(x0, x1 + 1):
            if not (0 <= xx < LOW_W and 0 <= yy < LOW_H):
                continue
            if (xx + yy + phase) % density == 0:
                px(img, xx, yy, color)


def dither_ring(img, cx, cy, r_inner, r_outer, glow_color):
    """A soft dithered halo around a point light (LED, lamp bulb), stippled
    onto whatever is already drawn there."""
    for yy in range(cy - r_outer, cy + r_outer + 1):
        for xx in range(cx - r_outer, cx + r_outer + 1):
            if not (0 <= xx < LOW_W and 0 <= yy < LOW_H):
                continue
            d2 = (xx - cx) ** 2 + (yy - cy) ** 2
            if r_inner * r_inner <= d2 <= r_outer * r_outer and (xx + yy) % 2 == 0:
                px(img, xx, yy, glow_color)


def desk_shadow(img, x0, x1, y):
    rect(img, x0, y, x1, y, SHADOW_ON_DESK)


# ---------------------------------------------------------------------------
# Background layers
# ---------------------------------------------------------------------------

def draw_background(img):
    rect(img, 0, 0, LOW_W - 1, WALL_FLOOR_Y - 1, WALL_BG)
    rect(img, 0, 0, LOW_W - 1, 8, WALL_BG_SHADOW)

    for lx in range(2, LOW_W - 2, 38):
        ImageDraw.Draw(img).line([(lx, 9), (lx, WALL_FLOOR_Y - 1)], fill=WALL_PANEL_LINE)

    # moonlight spilling across the wall to the right of the window
    dither_rect(img, 62, 12, 108, 50, WALL_BG, WALL_MOONLIGHT, density=5)

    rect(img, 0, WALL_FLOOR_Y - 2, LOW_W - 1, WALL_FLOOR_Y - 2, BASEBOARD_HI)
    rect(img, 0, WALL_FLOOR_Y - 1, LOW_W - 1, WALL_FLOOR_Y + 1, BASEBOARD)

    rect(img, 0, WALL_FLOOR_Y + 2, LOW_W - 1, LOW_H - 1, FLOOR)
    for lx in range(6, LOW_W - 2, 16):
        ImageDraw.Draw(img).line([(lx, WALL_FLOOR_Y + 2), (lx, LOW_H - 1)], fill=FLOOR_PLANK)

    rug_y0, rug_y1 = LOW_H - 10, LOW_H - 1
    rect(img, 62, rug_y0, LOW_W - 8, rug_y1, RUG_COLOR)
    rect(img, 62, rug_y0, LOW_W - 8, rug_y0, RUG_BORDER)
    for rx in range(68, LOW_W - 8, 7):
        px(img, rx, rug_y0 + 3, RUG_PATTERN)
        px(img, rx, rug_y0 + 6, RUG_PATTERN)


CITY_WINDOWS = [(4, 3), (9, 5), (15, 2), (21, 6), (28, 4), (34, 3), (41, 5)]
STARS = [
    (18, 12, 0), (28, 8, 1), (40, 14, 2), (46, 10, 0), (22, 18, 1),
    (36, 20, 2), (16, 16, 0), (32, 16, 1),
]


def draw_window(img, frame_idx):
    rect(img, WINDOW_X0 - 2, WINDOW_Y0 - 2, WINDOW_X1 + 2, WINDOW_Y1 + 2, WINDOW_FRAME)
    rect(img, WINDOW_X0 - 2, WINDOW_Y0 - 2, WINDOW_X1 + 2, WINDOW_Y0 - 1, WINDOW_FRAME_HI)

    low_band = WINDOW_Y0 + int((WINDOW_Y1 - WINDOW_Y0) * 0.55)
    rect(img, WINDOW_X0, WINDOW_Y0, WINDOW_X1, low_band, SKY)
    rect(img, WINDOW_X0, low_band, WINDOW_X1, WINDOW_Y1, SKY_LOW)

    mx, my, mr = WINDOW_X0 + 9, WINDOW_Y0 + 8, 5
    ImageDraw.Draw(img).ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=MOON)
    ImageDraw.Draw(img).ellipse([mx - 1, my - 2, mx + mr, my + mr - 1], fill=MOON_SHADOW)

    for (sx, sy, seed) in STARS:
        wx, wy = WINDOW_X0 + sx, WINDOW_Y0 + sy
        if wx >= WINDOW_X1 or wy >= low_band:
            continue
        on = ((frame_idx + seed * 5) % 18) < 13
        px(img, wx, wy, STAR_BRIGHT if on else STAR_DIM)

    span = (WINDOW_X1 - WINDOW_X0) + 14
    cx = WINDOW_X0 - 10 + int((frame_idx / NUM_FRAMES) * span)
    cy = WINDOW_Y0 + 5
    for dx, dy, w in [(0, 0, 6), (3, -1, 4), (6, 0, 5)]:
        x0, y0 = cx + dx, cy + dy
        x1 = x0 + w
        if x1 > WINDOW_X0 and x0 < WINDOW_X1:
            ImageDraw.Draw(img).rectangle(
                [max(x0, WINDOW_X0), y0, min(x1, WINDOW_X1), y0 + 1], fill=CLOUD
            )

    # distant futuristic city silhouette with tiny lit windows
    heights = [8, 13, 6, 16, 10, 14, 7]
    bw = (WINDOW_X1 - WINDOW_X0) / len(heights)
    for i, h in enumerate(heights):
        x0 = int(WINDOW_X0 + i * bw)
        x1 = int(WINDOW_X0 + (i + 1) * bw) - 1
        rect(img, x0, WINDOW_Y1 - h, x1, WINDOW_Y1, SKYLINE)
    for i, (cwx, cwy) in enumerate(CITY_WINDOWS):
        wx, wy = WINDOW_X0 + cwx, WINDOW_Y1 - cwy
        if wy <= WINDOW_Y0:
            continue
        on = ((frame_idx // 2 + i * 3) % 9) < 6
        px(img, wx, wy, CITY_WINDOW_ON if on else CITY_WINDOW_OFF)

    mid_x = (WINDOW_X0 + WINDOW_X1) // 2
    rect(img, mid_x, WINDOW_Y0, mid_x, WINDOW_Y1, WINDOW_FRAME)
    rect(img, WINDOW_X0, low_band, WINDOW_X1, low_band, WINDOW_FRAME)


def draw_identity_poster(img):
    rect(img, POSTER_X0, POSTER_Y0, POSTER_X1, POSTER_Y1, POSTER_FRAME)
    rect(img, POSTER_X0 + 2, POSTER_Y0 + 2, POSTER_X1 - 2, POSTER_Y1 - 2, POSTER_BG)
    cx = (POSTER_X0 + POSTER_X1) // 2
    draw_pixel_text(img, cx, POSTER_Y0 + 4, "VIGNESH KRISHNA", POSTER_TEXT, center=True)
    draw_pixel_text(img, cx, POSTER_Y0 + 13, "AI / ML / DL ENGINEER", POSTER_ACCENT, center=True)


def draw_architecture_poster(img):
    """A small abstract system-architecture sketch -- deliberately not the
    RAG pipeline (that lives on the hero monitor) so it reads as a second,
    distinct artifact rather than a repeated label."""
    rect(img, DIAGRAM_X0, DIAGRAM_Y0, DIAGRAM_X1, DIAGRAM_Y1, DIAGRAM_FRAME)
    rect(img, DIAGRAM_X0 + 2, DIAGRAM_Y0 + 2, DIAGRAM_X1 - 2, DIAGRAM_Y1 - 2, DIAGRAM_BG)
    nodes = [
        (DIAGRAM_X0 + 7, DIAGRAM_Y0 + 6),
        (DIAGRAM_X0 + 22, DIAGRAM_Y0 + 6),
        (DIAGRAM_X0 + 14, DIAGRAM_Y0 + 15),
        (DIAGRAM_X0 + 29, DIAGRAM_Y0 + 15),
    ]
    edges = [(0, 2), (1, 2), (2, 3)]
    d = ImageDraw.Draw(img)
    for a, b in edges:
        d.line([nodes[a], nodes[b]], fill=DIAGRAM_LINE)
    for nx, ny in nodes:
        rect(img, nx - 1, ny - 1, nx + 1, ny + 1, DIAGRAM_NODE)


# ---------------------------------------------------------------------------
# Left zone: server rack
# ---------------------------------------------------------------------------

def draw_server_rack(img, frame_idx):
    rect(img, RACK_X0, RACK_Y0, RACK_X1, RACK_Y1, RACK_BODY)
    rect(img, RACK_X0, RACK_Y0, RACK_X1, RACK_Y0 + 1, RACK_BODY_HI)
    rect(img, RACK_X0, RACK_Y1 - 4, RACK_X1, RACK_Y1, DESK_LEG_SHADOW)

    unit_top = RACK_Y0 + 3
    unit_bottom = RACK_Y1 - 6
    n_units = 4
    unit_h = (unit_bottom - unit_top - (n_units - 1)) // n_units

    for u in range(n_units):
        uy0 = unit_top + u * (unit_h + 1)
        uy1 = uy0 + unit_h
        rect(img, RACK_X0 + 2, uy0, RACK_X1 - 2, uy1, RACK_UNIT)
        # vent dashes on the left of the unit
        for vx in range(RACK_X0 + 4, RACK_X0 + 20, 3):
            rect(img, vx, uy0 + unit_h // 2, vx + 1, uy0 + unit_h // 2, RACK_VENT)
        # LEDs on the right of the unit, cycling
        for i in range(3):
            lx = RACK_X1 - 14 + i * 4
            on = ((frame_idx // 2 + u * 2 + i) % 5) < 3
            color = LED_COLORS[(u + i) % len(LED_COLORS)]
            px(img, lx, uy0 + unit_h // 2, color if on else tuple(c // 3 for c in color))

    # rack-mounted mini activity bar (data throughput, top unit)
    bar_x0 = RACK_X0 + 4
    bar_w = int(10 + 8 * pulse(frame_idx, 10, lo=0.0, hi=1.0))
    rect(img, bar_x0, unit_top - 2, bar_x0 + 18, unit_top - 2, RACK_VENT)
    rect(img, bar_x0, unit_top - 2, bar_x0 + bar_w, unit_top - 2, MONITOR_LED)

    # Docker sticker decal on the rack door
    dx, dy = RACK_X0 + 6, RACK_Y1 - 16
    rect(img, dx, dy + 2, dx + 8, dy + 4, ICON_DOCKER)
    for i in range(3):
        rect(img, dx + 1 + i * 2, dy, dx + 2 + i * 2, dy + 1, ICON_DOCKER)

    # small network switch beneath the main unit, own LED row
    sw_y0 = RACK_Y1 - 5
    rect(img, RACK_X0 - 6, sw_y0, RACK_X0 + 18, RACK_Y1 - 1, SWITCH_BODY)
    for i in range(5):
        on = ((frame_idx + i * 2) % 8) < 5
        color = LED_COLORS[i % len(LED_COLORS)]
        px(img, RACK_X0 - 4 + i * 4, sw_y0 + 2, color if on else tuple(c // 3 for c in color))

    # cable bundle running from the rack toward the desk
    d = ImageDraw.Draw(img)
    d.line([(RACK_X1, RACK_Y1 - 2), (RACK_X1 + 6, RACK_Y1 - 2), (DESK_X0 + 2, DESK_SURFACE_Y + 4)], fill=CABLE_COLOR)
    d.line([(RACK_X1, RACK_Y1 - 5), (RACK_X1 + 10, RACK_Y1 - 5), (DESK_X0 + 2, DESK_SURFACE_Y + 8)], fill=CABLE_COLOR)


# ---------------------------------------------------------------------------
# Right zone: shelf, books, tech easter eggs
# ---------------------------------------------------------------------------

BOTTOM_SHELF_BOOK_HEIGHTS = [10, 8, 11, 8, 9]


def shelf_bottom_spine_x(index):
    x = SHELF_X0 + 2
    for i, h in enumerate(BOTTOM_SHELF_BOOK_HEIGHTS):
        if i == index:
            return x, h
        x += 6
    return x, 9


def draw_shelves(img):
    for plank_y in (SHELF_PLANK_1_Y, SHELF_PLANK_2_Y):
        rect(img, SHELF_X0, plank_y, SHELF_X1, plank_y + 2, SHELF_WOOD)
        rect(img, SHELF_X0, plank_y, SHELF_X1, plank_y, SHELF_WOOD_HI)
        rect(img, SHELF_X0, plank_y + 3, SHELF_X1, plank_y + 3, WALL_PANEL_LINE)

    # top row: one book, a robot figurine, a trophy, and the LangGraph tablet
    x = SHELF_X0 + 2
    rect(img, x, SHELF_PLANK_1_Y - 9, x + 5, SHELF_PLANK_1_Y - 1, BOOK_COLORS[0])
    rect(img, x, SHELF_PLANK_1_Y - 9, x + 5, SHELF_PLANK_1_Y - 9, (255, 255, 255))
    x += 7

    fig_x = x
    rect(img, fig_x, SHELF_PLANK_1_Y - 7, fig_x + 4, SHELF_PLANK_1_Y - 3, (150, 150, 160))
    rect(img, fig_x + 1, SHELF_PLANK_1_Y - 9, fig_x + 3, SHELF_PLANK_1_Y - 8, (150, 150, 160))
    px(img, fig_x + 1, SHELF_PLANK_1_Y - 6, (90, 220, 170))
    px(img, fig_x + 3, SHELF_PLANK_1_Y - 6, (90, 220, 170))
    x = fig_x + 7

    tro_x = x
    rect(img, tro_x + 1, SHELF_PLANK_1_Y - 3, tro_x + 3, SHELF_PLANK_1_Y - 1, TROPHY_BASE)
    rect(img, tro_x, SHELF_PLANK_1_Y - 8, tro_x + 4, SHELF_PLANK_1_Y - 4, TROPHY_CUP)
    px(img, tro_x, SHELF_PLANK_1_Y - 9, TROPHY_CUP)
    px(img, tro_x + 4, SHELF_PLANK_1_Y - 9, TROPHY_CUP)

    # bottom row: varied book spines, some leaning for a lived-in feel
    for i, h in enumerate(BOTTOM_SHELF_BOOK_HEIGHTS):
        bx, _ = shelf_bottom_spine_x(i)
        color = BOOK_COLORS[(i + 2) % len(BOOK_COLORS)]
        rect(img, bx, SHELF_PLANK_2_Y - h, bx + 5, SHELF_PLANK_2_Y - 1, color)
        rect(img, bx, SHELF_PLANK_2_Y - h, bx + 5, SHELF_PLANK_2_Y - h, (255, 255, 255))
        rect(img, bx, SHELF_PLANK_2_Y - h, bx, SHELF_PLANK_2_Y - 1, (0, 0, 0))


def draw_shelf_tablet(img, frame_idx):
    """LangGraph-style node graph on a small tablet propped on the shelf."""
    tx0, ty0 = SHELF_X0 + 28, SHELF_PLANK_1_Y - 22
    tx1, ty1 = tx0 + 14, ty0 + 22
    rect(img, tx0, ty0, tx1, ty1, TABLET_BODY)
    rect(img, tx0 + 1, ty0 + 1, tx1 - 1, ty1 - 5, TABLET_SCREEN)
    glow = pulse(frame_idx, 12)
    node_color = tuple(int(c * glow) for c in NODE_COLOR)
    nodes = [(tx0 + 4, ty0 + 5), (tx0 + 10, ty0 + 5), (tx0 + 7, ty0 + 11)]
    d = ImageDraw.Draw(img)
    d.line([nodes[0], nodes[1]], fill=NODE_LINE)
    d.line([nodes[0], nodes[2]], fill=NODE_LINE)
    d.line([nodes[1], nodes[2]], fill=NODE_LINE)
    for nx, ny in nodes:
        rect(img, nx - 1, ny - 1, nx + 1, ny + 1, node_color)
    rect(img, tx0 + 2, ty1 - 3, tx1 - 2, ty1 - 3, (60, 60, 68))


def draw_technology_elements(img):
    """Technology as environmental easter eggs only: stickers on the rack
    (drawn separately) and tiny glyphs painted directly onto book spines --
    never a separate icon card floating in space."""
    ax, _ = shelf_bottom_spine_x(0)
    ay = SHELF_PLANK_2_Y - 3
    rect(img, ax, ay, ax + 1, ay + 1, ICON_PY_BLUE)
    rect(img, ax + 1, ay + 1, ax + 2, ay + 2, ICON_PY_YELLOW)

    az_x, _ = shelf_bottom_spine_x(1)
    az_y = SHELF_PLANK_2_Y - 4
    px(img, az_x + 1, az_y, ICON_AZURE)
    px(img, az_x + 2, az_y, ICON_AZURE)
    px(img, az_x + 2, az_y - 1, ICON_AZURE)
    px(img, az_x + 3, az_y - 1, ICON_AZURE)

    sp_x, _ = shelf_bottom_spine_x(3)
    sp_y = SHELF_PLANK_2_Y - 4
    px(img, sp_x + 3, sp_y - 2, ICON_SPARK)
    px(img, sp_x + 2, sp_y - 1, ICON_SPARK)
    px(img, sp_x + 3, sp_y, ICON_SPARK)
    px(img, sp_x + 2, sp_y + 1, ICON_SPARK)

    fb_x, _ = shelf_bottom_spine_x(4)
    fb_y = SHELF_PLANK_2_Y - 5
    px(img, fb_x + 1, fb_y, ICON_FABRIC)
    px(img, fb_x + 3, fb_y, ICON_FABRIC)
    px(img, fb_x + 2, fb_y + 1, ICON_FABRIC)
    px(img, fb_x + 1, fb_y + 2, ICON_FABRIC)
    px(img, fb_x + 3, fb_y + 2, ICON_FABRIC)


def draw_vector_db(img, frame_idx):
    """Vector DB as a small standalone desk device: a stack of disks with
    a blinking activity light, not a labeled card."""
    vx0, vy0 = VDB_X0, VDB_Y0
    desk_shadow(img, vx0 - 1, vx0 + 13, DESK_SURFACE_Y + 1)
    d = ImageDraw.Draw(img)
    for i in range(3):
        yy = vy0 + i * 4
        d.ellipse([vx0, yy, vx0 + 12, yy + 4], fill=VDB_COLOR, outline=VDB_HI)
    rect(img, vx0, vy0 + 2, vx0 + 12, vy0 + DESK_SURFACE_Y - vy0 - 2, VDB_COLOR)
    d.ellipse([vx0, vy0, vx0 + 12, vy0 + 4], fill=VDB_HI)
    on = (frame_idx % 10) < 6
    px(img, vx0 + 6, vy0 + 1, MONITOR_LED if on else (40, 90, 70))


def draw_dev_board(img, frame_idx):
    """A tiny microcontroller/dev-board gadget with one blinking status LED."""
    bx0, by0 = DEVBOARD_X0, DEVBOARD_Y0
    desk_shadow(img, bx0 - 1, bx0 + 11, DESK_SURFACE_Y + 1)
    rect(img, bx0, by0, bx0 + 10, DESK_SURFACE_Y, DEVBOARD_BODY)
    rect(img, bx0 + 2, by0 + 1, bx0 + 5, by0 + 3, DEVBOARD_CHIP)
    for i in range(3):
        px(img, bx0 + 2 + i, by0 + 4, (60, 60, 68))
    on = (frame_idx % 6) < 3
    px(img, bx0 + 8, by0 + 1, LED_COLORS[1] if on else (30, 70, 40))


# ---------------------------------------------------------------------------
# Desk structure
# ---------------------------------------------------------------------------

def draw_desk(img, part):
    if part == "top":
        rect(img, DESK_X0, DESK_SURFACE_Y - 4, DESK_X1, DESK_SURFACE_Y - 1, DESK_TOP)
        rect(img, DESK_X0, DESK_SURFACE_Y - 4, DESK_X1, DESK_SURFACE_Y - 4, DESK_TOP_HI)
        return

    rect(img, DESK_X0, DESK_SURFACE_Y, DESK_X0 + 6, DESK_FRONT_BOTTOM, DESK_LEG)
    rect(img, DESK_X1 - 6, DESK_SURFACE_Y, DESK_X1, DESK_FRONT_BOTTOM, DESK_LEG)
    rect(img, DESK_X0, DESK_FRONT_BOTTOM - 2, DESK_X0 + 6, DESK_FRONT_BOTTOM, DESK_LEG_SHADOW)
    rect(img, DESK_X1 - 6, DESK_FRONT_BOTTOM - 2, DESK_X1, DESK_FRONT_BOTTOM, DESK_LEG_SHADOW)

    rect(img, DESK_X0 + 48, DESK_SURFACE_Y, DESK_X1 - 48, DESK_FRONT_BOTTOM, DESK_FRONT)
    rect(img, DESK_X0 + 48, DESK_SURFACE_Y, DESK_X1 - 48, DESK_SURFACE_Y + 1, DESK_FRONT_SHADOW)
    for lx in range(DESK_X0 + 60, DESK_X1 - 48, 22):
        ImageDraw.Draw(img).line(
            [(lx, DESK_SURFACE_Y + 4), (lx, DESK_FRONT_BOTTOM - 4)], fill=DESK_FRONT_LINE
        )

    for dx0, dx1 in [(DESK_X0 + 8, DESK_X0 + 46), (DESK_X1 - 46, DESK_X1 - 8)]:
        for dy0, dy1 in [(DESK_SURFACE_Y + 2, DESK_SURFACE_Y + 15), (DESK_SURFACE_Y + 17, DESK_SURFACE_Y + 30)]:
            rect(img, dx0, dy0, dx1, dy1, DRAWER_FRONT)
            rect(img, dx0, dy0, dx1, dy0, DRAWER_FRONT_HI)
            rect(img, dx0, dy0, dx0, dy1, DRAWER_SEAM)
            rect(img, dx1, dy0, dx1, dy1, DRAWER_SEAM)
            hx = (dx0 + dx1) // 2
            hy = (dy0 + dy1) // 2
            rect(img, hx - 4, hy, hx + 4, hy, DRAWER_HANDLE)


# ---------------------------------------------------------------------------
# The hero monitor: RAG pipeline visualization
# ---------------------------------------------------------------------------

PIPELINE_STAGES = [
    ("SRC", NODE_SOURCE),
    ("RET", NODE_RETRIEVE),
    ("RNK", NODE_RANK),
    ("GEN", NODE_GENERATE),
]


def draw_monitor(img, frame_idx):
    glow = GLOW_TEAL if pulse(frame_idx, 18) > 0.65 else GLOW_TEAL_SOFT
    stipple(img, MONITOR_X0 - 3, MONITOR_BEZEL_Y0 - 3, MONITOR_X1 + 3, MONITOR_BEZEL_Y1, glow, density=3)

    rect(img, MONITOR_X0, MONITOR_BEZEL_Y0, MONITOR_X1, MONITOR_BEZEL_Y1, MONITOR_BEZEL)
    rect(img, MONITOR_X0, MONITOR_BEZEL_Y0, MONITOR_X1, MONITOR_BEZEL_Y0 + 1, MONITOR_BEZEL_HI)

    # subtle screen flicker: occasional one-frame brightness dip
    flicker = (frame_idx % 17) == 0
    screen_bg = tuple(max(0, c - 3) for c in SCREEN_BG) if flicker else SCREEN_BG
    rect(img, SCREEN_X0, SCREEN_Y0, SCREEN_X1, SCREEN_Y1, screen_bg)

    led_x, led_y = MONITOR_X1 - 3, MONITOR_BEZEL_Y1 - 2
    if (frame_idx % 16) < 13:
        px(img, led_x, led_y, MONITOR_LED)

    neck_x0, neck_x1 = MONITOR_CX - 4, MONITOR_CX + 4
    rect(img, neck_x0, MONITOR_BEZEL_Y1, neck_x1, MONITOR_BEZEL_Y1 + 6, MONITOR_STAND)
    rect(img, MONITOR_CX - 12, MONITOR_BEZEL_Y1 + 6, MONITOR_CX + 12, MONITOR_BEZEL_Y1 + 8, MONITOR_STAND)
    rect(img, MONITOR_CX - 12, MONITOR_BEZEL_Y1 + 6, MONITOR_CX + 12, MONITOR_BEZEL_Y1 + 6, MONITOR_BEZEL_HI)

    # --- RAG pipeline: SOURCE -> RETRIEVE -> RANK -> GENERATE, pinned to
    # the top strip that stays clear above the character's head ----------
    pipe_y = SCREEN_Y0 + 2
    n = len(PIPELINE_STAGES)
    span = (SCREEN_X1 - SCREEN_X0 - 6)
    node_w = 12
    xs = [SCREEN_X0 + 3 + int(i * (span - node_w) / (n - 1)) for i in range(n)]

    for i in range(n - 1):
        x_a = xs[i] + node_w
        x_b = xs[i + 1]
        rect(img, x_a, pipe_y + 2, x_b, pipe_y + 2, PIPE_LINE)

    for (label, color), nx in zip(PIPELINE_STAGES, xs):
        rect(img, nx, pipe_y, nx + node_w, pipe_y + 5, color)
        draw_pixel_text(img, nx + 1, pipe_y + 1, label, SCREEN_BG)

    # data particles flowing left to right across the whole pipeline
    total_span = xs[-1] - xs[0]
    for p in range(2):
        prog = ((frame_idx * 3 + p * (total_span // 2)) % total_span)
        part_x = xs[0] + node_w // 2 + prog
        px(img, part_x, pipe_y + 2, PIPE_PARTICLE)

    # the character's head occupies the middle of the screen below the
    # pipeline, so the graph and status readout live in the clear bands
    # to either side of it instead of stacking underneath
    band_y0 = pipe_y + 9

    # left band: a small live bar chart ("graph updating")
    bar_x0 = SCREEN_X0 + 3
    bar_base = band_y0 + 16
    for i in range(4):
        bh = 3 + ((frame_idx + i * 5) % 13)
        bx = bar_x0 + i * 3
        rect(img, bx, bar_base - bh, bx + 1, bar_base, GRAPH_LINE)
    rect(img, bar_x0 - 1, bar_base + 1, bar_x0 + 11, bar_base + 1, SCREEN_GRID)

    # right band: short cycling status code + blinking cursor
    codes = ["SRCH", "READ", "AGNT", "DONE"]
    code = codes[(frame_idx // 7) % len(codes)]
    status_x = SCREEN_X1 - 3 - measure_pixel_text(code)
    draw_pixel_text(img, status_x, band_y0, code, NODE_RETRIEVE)
    if (frame_idx % 8) < 4:
        rect(img, SCREEN_X1 - 3, band_y0, SCREEN_X1 - 2, band_y0 + 4, CURSOR_COLOR)
    # a tiny confidence bar beneath the status code
    conf_w = 4 + ((frame_idx * 2) % 14)
    rect(img, status_x, band_y0 + 7, status_x + conf_w, band_y0 + 7, NODE_GENERATE)


# ---------------------------------------------------------------------------
# Desk objects
# ---------------------------------------------------------------------------

def draw_desk_objects(img, frame_idx):
    # keyboard + mouse
    desk_shadow(img, KEYBOARD_X0 - 1, KEYBOARD_X1 + 1, KEYBOARD_Y1 + 1)
    rect(img, KEYBOARD_X0, KEYBOARD_Y0, KEYBOARD_X1, KEYBOARD_Y1, KEY_DARK)
    rect(img, KEYBOARD_X0, KEYBOARD_Y0, KEYBOARD_X1, KEYBOARD_Y0, MONITOR_BEZEL_HI)
    for kx in range(KEYBOARD_X0 + 2, KEYBOARD_X1 - 1, 3):
        px(img, kx, KEYBOARD_Y0 + 1, KEY_LIGHT)

    rect(img, MOUSE_X0, MOUSE_Y0, MOUSE_X0 + 4, MOUSE_Y0 + 6, MOUSE_BODY)
    rect(img, MOUSE_X0, MOUSE_Y0, MOUSE_X0 + 4, MOUSE_Y0 + 1, MOUSE_HI)
    px(img, MOUSE_X0 + 2, MOUSE_Y0 + 2, KEY_LIGHT)

    # potted plant
    px0, py0 = PLANT_X0, PLANT_Y0
    desk_shadow(img, px0 - 1, px0 + 9, DESK_SURFACE_Y + 1)
    rect(img, px0, py0 + 8, px0 + 8, DESK_SURFACE_Y, PLANT_POT)
    rect(img, px0, py0 + 8, px0 + 8, py0 + 8, PLANT_POT)
    rect(img, px0 + 1, py0 + 2, px0 + 3, py0 + 8, PLANT_LEAF)
    rect(img, px0 + 3, py0, px0 + 5, py0 + 8, PLANT_LEAF_HI)
    rect(img, px0 + 5, py0 + 3, px0 + 7, py0 + 8, PLANT_LEAF)

    # pen cup
    cx0, cy0 = PENCUP_X0, PENCUP_Y0
    desk_shadow(img, cx0 - 1, cx0 + 7, DESK_SURFACE_Y + 1)
    rect(img, cx0, cy0, cx0 + 6, DESK_SURFACE_Y, PEN_CUP_BODY)
    rect(img, cx0, cy0, cx0 + 6, cy0, PEN_CUP_HI)
    for i, pcolor in enumerate(PEN_COLORS):
        ImageDraw.Draw(img).line(
            [(cx0 + 1 + i * 2, cy0), (cx0 + 1 + i * 2 - 1, cy0 - 7)], fill=pcolor
        )

    # small open notebook
    nx0, ny0 = NOTEBOOK_X0, NOTEBOOK_Y0
    desk_shadow(img, nx0 - 1, nx0 + 13, DESK_SURFACE_Y + 1)
    rect(img, nx0, ny0, nx0 + 12, DESK_SURFACE_Y, NOTEBOOK_PAGE)
    rect(img, nx0, ny0, nx0 + 12, ny0 + 1, NOTEBOOK_COVER)
    for i in range(3):
        rect(img, nx0 + 2, ny0 + 3 + i * 2, nx0 + 9, ny0 + 3 + i * 2, NOTEBOOK_LINE)
    for i in range(4):
        px(img, nx0 + 3 * i, ny0, NOTEBOOK_SPIRAL)

    # desk lamp: warm light source, contrasting the monitor's cyan glow --
    # drawn with a wide weighted base and a thick, light-toned pole/arm so
    # it reads clearly against the dark wall instead of just its glow
    lx0 = LAMP_BASE_X0
    base_y0 = DESK_SURFACE_Y - 4
    desk_shadow(img, lx0 - 1, lx0 + 11, DESK_SURFACE_Y + 1)
    rect(img, lx0, base_y0, lx0 + 10, DESK_SURFACE_Y, LAMP_BODY)
    rect(img, lx0, base_y0, lx0 + 10, base_y0, LAMP_HI)

    pole_x = lx0 + 4
    pole_top = base_y0 - 34
    rect(img, pole_x, pole_top, pole_x + 1, base_y0, LAMP_HI)

    ax, ay = pole_x, pole_top
    for _ in range(7):
        rect(img, ax, ay, ax + 1, ay + 1, LAMP_HI)
        ax += 2
        ay -= 2
    bulb_x, bulb_y = ax + 1, ay + 1

    glow = LAMP_GLOW if pulse(frame_idx, 22) > 0.5 else LAMP_GLOW_SOFT
    dither_ring(img, bulb_x, bulb_y, 2, 7, glow)
    rect(img, bulb_x - 1, bulb_y - 1, bulb_x + 1, bulb_y + 1, LAMP_BULB)

    # coffee mug with rising steam
    mx0, my0 = MUG_X0, MUG_Y0
    desk_shadow(img, mx0 - 1, mx0 + 9, DESK_SURFACE_Y + 1)
    rect(img, mx0, my0, mx0 + 7, DESK_SURFACE_Y, MUG_BODY)
    rect(img, mx0, my0, mx0 + 7, my0 + 1, MUG_HI)
    ImageDraw.Draw(img).arc([mx0 + 6, my0 + 1, mx0 + 11, my0 + 8], -90, 90, fill=MUG_BODY)
    for i in range(2):
        wobble = int(math.sin((frame_idx + i * 4) / 3.0) * 1.5)
        sy = my0 - 2 - ((frame_idx * 2 + i * 6) % 11)
        sx = mx0 + 2 + i * 3 + wobble
        fade = 1.0 - ((frame_idx * 2 + i * 6) % 11) / 11.0
        if fade > 0.15:
            px(img, sx, sy, STEAM)


# ---------------------------------------------------------------------------
# Chair + character
# ---------------------------------------------------------------------------

def draw_chair(img):
    head_top = CHAR_HEAD_Y0 - 3
    rect(img, CHAR_TORSO_X0 - 8, head_top, CHAR_TORSO_X0 - 3, CHAR_TORSO_Y0, CHAIR)
    rect(img, CHAR_TORSO_X1 + 3, head_top, CHAR_TORSO_X1 + 8, CHAR_TORSO_Y0, CHAIR)
    rect(img, CHAR_TORSO_X0 - 9, head_top + 1, CHAR_TORSO_X0 - 8, head_top + 6, CHAIR)
    rect(img, CHAR_TORSO_X1 + 8, head_top + 1, CHAR_TORSO_X1 + 9, head_top + 6, CHAIR)

    rect(img, CHAR_TORSO_X0 - 8, CHAR_TORSO_Y0 - 5, CHAR_TORSO_X1 + 8, CHAR_TORSO_Y0 + 3, CHAIR)
    rect(img, CHAR_TORSO_X0 - 8, CHAR_TORSO_Y0 - 5, CHAR_TORSO_X1 + 8, CHAR_TORSO_Y0 - 4, CHAIR_HI)
    rect(img, CHAR_TORSO_X0 + 16, CHAR_TORSO_Y0 - 4, CHAR_TORSO_X0 + 16, CHAR_TORSO_Y0 + 2, CHAIR_HI)

    arm_y0, arm_y1 = CHAR_TORSO_Y1 - 4, CHAR_TORSO_Y1 + 3
    rect(img, CHAR_TORSO_X0 - 12, arm_y0, CHAR_TORSO_X0 - 7, arm_y1, CHAIR)
    rect(img, CHAR_TORSO_X0 - 12, arm_y0, CHAR_TORSO_X0 - 7, arm_y0, CHAIR_HI)
    rect(img, CHAR_TORSO_X1 + 7, arm_y0, CHAR_TORSO_X1 + 12, arm_y1, CHAIR)
    rect(img, CHAR_TORSO_X1 + 7, arm_y0, CHAR_TORSO_X1 + 12, arm_y0, CHAIR_HI)


HEAD_ROW_INSET = [3, 1, 0]


def draw_character(img, frame_idx):
    """Back view only: the developer faces the monitor, away from the
    viewer, so the head is a solid hair silhouette with no face."""
    bob = 0 if (frame_idx % 10) < 5 else -1

    hx0, hy0, hx1, hy1 = CHAR_HEAD_X0, CHAR_HEAD_Y0 + bob, CHAR_HEAD_X1, CHAR_HEAD_Y1 + bob
    for ry in range(hy0, hy1 + 1):
        inset = HEAD_ROW_INSET[min(ry - hy0, len(HEAD_ROW_INSET) - 1)]
        row_color = HAIR_HI if (ry - hy0) < 2 else HAIR
        rect(img, hx0 + inset, ry, hx1 - inset, ry, row_color)
    rect(img, hx0 + 7, hy0 + 4, hx0 + 7, hy1 - 3, HAIR_DARK)
    rect(img, hx1 - 6, hy0 + 4, hx1 - 6, hy1 - 3, HAIR_DARK)

    # headphones: a flat band across the crown plus rounded ear cups --
    # simple stepped shapes read far more cleanly at this scale than a
    # curved arc would
    rect(img, hx0 + 4, hy0 - 2, hx1 - 4, hy0 - 2, HEADPHONE)
    px(img, hx0 + 2, hy0 - 1, HEADPHONE)
    px(img, hx1 - 2, hy0 - 1, HEADPHONE)
    rect(img, hx0 - 3, hy0 + 3, hx0, hy0 + 10, HEADPHONE)
    rect(img, hx0 - 3, hy0 + 3, hx0 - 2, hy0 + 4, HEADPHONE_HI)
    rect(img, hx1, hy0 + 3, hx1 + 3, hy0 + 10, HEADPHONE)
    rect(img, hx1 + 2, hy0 + 3, hx1 + 3, hy0 + 4, HEADPHONE_HI)

    nx0, nx1 = CHAR_HEAD_X0 + 8, CHAR_HEAD_X1 - 8
    rect(img, nx0, hy1, nx1, CHAR_NECK_Y1 + bob, SKIN)

    ty0, ty1 = CHAR_TORSO_Y0 + bob, CHAR_TORSO_Y1
    rect(img, CHAR_TORSO_X0, ty0, CHAR_TORSO_X1, ty1, HOODIE)
    rect(img, CHAR_TORSO_X0, ty0, CHAR_TORSO_X0 + 5, ty1, HOODIE_SHADOW)
    rect(img, CHAR_TORSO_X1 - 5, ty0, CHAR_TORSO_X1, ty1, HOODIE_HI)
    rect(img, CHAR_TORSO_X0 + 3, ty0, CHAR_TORSO_X1 - 3, ty0 + 2, HOODIE_HI)
    px(img, CHAR_TORSO_X0, ty0, WALL_BG if bob == 0 else HOODIE)
    px(img, CHAR_TORSO_X1, ty0, WALL_BG if bob == 0 else HOODIE)
    rect(img, CHAR_TORSO_X0 + 16, ty0, CHAR_TORSO_X1 - 16, ty0 + 1, HOODIE_SHADOW)
    px(img, CHAR_TORSO_X0 + 20, ty0 + 3, HOODIE_SHADOW)
    px(img, CHAR_TORSO_X1 - 20, ty0 + 3, HOODIE_SHADOW)

    typing_l = 1 if (frame_idx % 4) < 2 else 0
    typing_r = 0 if (frame_idx % 4) < 2 else 1
    arm_top = ty1
    cap_h = 3
    for kx0, kx1, typing in [
        (KEYBOARD_X0, KEYBOARD_X0 + 8, typing_l),
        (KEYBOARD_X1 - 8, KEYBOARD_X1, typing_r),
    ]:
        rect(img, kx0, arm_top, kx1, arm_top + cap_h, HOODIE)
        fx0, fx1 = kx0 + 1, kx1 - 1
        fy1 = CHAR_ARM_Y1 - 1 + typing
        rect(img, fx0, arm_top + cap_h, fx1, fy1, HOODIE_SHADOW)
        rect(img, fx0, fy1 - 2, fx1, fy1 - 2, HOODIE_HI)
        rect(img, fx0, fy1 - 1, fx1, fy1, SKIN)


# ---------------------------------------------------------------------------
# Frame assembly
# ---------------------------------------------------------------------------

def build_low_res_frame(frame_idx):
    img = Image.new("RGB", (LOW_W, LOW_H), WALL_BG)

    draw_background(img)
    draw_window(img, frame_idx)
    draw_identity_poster(img)
    draw_architecture_poster(img)
    draw_server_rack(img, frame_idx)
    draw_shelves(img)
    draw_shelf_tablet(img, frame_idx)
    draw_technology_elements(img)
    draw_desk(img, "top")
    draw_monitor(img, frame_idx)
    draw_desk_objects(img, frame_idx)
    draw_vector_db(img, frame_idx)
    draw_dev_board(img, frame_idx)
    draw_chair(img)
    draw_character(img, frame_idx)
    draw_desk(img, "front")

    return img


def upscale(img):
    return img.resize((FINAL_W, FINAL_H), Image.NEAREST)


def generate_frames():
    return [upscale(build_low_res_frame(i)) for i in range(NUM_FRAMES)]


def main():
    frames = generate_frames()

    sample = Image.new("RGB", (FINAL_W, FINAL_H * 4))
    for i, idx in enumerate([0, NUM_FRAMES // 3, 2 * NUM_FRAMES // 3, NUM_FRAMES - 1]):
        sample.paste(frames[idx], (0, i * FINAL_H))
    palette_img = sample.quantize(colors=96, dither=Image.Dither.NONE)

    frames_p = [f.quantize(palette=palette_img, dither=Image.Dither.NONE) for f in frames]

    frames_p[0].save(
        GIF_PATH,
        save_all=True,
        append_images=frames_p[1:],
        duration=FRAME_DURATION_MS,
        loop=0,
        optimize=True,
        disposal=2,
    )
    print(f"Saved GIF: {GIF_PATH}")

    frames[0].save(PREVIEW_PATH)
    print(f"Saved preview PNG: {PREVIEW_PATH}")


if __name__ == "__main__":
    main()
