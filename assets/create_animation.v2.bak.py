"""
Generates assets/ai-engineer.gif: a pixel-art nighttime AI/ML engineer
workspace scene, rendered at low resolution and upscaled with
nearest-neighbor sampling for authentic blocky pixel-art edges.

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

LOW_W, LOW_H = 200, 120          # low-res pixel-art canvas
SCALE = 4                        # nearest-neighbor upscale factor
FINAL_W, FINAL_H = LOW_W * SCALE, LOW_H * SCALE

NUM_FRAMES = 24
FRAME_DURATION_MS = 150

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------

WALL_BG = (24, 26, 54)
WALL_BG_SHADOW = (19, 20, 44)
FLOOR = (33, 22, 32)
FLOOR_EDGE = (44, 30, 42)

WINDOW_FRAME = (96, 84, 70)
WINDOW_FRAME_HI = (126, 110, 90)
SKY = (16, 15, 42)
SKY_LOW = (26, 22, 58)
STAR_BRIGHT = (235, 235, 205)
STAR_DIM = (140, 140, 122)
MOON = (232, 222, 182)
MOON_SHADOW = (202, 190, 152)
CLOUD = (46, 44, 84)
SKYLINE = (12, 11, 30)

POSTER_FRAME = (150, 128, 88)
POSTER_BG = (22, 20, 42)
POSTER_TEXT = (232, 234, 226)
POSTER_ACCENT = (120, 230, 190)

SHELF_WOOD = (108, 74, 48)
SHELF_WOOD_HI = (134, 96, 64)
BOOK_COLORS = [
    (196, 90, 90),
    (90, 156, 200),
    (222, 182, 92),
    (120, 188, 140),
    (168, 120, 198),
    (92, 198, 188),
]

DESK_TOP = (122, 80, 50)
DESK_TOP_HI = (146, 100, 64)
DESK_FRONT = (88, 56, 34)
DESK_FRONT_SHADOW = (68, 42, 26)
DESK_FRONT_LINE = (100, 64, 40)

MONITOR_BEZEL = (26, 26, 32)
MONITOR_BEZEL_HI = (42, 42, 50)
MONITOR_STAND = (34, 34, 40)
SCREEN_BG = (7, 12, 20)
SCREEN_LINE_1 = (90, 220, 150)
SCREEN_LINE_2 = (90, 170, 230)
SCREEN_LINE_3 = (230, 200, 100)
SCREEN_LINE_4 = (170, 120, 220)
CURSOR_COLOR = (130, 245, 180)
PARTICLE_COLOR = (110, 230, 200)

CHAIR = (28, 28, 38)
CHAIR_HI = (44, 44, 56)

HAIR = (38, 27, 24)
HAIR_HI = (58, 42, 36)
HAIR_DARK = (26, 18, 16)
SKIN = (214, 168, 138)
HOODIE = (56, 88, 128)
HOODIE_SHADOW = (38, 62, 94)
HOODIE_HI = (78, 116, 156)

MUG_BODY = (198, 82, 70)
MUG_HI = (222, 112, 98)
STEAM = (205, 205, 214)

KEY_DARK = (20, 20, 26)
KEY_LIGHT = (60, 60, 70)

PLANT_POT = (118, 68, 48)
PLANT_LEAF = (70, 150, 92)
PLANT_LEAF_HI = (96, 180, 116)

TABLET_BODY = (30, 30, 38)
TABLET_SCREEN = (14, 30, 40)
NODE_COLOR = (120, 220, 190)
NODE_LINE = (60, 120, 110)

LED_COLORS = [(230, 80, 80), (90, 220, 130), (90, 160, 230), (230, 200, 90)]
BOX_BODY = (32, 32, 40)
BOX_BODY_HI = (48, 48, 58)
CABLE_COLOR = (18, 18, 24)
VDB_COLOR = (120, 170, 220)
VDB_HI = (160, 200, 235)

ICON_PY_BLUE = (70, 130, 200)
ICON_PY_YELLOW = (220, 200, 90)
ICON_DOCKER = (80, 170, 220)
ICON_AZURE = (90, 160, 230)
ICON_SPARK = (230, 140, 70)
ICON_FABRIC = (200, 120, 200)

WALL_MOONLIGHT = (42, 42, 80)
WALL_PANEL_LINE = (20, 22, 46)
BASEBOARD = (52, 42, 56)
BASEBOARD_HI = (66, 54, 70)
FLOOR_PLANK = (38, 26, 36)
RUG_COLOR = (58, 38, 58)
RUG_BORDER = (78, 52, 78)
RUG_PATTERN = (48, 32, 50)

GLOW_TEAL = (34, 58, 64)
GLOW_TEAL_SOFT = (26, 40, 50)

DRAWER_FRONT = (78, 50, 30)
DRAWER_FRONT_HI = (98, 64, 40)
DRAWER_SEAM = (58, 36, 22)
DRAWER_HANDLE = (206, 184, 132)
DESK_LEG = (60, 38, 24)
DESK_LEG_SHADOW = (44, 26, 16)

MOUSE_BODY = (28, 28, 36)
MOUSE_HI = (48, 48, 58)
PEN_CUP_BODY = (64, 64, 76)
PEN_CUP_HI = (86, 86, 100)
PEN_COLORS = [(220, 90, 90), (90, 180, 220), (230, 200, 90)]

SHADOW_ON_DESK = (72, 46, 28)
SHADOW_ON_FLOOR = (24, 16, 24)

MONITOR_LED = (100, 235, 150)
FLOOR_GLOW = (54, 56, 46)
FLOOR_GLOW_SOFT = (44, 44, 40)
SILL_COLOR = (86, 74, 62)
SILL_PLANT_POT = (108, 62, 44)
SILL_PLANT_LEAF = (78, 158, 100)

TROPHY_CUP = (210, 190, 110)
TROPHY_BASE = (150, 110, 70)

# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

WALL_FLOOR_Y = 86
DESK_SURFACE_Y = 81
DESK_FRONT_BOTTOM = 112

WINDOW_X0, WINDOW_Y0, WINDOW_X1, WINDOW_Y1 = 10, 10, 54, 46
POSTER_X0, POSTER_Y0, POSTER_X1, POSTER_Y1 = 55, 6, 149, 34
SHELF_X0, SHELF_X1 = 150, 196
SHELF_PLANK_1_Y = 20
SHELF_PLANK_2_Y = 44

MONITOR_CX = 100
MONITOR_X0, MONITOR_X1 = MONITOR_CX - 24, MONITOR_CX + 24
MONITOR_BEZEL_Y0, MONITOR_BEZEL_Y1 = 38, 74
SCREEN_X0, SCREEN_X1 = MONITOR_X0 + 3, MONITOR_X1 - 3
SCREEN_Y0, SCREEN_Y1 = MONITOR_BEZEL_Y0 + 3, MONITOR_BEZEL_Y1 - 3

KEYBOARD_X0, KEYBOARD_X1 = 86, 114
KEYBOARD_Y0, KEYBOARD_Y1 = 77, 81

CHAR_HEAD_X0, CHAR_HEAD_X1 = 90, 110
CHAR_HEAD_Y0, CHAR_HEAD_Y1 = 48, 64
CHAR_NECK_Y0, CHAR_NECK_Y1 = 64, 67
CHAR_TORSO_X0, CHAR_TORSO_X1 = 84, 116
CHAR_TORSO_Y0, CHAR_TORSO_Y1 = 67, 77
CHAR_ARM_Y1 = KEYBOARD_Y1

MUG_X0, MUG_Y0 = 122, 69
TABLET_X0, TABLET_Y0 = 58, 57
PLANT_X0, PLANT_Y0 = 44, 67

FLOOR_BOX_X0, FLOOR_BOX_Y0 = 18, 96
FLOOR_VDB_X0, FLOOR_VDB_Y0 = 40, 100


# A hand-authored 3x5 pixel bitmap font. System TrueType fonts break up
# into illegible fragments at these pixel heights even when supersampled
# and downscaled, so glyphs are drawn from these fixed bit patterns
# instead -- this is what keeps the sign genuinely "pixel art" rather
# than blurry antialiased text shrunk down.
PIXEL_FONT_3X5 = {
    "A": ["010", "101", "111", "101", "101"],
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
    "V": ["101", "101", "101", "101", "010"],
    "Y": ["101", "101", "010", "010", "010"],
    " ": ["000", "000", "000", "000", "000"],
    "/": ["001", "001", "010", "100", "100"],
    ".": ["000", "000", "000", "000", "010"],
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
    used for glow/light bleed so it doesn't erase the texture beneath it,
    unlike a filled rect or a smooth alpha blend would."""
    for yy in range(y0, y1 + 1):
        for xx in range(x0, x1 + 1):
            if not (0 <= xx < LOW_W and 0 <= yy < LOW_H):
                continue
            if (xx + yy + phase) % density == 0:
                px(img, xx, yy, color)


