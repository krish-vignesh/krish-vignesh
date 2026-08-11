"use strict";
/**
 * Central color palette, grouped by role. Deliberately small and reused
 * everywhere so the scene reads as one consistent pixel-art piece instead
 * of a pile of arbitrary colors.
 */

const palette = {
  // background darks
  bgWallTop: [19, 20, 42],
  bgWallShadow: [15, 16, 34],
  bgPanelLine: [15, 17, 36],
  bgMoonlight: [34, 36, 66],

  // wall darks / floor
  floor: [28, 19, 28],
  floorPlank: [34, 23, 32],
  baseboard: [46, 38, 52],
  baseboardHi: [60, 50, 64],
  rug: [52, 34, 54],
  rugBorder: [72, 48, 74],
  rugPattern: [44, 29, 46],

  // deep shadows (contact shadows under objects)
  shadowDesk: [66, 42, 25],
  shadowFloor: [20, 14, 20],
  shadowSoft: [12, 12, 20],

  // wood / metal
  woodDeskTop: [116, 76, 47],
  woodDeskTopHi: [140, 97, 61],
  woodDeskFront: [82, 53, 31],
  woodDeskFrontShadow: [62, 39, 23],
  woodDeskFrontLine: [94, 61, 37],
  woodShelf: [102, 69, 45],
  woodShelfHi: [128, 90, 60],
  metalLeg: [56, 35, 21],
  metalLegShadow: [40, 23, 13],
  metalDrawer: [74, 47, 27],
  metalDrawerHi: [94, 61, 37],
  metalDrawerSeam: [54, 33, 19],
  metalHandle: [200, 178, 128],
  metalDark: [30, 32, 40],
  metalDarkHi: [46, 48, 58],
  metalCase: [28, 30, 38],

  // skin / hair / clothing
  skin: [212, 166, 136],
  hair: [37, 26, 23],
  hairHi: [57, 41, 35],
  hairDark: [25, 17, 15],
  hoodie: [52, 84, 124],
  hoodieShadow: [34, 58, 90],
  hoodieHi: [74, 112, 152],
  headphone: [28, 28, 34],
  headphoneHi: [50, 50, 58],
  chair: [24, 24, 34],
  chairHi: [40, 40, 52],

  // cyan monitor light
  screenBg: [6, 11, 18],
  screenGrid: [13, 21, 29],
  cyanGlowStrong: [30, 54, 60],
  cyanGlowSoft: [22, 36, 44],
  cyanCursor: [128, 244, 178],

  // teal technology light (secondary devices / nodes)
  tealNode: [110, 216, 186],
  tealNodeLine: [56, 116, 106],
  tealParticle: [148, 238, 208],

  // warm desk light (lamp)
  warmBulb: [255, 212, 138],
  warmGlow: [84, 64, 39],
  warmGlowSoft: [56, 45, 31],

  // orange / red / green / blue LEDs
  ledRed: [228, 78, 78],
  ledGreen: [88, 218, 128],
  ledBlue: [88, 158, 228],
  ledYellow: [228, 198, 88],
  ledOrange: [226, 138, 68],

  // purple accent
  purpleAccent: [198, 120, 220],
  purpleNode: [196, 128, 216],

  // pink accent
  pinkAccent: [232, 130, 168],
  pinkAccentSoft: [180, 90, 122],

  // blue night sky
  skyTop: [13, 13, 38],
  skyLow: [23, 20, 54],
  moon: [228, 218, 178],
  moonShadow: [198, 186, 148],
  cloud: [42, 40, 78],
  starBright: [230, 230, 200],
  starDim: [136, 136, 118],
  skyline: [10, 10, 26],
  cityWindowOn: [232, 198, 118],
  cityWindowOff: [38, 34, 56],

  // frames / posters
  frameWood: [144, 122, 82],
  frameWoodHi: [122, 106, 88],
  posterBg: [18, 16, 38],
  posterText: [230, 232, 224],
  posterAccent: [118, 228, 188],
  diagramFrame: [88, 94, 108],
  diagramBg: [15, 17, 28],

  // book / misc accents
  books: [
    [194, 88, 88],
    [88, 154, 198],
    [220, 180, 90],
    [118, 186, 138],
    [166, 118, 196],
    [90, 196, 186],
  ],
  trophyCup: [208, 188, 108],
  trophyBase: [148, 108, 68],
  plantPot: [112, 64, 44],
  plantLeaf: [66, 146, 88],
  plantLeafHi: [92, 176, 112],
  penCupBody: [60, 60, 72],
  penCupHi: [82, 82, 96],
  pens: [
    [218, 88, 88],
    [88, 178, 218],
    [228, 198, 88],
  ],
  notebookCover: [174, 58, 62],
  notebookPage: [220, 212, 188],
  notebookLine: [148, 140, 118],
  notebookSpiral: [168, 168, 176],
  mugBody: [196, 80, 68],
  mugHi: [220, 110, 96],
  steam: [204, 204, 213],
  keyDark: [17, 17, 23],
  keyLight: [56, 56, 66],
  mouseBody: [25, 25, 33],
  mouseHi: [45, 45, 55],
  speakerBody: [26, 26, 34],
  speakerCone: [44, 44, 56],
  usbBody: [70, 74, 86],
  usbMetal: [190, 194, 200],
  boxBody: [64, 48, 34],
  boxTape: [92, 74, 52],

  vectorDb: [118, 168, 218],
  vectorDbHi: [158, 198, 233],
  devBoardBody: [30, 62, 42],
  devBoardChip: [17, 17, 21],

  iconPyBlue: [68, 128, 198],
  iconPyYellow: [218, 198, 88],
  iconDocker: [78, 168, 218],
  iconAzure: [88, 158, 228],
  iconSpark: [228, 138, 68],
  iconFabric: [198, 118, 198],

  transparent: null,
};

module.exports = palette;
