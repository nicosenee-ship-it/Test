# -*- coding: utf-8 -*-
"""Dossier d'adaptation V2 (réemploi maximal) - L'Arbre à Makis - Cellule 09 Marques Avenue La Séguinière.
Génère un PDF A3 paysage (plans redessinés d'après le DAT La Mie Câline du 20/03/2015).
Coordonnées plan en cm : x = profondeur depuis le vitrage de façade (0) vers le mur du fond (1545),
y = largeur depuis le mur latéral haut (0) vers le mur latéral bas (1150)."""
import os, math
from reportlab.lib.pagesizes import A3, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white, black, Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "Dossier_LAM_La_Seguiniere_cellule09_V2.pdf")
LOGO = os.path.join(HERE, "logo_lam.png")

pdfmetrics.registerFont(TTFont("F", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("FB", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("FI", "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"))

W, H = landscape(A3)
NAVY = HexColor("#13213c"); GREEN = HexColor("#8cc63f"); SALMON = HexColor("#e8765a")
BLUE = HexColor("#2f6db5"); RED = HexColor("#d0312d"); GREY = HexColor("#777777")
LGREY = HexColor("#e9e9e9"); WALL = HexColor("#3a3a3a"); WOOD = HexColor("#d9b98a")
ORANGE = HexColor("#f29c1f"); BROWN = HexColor("#8b5a2b"); PURPLE = HexColor("#7d4fb3")



# --------------------------------------------------------------------------- géométrie V2 (réemploi maximal)
# Cotes relevées sur le plan « état projeté » La Mie Câline (DAT 2015, ech. 1/75) — précision ± 10 cm.
DEPTH, WIDTH = 1545, 1150
S = 28.3465 / 75.0          # 1/75 : points par cm réel
OX, OY = 150, 735           # origine page (x=0 vitrage, y=0 mur haut)
MAG = HexColor("#c2185b")   # éléments créés

def P(x, y):
    return OX + x * S, OY - y * S

ZONES = [  # (x1, y1, x2, y2, couleur)
 (0, 0, 655, 1150, HexColor("#f6f1e7")), (655, 0, 983, 427, HexColor("#f6f1e7")),
 (545, 430, 655, 1150, HexColor("#eef3e6")),
 (655, 427, 983, 733, HexColor("#e3f0fb")),
 (655, 733, 741, 837, HexColor("#e3f0fb")),
 (741, 733, 983, 837, HexColor("#f4f4f4")),
 (655, 837, 1058, 1150, HexColor("#fde9e3")),
 (983, 0, 1160, 200, HexColor("#efe7f7")),
 (983, 200, 1160, 700, HexColor("#f4f4f4")), (983, 700, 1395, 830, HexColor("#f4f4f4")),
 (983, 830, 1058, 837, HexColor("#f4f4f4")),
 (1160, 0, 1395, 445, HexColor("#f4f4f4")), (1160, 445, 1395, 700, HexColor("#fff6d9")),
 (1058, 830, 1370, 1150, HexColor("#dcecff")), (1370, 830, 1395, 1150, HexColor("#f4f4f4")),
 (1395, 0, 1545, 1150, HexColor("#f4f4f4")), (1400, 800, 1545, 1065, HexColor("#efe2d3")),
]

SURF = [
 ("Espace vente libre-service + caisse + salle", [(0, 0, 545, 1150), (545, 0, 655, 430), (655, 0, 983, 427)]),
 ("Zone service derrière le comptoir", [(545, 430, 655, 1150)]),
 ("Cuisson (zone existante cuisson + plaquage)", [(655, 837, 1058, 1150)]),
 ("Préparation froide (existante)", [(655, 427, 983, 733)]),
 ("Niche vitrine existante + ex-zone pousse (armoires +)", [(655, 733, 741, 837), (741, 733, 983, 837)]),
 ("Plonge (existante)", [(983, 0, 1160, 200)]),
 ("Chambre froide négative (existante)", [(1058, 830, 1370, 1150)]),
 ("Réserve sèche CF (existante)", [(1160, 445, 1395, 700)]),
 ("Vestiaires H/F, WC personnel, bureau (existants)", [(1160, 0, 1395, 445)]),
 ("Circulations, réception, conteneurs, TGBT", [(983, 200, 1160, 700), (983, 700, 1395, 830), (983, 830, 1058, 837),
                                               (1370, 830, 1395, 1150), (1395, 0, 1545, 1150)]),
]

def area(rects):
    return sum((x2 - x1) * (y2 - y1) for x1, y1, x2, y2 in rects) / 1e4

# cloisons EXISTANTES (toutes conservées) — ligne médiane
PARTS = [
 (983, 0, 983, 690),                                                   # salle | plonge / degt
 (655, 427, 983, 427), (655, 733, 930, 733), (930, 733, 983, 690),     # prépa froide (pan coupé)
 (655, 733, 741, 733), (741, 733, 741, 837), (655, 837, 741, 837),     # niche vitrine boissons
 (893, 948, 893, 1150),                                                # muret cuisson / plaquage
 (983, 200, 1160, 200), (1160, 0, 1160, 700),                          # plonge
 (1395, 0, 1395, 700), (1160, 445, 1395, 445), (1160, 700, 1395, 700), # vestiaires / réserve
 (1160, 110, 1395, 110), (1160, 275, 1395, 275), (1280, 110, 1280, 445),
 (1392, 1073, 1545, 1073), (1392, 1073, 1392, 1150),                   # local TGBT
]
GLASS = [(655, 427, 655, 733), (655, 837, 655, 1053)]     # verrières existantes (prépa, cuisson)
CF_PARTS = [(1160, 445, 1395, 445), (1160, 700, 1395, 700), (1395, 0, 1395, 700), (1392, 1073, 1545, 1073), (1392, 1073, 1392, 1150)]
DOORS = [  # existantes
 ("v", 655, 1053, 1135), ("h", 733, 935, 975), ("h", 200, 1050, 1140), ("v", 1395, 540, 630),
 ("v", 1395, 150, 230), ("v", 1395, 320, 400), ("v", 1395, 20, 100), ("v", 1160, 610, 690),
]


# --------------------------------------------------------------------------- primitives

def rect(c, x1, y1, x2, y2, fill=None, stroke=black, lw=0.5, dash=None, r=0):
    X1, Y1 = P(x1, y1); X2, Y2 = P(x2, y2)
    c.saveState(); c.setLineWidth(lw)
    if dash: c.setDash(list(dash))
    if fill is not None: c.setFillColor(fill)
    if stroke is not None: c.setStrokeColor(stroke)
    if r:
        c.roundRect(min(X1, X2), min(Y1, Y2), abs(X2 - X1), abs(Y2 - Y1), r,
                    fill=1 if fill is not None else 0, stroke=1 if stroke is not None else 0)
    else:
        c.rect(min(X1, X2), min(Y1, Y2), abs(X2 - X1), abs(Y2 - Y1),
               fill=1 if fill is not None else 0, stroke=1 if stroke is not None else 0)
    c.restoreState()

def line(c, x1, y1, x2, y2, col=black, lw=0.6, dash=None):
    c.saveState(); c.setStrokeColor(col); c.setLineWidth(lw)
    if dash: c.setDash(list(dash))
    X1, Y1 = P(x1, y1); X2, Y2 = P(x2, y2); c.line(X1, Y1, X2, Y2); c.restoreState()

def txt(c, x, y, s, size=6, font="F", col=black, align="c", rot=0):
    X, Y = P(x, y)
    c.saveState(); c.setFillColor(col); c.setFont(font, size); c.translate(X, Y); c.rotate(rot)
    lines = s.split("\n"); n = len(lines)
    for i, l in enumerate(lines):
        yy = (n - 1) * size * 0.6 - i * size * 1.2 - size * 0.35
        if align == "c": c.drawCentredString(0, yy, l)
        elif align == "l": c.drawString(0, yy, l)
        else: c.drawRightString(0, yy, l)
    c.restoreState()

def circle(c, x, y, r, fill=None, stroke=black, lw=0.5):
    X, Y = P(x, y); c.saveState(); c.setLineWidth(lw)
    if fill is not None: c.setFillColor(fill)
    if stroke is not None: c.setStrokeColor(stroke)
    c.circle(X, Y, r * S, fill=1 if fill is not None else 0, stroke=1 if stroke is not None else 0)
    c.restoreState()

def arrow_path(c, pts, col, lw=1.6, dash=None, head=True):
    c.saveState(); c.setStrokeColor(col); c.setFillColor(col); c.setLineWidth(lw)
    c.setLineJoin(1); c.setLineCap(1)
    if dash: c.setDash(list(dash))
    p = c.beginPath(); X, Y = P(*pts[0]); p.moveTo(X, Y)
    for q in pts[1:]:
        X, Y = P(*q); p.lineTo(X, Y)
    c.drawPath(p, stroke=1, fill=0)
    if head:
        c.setDash()
        (x1, y1), (x2, y2) = P(*pts[-2]), P(*pts[-1])
        a = math.atan2(y2 - y1, x2 - x1); L = 7
        p = c.beginPath(); p.moveTo(x2, y2)
        p.lineTo(x2 - L * math.cos(a - 0.4), y2 - L * math.sin(a - 0.4))
        p.lineTo(x2 - L * math.cos(a + 0.4), y2 - L * math.sin(a + 0.4)); p.close()
        c.drawPath(p, stroke=0, fill=1)
    c.restoreState()

def badge(c, x, y, s, col, size=6.5):
    X, Y = P(x, y); c.saveState(); c.setFillColor(col); c.circle(X, Y, size * 0.95, fill=1, stroke=0)
    c.setFillColor(white); c.setFont("FB", size); c.drawCentredString(X, Y - size * 0.36, s); c.restoreState()

# --------------------------------------------------------------------------- plan de base

# --------------------------------------------------------------------------- plan de base V2
def draw_shell(c, cf=False, terrace_text=True):
    rect(c, -330, 0, 0, WIDTH, fill=HexColor("#f3f3f3"), stroke=None)
    for yy in (0, WIDTH): line(c, -330, yy, 0, yy, GREY, 0.5)
    line(c, -330, -25, -330, WIDTH + 25, GREY, 0.6, dash=(4, 2, 1, 2))
    if terrace_text:
        txt(c, -170, 575, "TERRASSE EXTÉRIEURE\nCOUVERTE (sous auvent)\n→ terrasse saisonnière\n≈ 16 places, mobilier\nmobile (accord centre)", 6.5, "F", GREY, rot=90)
    for (x1, y1, x2, y2, col) in ZONES: rect(c, x1, y1, x2, y2, fill=col, stroke=None)
    wc = RED if cf else WALL
    rect(c, -20, -25, DEPTH + 25, 0, fill=wc, stroke=None)
    rect(c, -20, WIDTH, DEPTH + 25, WIDTH + 25, fill=wc, stroke=None)
    rect(c, DEPTH, 0, DEPTH + 25, WIDTH, fill=WALL, stroke=None)
    for (a, b) in [(15, 115), (640, 740)]:
        rect(c, DEPTH - 1, a, DEPTH + 26, b, fill=white, stroke=None)
        line(c, DEPTH + 25, a, DEPTH + 25 + (b - a), a, black, 0.5)
    for xp in (-20, 622, 1225, DEPTH):
        for yp in (-35, WIDTH - 5):
            rect(c, xp - 18, yp, xp + 22, yp + 40, fill=HexColor("#555555"), stroke=black, lw=0.3)
    rect(c, -6, 0, 6, 455, fill=HexColor("#bfe0f5"), stroke=BLUE, lw=0.4)
    rect(c, -6, 695, 6, WIDTH, fill=HexColor("#bfe0f5"), stroke=BLUE, lw=0.4)
    for a, b in [(455, 575), (695, 575)]:
        X, Y = P(0, a); r = abs(b - a) * S
        c.saveState(); c.setStrokeColor(black); c.setLineWidth(0.4); c.setDash(2, 1.5)
        if a < b: c.arc(X - r, Y - r, X + r, Y + r, 180, 90)
        else: c.arc(X - r, Y - r, X + r, Y + r, 180, -90)
        c.restoreState(); line(c, 0, a, -abs(b - a), a, black, 0.6)
    # verrière haute (imposte) existante entre salle et alcôve
    line(c, 655, 0, 655, 427, BLUE, 0.6, dash=(3, 2))
    for (x1, y1, x2, y2) in PARTS:
        is_cf = cf and (x1, y1, x2, y2) in CF_PARTS
        col = RED if is_cf else WALL; t = 6
        if x1 == x2: rect(c, x1 - t, y1, x1 + t, y2, fill=col, stroke=None)
        elif y1 == y2: rect(c, x1, y1 - t, x2, y1 + t, fill=col, stroke=None)
        else: line(c, x1, y1, x2, y2, col, 4.5)
    for (x1, y1, x2, y2) in GLASS:
        rect(c, x1 - 4, y1, x1 + 4, y2, fill=HexColor("#bfe0f5"), stroke=BLUE, lw=0.5)
    rect(c, 1058, 830, 1370, 1150, fill=None, stroke=BLUE, lw=2.2)
    for ax, k, a, b in DOORS:
        if ax == "v":
            rect(c, k - 8, a, k + 8, b, fill=white, stroke=None)
            line(c, k, a, k + (b - a) * 0.9, a, black, 0.5)
            X, Y = P(k, a); r = (b - a) * S
            c.saveState(); c.setLineWidth(0.3); c.setDash(1.5, 1.5); c.arc(X - r, Y - r, X + r, Y + r, 270, 90); c.restoreState()
        else:
            rect(c, a, k - 8, b, k + 8, fill=white, stroke=None)
            line(c, a, k, a, k - (b - a) * 0.9, black, 0.5)
            X, Y = P(a, k); r = (b - a) * S
            c.saveState(); c.setLineWidth(0.3); c.setDash(1.5, 1.5); c.arc(X - r, Y - r, X + r, Y + r, 0, 90); c.restoreState()
    rect(c, 1200, 822, 1310, 838, fill=white, stroke=BLUE, lw=0.8)
    # option : passe desserte (non structurel)
    rect(c, 977, 90, 989, 170, fill=HexColor("#ffe7a8"), stroke=MAG, lw=0.9, dash=(2, 1.5))

def lm(c, x, y, new=False):
    rect(c, x, y, x + 40, y + 38, fill=white, stroke=MAG if new else BLUE, lw=0.9 if new else 0.6)
    circle(c, x + 20, y + 19, 9, stroke=MAG if new else BLUE)

def draw_equipment(c, labels=True):
    # murale LS (mur bas : alimentations des ex-meubles turbochef / vitrine boissons)
    mods = ["Sushis\n& makis", "Rolls\n& bowls", "Baos & snacks\nfroids", "Desserts\n& boissons"]
    for i, m in enumerate(mods):
        x1 = 50 + i * 120
        rect(c, x1, 1065, x1 + 120, 1150, fill=HexColor("#cfe6f7"), stroke=NAVY, lw=0.6)
        if labels: txt(c, x1 + 60, 1107, m, 5.2, "F", NAVY)
    if labels: txt(c, 290, 1045, "MURALE LIBRE-SERVICE 4 × 1,20 m — groupe logé (plug-in), 0/+3 °C", 5.4, "FB", NAVY)
    # îlot retail
    rect(c, 110, 620, 330, 850, fill=WOOD, stroke=BROWN, lw=0.8, r=12)
    circle(c, 220, 735, 32, fill=HexColor("#6aa84f"), stroke=HexColor("#38761d"))
    if labels:
        txt(c, 220, 650, "ÎLOT « L'ARBRE » retail", 5.2, "FB")
        txt(c, 220, 810, "sauces, chips d'algues,\ncacahuètes wasabi, thés…", 4.6)
    # comptoir caisse
    rect(c, 470, 430, 545, 900, fill=WOOD, stroke=BROWN, lw=0.8)
    rect(c, 545, 430, 655, 458, fill=WOOD, stroke=BROWN, lw=0.5)
    rect(c, 470, 470, 500, 560, fill=white, stroke=BROWN, lw=0.4)
    rect(c, 538, 945, 552, 1040, fill=None, stroke=BROWN, lw=0.5, dash=(2, 1.5))
    lm(c, 610, 470, new=True)
    if labels:
        txt(c, 507, 515, "CAISSE 1\nPMR h 0,80", 4.6, "FB", rot=90)
        txt(c, 507, 640, "CAISSE 2", 4.8, "FB", rot=90)
        txt(c, 507, 730, "impulse retail", 4.4, rot=90)
        txt(c, 507, 845, "RETRAIT\nCHAUD", 4.6, "FB", rot=90)
        txt(c, 520, 993, "portillon", 4, "F", BROWN, rot=90)
        txt(c, 600, 700, "ZONE SERVICE", 5.2, "FB", HexColor("#4f7a28"), rot=90)
    # places : mange-debout vitrine (ex-mange-debout La Mie Câline)
    rect(c, 0, 60, 45, 420, fill=WOOD, stroke=BROWN, lw=0.5)
    for i in range(5): circle(c, 75, 60 + 360 * (i + 0.5) / 5, 17, fill=white, stroke=GREY)
    rect(c, 120, 0, 465, 55, fill=HexColor("#2c3e5c"), stroke=None)
    for xt in (130, 215, 300, 385):
        rect(c, xt, 65, xt + 65, 125, fill=WOOD, stroke=BROWN, lw=0.5)
        rect(c, xt + 12, 135, xt + 53, 172, fill=white, stroke=GREY, lw=0.5)
    for i, xt in enumerate((140, 260, 380)):
        rect(c, xt, 260, xt + 70, 320, fill=WOOD, stroke=BROWN, lw=0.5)
        rect(c, xt + 15, 215, xt + 55, 252, fill=white, stroke=GREY, lw=0.5)
        rect(c, xt + 15, 328, xt + 55, 365, fill=white, stroke=GREY, lw=0.5, dash=(2, 1.5) if i == 2 else None)
    # alcôve (banquette existante)
    rect(c, 665, 0, 925, 55, fill=HexColor("#2c3e5c"), stroke=None)
    for xt in (675, 760, 845):
        rect(c, xt, 65, xt + 70, 130, fill=WOOD, stroke=BROWN, lw=0.5)
        rect(c, xt + 15, 140, xt + 55, 180, fill=white, stroke=GREY, lw=0.5)
    for xt in (680, 790):
        rect(c, xt, 260, xt + 80, 320, fill=WOOD, stroke=BROWN, lw=0.5)
        rect(c, xt + 20, 215, xt + 60, 252, fill=white, stroke=GREY, lw=0.5)
        rect(c, xt + 20, 328, xt + 60, 365, fill=white, stroke=GREY, lw=0.5, dash=(2, 1.5) if xt == 790 else None)
    rect(c, 935, 70, 977, 190, fill=HexColor("#ffe7a8"), stroke=ORANGE, lw=0.6)
    if labels:
        txt(c, 22, 240, "mange-debout", 4.2, "F", BROWN, rot=90)
        txt(c, 292, 27, "banquette", 4.4, "F", white)
        txt(c, 795, 27, "banquette existante", 4.4, "F", white)
        txt(c, 420, 385, "PMR", 4.2, "FB", BLUE); txt(c, 830, 385, "PMR", 4.2, "FB", BLUE)
        txt(c, 820, 405, "ESPACE DÉTENTE", 5.2, "FB", NAVY)
        txt(c, 956, 130, "desserte", 3.8, "F", BROWN, rot=90)
    # prépa froide (existante)
    rect(c, 830, 437, 975, 500, fill=HexColor("#cfe6f7"), stroke=NAVY, lw=0.5)
    rect(c, 667, 537, 730, 722, fill=HexColor("#cfe6f7"), stroke=NAVY, lw=0.5)
    rect(c, 800, 640, 900, 722, fill=HexColor("#dddddd"), stroke=GREY, lw=0.5)
    lm(c, 765, 437)
    if labels:
        txt(c, 902, 468, "armoire + existante", 4.2)
        txt(c, 698, 630, "saladette 3 portes\n(existante)", 4.0, rot=90)
        txt(c, 850, 681, "plan inox", 4.2)
        txt(c, 840, 570, "PRÉPA FROIDE", 5.4, "FB", NAVY)
    # niche vitrine + ex-pousse
    rect(c, 662, 742, 735, 828, fill=HexColor("#cfe6f7"), stroke=NAVY, lw=0.5)
    rect(c, 760, 745, 830, 815, fill=HexColor("#cfe6f7"), stroke=NAVY, lw=0.5)
    rect(c, 835, 745, 905, 815, fill=HexColor("#cfe6f7"), stroke=NAVY, lw=0.5)
    if labels:
        txt(c, 698, 785, "niche\nvitrine\n(stock\ntampon)", 3.6)
        txt(c, 832, 780, "2 armoires +", 3.8, "FB", NAVY)
    # cuisson (emprise du four Wind)
    rect(c, 650, 830, 1063, 1150, fill=None, stroke=RED, lw=0.9, dash=(4, 2))
    rect(c, 700, 1060, 790, 1145, fill=HexColor("#f6c9bd"), stroke=black, lw=0.5)
    rect(c, 797, 1060, 842, 1145, fill=HexColor("#f6c9bd"), stroke=black, lw=0.5)
    rect(c, 900, 1075, 1050, 1145, fill=HexColor("#cfe6f7"), stroke=black, lw=0.5)
    rect(c, 984, 856, 1058, 973, fill=HexColor("#dddddd"), stroke=GREY, lw=0.5)
    lm(c, 900, 975, new=True)
    if labels:
        txt(c, 745, 1102, "four mixte\n6 GN1/1", 4.0); txt(c, 820, 1102, "fri-\nteuse", 3.8)
        txt(c, 975, 1110, "plan réfrigéré", 4.0)
        txt(c, 1021, 915, "dressage\n(ex-table\nà plaquer)", 3.6)
        txt(c, 790, 930, "CUISSON", 6.5, "FB", RED)
        txt(c, 790, 965, "à l'emplacement\ndu four Wind", 4.4, "FI", RED)
    # plonge (existante)
    rect(c, 995, 8, 1088, 70, fill=HexColor("#dddddd"), stroke=GREY, lw=0.5)
    rect(c, 1092, 8, 1152, 70, fill=HexColor("#cfcfe8"), stroke=GREY, lw=0.5)
    rect(c, 995, 85, 1050, 190, fill=HexColor("#dddddd"), stroke=GREY, lw=0.5)
    if labels:
        txt(c, 1041, 39, "plonge", 4.2); txt(c, 1122, 39, "LV\nfrontal", 3.8)
        txt(c, 1095, 105, "PLONGE", 5.2, "FB", PURPLE)
    lm(c, 1110, 150)
    # DEGT N°1 : lave-mains existant
    lm(c, 990, 320)
    # réserve / vestiaires / chambre
    rect(c, 1170, 455, 1385, 490, fill=None, stroke=GREY, lw=0.5)
    rect(c, 1170, 655, 1385, 690, fill=None, stroke=GREY, lw=0.5)
    if labels:
        txt(c, 1277, 572, "RÉSERVE\nSÈCHE (CF)\nretail + emballages", 4.8, "FB", BROWN)
        txt(c, 1277, 55, "BUREAU", 5, "FB")
        txt(c, 1220, 192, "VEST. H", 4.6, "FB"); txt(c, 1337, 192, "WC", 4.6)
        txt(c, 1220, 360, "VEST. F", 4.6, "FB"); txt(c, 1337, 360, "WC", 4.6)
        txt(c, 1215, 975, "CHAMBRE FROIDE\nNÉGATIVE −18 °C\n(existante, conservée)\nbaos, gyozas,\npoulet pané, stock", 5.0, "FB", BLUE)
        txt(c, 1225, 765, "rampes existantes", 4.2, "FI", GREY)
        txt(c, 1075, 450, "DEGT N°1", 5.4, "FB", GREY, rot=90)
    # DEGT 2 : réception mobile, conteneurs, TGBT
    rect(c, 1488, 130, 1542, 330, fill=HexColor("#dddddd"), stroke=GREY, lw=0.5, dash=(2, 1.5))
    for i, yb in enumerate((820, 880, 940)):
        rect(c, 1420, yb, 1480, yb + 52, fill=HexColor("#b9d7a8") if i == 2 else HexColor("#cccccc"), stroke=GREY, lw=0.4)
    rect(c, 1495, 830, 1540, 880, fill=HexColor("#f1d58a"), stroke=GREY, lw=0.4)
    circle(c, 1435, 1040, 18, fill=HexColor("#8b5a2b"), stroke=None)
    if labels:
        txt(c, 1515, 230, "réception\n(table mobile)", 4.0, "FB", rot=90)
        txt(c, 1470, 450, "DEGT N°2", 5.4, "FB", GREY, rot=90)
        txt(c, 1517, 920, "huiles", 3.6)
        txt(c, 1505, 1010, "conte-\nneurs à\ncouvercle", 3.6, "FB", BROWN)
        txt(c, 1470, 1112, "TGBT (exist.)", 4.4, "FB")
        txt(c, DEPTH + 60, 65, "P1\nentrée\npersonnel\n+ livraisons", 4.6, "FB", NAVY, "l")
        txt(c, DEPTH + 60, 690, "P2\nsortie déchets\n+ issue de\nsecours", 4.6, "FB", BROWN, "l")
        txt(c, -45, 575, "ENTRÉE CLIENTS\n2 vantaux 2,40 m", 5.2, "FB", NAVY, rot=90)



def dims(c):
    # cotes générales
    y = WIDTH + 95
    line(c, 0, y, DEPTH, y, GREY, 0.4)
    for xx in (0, 655, 983, 1395, DEPTH): line(c, xx, y - 15, xx, y + 15, GREY, 0.4)
    for a, b in [(0, 655), (655, 983), (983, 1395), (1395, DEPTH)]:
        txt(c, (a + b) / 2, y - 22, f"{(b - a):.0f}", 5, "F", GREY)
    txt(c, DEPTH / 2, y + 30, "15,45 m (cotes relevées sur le DAT 2015 — à confirmer par relevé)", 5, "FI", GREY)
    x = DEPTH + 220
    line(c, x, 0, x, WIDTH, GREY, 0.4); line(c, x - 15, 0, x + 15, 0, GREY, 0.4); line(c, x - 15, WIDTH, x + 15, WIDTH, GREY, 0.4)
    txt(c, x + 22, WIDTH / 2, "11,50 m (1149,5)", 5, "F", GREY, rot=90)

def scale_bar(c, X, Y):
    c.saveState(); c.setFont("F", 6)
    for i in range(5):
        c.setFillColor(black if i % 2 == 0 else white); c.rect(X + i * 100 * S, Y, 100 * S, 4, fill=1, stroke=1)
    c.setFillColor(black)
    for i in range(6): c.drawCentredString(X + i * 100 * S, Y - 8, f"{i} m")
    c.drawString(X + 520 * S, Y, "Échelle 1/75 (A3)")
    c.restoreState()

def north(c, X, Y):
    c.saveState(); c.setFont("FB", 7); c.drawCentredString(X, Y, "Façade ← | → Fond de cellule"); c.restoreState()

# --------------------------------------------------------------------------- cartouche
def cartouche(c, titre, phase="ESQUISSE", ech="1/75", num=1):
    c.saveState()
    c.setFillColor(NAVY); c.rect(20, 18, W - 40, 52, fill=1, stroke=0)
    if os.path.exists(LOGO):
        c.setFillColor(white); c.roundRect(26, 22, 70, 44, 4, fill=1, stroke=0)
        c.drawImage(LOGO, 29, 24, 64, 40, preserveAspectRatio=True, mask="auto")
    c.setFillColor(white)
    c.setFont("FB", 9); c.drawString(108, 52, "L'ARBRE À MAKIS — SUSHIS · BOWLS · BAOS — PRÊT À MANGER")
    c.setFont("F", 7.5); c.drawString(108, 40, "Cellule n°09 — Espace commercial Marques Avenue — Rue du Bocage — 49280 La Séguinière")
    c.drawString(108, 29, "Reprise du local La Mie Câline — fond de plan : DAT ChauvierePajot du 20/03/2015")
    c.setStrokeColor(white); c.setLineWidth(0.5)
    for xx in (560, 660, 1010, 1110): c.line(xx, 22, xx, 66)
    c.setFont("F", 6.5); c.drawString(568, 54, "Phase"); c.setFont("FB", 9); c.drawString(568, 36, phase)
    c.setFont("FB", 11); c.drawCentredString(835, 42, titre)
    c.setFont("F", 6.5); c.drawString(1018, 54, "Échelle"); c.setFont("FB", 9); c.drawString(1018, 36, ech)
    c.setFont("F", 6.5); c.drawString(1118, 54, "Planche"); c.setFont("FB", 12); c.drawString(1118, 32, f"{num:02d}")
    c.setFillColor(GREY); c.setFont("FI", 6)
    c.drawString(22, 8, "Document de travail préparatoire (programme + esquisse d'aménagement). Il ne remplace pas les plans d'exécution ni la notice "
                        "d'un maître d'œuvre / bureau de contrôle. Cotes à vérifier sur site. Date : 17/11/2026.")
    c.restoreState()

def para(c, X, Y, w, text, size=8, font="F", lead=1.35, col=black):
    """Texte justifié simple à gauche, retourne Y final. '**' en début de ligne = gras."""
    c.saveState(); c.setFillColor(col)
    y = Y
    for raw in text.split("\n"):
        f = font; s = raw
        if s.startswith("**"): f = "FB"; s = s[2:]
        bullet = s.startswith("• ")
        indent = 9 if bullet else 0
        words = s.split(" "); cur = ""
        first = True
        for wd in words + [None]:
            test = (cur + " " + wd).strip() if wd is not None else None
            if wd is not None and pdfmetrics.stringWidth(test, f, size) <= w - (0 if first else indent):
                cur = test; continue
            c.setFont(f, size); c.drawString(X + (0 if first else indent), y, cur)
            y -= size * lead; first = False; cur = wd or ""
            if wd is None: break
        if raw == "": y -= size * 0.3
    c.restoreState(); return y

def table(c, X, Y, cols, rows, size=7, head_fill=NAVY, lead=1.25, zebra=True, pad=3):
    """cols: liste de (titre, largeur). Retourne Y bas."""
    c.saveState()
    def wrap(s, w, f):
        out = []
        for part in str(s).split("\n"):
            cur = ""
            for wd in part.split(" "):
                t = (cur + " " + wd).strip()
                if pdfmetrics.stringWidth(t, f, size) <= w - 2 * pad: cur = t
                else: out.append(cur); cur = wd
            out.append(cur)
        return out
    y = Y
    hh = size * lead + 2 * pad
    x = X
    c.setFillColor(head_fill); c.rect(X, y - hh, sum(w for _, w in cols), hh, fill=1, stroke=0)
    c.setFillColor(white); c.setFont("FB", size)
    for t, w in cols: c.drawString(x + pad, y - hh + pad + 1, t); x += w
    y -= hh
    for i, r in enumerate(rows):
        bold = isinstance(r, tuple) and len(r) == len(cols) + 1 and r[-1] == "B"
        cells = [wrap(v, w, "FB" if (bold or j == 0) else "F") for j, (v, (_, w)) in enumerate(zip(r, cols))]
        n = max(len(cc) for cc in cells); rh = n * size * lead + 2 * pad
        if zebra and i % 2 == 0:
            c.setFillColor(HexColor("#f2f4f8")); c.rect(X, y - rh, sum(w for _, w in cols), rh, fill=1, stroke=0)
        x = X
        for j, (cc, (_, w)) in enumerate(zip(cells, cols)):
            c.setFillColor(black); c.setFont("FB" if (bold or j == 0) else "F", size)
            for k, l in enumerate(cc): c.drawString(x + pad, y - pad - size * (k + 1) * lead + size * 0.25, l)
            x += w
        c.setStrokeColor(HexColor("#cccccc")); c.setLineWidth(0.3); c.line(X, y - rh, X + sum(w for _, w in cols), y - rh)
        y -= rh
    c.restoreState(); return y

def h1(c, X, Y, s, col=NAVY, size=15):
    c.saveState(); c.setFillColor(col); c.setFont("FB", size); c.drawString(X, Y, s)
    c.setStrokeColor(GREEN); c.setLineWidth(2); c.line(X, Y - 5, X + 60, Y - 5); c.restoreState()

def legend_box(c, X, Y, items, title):
    c.saveState(); c.setFont("FB", 8); c.setFillColor(NAVY); c.drawString(X, Y, title); y = Y - 14
    for kind, col, lab in items:
        c.setStrokeColor(col); c.setFillColor(col)
        if kind == "line": c.setLineWidth(2); c.line(X, y + 3, X + 22, y + 3)
        elif kind == "dash": c.setLineWidth(1.5); c.setDash(4, 2); c.line(X, y + 3, X + 22, y + 3); c.setDash()
        elif kind == "box": c.rect(X, y - 1, 22, 9, fill=1, stroke=0)
        elif kind == "dot": c.circle(X + 11, y + 3, 5, fill=1, stroke=0)
        c.setFillColor(black); c.setFont("F", 7); c.drawString(X + 30, y, lab); y -= 13
    c.restoreState(); return y

# =========================================================================== PAGES


def page_facade(c):
    h1(c, 40, H - 50, "10 — Façade et enseigne (caisson existant réhabillé)")
    s = 0.85; ox, oy = 110, 120
    def F(x, y): return ox + x * s, oy + y * s
    # bâtiment : largeur 1150 + poteaux ; égout +6.05 ; faîtage +11.75 (cm*0.1 -> on garde cm/ ratio)
    k = 0.6  # cm -> unités
    Wd = 1150 * k; h_eg = 605 * k; h_f = 1175 * k
    c.saveState()
    c.setFillColor(HexColor("#2b2f36")); p = c.beginPath()
    x0, y0 = F(0, 0)
    p.moveTo(*F(-40, h_eg)); p.lineTo(*F(Wd / 2, h_f)); p.lineTo(*F(Wd + 40, h_eg)); p.close(); c.drawPath(p, fill=1, stroke=0)
    c.setStrokeColor(HexColor("#4a505a")); c.setLineWidth(0.6)
    for i in range(1, 40):
        xx = -40 + i * (Wd + 80) / 40
        top = h_eg + (h_f - h_eg) * (1 - abs(xx - Wd / 2) / (Wd / 2 + 40))
        c.line(*F(xx, h_eg), *F(xx, top))
    c.setFillColor(HexColor("#c9ccd1"))
    for xx in (-40, Wd):
        X, Y = F(xx, 0); c.rect(X, Y, 40 * k * s, h_eg * s, fill=1, stroke=0)
    # bandeau enseigne
    c.setFillColor(NAVY); X, Y = F(0, 478 * k); c.rect(X, Y, Wd * s, 148 * k * s, fill=1, stroke=0)
    c.setFillColor(white); bx, by = F(Wd / 2 - 75, 478 * k + 6); c.roundRect(bx, by, 150 * s, (148 * k - 12) * s, 4, fill=1, stroke=0)
    c.drawImage(LOGO, bx + 3, by + 2, 150 * s - 6, (148 * k - 12) * s - 4, preserveAspectRatio=True, mask="auto")
    c.setFont("FB", 9); c.setFillColor(white)
    X, Y = F(30, 478 * k + 52); c.drawString(X, Y, "SUSHIS · BOWLS · BAOS")
    X, Y = F(30, 478 * k + 26); c.setFont("F", 7); c.drawString(X, Y, "PRÊT À MANGER — SUR PLACE OU À EMPORTER")
    X, Y = F(Wd - 30, 478 * k + 52); c.setFont("FB", 9); c.drawRightString(X, Y, "FRAIS · GOURMAND · RESPONSABLE")
    X, Y = F(Wd - 30, 478 * k + 26); c.setFont("F", 7); c.drawRightString(X, Y, "Préparé à Maulévrier")
    # vitrage
    c.setFillColor(HexColor("#cfe3ef")); X, Y = F(0, 0); c.rect(X, Y, Wd * s, 478 * k * s, fill=1, stroke=0)
    c.setStrokeColor(HexColor("#5a6b78")); c.setLineWidth(1)
    for xx in (Wd * 0.2, Wd * 0.4, Wd * 0.6, Wd * 0.8): c.line(*F(xx, 0), *F(xx, 478 * k))
    dx1, dx2 = Wd / 2 - 120 * k, Wd / 2 + 120 * k
    c.setFillColor(HexColor("#b5d3e6")); X, Y = F(dx1, 0); c.rect(X, Y, (dx2 - dx1) * s, 300 * k * s, fill=1, stroke=1)
    c.line(*F(Wd / 2, 0), *F(Wd / 2, 300 * k)); c.line(*F(dx1, 300 * k), *F(dx2, 300 * k))
    # bandes contrastées
    c.setStrokeColor(NAVY); c.setLineWidth(2.2)
    for hh in (110, 160): c.line(*F(0, hh * k), *F(Wd, hh * k))
    c.setFillColor(GREEN); c.setFont("FB", 6)
    # vitrophanie gauche (texte)
    c.setFillColor(NAVY); X, Y = F(30, 330 * k); c.setFont("FB", 11); c.drawString(X, Y, "Le goût du bon sens.")
    X, Y = F(Wd - 30, 330 * k); c.setFont("F", 8); c.drawRightString(X, Y, "Sushis · Bowls · Baos · Retail japonais")
    c.setFillColor(GREY); c.setFont("F", 7); X, Y = F(-40, -14); c.drawString(X, Y, "±0,00")
    X, Y = F(Wd / 2, h_f + 8); c.drawCentredString(X, Y, "+11,75"); X, Y = F(Wd + 45, h_eg); c.drawString(X, Y, "+6,05")
    c.restoreState()
    para(c, 880, H - 90, 280,
         "**Principe\n"
         "• Caisson d'enseigne existant conservé (bandeau 11,50 × 1,48 m, structure et alimentation) : seules les faces et les lettres changent.\n"
         "• Fond bleu marine, logo L'Arbre à Makis rétroéclairé sur caisson blanc au centre, lettres découpées blanches à gauche et à droite (bloc de messages repris de la perspective d'ambiance).\n"
         "• Vitrine : vitrophanie partielle qui laisse voir l'îlot et les vitrines, bandes contrastées à 1,10 m et 1,60 m (accessibilité), horaires et allergènes/QR code sur la porte.\n"
         "• Coupure d'urgence de l'enseigne lumineuse conservée.\n"
         "\n"
         "**Autorisations\n"
         "• Validation par le bailleur / la direction du centre (charte enseignes Marques Avenue) avant toute fabrication.\n"
         "• Demande d'autorisation d'enseigne en mairie si la commune ou l'Agglomération du Choletais a un règlement local de publicité : à vérifier en mairie de La Séguinière.\n"
         "\n"
         "**Vue d'insertion\n"
         "À produire par l'enseigniste à partir de la photo 1 du DAT 2015 (même point de vue) pour le dossier mairie / centre.", 8)
    cartouche(c, "FAÇADE ET ENSEIGNE", phase="ESQUISSE V2", ech="≈ 1/55", num=10)


# =========================================================================== PAGES V2
def label_min(c, items):
    for (x, y, s) in items: txt(c, x, y, s, 6, "FB", HexColor("#333333"))

def page_cover(c):
    c.setFillColor(NAVY); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(white); c.roundRect(W / 2 - 170, H - 330, 340, 240, 10, fill=1, stroke=0)
    c.drawImage(LOGO, W / 2 - 150, H - 320, 300, 220, preserveAspectRatio=True, mask="auto")
    c.setFillColor(white); c.setFont("FB", 24)
    c.drawCentredString(W / 2, H - 390, "DOSSIER D'ADAPTATION DU LOCAL — V2 « RÉEMPLOI MAXIMAL »")
    c.setFont("F", 14)
    c.drawCentredString(W / 2, H - 418, "Point de vente « prêt-à-manger » japonais — libre-service, retail, consommation sur place, cuisson à l'arrière")
    c.drawCentredString(W / 2, H - 438, "Aucune cloison déplacée, aucun gros œuvre : on s'installe dans les murs, les réseaux et l'extraction de La Mie Câline")
    c.setStrokeColor(GREEN); c.setLineWidth(2); c.line(W / 2 - 200, H - 456, W / 2 + 200, H - 456)
    c.setFont("FB", 12)
    c.drawCentredString(W / 2, H - 484, "CELLULE N°09 — ESPACE COMMERCIAL MARQUES AVENUE — RUE DU BOCAGE — 49280 LA SÉGUINIÈRE")
    c.setFont("F", 10.5)
    c.drawCentredString(W / 2, H - 504, "Reprise du local exploité par La Mie Câline (DAT « terminal de cuisson », ChauvierePajot, 20/03/2015)")
    c.setFont("FB", 10); c.drawString(170, 300, "PIÈCES DU DOSSIER")
    pieces = ["01  Programme et tableau des surfaces", "02  Réemploi de l'existant : ce que l'on garde, élément par élément",
              "03  Plan RDC projeté (existant conservé / créé)", "04  Plan hygiène — marche en avant, flux et températures (DDPP)",
              "05  Espace cuisson à l'emplacement du four Wind", "06  Plan de sécurité incendie (ERP N + M)", "07  Plan d'accessibilité PMR",
              "08  Notice hygiène — check-list DDPP", "09  Travaux strictement nécessaires (et ce que l'on évite)",
              "10  Façade et enseigne (caisson existant réhabillé)", "11  Démarches, calendrier et points à valider"]
    c.setFont("F", 9.5)
    for i, p in enumerate(pieces): c.drawString(170, 282 - i * 15, p)
    c.setFont("FB", 10); c.drawString(700, 300, "STATUT DU DOCUMENT")
    para(c, 700, 282, 330, "Version 2 du 17/11/2026, qui remplace la V1 : même concept, mais tout est calé sur les cloisons, réseaux et équipements existants pour réduire l'investissement.\n"
         "Fond de plan redessiné d'après le DAT 2015 (précision ± 10 cm, cotes non relevées sur site).\n"
         "Les pièces réglementaires (Cerfa 13824, notices signées) restent à produire par le maître d'œuvre à partir de ce programme.", 9, col=white)
    c.setFont("F", 8); c.setFillColor(HexColor("#b8c2d6")); c.drawString(170, 50, "L'Arbre à Makis — produits préparés à Maulévrier — V2 du 17/11/2026")

def page_programme(c):
    h1(c, 40, H - 50, "01 — Programme et principe : s'installer dans l'existant")
    para(c, 40, H - 80, 620,
        "**La règle de la V2\n"
        "On ne déplace aucune cloison, on ne crée aucune ouverture dans un mur et on ne touche ni aux sols, ni aux plafonds, ni à la façade. Chaque fonction de L'Arbre à Makis est posée là où La Mie Câline avait déjà les murs, l'eau, l'électricité ou l'extraction nécessaires. Les seuls travaux sont des raccordements de second œuvre (planche 09).\n"
        "\n"
        "**Ce qui va où\n"
        "• Cuisson : four mixte + friteuse (≈ 19 kW) sur les 1,46 m occupés par le four Wind, sous l'extraction existante et sur sa ligne électrique. La verrière laisse voir la cuisson depuis la boutique.\n"
        "• Préparation froide : la pièce existante, avec sa saladette 3 portes, son armoire positive et son lave-mains.\n"
        "• Froid : la chambre froide reste négative (surgelés : baos, gyozas, poulet pané, stock). Le frais du jour est stocké dans 2 armoires positives posées à l'emplacement de l'armoire de pousse (prise déjà en place) et dans l'armoire de la prépa.\n"
        "• Murale libre-service de 4,80 m le long du mur où se trouvaient les meubles bas et la vitrine boissons de La Mie Câline (alimentations électriques déjà sur ce mur). Modèle à groupe logé : pas de groupe en toiture ni de liaisons frigorifiques.\n"
        "• Caisse : un comptoir mobile devant la verrière de la prépa. La zone de service derrière rejoint la porte existante vers la cuisson.\n"
        "• Salle : la zone tables et mange-debout de La Mie Câline + l'alcôve avec sa banquette.\n"
        "• Plonge, vestiaires, WC, bureau, réserve CF, local TGBT : inchangés.\n"
        "• Déchets : conteneurs à couvercle dans le recoin derrière la porte P2, sans local maçonné.\n"
        "\n"
        "**Ce que l'on a retiré par rapport à la V1\n"
        "Cloisonnement de la cuisson, passe chaude percée dans la verrière, local déchets construit, reconversion de la chambre froide en positif, reprise des sols de la cuisson : rien de tout cela n'est nécessaire si l'existant est en bon état.\n"
        "\n"
        "**La contrepartie à accepter\n"
        "Il n'y a qu'une seule porte entre l'avant et l'arrière, celle de La Mie Câline, qui donne dans la cuisson. Le réassort de la murale, les produits chauds et les déchets de la salle passent tous par là. La DDPP l'accepte si les produits circulent en bacs fermés et si les flux sont séparés dans le temps, ce qui est écrit dans le PMS (planche 04). C'est déjà ainsi que fonctionnait La Mie Câline.", 8.4)
    rows = []; tot = 0
    for lab, rects in SURF:
        a = area(rects); tot += a; rows.append((lab, f"{a:.1f} m²"))
    rows.append(("TOTAL intérieur (hors cloisons)", f"{tot:.1f} m²", "B"))
    c.setFont("FB", 10); c.setFillColor(NAVY); c.drawString(700, H - 80, "Tableau des surfaces (plan redessiné)")
    y = table(c, 700, H - 90, [("Zone", 300), ("Surface", 80)], rows, 7.4)
    rows2 = [("Mange-debout en vitrine (emplacement La Mie Câline)", "5"), ("Tables + banquette côté mur haut", "14"),
             ("Espace détente, alcôve avec banquette existante", "10"), ("Total intérieur (dont 2 places PMR)", "29", "B"),
             ("Terrasse sous auvent (saisonnier, accord centre)", "≈ 16")]
    c.setFont("FB", 10); c.setFillColor(NAVY); c.drawString(700, y - 22, "Places assises (La Mie Câline : 53)")
    y = table(c, 700, y - 32, [("Emplacement", 300), ("Places", 80)], rows2, 7.4)
    para(c, 700, y - 18, 400,
         "**Loi AGEC : au-delà de 20 personnes servies en même temps (intérieur + terrasse, assises ou debout), la vaisselle doit être réutilisable pour la consommation sur place. Le lave-vaisselle frontal se loge dans la plonge existante. Le cas des produits vendus préemballés en libre-service puis mangés sur place reste à faire confirmer.", 7.6)
    cartouche(c, "PROGRAMME ET SURFACES", phase="ESQUISSE V2", ech="—", num=1)

def page_reemploi(c):
    h1(c, 40, H - 50, "02 — Réemploi de l'existant : ce que l'on garde, élément par élément")
    cols = [("Élément existant (DAT 2015)", 270), ("Usage L'Arbre à Makis", 400), ("Travaux", 300), ("Condition / à vérifier", 160)]
    rows = [
     ("Enveloppe, murs mitoyens CF 1 h, façade vitrée, porte 2 vantaux 2,40 m", "Inchangés", "Aucun", "—"),
     ("Cloisons du back-office : prépa froide, plonge, vestiaires H/F + WC, bureau, réserve CF, local TGBT, muret cuisson, niche vitrine", "Toutes gardées, avec la même fonction (sauf l'ex-pousse, qui devient le stockage frais)", "Aucun", "État des lieux"),
     ("Verrières prépa froide / cuisson, imposte vitrée de l'alcôve", "Gardées : la cuisson et la prépa restent visibles depuis la boutique", "Nettoyage", "—"),
     ("Porte vente → cuisson (bas de la verrière)", "Seule liaison avant / arrière : réassort, retrait chaud, retour des déchets de la salle", "Aucun", "Flux séparés dans le temps (PMS)"),
     ("Sols (carrelage arrière, sol de la vente), plafonds (dalles métalliques, plafond plâtre)", "Conservés", "Réparations ponctuelles seulement", "Joints et plinthes de la cuisson en bon état"),
     ("Extraction : conduit SF ¼ h, extracteur 400 °C ½ h, écran de cantonnement, arrêts d'urgence", "Gardés pour four mixte + friteuse à l'emplacement du four Wind", "Ramonage, contrôle, filtres à chocs", "Hotte encore en place ?"),
     ("Ligne électrique du four Wind", "Alimente four mixte + friteuse (≈ 19 kW, sans doute moins que le four à sole)", "Contrôle", "Section et protection"),
     ("Chambre froide 3 × 3 m négative + groupe", "Reste en négatif : surgelés et stock", "Aucun", "Contrôle frigoriste"),
     ("Armoire positive + saladette 3 portes de la prépa", "Gardées telles quelles", "Aucun", "Cédées avec le local ?"),
     ("Prise de l'armoire de pousse", "2 armoires positives plug-in (frais du jour)", "Aucun", "—"),
     ("Alimentations des meubles bas turbochef / vitrine boissons (mur bas)", "Murale libre-service 4,80 m à groupe logé", "Prises à adapter si besoin", "Puissance de la murale"),
     ("Niche vitrine boissons dans la cloison", "Vitrine boissons ou stock tampon côté comptoir", "Aucun", "—"),
     ("Lave-mains : prépa, DEGT N°1, plonge, WC", "Conservés", "Aucun", "Commande non manuelle ?"),
     ("Plonge", "Conservée + lave-vaisselle frontal (vaisselle réutilisable)", "Raccordement sur les attentes en place", "—"),
     ("Éclairage (plan Easylum), BAES, extincteurs, coupure enseigne", "Conservés ; spots réorientés vers la murale et l'îlot", "Réglage, 1 ou 2 déplacements", "—"),
     ("Caisson d'enseigne bandeau 11,50 × 1,48 m", "Conservé, nouvelles faces L'Arbre à Makis", "Faces et lettres seulement", "Charte du centre"),
     ("Banquette de l'alcôve, mange-debout en vitrine", "Conservés", "Aucun", "Cédés avec le local ?"),
    ]
    y = table(c, 40, H - 70, cols, rows, 7.3)
    para(c, 40, y - 18, 1100,
         "**Le levier n°1 sur l'investissement n'est pas dans les travaux : c'est la reprise du matériel. Avant de signer, il faut un inventaire contradictoire de ce que La Mie Câline laisse et de ce qu'elle emporte (hotte, chambre froide et groupe, saladette, armoire positive, banquette, mange-debout, lave-mains), avec son état. Ce qui est déjà en place doit être soit repris pour un prix symbolique, soit déduit du droit d'entrée. Chaque équipement manquant redevient un achat.", 8.2)
    cartouche(c, "RÉEMPLOI DE L'EXISTANT", phase="ESQUISSE V2", ech="—", num=2)

def page_plan(c):
    draw_shell(c); draw_equipment(c); dims(c)
    scale_bar(c, 150, 120)
    c.setFont("FB", 12); c.setFillColor(NAVY); c.drawString(40, H - 40, "03 — Plan RDC projeté : existant conservé, aucune cloison créée")
    X = 905; y = H - 75
    c.setFont("FB", 9); c.setFillColor(NAVY); c.drawString(X, y, "Parcours client"); y -= 14
    y = para(c, X, y, 272,
             "1. Entrée face à l'îlot « L'Arbre » (produits phares + retail).\n"
             "2. Murale libre-service le long du mur bas : sushis → rolls & bowls → baos → desserts & boissons.\n"
             "3. Caisse devant la verrière de la prépa : 2 postes dont 1 PMR, retrait des produits chauds en bout de comptoir.\n"
             "4. Places dans la zone salle de La Mie Câline et dans l'alcôve.", 7.3)
    y -= 6
    c.setFont("FB", 9); c.setFillColor(NAVY); c.drawString(X, y, "Back-office (inchangé)"); y -= 14
    y = para(c, X, y, 272,
             "• Cuisson à la place du four Wind, sous l'extraction existante.\n"
             "• Frais : armoire de la prépa + 2 armoires à la place de l'armoire de pousse.\n"
             "• Surgelés : chambre froide négative existante.\n"
             "• Réception sur table mobile à P1, conteneurs à couvercle au-delà de P2.\n"
             "• Seuls ajouts : 2 lave-mains (caisse, cuisson). En option, une passe desserte dans la cloison légère de la plonge.", 7.3)
    y -= 8
    y = legend_box(c, X, y, [("box", WALL, "Cloisons / murs existants conservés"), ("box", HexColor("#bfe0f5"), "Verrières existantes"),
                             ("box", MAG, "Créé : lave-mains, option passe desserte (pointillé)"),
                             ("box", HexColor("#f6f1e7"), "Espace public (vente + salle)"), ("box", HexColor("#eef3e6"), "Zone service derrière comptoir"),
                             ("box", HexColor("#e3f0fb"), "Préparation froide"), ("box", HexColor("#fde9e3"), "Cuisson (zone existante)"),
                             ("box", HexColor("#efe7f7"), "Plonge"), ("box", HexColor("#dcecff"), "Chambre froide négative"),
                             ("box", HexColor("#fff6d9"), "Réserve sèche"), ("box", HexColor("#efe2d3"), "Conteneurs déchets"),
                             ("dot", BLUE, "Lave-mains existant")], "Légende")
    cartouche(c, "PLAN RDC PROJETÉ", phase="ESQUISSE V2", num=3)

def tag(c, x, y, s, col):
    X, Y = P(x, y); c.saveState(); c.setFillColor(white); c.setStrokeColor(col)
    wdt = pdfmetrics.stringWidth(s, "FB", 6) + 6; c.roundRect(X - wdt / 2, Y - 5, wdt, 11, 3, fill=1, stroke=1)
    c.setFillColor(col); c.setFont("FB", 6); c.drawCentredString(X, Y - 2, s); c.restoreState()

def page_hygiene(c):
    draw_shell(c, terrace_text=False); draw_equipment(c, labels=False)
    label_min(c, [(290, 1107, "MURALE LS"), (220, 735, "ÎLOT"), (507, 640, "CAISSE"), (840, 560, "PRÉPA FROIDE"),
                  (790, 930, "CUISSON"), (1072, 120, "PLONGE"), (1215, 990, "CH. NÉGATIVE"), (1277, 572, "RÉSERVE"),
                  (1277, 250, "VESTIAIRES / WC"), (1470, 960, "DÉCHETS")])
    G = HexColor("#2e8b57")
    arrow_path(c, [(DEPTH + 40, 65), (1460, 65), (1460, 760), (1250, 760), (1250, 840)], G)
    arrow_path(c, [(1460, 585), (1400, 585)], G, lw=1.2)
    arrow_path(c, [(1200, 760), (1000, 790), (920, 790)], G)
    arrow_path(c, [(870, 760), (955, 715), (900, 650)], G, lw=1.2)
    arrow_path(c, [(800, 600), (955, 715), (960, 840), (700, 1000), (680, 1095), (600, 1095), (600, 990), (440, 990), (300, 1050)], G, dash=(5, 2))
    arrow_path(c, [(760, 1040), (690, 1095), (600, 1095), (600, 870), (548, 860)], HexColor("#c0392b"))
    arrow_path(c, [(1100, 210), (1100, 718), (1460, 718), (1460, 815)], BROWN, dash=(2, 2))
    arrow_path(c, [(1530, 900), (1530, 700), (DEPTH + 45, 700)], BROWN, dash=(2, 2))
    arrow_path(c, [(400, 200), (600, 160), (930, 120), (1015, 130)], ORANGE, dash=(6, 2))
    arrow_path(c, [(DEPTH + 40, 40), (1420, 40), (1420, 190), (1370, 190)], BLUE, lw=1.2)
    arrow_path(c, [(-60, 575), (60, 575), (60, 960), (420, 1000)], GREY, lw=1.2)
    arrow_path(c, [(420, 1000), (400, 900), (420, 760), (465, 640)], GREY, lw=1.2)
    for (x, y, s, col) in [(290, 1020, "0/+3 °C", BLUE), (1215, 1070, "−18 °C", BLUE), (870, 830, "0/+3 °C", BLUE),
                           (902, 515, "0/+3 °C", BLUE), (760, 1015, "≥ 63 °C maintien", RED)]:
        tag(c, x, y, s, col)
    for (x, y, s) in [(1500, 110, "1"), (1440, 600, "2"), (1250, 900, "3"), (950, 780, "3'"), (820, 660, "4"), (870, 1000, "4'"),
                      (620, 1040, "5"), (500, 940, "6"), (1050, 120, "7"), (1490, 840, "8")]:
        badge(c, x, y, s, NAVY)
    c.setFont("FB", 12); c.setFillColor(NAVY); c.drawString(40, H - 40, "04 — Plan hygiène : marche en avant, flux et températures")
    X = 905; y = H - 70
    y = legend_box(c, X, y, [("line", G, "Produits (labo → stockage → prépa → vitrine)"),
                             ("line", HexColor("#c0392b"), "Produits chauds (cuisson → retrait)"),
                             ("dash", BROWN, "Déchets (→ conteneurs → P2)"), ("dash", ORANGE, "Vaisselle sale (option passe desserte)"),
                             ("line", BLUE, "Personnel"), ("line", GREY, "Clients")], "Flux")
    y -= 4
    c.setFont("FB", 9); c.setFillColor(NAVY); c.drawString(X, y, "Étapes"); y -= 13
    y = para(c, X, y, 272,
             "1 Réception à P1 : T° à cœur, DLC, décartonnage, bacs navettes du labo.\n"
             "2 Retail et sec en réserve CF.  3 Surgelés en chambre négative.  3' Frais du jour en armoires positives.\n"
             "4 Prépa froide : assemblage, étiquetage.  4' Cuisson minute.\n"
             "5 Passage par la porte existante cuisson → zone service.\n"
             "6 Réassort de la murale par le portillon, retrait chaud au comptoir.\n"
             "7 Plonge.  8 Déchets en sacs fermés → conteneurs → P2.", 7.1)
    y -= 4
    c.setFont("FB", 9); c.setFillColor(RED); c.drawString(X, y, "Points à cadrer dans le PMS (pas de travaux)"); y -= 13
    para(c, X, y, 272,
         "• Une seule porte avant / arrière, et elle passe par la cuisson. Le réassort se fait en bacs fermés, hors coup de feu, jamais en même temps qu'un retour de déchets. Les déchets de la salle sortent en sacs fermés, après le service.\n"
         "• Le couloir des rampes est partagé entre livraisons et déchets : livraisons le matin, déchets après le service, nettoyage entre les deux.\n"
         "• Vaisselle sale : sans la passe desserte (option), elle part en bac fermé par la même porte, hors rush. La passe (petite ouverture dans une cloison légère) simplifie beaucoup le circuit : à arbitrer.\n"
         "• Déchets sans local maçonné : conteneurs à couvercle et pédale, sol lavable, évacuation chaque jour vers l'aire du centre. À présenter tel quel à la DDPP.", 7.1)
    cartouche(c, "HYGIÈNE — MARCHE EN AVANT", phase="ESQUISSE V2", num=4)

def page_cuisson(c):
    h1(c, 40, H - 50, "05 — Espace cuisson : à l'emplacement du four Wind, sans travaux de structure")
    s2 = 28.3465 / 25.0
    ox, oy = 150, H - 100
    def Q(x, y): return ox + (x - 640) * s2, oy - (y - 720) * s2
    def R(x1, y1, x2, y2, fill=None, stroke=black, lw=0.6, dash=None):
        X1, Y1 = Q(x1, y1); X2, Y2 = Q(x2, y2); c.saveState(); c.setLineWidth(lw)
        if dash: c.setDash(list(dash))
        if fill is not None: c.setFillColor(fill)
        c.setStrokeColor(stroke if stroke is not None else black)
        c.rect(min(X1, X2), min(Y1, Y2), abs(X2 - X1), abs(Y2 - Y1), fill=1 if fill is not None else 0, stroke=1 if stroke is not None else 0)
        c.restoreState()
    def T(x, y, s, size=7, font="F", col=black):
        X, Y = Q(x, y); c.saveState(); c.setFillColor(col); c.setFont(font, size)
        ls = s.split("\n")
        for i, l in enumerate(ls): c.drawCentredString(X, Y + (len(ls) - 1) * size * 0.6 - i * size * 1.2 - size * 0.35, l)
        c.restoreState()
    R(655, 837, 1058, 1150, fill=HexColor("#fde9e3"), stroke=None)
    R(655, 733, 1058, 837, fill=HexColor("#f4f4f4"), stroke=None)
    R(640, 1150, 1075, 1175, fill=RED, stroke=None)
    for (x1, y1, x2, y2) in [(655, 727, 930, 739), (735, 733, 747, 837), (655, 831, 741, 843), (887, 948, 899, 1150)]:
        R(x1, y1, x2, y2, fill=WALL, stroke=None)
    R(651, 837, 659, 1053, fill=HexColor("#bfe0f5"), stroke=BLUE)
    R(651, 727, 659, 837, fill=WALL, stroke=None)
    R(1058, 830, 1066, 1150, fill=BLUE, stroke=None)
    R(650, 830, 1063, 1148, stroke=RED, lw=1.2, dash=(5, 3))
    R(700, 1060, 790, 1145, fill=HexColor("#f6c9bd")); T(745, 1102, "Four mixte\n6 GN 1/1\n≈ 10 kW", 6.3)
    R(797, 1060, 842, 1145, fill=HexColor("#f6c9bd")); T(820, 1102, "Fri-\nteuse\n10 L\n≈ 9 kW", 6)
    R(900, 1075, 1050, 1145, fill=HexColor("#cfe6f7")); T(975, 1110, "Plan réfrigéré\n(garnitures baos)", 6.3)
    R(984, 856, 1058, 973, fill=HexColor("#dddddd"), stroke=GREY); T(1021, 915, "Dressage\n(ex-table\nà plaquer)", 6)
    R(900, 975, 940, 1013, fill=white, stroke=MAG, lw=1.2); T(920, 994, "LM", 6, "FB", MAG)
    R(760, 745, 830, 815, fill=HexColor("#cfe6f7")); R(835, 745, 905, 815, fill=HexColor("#cfe6f7"))
    T(795, 780, "armoire +", 5.5, "FB", NAVY); T(870, 780, "armoire +", 5.5, "FB", NAVY)
    T(990, 790, "sur la prise de\nl'ex-armoire\nde pousse", 5.5, "FI", NAVY)
    R(662, 742, 735, 828, fill=HexColor("#cfe6f7")); T(698, 785, "niche\nexistante", 5.5)
    # cote emprise four Wind
    X1, Y1 = Q(696, 1046); X2, Y2 = Q(842, 1046)
    c.setStrokeColor(RED); c.setLineWidth(0.6); c.line(X1, Y1, X2, Y2); c.line(X1, Y1 - 3, X1, Y1 + 3); c.line(X2, Y2 - 3, X2, Y2 + 3)
    T(769, 1036, "emprise ex-four Wind 1,46 m", 6, "FB", RED)
    T(800, 900, "ZONE CUISSON EXISTANTE (≈ 12,6 m²)", 8.5, "FB", RED)
    T(800, 925, "écran de cantonnement, conduit et extracteur conservés", 6.5, "FI", RED)
    T(600, 1094, "porte\nexistante\n→ zone\nservice", 6, "FI", GREY)
    T(600, 940, "verrière\nexistante", 6, "FI", BLUE)
    T(990, 745, "DEGT / ex-pousse", 6, "FI", GREY)
    X, Y = Q(1035, 1060); c.setFillColor(RED); c.circle(X, Y, 6, fill=1, stroke=0); c.setFillColor(white); c.setFont("FB", 5); c.drawCentredString(X, Y - 2, "F")
    c.setFont("FI", 7); c.setFillColor(GREY); c.drawString(ox, oy - 470 * s2 - 12, "Zoom échelle 1/25 — gris foncé = existant conservé ; magenta = créé ; F = extincteur classe F + couverture anti-feu")
    X = 690; y = H - 80
    rows = [("Four mixte 6 niveaux GN 1/1", "10", "Baos (vapeur), remise en T° gyozas, karaage, plats chauds du labo"),
            ("Friteuse électrique 1 bac 10 L", "9", "Poulet croustillant, gyozas frits, tempura"),
            ("Plan réfrigéré", "—", "Garnitures et sauces des baos"),
            ("Rampe chauffante au retrait (comptoir)", "≈ 1", "Maintien ≥ 63 °C quelques minutes"),
            ("TOTAL cuisson", "≈ 19", "Sous le seuil de 20 kW : pas de « grande cuisine »", "B")]
    c.setFont("FB", 10); c.setFillColor(NAVY); c.drawString(X, y, "Équipement (électrique, posé, aucun gros œuvre)")
    y = table(c, X, y - 10, [("Appareil", 160), ("kW", 35), ("Usage", 265)], rows, 7.4)
    y -= 18
    c.setFont("FB", 10); c.setFillColor(NAVY); c.drawString(X, y, "Pourquoi exactement à cet endroit"); y -= 14
    y = para(c, X, y, 460,
             "• Four mixte (90 cm) + friteuse (45 cm) = 1,35 m : ça tient dans les 1,46 m du four Wind.\n"
             "• Ils restent sous l'extraction existante : conduit SF ¼ h, extracteur 400 °C ½ h et commandes d'arrêt d'urgence ont été acceptés en 2015.\n"
             "• La ligne électrique du four à sole sert pour les deux appareils. Un four à sole de boulangerie consomme en général autant ou plus que 19 kW, ce qui reste à vérifier sur la plaque du four ou le TGBT.\n"
             "• La verrière existante donne une cuisson « vitrine », sans aucun percement.\n"
             "• La table à plaquer devient le plan de dressage. Le muret existant sépare la cuisson du plan réfrigéré.\n"
             "• En restant sous 20 kW, l'écran de cantonnement de La Mie Câline n'est plus obligatoire : on le garde (coût zéro) plutôt que de le déposer.", 7.8)
    y -= 4
    c.setFont("FB", 10); c.setFillColor(NAVY); c.drawString(X, y, "Les seuls postes cuisson à budgéter"); y -= 14
    para(c, X, y, 460,
         "• Hotte : si celle du four Wind est encore là, on change seulement les filtres (filtres à chocs, obligatoires avec une friteuse) et on fait ramoner et contrôler le conduit. Si elle a été déposée, il faut une hotte murale d'environ 1,80 m raccordée sur le conduit existant. C'est le seul vrai poste cuisson du projet : à trancher à l'état des lieux.\n"
         "• Eau et vidange du four mixte : à piquer sur l'arrivée du four Wind (les fours à sole à buée en ont une) ou sur le réseau de la prépa, à 3 m. La bonde de sol du plaquage sert à l'évacuation.\n"
         "• Lave-mains à commande non manuelle en cuisson, sur la même arrivée d'eau.\n"
         "• Extincteur classe F + couverture anti-feu.\n"
         "• Ne pas ajouter d'appareil plus tard (cuiseur vapeur, wok…) sans refaire le compte des 20 kW.", 7.8)
    cartouche(c, "ESPACE CUISSON", phase="ESQUISSE V2", ech="1/25", num=5)

def page_incendie(c):
    draw_shell(c, cf=True, terrace_text=False); draw_equipment(c, labels=False)
    label_min(c, [(290, 1107, "MURALE LS"), (220, 735, "ÎLOT"), (507, 640, "CAISSE"), (840, 560, "PRÉPA FROIDE"),
                  (790, 930, "CUISSON"), (1072, 120, "PLONGE"), (1215, 990, "CH. NÉGATIVE"), (1277, 572, "RÉSERVE"), (1470, 960, "CONTENEURS")])
    txt(c, 860, 1180, "écran de cantonnement existant conservé (h ≥ 0,50 m)", 5, "FB", RED)
    arrow_path(c, [(770, 1090), (900, 900), (1250, 720), (1500, 330), (DEPTH, 300)], RED, lw=1, dash=(3, 2), head=False)
    txt(c, 1330, 460, "conduit d'extraction existant\nM0 / A2-s1,d0 – SF ¼ h", 5, "FI", RED)
    GG = HexColor("#1a9e3f")
    arrow_path(c, [(200, 575), (-80, 575)], GG, lw=3)
    arrow_path(c, [(1470, 700), (DEPTH + 70, 690)], GG, lw=3)
    arrow_path(c, [(1470, 120), (DEPTH + 70, 65)], GG, lw=2)
    txt(c, 150, 540, "dégagement principal 2 UP (2,40 m)", 5.5, "FB", GG)
    for (x, y) in [(15, 420), (15, 730), (1530, 640), (1530, 120), (1100, 500), (800, 400), (600, 1100)]:
        X, Y = P(x, y); c.setFillColor(GG); c.rect(X - 6, Y - 3, 12, 6, fill=1, stroke=0)
    for (x, y, k) in [(60, 700, "E"), (630, 560, "E"), (870, 1030, "F"), (1000, 790, "C"), (1480, 1100, "C"), (1500, 450, "E")]:
        X, Y = P(x, y); c.setFillColor(RED); c.circle(X, Y, 6, fill=1, stroke=0); c.setFillColor(white); c.setFont("FB", 6); c.drawCentredString(X, Y - 2, k)
    X, Y = P(620, 1040); c.setFillColor(RED); c.rect(X - 7, Y - 7, 14, 14, fill=1, stroke=0)
    X, Y = P(20, 470); c.setFillColor(ORANGE); c.rect(X - 5, Y - 5, 10, 10, fill=1, stroke=0)
    c.setFont("FB", 12); c.setFillColor(NAVY); c.drawString(40, H - 40, "06 — Plan de sécurité incendie (ERP type N + M, 5e catégorie)")
    X = 905; y = H - 70
    y = legend_box(c, X, y, [("line", RED, "Parois coupe-feu existantes (mitoyens CF 1 h, réserve, TGBT)"),
                             ("dash", RED, "Écran de cantonnement / conduit d'extraction existants"),
                             ("line", GG, "Dégagements / sens d'évacuation"), ("box", GG, "BAES"),
                             ("dot", RED, "Extincteurs : E eau 6 L · C CO₂ 2 kg · F classe F"),
                             ("box", RED, "Arrêts d'urgence cuisson / élec. / ventilation (existants)"),
                             ("box", ORANGE, "Coupure d'urgence enseigne (existante)")], "Légende sécurité")
    y -= 6
    para(c, X, y, 272,
         "**Classement (estimation à confirmer)\n"
         "Type N + M. Effectif : 29 places + vente ≈ 75 personnes, contre 53 places pour La Mie Câline. 5e catégorie, sans changement.\n"
         "**Aucune modification du recoupement\n"
         "Murs CF, réserve CF, local TGBT, dégagements, écran de cantonnement, conduit et commandes d'arrêt : tout est conservé. Cuisson ramenée sous 20 kW, donc un risque plus faible qu'avec le four à sole.\n"
         "**Seuls ajustements\n"
         "• Extincteur classe F + couverture anti-feu près de la friteuse.\n"
         "• 1 ou 2 BAES / extincteurs déplacés selon le mobilier.\n"
         "• Conteneurs déchets dans le cul-de-sac au-delà de P2 : hors cheminement d'évacuation, à faire valider par le bureau de contrôle (sinon, aire extérieure du centre).\n"
         "• Décor (arbre, végétal, bois) : réaction au feu M1 / B-s3,d0, végétal stabilisé ou artificiel classé.\n"
         "• Attestations à jour : ramonage du conduit, électricité, extincteurs, registre de sécurité.", 7.2)
    cartouche(c, "SÉCURITÉ INCENDIE", phase="ESQUISSE V2", num=6)

def page_pmr(c):
    draw_shell(c, terrace_text=False); draw_equipment(c, labels=False)
    label_min(c, [(290, 1107, "MURALE LS"), (220, 735, "ÎLOT"), (840, 560, "PRÉPA FROIDE"), (790, 930, "CUISSON")])
    G = HexColor("#1a9e3f")
    for (cx, cy) in [(400, 530), (420, 985), (330, 410)]:
        circle(c, cx, cy, 75, fill=None, stroke=G, lw=1)
    txt(c, 400, 610, "Ø 1,50 m", 5, "FB", G)
    for (a, b, xx, lab) in [(850, 1065, 220, "2,15 m"), (900, 1065, 507, "1,65 m")]:
        line(c, xx, a, xx, b, G, 0.8); txt(c, xx + 22, (a + b) / 2, lab, 5.5, "FB", G, rot=90)
    line(c, 330, 760, 470, 760, G, 0.8); txt(c, 400, 748, "1,40 m", 5.5, "FB", G)
    arrow_path(c, [(-80, 575), (60, 575), (60, 960), (420, 1000)], G, lw=1.6)
    arrow_path(c, [(60, 575), (380, 560), (465, 515)], G, lw=1.6)
    for (x, y, s) in [(507, 515, "caisse PMR"), (415, 345, "table PMR"), (830, 345, "table PMR")]:
        badge(c, x, y, "♿", BLUE, 7); txt(c, x, y + 30, s, 5.2, "FB", BLUE)
    c.setFont("FB", 12); c.setFillColor(NAVY); c.drawString(40, H - 40, "07 — Plan d'accessibilité PMR (ERP existant)")
    X0, Y0 = 905, H - 95
    c.setFont("FB", 9); c.setFillColor(NAVY); c.drawString(X0, Y0, "Détail caisse PMR (repris du DAT 2015)")
    k = 1.25; bx, by = X0 + 90, Y0 - 150
    c.setStrokeColor(black); c.setLineWidth(0.8); c.line(bx - 60, by, bx + 160, by)
    c.setFillColor(WOOD); c.rect(bx + 30 * k, by, 75 * k, 95 * k, fill=1, stroke=1)
    c.setFillColor(white); c.rect(bx, by + 70 * k, 30 * k, 10 * k, fill=1, stroke=1)
    c.setDash(2, 2); c.line(bx, by + 70 * k, bx, by); c.setDash()
    c.setFont("F", 6); c.setFillColor(black)
    c.drawString(bx + 105 * k + 6, by + 92 * k, "comptoir h 0,95")
    c.drawRightString(bx - 4, by + 77 * k, "tablette h 0,80 max")
    c.drawRightString(bx - 4, by + 35 * k, "vide h 0,70 mini")
    c.drawString(bx, by + 84 * k, "prof. 0,30 · larg. 0,60")
    c.drawString(X0, by - 12, "Coupe sur la caisse 1 — terminal de paiement et écran client entre 0,90 et 1,30 m")
    para(c, X0, Y0 - 185, 272,
         "**Exigences (arrêté du 8 décembre 2014 — ERP existants), toutes tenues sans travaux\n"
         "• Entrée de plain-pied existante, porte 2,40 m.\n"
         "• Bandes contrastées sur la vitrine à 1,10 m et 1,60 m : intégrées à la vitrophanie.\n"
         "• Cheminement ≥ 1,20 m partout : 1,40 m entre îlot et caisse, 1,65 m entre comptoir et murale, 2,15 m devant la murale. Aires de rotation Ø 1,50 m devant la caisse, la murale et une table PMR.\n"
         "• Murale libre-service : une partie de chaque famille de produits entre 0,40 et 1,30 m.\n"
         "• 2 places PMR (salle et alcôve) : chaise amovible, vide sous table h 0,70 m.\n"
         "• Écrans menu : carte papier en gros caractères à la caisse.\n"
         "**Sanitaires clients\n"
         "Il n'y en a pas dans le local, comme pour La Mie Câline : il faut l'accord écrit du centre pour ses sanitaires publics accessibles, à mentionner dans la notice.\n"
         "**Registre public d'accessibilité à tenir dès l'ouverture.", 7.2)
    cartouche(c, "ACCESSIBILITÉ PMR", phase="ESQUISSE V2", num=7)

def page_ddpp(c):
    h1(c, 40, H - 50, "08 — Notice hygiène : check-list DDPP de Maine-et-Loire (version réemploi)")
    para(c, 40, H - 72, 1100, "Cadre : règlement (CE) 852/2004, règlement (CE) 853/2004, arrêté du 21/12/2009 (commerce de détail, températures), "
         "GBPH restaurateur, décret 2011-731 (formation hygiène). Vente directe au consommateur : déclaration d'activité, pas d'agrément pour la boutique.", 8)
    cols = [("Thème", 150), ("Exigence", 380), ("Réponse dans le projet V2", 440), ("Statut", 100)]
    rows = [
     ("Déclaration", "Déclarer l'établissement avant l'ouverture (Cerfa 13984, en ligne)", "Activité « restauration commerciale + commerce de détail »", "À faire J−30"),
     ("Approvisionnement", "Un fournisseur qui livre un autre établissement doit être agréé CE ou bénéficier d'une dérogation", "Vérifier que le statut du labo de Maulévrier couvre ce flux et ces volumes", "Point bloquant"),
     ("Formation", "Au moins une personne formée à l'hygiène en restauration commerciale (14 h)", "Responsable + un second titulaire", "À planifier"),
     ("PMS / HACCP", "Plan de maîtrise sanitaire écrit", "Adapter celui du labo. Y écrire les règles de circulation par l'unique porte avant / arrière (planche 04)", "À rédiger"),
     ("Marche en avant", "Pas de croisement propre / sale, ou séparation dans le temps documentée", "Séparation dans le temps et bacs fermés à la porte cuisson / zone service ; option passe desserte", "Procédure"),
     ("Locaux", "Revêtements lisses, lavables, en bon état", "Revêtements existants conservés : les faire contrôler à l'état des lieux (joints, plinthes, dalles)", "À vérifier"),
     ("Lavage des mains", "Lave-mains à commande non manuelle près des postes", "4 existants (prépa, DEGT N°1, plonge, WC) + 2 créés (caisse, cuisson). Robinets à passer en commande non manuelle si besoin", "Petits travaux"),
     ("Personnel", "Vestiaires séparés, WC sans ouverture directe sur une zone de manipulation", "Bloc existant inchangé", "Existant"),
     ("Froid", "Enceintes capables de tenir les T°, contrôle et enregistrement", "Chambre négative existante −18 °C ; armoires positives 0/+3 °C (prépa + 2 en ex-pousse) ; murale LS 0/+3 °C ; sondes connectées", "Prévu"),
     ("Vitrines libre-service", "Produits protégés, T° maîtrisée, étiquetage complet", "Préemballés et étiquetés au labo ; rideaux de nuit ; T° relevée 2 fois/jour", "Prévu"),
     ("Chaîne chaude", "Cuisson à cœur, maintien ≥ 63 °C, pas de refroidissement sur place", "Cuisson minute, rampe chauffante courte, invendus chauds jetés", "Procédure"),
     ("Huiles de friture", "Contrôle et collecte des huiles usagées", "Testeur, registre, bidons fermés dans la zone conteneurs, prestataire", "Procédure"),
     ("Allergènes", "Information écrite sur les 14 allergènes", "Étiquettes labo + classeur / QR code en caisse pour les produits chauds", "Prévu"),
     ("Origine des viandes", "Origine des viandes achetées crues et servies", "Poulet livré préparé par le labo : obligation à vérifier ; afficher l'origine par précaution", "À vérifier"),
     ("Déchets", "Conteneurs fermés, zone lavable ; tri à la source des biodéchets", "Pas de local maçonné : conteneurs à couvercle et pédale au-delà de P2, évacuation chaque jour vers l'aire du centre. À présenter à la DDPP", "À valider"),
     ("Nuisibles", "Plan de lutte", "Contrat 3D, piège à insectes à plaque engluée, bas de portes arrière", "Contrat"),
     ("Invendus", "Traçabilité", "Destruction tracée ou anti-gaspi en fin de journée dans la limite des DLC", "Procédure"),
    ]
    table(c, 40, H - 92, cols, rows, 7.1)
    cartouche(c, "NOTICE HYGIÈNE — DDPP", phase="ESQUISSE V2", ech="—", num=8)

def page_travaux(c):
    h1(c, 40, H - 50, "09 — Travaux strictement nécessaires (et ce que l'on évite)")
    cols = [("Niveau", 150), ("Poste", 330), ("Nature", 300), ("Remarque", 290)]
    rows = [
     ("A — Indispensable", "Lave-mains caisse", "Plomberie : piquage sur le réseau de la prépa, traversée de cloison légère", "Exigence DDPP"),
     ("A — Indispensable", "Lave-mains cuisson + eau / vidange du four mixte", "Plomberie : piquage sur l'arrivée de l'ex-four Wind ou de la prépa, bonde de sol existante", "Selon les attentes en place"),
     ("A — Indispensable", "Extraction", "Ramonage + contrôle du conduit et de l'extracteur, filtres à chocs", "Hotte à racheter seulement si elle a été déposée"),
     ("A — Indispensable", "Électricité", "Contrôle de la ligne cuisson, prises de la murale et des caisses", "Par un électricien, avant de commander le matériel"),
     ("A — Indispensable", "Sécurité", "Extincteur classe F, couverture anti-feu, 1 ou 2 BAES / extincteurs déplacés", "—"),
     ("A — Indispensable", "Enseigne", "Nouvelles faces / lettres sur le caisson existant, vitrophanie", "Charte du centre"),
     ("B — Recommandé", "Passe desserte salle → plonge", "Ouverture d'environ 80 × 60 cm dans la cloison légère de la plonge + encadrement inox (plaquiste, ½ journée)", "Pas de la structure. Simplifie le circuit vaisselle ; sans elle : bacs fermés par la porte cuisson"),
     ("C — Matériel posé", "Murale LS à groupe logé, four mixte, friteuse, plan réfrigéré, 2 armoires +, lave-vaisselle frontal", "Achat et pose, sans travaux", "Négocier la reprise de ce qui existe déjà (planche 02)"),
     ("C — Matériel posé", "Comptoir caisse, îlot « L'Arbre », mobilier, conteneurs, sondes de T°", "Agencement mobile", "Décor bois et végétal classé M1"),
    ]
    y = table(c, 40, H - 70, cols, rows, 7.4)
    c.setFont("FB", 10); c.setFillColor(NAVY); c.drawString(40, y - 24, "Ce que la V2 évite par rapport à la V1")
    y2 = table(c, 40, y - 34, [("Poste de la V1", 380), ("Pourquoi on n'en a plus besoin", 690)], [
        ("Cloisonnement de la cuisson (2 cloisons + portes)", "On reste sous 20 kW dans la zone de cuisson existante, déjà encadrée par la verrière, le muret et l'écran de cantonnement"),
        ("Passe chaude percée dans la verrière", "Le retrait chaud passe par la porte existante cuisson / zone service, à 2 m du comptoir"),
        ("Local déchets maçonné et coupe-feu", "Conteneurs fermés dans le recoin derrière P2, évacuation quotidienne vers l'aire du centre"),
        ("Reconversion de la chambre froide en positif", "Elle reste négative (surgelés). Le frais va dans des armoires plug-in sur les prises existantes"),
        ("Reprise des sols de la cuisson et de la plonge, siphons", "Revêtements existants conservés s'ils sont en bon état (à vérifier)"),
        ("Groupe froid déporté pour la murale", "Murale à groupe logé : pas de liaisons frigorifiques ni d'intervention en toiture"),
        ("Nouvelle enseigne complète", "Caisson et alimentation conservés, seules les faces changent"),
    ], 7.4)
    para(c, 40, y2 - 18, 1080,
         "**Ce qui peut encore faire grimper la facture, et qu'il faut savoir avant de signer : une hotte déposée, un groupe froid de la chambre hors service, une ligne électrique insuffisante, des sols ou joints dégradés en cuisson, un séparateur à graisses exigé par le réseau. Chacun se vérifie lors d'une seule visite avec un frigoriste / cuisiniste et un électricien.", 8.2)
    cartouche(c, "TRAVAUX STRICTEMENT NÉCESSAIRES", phase="ESQUISSE V2", ech="—", num=9)

def page_demarches(c):
    h1(c, 40, H - 50, "11 — Démarches, calendrier et points à valider")
    cols = [("Démarche", 220), ("Auprès de", 170), ("Contenu", 380), ("Délai indicatif", 140)]
    rows = [
     ("Inventaire de reprise + état des lieux technique", "La Mie Câline / bailleur + frigoriste, électricien", "Liste des équipements laissés et de leur état (hotte, chambre froide, groupe, saladette, armoires, banquette), conduit, ligne cuisson", "Avant toute offre"),
     ("Accord du bailleur / du centre", "Marques Avenue", "Plan, enseigne (faces seules), cuisson électrique < 20 kW, terrasse, sanitaires publics, aire de déchets", "Avant signature"),
     ("Autorisation de travaux ERP (art. L122-3 CCH)", "Mairie de La Séguinière (SDIS 49 + commission accessibilité)", "Dossier léger : mêmes cloisons, même classement, effectif en baisse, cuisson moins puissante. À confirmer en mairie : AT ou simple information", "Jusqu'à 4 mois : se renseigner tout de suite"),
     ("Enseigne", "Mairie (si règlement local de publicité)", "Changement des faces du caisson existant", "≈ 2 mois si exigé"),
     ("Déclaration d'activité", "DDPP de Maine-et-Loire", "Cerfa 13984 (en ligne)", "Avant ouverture"),
     ("Statut sanitaire du labo", "DDPP du lieu du labo", "Agrément CE ou dérogation couvrant la livraison de la boutique", "À sécuriser avant engagement"),
     ("Licence boissons (si bière / saké)", "Mairie + permis d'exploitation", "Petite licence restaurant ou licence restaurant", "≈ 1 mois + formation"),
    ]
    y = table(c, 40, H - 70, cols, rows, 7.6)
    para(c, 40, y - 18, 520,
         "**Points ouverts\n"
         "1. Ce que La Mie Câline laisse réellement (c'est ce qui fixe le budget).\n"
         "2. Cotes : relevé sur site (plan à ± 10 cm).\n"
         "3. Puissance de la ligne du four Wind et état de l'extraction.\n"
         "4. Acceptation par la DDPP de l'unique porte avant / arrière (séparation dans le temps) et des conteneurs sans local.\n"
         "5. Loi AGEC : cas des produits préemballés consommés sur place.\n"
         "6. Accord écrit du centre pour les sanitaires publics et l'aire de déchets.\n"
         "7. Séparateur à graisses : exigence du gestionnaire du réseau.", 8.2)
    para(c, 600, y - 18, 520,
         "**À garder en tête : la cuisson reste le poste qui change le modèle\n"
         "Même sans travaux de structure, la cuisson minute ajoute du personnel au poste chaud pendant le rush, l'entretien de l'extraction et des huiles, et des contrôles. Si l'offre chaude ne paie pas ce poste, le repli le moins cher est simple : supprimer la friteuse et garder seulement le four mixte (≈ 10 kW, pas d'huile), sans rien changer au plan.\n"
         "Le chiffrage de la boutique avec et sans cuisson reste à faire avant de figer le choix.", 8.2, col=HexColor("#7a1f1f"))
    cartouche(c, "DÉMARCHES ET POINTS À VALIDER", phase="ESQUISSE V2", ech="—", num=11)

def main():
    c = canvas.Canvas(OUT, pagesize=(W, H))
    c.setTitle("Dossier d'adaptation V2 (réemploi maximal) — L'Arbre à Makis — Cellule 09 La Séguinière")
    c.setAuthor("L'Arbre à Makis")
    for f in (page_cover, page_programme, page_reemploi, page_plan, page_hygiene, page_cuisson, page_incendie, page_pmr,
              page_ddpp, page_travaux, page_facade, page_demarches):
        f(c); c.showPage()
    c.save()
    print("OK", OUT)
    tot = 0
    for lab, r in SURF:
        a = area(r); tot += a; print(f"{lab:55s} {a:6.1f}")
    print("TOTAL", round(tot, 1))

if __name__ == "__main__":
    main()