def dither_ring(img, cx, cy, r_inner, r_outer, glow_color):
    """A soft dithered halo around a point light (LED, screen glow),
    stippled onto whatever is already drawn there."""
    for yy in range(cy - r_outer, cy + r_outer + 1):
        for xx in range(cx - r_outer, cx + r_outer + 1):
            if not (0 <= xx < LOW_W and 0 <= yy < LOW_H):
                continue
            d2 = (xx - cx) ** 2 + (yy - cy) ** 2
            if r_inner * r_inner <= d2 <= r_outer * r_outer and (xx + yy) % 2 == 0:
                px(img, xx, yy, glow_color)


# ---------------------------------------------------------------------------
# Scene functions
# ---------------------------------------------------------------------------

def draw_background(img):
    # wall
    rect(img, 0, 0, LOW_W - 1, WALL_FLOOR_Y - 1, WALL_BG)
    rect(img, 0, 0, LOW_W - 1, 8, WALL_BG_SHADOW)

    # faint vertical panel seams for wall texture, not a flat block
    for lx in range(2, LOW_W - 2, 34):
        ImageDraw.Draw(img).line([(lx, 9), (lx, WALL_FLOOR_Y - 1)], fill=WALL_PANEL_LINE)

    # moonlight spilling across the wall to the right of the window
    dither_rect(img, 54, 12, 96, 50, WALL_BG, WALL_MOONLIGHT, density=5)

    # baseboard trim
    rect(img, 0, WALL_FLOOR_Y - 2, LOW_W - 1, WALL_FLOOR_Y - 2, BASEBOARD_HI)
    rect(img, 0, WALL_FLOOR_Y - 1, LOW_W - 1, WALL_FLOOR_Y + 1, BASEBOARD)

    # floor with plank seams
    rect(img, 0, WALL_FLOOR_Y + 2, LOW_W - 1, LOW_H - 1, FLOOR)
    for lx in range(6, LOW_W - 2, 16):
        ImageDraw.Draw(img).line([(lx, WALL_FLOOR_Y + 2), (lx, LOW_H - 1)], fill=FLOOR_PLANK)

    # a rug across the visible foreground floor strip, for a nearer layer
    rug_y0, rug_y1 = LOW_H - 9, LOW_H - 1
    rect(img, 16, rug_y0, LOW_W - 16, rug_y1, RUG_COLOR)
    rect(img, 16, rug_y0, LOW_W - 16, rug_y0, RUG_BORDER)
    for rx in range(20, LOW_W - 16, 6):
        px(img, rx, rug_y0 + 3, RUG_PATTERN)
        px(img, rx, rug_y0 + 6, RUG_PATTERN)


STARS = [
    (16, 16, 0), (24, 12, 1), (34, 18, 2), (44, 14, 0), (20, 28, 1),
    (40, 30, 2), (14, 22, 0), (30, 24, 1),
]


def draw_window(img, frame_idx):
    rect(img, WINDOW_X0 - 2, WINDOW_Y0 - 2, WINDOW_X1 + 2, WINDOW_Y1 + 2, WINDOW_FRAME)
    rect(img, WINDOW_X0 - 2, WINDOW_Y0 - 2, WINDOW_X1 + 2, WINDOW_Y0 - 1, WINDOW_FRAME_HI)

    low_band = WINDOW_Y0 + int((WINDOW_Y1 - WINDOW_Y0) * 0.6)
    rect(img, WINDOW_X0, WINDOW_Y0, WINDOW_X1, low_band, SKY)
    rect(img, WINDOW_X0, low_band, WINDOW_X1, WINDOW_Y1, SKY_LOW)

    # moon
    mx, my, mr = WINDOW_X0 + 10, WINDOW_Y0 + 9, 5
    ImageDraw.Draw(img).ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=MOON)
    ImageDraw.Draw(img).ellipse([mx - 1, my - 2, mx + mr, my + mr - 1], fill=MOON_SHADOW)

    # stars twinkle
    for (sx, sy, seed) in STARS:
        wx, wy = WINDOW_X0 + sx, WINDOW_Y0 + sy
        if wx >= WINDOW_X1 or wy >= low_band:
            continue
        on = ((frame_idx + seed * 5) % 16) < 11
        px(img, wx, wy, STAR_BRIGHT if on else STAR_DIM)

    # drifting cloud
    span = (WINDOW_X1 - WINDOW_X0) + 14
    cx = WINDOW_X0 - 10 + int((frame_idx / NUM_FRAMES) * span)
    cy = WINDOW_Y0 + 6
    for dx, dy, w in [(0, 0, 6), (3, -1, 4), (6, 0, 5)]:
        x0, y0 = cx + dx, cy + dy
        x1 = x0 + w
        if x1 > WINDOW_X0 and x0 < WINDOW_X1:
            ImageDraw.Draw(img).rectangle(
                [max(x0, WINDOW_X0), y0, min(x1, WINDOW_X1), y0 + 1], fill=CLOUD
            )

    # distant skyline silhouette
    heights = [4, 7, 3, 6, 5, 8, 4]
    bw = (WINDOW_X1 - WINDOW_X0) / len(heights)
    for i, h in enumerate(heights):
        x0 = int(WINDOW_X0 + i * bw)
        x1 = int(WINDOW_X0 + (i + 1) * bw) - 1
        rect(img, x0, WINDOW_Y1 - h, x1, WINDOW_Y1, SKYLINE)

    # window mullion (cross-bar panes), drawn over the sky for a real frame
    mid_x = (WINDOW_X0 + WINDOW_X1) // 2
    rect(img, mid_x, WINDOW_Y0, mid_x, WINDOW_Y1, WINDOW_FRAME)
    rect(img, WINDOW_X0, low_band, WINDOW_X1, low_band, WINDOW_FRAME)

    # windowsill with a tiny plant, grounding the window in the room
    sill_y = WINDOW_Y1 + 2
    rect(img, WINDOW_X0 - 3, sill_y, WINDOW_X1 + 3, sill_y + 2, SILL_COLOR)
    rect(img, WINDOW_X0 - 3, sill_y, WINDOW_X1 + 3, sill_y, WINDOW_FRAME_HI)
    pot_x = WINDOW_X1 - 6
    rect(img, pot_x, sill_y - 4, pot_x + 5, sill_y, SILL_PLANT_POT)
    rect(img, pot_x + 1, sill_y - 8, pot_x + 2, sill_y - 4, SILL_PLANT_LEAF)
    rect(img, pot_x + 3, sill_y - 9, pot_x + 4, sill_y - 4, SILL_PLANT_LEAF)
    px(img, pot_x + 2, sill_y - 9, SILL_PLANT_LEAF)


def draw_poster(img):
    rect(img, POSTER_X0, POSTER_Y0, POSTER_X1, POSTER_Y1, POSTER_FRAME)
    rect(img, POSTER_X0 + 2, POSTER_Y0 + 2, POSTER_X1 - 2, POSTER_Y1 - 2, POSTER_BG)
    cx = (POSTER_X0 + POSTER_X1) // 2
    draw_pixel_text(img, cx, POSTER_Y0 + 6, "VIGNESH KRISHNA", POSTER_TEXT, center=True)
    draw_pixel_text(img, cx, POSTER_Y0 + 17, "AI / ML / DL ENGINEER", POSTER_ACCENT, center=True)


BOTTOM_SHELF_BOOK_HEIGHTS = [11, 9, 12, 8, 10, 9]


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
        # cast shadow strip on the wall just under the plank
        rect(img, SHELF_X0, plank_y + 3, SHELF_X1, plank_y + 3, WALL_PANEL_LINE)

    # top row: a couple of short books + small figurine + a little trophy
    x = SHELF_X0 + 2
    for i, h in enumerate([9, 7]):
        w = 5
        rect(img, x, SHELF_PLANK_1_Y - h, x + w, SHELF_PLANK_1_Y - 1, BOOK_COLORS[i])
        rect(img, x, SHELF_PLANK_1_Y - h, x + w, SHELF_PLANK_1_Y - h, (255, 255, 255))
        x += w + 1
    # tiny robot figurine
    fig_x = x + 3
    rect(img, fig_x, SHELF_PLANK_1_Y - 7, fig_x + 4, SHELF_PLANK_1_Y - 3, (150, 150, 160))
    rect(img, fig_x + 1, SHELF_PLANK_1_Y - 9, fig_x + 3, SHELF_PLANK_1_Y - 8, (150, 150, 160))
    px(img, fig_x + 1, SHELF_PLANK_1_Y - 6, (90, 220, 170))
    px(img, fig_x + 3, SHELF_PLANK_1_Y - 6, (90, 220, 170))
    # small trophy cup
    tro_x = fig_x + 8
    rect(img, tro_x + 1, SHELF_PLANK_1_Y - 3, tro_x + 3, SHELF_PLANK_1_Y - 1, TROPHY_BASE)
    rect(img, tro_x, SHELF_PLANK_1_Y - 8, tro_x + 4, SHELF_PLANK_1_Y - 4, TROPHY_CUP)
    px(img, tro_x, SHELF_PLANK_1_Y - 9, TROPHY_CUP)
    px(img, tro_x + 4, SHELF_PLANK_1_Y - 9, TROPHY_CUP)

    # bottom row: varied book spines, some leaning for a lived-in feel
    for i, h in enumerate(BOTTOM_SHELF_BOOK_HEIGHTS):
        x, _ = shelf_bottom_spine_x(i)
        w = 5
        color = BOOK_COLORS[(i + 2) % len(BOOK_COLORS)]
        rect(img, x, SHELF_PLANK_2_Y - h, x + w, SHELF_PLANK_2_Y - 1, color)
        rect(img, x, SHELF_PLANK_2_Y - h, x + w, SHELF_PLANK_2_Y - h, (255, 255, 255))
        rect(img, x, SHELF_PLANK_2_Y - h, x, SHELF_PLANK_2_Y - 1, (0, 0, 0))


def draw_desk(img, part):
    if part == "top":
        rect(img, 4, DESK_SURFACE_Y - 4, LOW_W - 4, DESK_SURFACE_Y - 1, DESK_TOP)
        rect(img, 4, DESK_SURFACE_Y - 4, LOW_W - 4, DESK_SURFACE_Y - 4, DESK_TOP_HI)
        return

    # legs (outer posts)
    rect(img, 4, DESK_SURFACE_Y, 9, DESK_FRONT_BOTTOM, DESK_LEG)
    rect(img, LOW_W - 9, DESK_SURFACE_Y, LOW_W - 4, DESK_FRONT_BOTTOM, DESK_LEG)
    rect(img, 4, DESK_FRONT_BOTTOM - 2, 9, DESK_FRONT_BOTTOM, DESK_LEG_SHADOW)
    rect(img, LOW_W - 9, DESK_FRONT_BOTTOM - 2, LOW_W - 4, DESK_FRONT_BOTTOM, DESK_LEG_SHADOW)

    # centre modesty panel (open knee-space where the character sits)
    rect(img, 53, DESK_SURFACE_Y, 147, DESK_FRONT_BOTTOM, DESK_FRONT)
    rect(img, 53, DESK_SURFACE_Y, 147, DESK_SURFACE_Y + 1, DESK_FRONT_SHADOW)
    for lx in range(65, 147, 22):
        ImageDraw.Draw(img).line(
            [(lx, DESK_SURFACE_Y + 4), (lx, DESK_FRONT_BOTTOM - 4)], fill=DESK_FRONT_LINE
        )

    # two stacked drawers on each side, with recessed seams and handles
    for dx0, dx1 in [(11, 53), (147, 189)]:
        for dy0, dy1 in [(DESK_SURFACE_Y + 2, DESK_SURFACE_Y + 14), (DESK_SURFACE_Y + 16, DESK_SURFACE_Y + 28)]:
            rect(img, dx0, dy0, dx1, dy1, DRAWER_FRONT)
            rect(img, dx0, dy0, dx1, dy0, DRAWER_FRONT_HI)
            rect(img, dx0, dy0, dx0, dy1, DRAWER_SEAM)
            rect(img, dx1, dy0, dx1, dy1, DRAWER_SEAM)
            hx = (dx0 + dx1) // 2
            hy = (dy0 + dy1) // 2
            rect(img, hx - 4, hy, hx + 4, hy, DRAWER_HANDLE)


def draw_monitor(img, frame_idx):
    # screen glow bleeding onto the wall and desk around the monitor --
    # stippled, not a smooth gradient, and drawn first so the bezel below
    # cleanly overwrites the center, leaving only the bleeding ring
    glow = GLOW_TEAL if pulse(frame_idx, 18) > 0.65 else GLOW_TEAL_SOFT
    stipple(img, MONITOR_X0 - 3, MONITOR_BEZEL_Y0 - 3, MONITOR_X1 + 3, MONITOR_BEZEL_Y1, glow, density=3)

    rect(img, MONITOR_X0, MONITOR_BEZEL_Y0, MONITOR_X1, MONITOR_BEZEL_Y1, MONITOR_BEZEL)
    rect(img, MONITOR_X0, MONITOR_BEZEL_Y0, MONITOR_X1, MONITOR_BEZEL_Y0 + 1, MONITOR_BEZEL_HI)
    rect(img, SCREEN_X0, SCREEN_Y0, SCREEN_X1, SCREEN_Y1, SCREEN_BG)

    # power LED on the lower bezel edge, slow blink
    led_x, led_y = MONITOR_X1 - 3, MONITOR_BEZEL_Y1 - 2
    if (frame_idx % 16) < 13:
        px(img, led_x, led_y, MONITOR_LED)

    # stand: neck + wider base plate with a highlight edge
    neck_x0, neck_x1 = MONITOR_CX - 3, MONITOR_CX + 3
    rect(img, neck_x0, MONITOR_BEZEL_Y1, neck_x1, MONITOR_BEZEL_Y1 + 5, MONITOR_STAND)
    rect(img, MONITOR_CX - 10, MONITOR_BEZEL_Y1 + 5, MONITOR_CX + 10, MONITOR_BEZEL_Y1 + 7, MONITOR_STAND)
    rect(img, MONITOR_CX - 10, MONITOR_BEZEL_Y1 + 5, MONITOR_CX + 10, MONITOR_BEZEL_Y1 + 5, MONITOR_BEZEL_HI)

    # status word cycling in the clear strip above the character's head --
    # the only part of the screen never occluded by them
    words = ["RAG...", "AGENT", "TRAIN", "INFER"]
    word = words[(frame_idx // 6) % len(words)]
    word_y = SCREEN_Y0 + 1
    draw_pixel_text(img, SCREEN_X0 + 2, word_y, word, SCREEN_LINE_1)
    cursor_on = (frame_idx % 8) < 4
    if cursor_on:
        cw = measure_pixel_text(word) + 2
        rect(img, SCREEN_X0 + 2 + cw, word_y, SCREEN_X0 + 3 + cw, word_y + 4, CURSOR_COLOR)

    # tiny live bar chart, top-right of the screen (training/inference metric)
    bar_colors = [SCREEN_LINE_1, SCREEN_LINE_2, SCREEN_LINE_3, SCREEN_LINE_1]
    bar_base = word_y + 4
    for i, bcolor in enumerate(bar_colors):
        bh = 2 + ((frame_idx + i * 3) % 4)
        bx = SCREEN_X1 - 10 + i * 2
        rect(img, bx, bar_base - bh, bx + 1, bar_base, bcolor)

    # decorative code-line dashes below -- naturally sit behind the
    # character's head/shoulders, like a busy editor glimpsed over someone
    line_colors = [SCREEN_LINE_1, SCREEN_LINE_2, SCREEN_LINE_3, SCREEN_LINE_2, SCREEN_LINE_4]
    lengths = [14, 10, 16, 8, 12]
    for i, (color, length) in enumerate(zip(line_colors, lengths)):
        ly = word_y + 8 + i * 3
        if ly > SCREEN_Y1 - 2:
            break
        rect(img, SCREEN_X0 + 2, ly, SCREEN_X0 + 2 + length, ly, color)

    # scrolling data particles on the right edge of the screen
    for i in range(3):
        phase = (frame_idx * 2 + i * 7) % (SCREEN_Y1 - SCREEN_Y0)
        py_ = SCREEN_Y0 + phase
        px_ = SCREEN_X1 - 2 - (i % 2)
        px(img, px_, py_, PARTICLE_COLOR)


def desk_shadow(img, x0, x1, y):
    rect(img, x0, y, x1, y, SHADOW_ON_DESK)


def draw_objects(img, frame_idx):
    # keyboard, with a grounding shadow and a mouse beside it
    desk_shadow(img, KEYBOARD_X0 - 1, KEYBOARD_X1 + 1, KEYBOARD_Y1 + 1)
    rect(img, KEYBOARD_X0, KEYBOARD_Y0, KEYBOARD_X1, KEYBOARD_Y1, KEY_DARK)
    rect(img, KEYBOARD_X0, KEYBOARD_Y0, KEYBOARD_X1, KEYBOARD_Y0, MONITOR_BEZEL_HI)
    for kx in range(KEYBOARD_X0 + 2, KEYBOARD_X1 - 1, 3):
        px(img, kx, KEYBOARD_Y0 + 1, KEY_LIGHT)

    mouse_x0, mouse_y0 = KEYBOARD_X1 + 3, KEYBOARD_Y0 - 1
    rect(img, mouse_x0, mouse_y0, mouse_x0 + 3, mouse_y0 + 5, MOUSE_BODY)
    rect(img, mouse_x0, mouse_y0, mouse_x0 + 3, mouse_y0 + 1, MOUSE_HI)
    px(img, mouse_x0 + 1, mouse_y0 + 2, KEY_LIGHT)

    # tablet with LangGraph-style node graph, glow pulses
    tx0, ty0 = TABLET_X0, TABLET_Y0
    tx1, ty1 = tx0 + 14, ty0 + 22
    desk_shadow(img, tx0 - 1, tx1 + 1, ty1 + 1)
    rect(img, tx0, ty0, tx1, ty1, TABLET_BODY)
    rect(img, tx0 + 1, ty0 + 1, tx1 - 1, ty1 - 5, TABLET_SCREEN)
    glow = pulse(frame_idx, 12)
    node_color = tuple(int(c * glow) for c in NODE_COLOR)
    nodes = [(tx0 + 4, ty0 + 5), (tx0 + 10, ty0 + 5), (tx0 + 7, ty0 + 11)]
    ImageDraw.Draw(img).line([nodes[0], nodes[1]], fill=NODE_LINE)
    ImageDraw.Draw(img).line([nodes[0], nodes[2]], fill=NODE_LINE)
    ImageDraw.Draw(img).line([nodes[1], nodes[2]], fill=NODE_LINE)
    for nx, ny in nodes:
        rect(img, nx - 1, ny - 1, nx + 1, ny + 1, node_color)
    rect(img, tx0 + 2, ty1 - 3, tx1 - 2, ty1 - 3, (60, 60, 68))

    # small potted plant
    px0, py0 = PLANT_X0, PLANT_Y0
    desk_shadow(img, px0 - 1, px0 + 9, py0 + 15)
    rect(img, px0, py0 + 8, px0 + 8, py0 + 14, PLANT_POT)
    rect(img, px0, py0 + 8, px0 + 8, py0 + 8, PLANT_POT)
    rect(img, px0 + 1, py0 + 2, px0 + 3, py0 + 8, PLANT_LEAF)
    rect(img, px0 + 3, py0, px0 + 5, py0 + 8, PLANT_LEAF_HI)
    rect(img, px0 + 5, py0 + 3, px0 + 7, py0 + 8, PLANT_LEAF)

    # a small pen cup beside the plant
    cup_x0, cup_y0 = px0 - 12, py0 + 4
    desk_shadow(img, cup_x0 - 1, cup_x0 + 7, py0 + 15)
    rect(img, cup_x0, cup_y0, cup_x0 + 6, py0 + 14, PEN_CUP_BODY)
    rect(img, cup_x0, cup_y0, cup_x0 + 6, cup_y0, PEN_CUP_HI)
    for i, pcolor in enumerate(PEN_COLORS):
        ImageDraw.Draw(img).line(
            [(cup_x0 + 1 + i * 2, cup_y0), (cup_x0 + 1 + i * 2 - 1, cup_y0 - 6)], fill=pcolor
        )

    # coffee mug with rising steam
    mx0, my0 = MUG_X0, MUG_Y0
    desk_shadow(img, mx0 - 1, mx0 + 9, my0 + 9)
    rect(img, mx0, my0, mx0 + 7, my0 + 8, MUG_BODY)
    rect(img, mx0, my0, mx0 + 7, my0 + 1, MUG_HI)
    ImageDraw.Draw(img).arc([mx0 + 6, my0 + 1, mx0 + 11, my0 + 7], -90, 90, fill=MUG_BODY)
    for i in range(2):
        wobble = int(math.sin((frame_idx + i * 4) / 3.0) * 1.5)
        sy = my0 - 2 - ((frame_idx * 2 + i * 6) % 10)
        sx = mx0 + 2 + i * 3 + wobble
        fade = 1.0 - ((frame_idx * 2 + i * 6) % 10) / 10.0
        if fade > 0.15:
            px(img, sx, sy, STEAM)


def draw_technology_elements(img):
    """Technology as environmental easter eggs only: two small stickers on
    the monitor bezel, and tiny glyphs painted directly onto three of the
    shelf's book spines -- never a separate icon card floating in space."""
    # Python sticker on the monitor bezel (bottom-left corner)
    sx, sy = MONITOR_X0 + 3, MONITOR_BEZEL_Y1 - 5
    rect(img, sx, sy, sx + 2, sy + 3, ICON_PY_BLUE)
    rect(img, sx + 2, sy + 1, sx + 4, sy + 4, ICON_PY_YELLOW)

    # Docker sticker on the monitor bezel (bottom-right corner)
    dx, dy = MONITOR_X1 - 8, MONITOR_BEZEL_Y1 - 5
    rect(img, dx, dy + 2, dx + 6, dy + 4, ICON_DOCKER)
    for i in range(3):
        rect(img, dx + 1 + i * 2, dy, dx + 2 + i * 2, dy + 1, ICON_DOCKER)

    # Azure glyph stamped onto a book spine (a small two-tone wedge)
    ax, _ = shelf_bottom_spine_x(1)
    ay = SHELF_PLANK_2_Y - 4
    px(img, ax + 1, ay, ICON_AZURE)
    px(img, ax + 2, ay, ICON_AZURE)
    px(img, ax + 2, ay - 1, ICON_AZURE)
    px(img, ax + 3, ay - 1, ICON_AZURE)

    # Spark glyph (tiny bolt) stamped onto another spine
    spx, _ = shelf_bottom_spine_x(3)
    spy = SHELF_PLANK_2_Y - 4
    px(img, spx + 3, spy - 2, ICON_SPARK)
    px(img, spx + 2, spy - 1, ICON_SPARK)
    px(img, spx + 3, spy, ICON_SPARK)
    px(img, spx + 2, spy + 1, ICON_SPARK)

    # Fabric glyph (tiny weave mark) stamped onto a third spine
    fx, _ = shelf_bottom_spine_x(5)
    fy = SHELF_PLANK_2_Y - 5
    px(img, fx + 1, fy, ICON_FABRIC)
    px(img, fx + 3, fy, ICON_FABRIC)
    px(img, fx + 2, fy + 1, ICON_FABRIC)
    px(img, fx + 1, fy + 2, ICON_FABRIC)
    px(img, fx + 3, fy + 2, ICON_FABRIC)


def draw_chair(img):
    head_top = CHAR_HEAD_Y0 - 3
    # headrest posts, capped for a cushioned silhouette
    rect(img, CHAR_TORSO_X0 - 6, head_top, CHAR_TORSO_X0 - 2, CHAR_TORSO_Y0, CHAIR)
    rect(img, CHAR_TORSO_X1 + 2, head_top, CHAR_TORSO_X1 + 6, CHAR_TORSO_Y0, CHAIR)
    rect(img, CHAR_TORSO_X0 - 7, head_top + 1, CHAR_TORSO_X0 - 6, head_top + 5, CHAIR)
    rect(img, CHAR_TORSO_X1 + 6, head_top + 1, CHAR_TORSO_X1 + 7, head_top + 5, CHAIR)

    # backrest crossbar behind the shoulders
    rect(img, CHAR_TORSO_X0 - 6, CHAR_TORSO_Y0 - 4, CHAR_TORSO_X1 + 6, CHAR_TORSO_Y0 + 2, CHAIR)
    rect(img, CHAR_TORSO_X0 - 6, CHAR_TORSO_Y0 - 4, CHAR_TORSO_X1 + 6, CHAR_TORSO_Y0 - 3, CHAIR_HI)
    rect(img, CHAR_TORSO_X0 + 13, CHAR_TORSO_Y0 - 3, CHAR_TORSO_X0 + 13, CHAR_TORSO_Y0 + 1, CHAIR_HI)

    # armrests, peeking out beyond the torso at elbow height
    arm_y0, arm_y1 = CHAR_TORSO_Y1 - 3, CHAR_TORSO_Y1 + 2
    rect(img, CHAR_TORSO_X0 - 9, arm_y0, CHAR_TORSO_X0 - 5, arm_y1, CHAIR)
    rect(img, CHAR_TORSO_X0 - 9, arm_y0, CHAR_TORSO_X0 - 5, arm_y0, CHAIR_HI)
    rect(img, CHAR_TORSO_X1 + 5, arm_y0, CHAR_TORSO_X1 + 9, arm_y1, CHAIR)
    rect(img, CHAR_TORSO_X1 + 5, arm_y0, CHAR_TORSO_X1 + 9, arm_y0, CHAIR_HI)


HEAD_ROW_INSET = [2, 1, 0]  # rounds only the top couple of rows


def draw_character(img, frame_idx):
    """Back view only: the developer faces the monitor, away from the
    viewer, so the head is a solid hair silhouette with no face."""
    bob_phase = (frame_idx % 10)
    bob = 0 if bob_phase < 5 else -1

    # head: back-of-head hair silhouette, rounded at the top so it isn't
    # just a flat block, plus a couple of darker strand lines for texture
    hx0, hy0, hx1, hy1 = CHAR_HEAD_X0, CHAR_HEAD_Y0 + bob, CHAR_HEAD_X1, CHAR_HEAD_Y1 + bob
    for ry in range(hy0, hy1 + 1):
        inset = HEAD_ROW_INSET[min(ry - hy0, len(HEAD_ROW_INSET) - 1)]
        row_color = HAIR_HI if (ry - hy0) < 2 else HAIR
        rect(img, hx0 + inset, ry, hx1 - inset, ry, row_color)
    rect(img, hx0 + 5, hy0 + 3, hx0 + 5, hy1 - 2, HAIR_DARK)
    rect(img, hx1 - 4, hy0 + 3, hx1 - 4, hy1 - 2, HAIR_DARK)
    # a sliver of neck skin peeking below the hairline
    nx0, nx1 = CHAR_HEAD_X0 + 6, CHAR_HEAD_X1 - 6
    rect(img, nx0, hy1, nx1, CHAR_NECK_Y1 + bob, SKIN)

    # torso: hoodie back, seen from behind, with sloped shoulder corners
    ty0, ty1 = CHAR_TORSO_Y0 + bob, CHAR_TORSO_Y1
    rect(img, CHAR_TORSO_X0, ty0, CHAR_TORSO_X1, ty1, HOODIE)
    rect(img, CHAR_TORSO_X0, ty0, CHAR_TORSO_X0 + 4, ty1, HOODIE_SHADOW)
    rect(img, CHAR_TORSO_X1 - 4, ty0, CHAR_TORSO_X1, ty1, HOODIE_HI)
    rect(img, CHAR_TORSO_X0 + 2, ty0, CHAR_TORSO_X1 - 2, ty0 + 2, HOODIE_HI)
    px(img, CHAR_TORSO_X0, ty0, WALL_BG if bob == 0 else HOODIE)
    px(img, CHAR_TORSO_X1, ty0, WALL_BG if bob == 0 else HOODIE)
    # hood seam + drawstring
    rect(img, CHAR_TORSO_X0 + 12, ty0, CHAR_TORSO_X1 - 12, ty0 + 1, HOODIE_SHADOW)
    px(img, CHAR_TORSO_X0 + 15, ty0 + 2, HOODIE_SHADOW)
    px(img, CHAR_TORSO_X1 - 15, ty0 + 2, HOODIE_SHADOW)

    # arms: a wider shoulder cap tapering into a narrower forearm, so the
    # elbow reads as a bend rather than a straight bar down to the keys
    typing_l = 1 if (frame_idx % 4) < 2 else 0
    typing_r = 0 if (frame_idx % 4) < 2 else 1
    arm_top = ty1
    cap_h = 3
    for kx0, kx1, typing in [
        (KEYBOARD_X0, KEYBOARD_X0 + 6, typing_l),
        (KEYBOARD_X1 - 6, KEYBOARD_X1, typing_r),
    ]:
        rect(img, kx0, arm_top, kx1, arm_top + cap_h, HOODIE)
        fx0, fx1 = kx0 + 1, kx1 - 1
        fy1 = CHAR_ARM_Y1 - 1 + typing
        rect(img, fx0, arm_top + cap_h, fx1, fy1, HOODIE_SHADOW)
        rect(img, fx0, fy1 - 2, fx1, fy1 - 2, HOODIE_HI)
        rect(img, fx0, fy1 - 1, fx1, fy1, SKIN)


def draw_floor_props(img, frame_idx):
    bx0, by0 = FLOOR_BOX_X0, FLOOR_BOX_Y0
    bx1, by1 = bx0 + 14, by0 + 14

    # soft LED glow bleeding onto the floor/rug around the box
    glow = FLOOR_GLOW if pulse(frame_idx, 6) > 0.5 else FLOOR_GLOW_SOFT
    dither_ring(img, bx0 + 7, by0 + 6, 3, 9, glow)
    rect(img, bx0 - 1, by1 + 1, bx1 + 1, by1 + 1, SHADOW_ON_FLOOR)

    rect(img, bx0, by0, bx1, by1, BOX_BODY)
    rect(img, bx0, by0, bx1, by0 + 2, BOX_BODY_HI)
    for i, base_color in enumerate(LED_COLORS[:3]):
        on = ((frame_idx // 2 + i * 3) % 6) < 3
        color = base_color if on else tuple(c // 3 for c in base_color)
        rect(img, bx0 + 2 + i * 4, by0 + 5, bx0 + 4 + i * 4, by0 + 7, color)

    cable_x = bx0 + 3
    ImageDraw.Draw(img).line(
        [(cable_x, by0), (cable_x, DESK_SURFACE_Y - 4), (cable_x + 6, DESK_SURFACE_Y - 4)],
        fill=CABLE_COLOR,
    )

    vx0, vy0 = FLOOR_VDB_X0, FLOOR_VDB_Y0
    rect(img, vx0 - 1, vy0 + 11, vx0 + 13, vy0 + 11, SHADOW_ON_FLOOR)
    for i in range(3):
        yy = vy0 + i * 4
        ImageDraw.Draw(img).ellipse([vx0, yy, vx0 + 12, yy + 4], fill=VDB_COLOR, outline=VDB_HI)
    rect(img, vx0, vy0 + 2, vx0 + 12, vy0 + 10, VDB_COLOR)
    ImageDraw.Draw(img).ellipse([vx0, vy0, vx0 + 12, vy0 + 4], fill=VDB_HI)


# ---------------------------------------------------------------------------
# Frame assembly
# ---------------------------------------------------------------------------

def build_low_res_frame(frame_idx):
    img = Image.new("RGB", (LOW_W, LOW_H), WALL_BG)

    draw_background(img)
    draw_window(img, frame_idx)
    draw_poster(img)
    draw_shelves(img)
    draw_desk(img, "top")
    draw_monitor(img, frame_idx)
    draw_objects(img, frame_idx)
    draw_technology_elements(img)
    draw_chair(img)
    draw_character(img, frame_idx)
    draw_desk(img, "front")
    draw_floor_props(img, frame_idx)

    return img


def upscale(img):
    return img.resize((FINAL_W, FINAL_H), Image.NEAREST)


def generate_frames():
    return [upscale(build_low_res_frame(i)) for i in range(NUM_FRAMES)]


def main():
    frames = generate_frames()

    sample = Image.new("RGB", (FINAL_W, FINAL_H * 3))
    for i, idx in enumerate([0, NUM_FRAMES // 2, NUM_FRAMES - 1]):
        sample.paste(frames[idx], (0, i * FINAL_H))
    palette_img = sample.quantize(colors=64, dither=Image.Dither.NONE)

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
