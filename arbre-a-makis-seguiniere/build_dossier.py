# -*- coding: utf-8 -*-
"""Dossier d'adaptation V3 (réemploi maximal + corrections audit DDPP) - L'Arbre à Makis - Cellule 09 Marques Avenue La Séguinière.
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
OUT = os.path.join(HERE, "Dossier_LAM_La_Seguiniere_cellule09_V3.pdf")
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
 ("Passage froid (ex-niche vitrine) + ex-zone pousse", [(655, 733, 741, 837), (741, 733, 983, 837)]),
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
 (655, 733, 741, 733), (655, 837, 741, 837),                         # ex-niche vitrine (fond ouvert en V3)
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
    # V3 : passe desserte (cloison légère) + passage froid (fond de niche ouvert, porte va-et-vient)
    rect(c, 977, 90, 989, 170, fill=HexColor("#ffe7a8"), stroke=MAG, lw=1.2)
    rect(c, 735, 742, 747, 830, fill=white, stroke=None)
    line(c, 741, 745, 741 + 80, 745, MAG, 0.9)
    X, Y = P(741, 745); r = 85 * S
    c.saveState(); c.setStrokeColor(MAG); c.setLineWidth(0.5); c.setDash(1.5, 1.5); c.arc(X - r, Y - r, X + r, Y + r, 270, 90); c.restoreState()

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
    if labels: txt(c, 290, 1045, "MURALE LS 4 × 1,20 m — portes vitrées classe M0, 0/+3 °C", 5.2, "FB", NAVY)
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
    # passage froid (ex-niche) + armoires positives
    rect(c, 845, 745, 915, 815, fill=HexColor("#cfe6f7"), stroke=NAVY, lw=0.5)
    rect(c, 1085, 300, 1155, 370, fill=HexColor("#cfe6f7"), stroke=NAVY, lw=0.5)
    # armoire produits d'entretien (DEGT N°2) + crédence inox cuisson
    rect(c, 1492, 420, 1542, 520, fill=HexColor("#eadcf2"), stroke=MAG, lw=0.9)
    rect(c, 690, 1143, 900, 1150, fill=MAG, stroke=None)
    if labels:
        txt(c, 698, 785, "passage\nfroid", 3.8, "FB", MAG)
        txt(c, 880, 780, "armoire +", 3.8, "FB", NAVY)
        txt(c, 1120, 335, "armoire\n+", 3.8, "FB", NAVY)
        txt(c, 1517, 470, "produits\nd'entre-\ntien", 3.4, "FB", MAG)
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
    cartouche(c, "FAÇADE ET ENSEIGNE", phase="ESQUISSE V3", ech="≈ 1/55", num=10)


def label_min(c, items):
    for (x, y, s) in items: txt(c, x, y, s, 6, "FB", HexColor("#333333"))








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
    txt(c, 150, 540, "dégagement principal 4 UP (2,40 m)", 5.5, "FB", GG)
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
    cartouche(c, "SÉCURITÉ INCENDIE", phase="ESQUISSE V3", num=6)

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
    cartouche(c, "ACCESSIBILITÉ PMR", phase="ESQUISSE V3", num=7)


# =========================================================================== PAGES V3 (V2 + mise en conformité DDPP)
PH = "ESQUISSE V3"

def page_cover(c):
    c.setFillColor(NAVY); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(white); c.roundRect(W / 2 - 170, H - 330, 340, 240, 10, fill=1, stroke=0)
    c.drawImage(LOGO, W / 2 - 150, H - 320, 300, 220, preserveAspectRatio=True, mask="auto")
    c.setFillColor(white); c.setFont("FB", 24)
    c.drawCentredString(W / 2, H - 390, "DOSSIER D'ADAPTATION DU LOCAL — V3")
    c.setFont("F", 14)
    c.drawCentredString(W / 2, H - 418, "Réemploi maximal de l'existant + corrections issues de l'audit DDPP")
    c.drawCentredString(W / 2, H - 438, "Aucun gros œuvre, aucune cloison déplacée : deux ouvertures dans des cloisons légères, des lave-mains et du matériel")
    c.setStrokeColor(GREEN); c.setLineWidth(2); c.line(W / 2 - 200, H - 456, W / 2 + 200, H - 456)
    c.setFont("FB", 12)
    c.drawCentredString(W / 2, H - 484, "CELLULE N°09 — ESPACE COMMERCIAL MARQUES AVENUE — RUE DU BOCAGE — 49280 LA SÉGUINIÈRE")
    c.setFont("F", 10.5)
    c.drawCentredString(W / 2, H - 504, "Reprise du local exploité par La Mie Câline (DAT « terminal de cuisson », ChauvierePajot, 20/03/2015)")
    c.setFont("FB", 10); c.drawString(170, 300, "PIÈCES DU DOSSIER")
    pieces = ["01  Programme et tableau des surfaces", "02  Réemploi de l'existant : ce que l'on garde, élément par élément",
              "03  Plan RDC projeté (existant conservé / créé)", "04  Plan hygiène — marche en avant, flux et températures (DDPP)",
              "05  Espace cuisson à l'emplacement du four Wind", "06  Plan de sécurité incendie (ERP N + M)", "07  Plan d'accessibilité PMR",
              "08  Notice hygiène — synthèse DDPP (détail : document « Audit DDPP »)", "09  Travaux strictement nécessaires",
              "10  Façade et enseigne (caisson existant réhabillé)", "11  Démarches, calendrier et points à valider"]
    c.setFont("F", 9.5)
    for i, p in enumerate(pieces): c.drawString(170, 282 - i * 15, p)
    c.setFont("FB", 10); c.drawString(700, 300, "STATUT DU DOCUMENT")
    para(c, 700, 282, 330, "Version 3 du 17/11/2026, qui remplace la V2 : même principe de réemploi, avec les corrections de l'audit DDPP (circuits, lave-mains, froid, revêtements).\n"
         "Fond de plan redessiné d'après le DAT 2015 (précision ± 10 cm, cotes non relevées sur site).\n"
         "Les pièces réglementaires (Cerfa 13824, notices signées) restent à produire par le maître d'œuvre.", 9, col=white)
    c.setFont("F", 8); c.setFillColor(HexColor("#b8c2d6")); c.drawString(170, 50, "L'Arbre à Makis — produits préparés à Maulévrier — V3 du 17/11/2026")

def page_programme(c):
    h1(c, 40, H - 50, "01 — Programme et principe : s'installer dans l'existant")
    para(c, 40, H - 80, 620,
        "**La règle\n"
        "Aucun gros œuvre, aucune cloison déplacée, ni sols, ni plafonds, ni façade à refaire. Chaque fonction est posée là où La Mie Câline avait déjà les murs, l'eau, l'électricité ou l'extraction. La V3 ajoute seulement ce que l'audit DDPP rend nécessaire : deux ouvertures dans des cloisons légères existantes, des lave-mains, une crédence inox et du matériel (planche 09).\n"
        "\n"
        "**Ce qui va où\n"
        "• Cuisson : four mixte + friteuse (≈ 19 kW) sur les 1,46 m du four Wind, sous l'extraction existante et sur sa ligne électrique.\n"
        "• Préparation froide : la pièce existante, avec sa saladette 3 portes, son armoire positive et son lave-mains.\n"
        "• Froid : la chambre froide reste négative (surgelés). Le frais du jour est stocké dans l'armoire de la prépa et dans 2 armoires positives (ex-zone pousse + couloir DEGT N°1).\n"
        "• Murale libre-service de 4,80 m à portes vitrées, le long du mur bas (alimentations existantes), à groupe logé.\n"
        "• Caisse : comptoir mobile devant la verrière de la prépa, zone de service derrière.\n"
        "• Salle : la zone tables de La Mie Câline + l'alcôve avec sa banquette.\n"
        "• Plonge, vestiaires, WC, bureau, réserve CF, local TGBT : inchangés.\n"
        "• Déchets : conteneurs à couvercle dans le recoin derrière la porte P2.\n"
        "\n"
        "**Circuits séparés (correction de l'audit)\n"
        "• Froid : la vitrine boissons encastrée est déposée et le fond de sa niche (cloison légère d'environ 1 m) est ouvert avec une porte va-et-vient. Le réassort passe directement des armoires positives à la zone de service, sans traverser la cuisson.\n"
        "• Chaud : la porte existante cuisson → zone de service ne sert plus qu'aux produits chauds et au personnel.\n"
        "• Sale : la vaisselle et les déchets de la salle repartent par une passe desserte vers la plonge, sans passer par la cuisson ni par le comptoir.", 8.4)
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
         "**Loi AGEC : au-delà de 20 personnes servies en même temps (intérieur + terrasse, assises ou debout), la vaisselle doit être réutilisable pour la consommation sur place. Le lave-vaisselle frontal tient dans la plonge existante. Le cas des produits préemballés vendus en libre-service puis mangés sur place reste à confirmer.", 7.6)
    cartouche(c, "PROGRAMME ET SURFACES", phase=PH, ech="—", num=1)

def page_reemploi(c):
    h1(c, 40, H - 50, "02 — Réemploi de l'existant : ce que l'on garde, élément par élément")
    cols = [("Élément existant (DAT 2015)", 270), ("Usage L'Arbre à Makis", 400), ("Travaux", 300), ("Condition / à vérifier", 160)]
    rows = [
     ("Enveloppe, murs mitoyens CF 1 h, façade vitrée, porte 2 vantaux 2,40 m", "Inchangés", "Aucun", "—"),
     ("Cloisons du back-office : prépa froide, plonge, vestiaires H/F + WC, bureau, réserve CF, local TGBT, muret cuisson", "Toutes gardées, avec la même fonction (sauf l'ex-pousse, qui devient stockage frais)", "Aucun", "État des lieux"),
     ("Niche de la vitrine boissons encastrée", "Devient le passage froid entre l'arrière et la zone de service", "Dépose de la vitrine, ouverture du fond de niche (cloison légère ≈ 1 m), porte va-et-vient", "Cloison non porteuse (à confirmer)"),
     ("Cloison légère salle / plonge", "Passe desserte (vaisselle et déchets de la salle)", "Ouverture ≈ 80 × 60 cm + encadrement inox", "—"),
     ("Verrières prépa froide / cuisson, imposte vitrée de l'alcôve", "Gardées : cuisson et prépa visibles depuis la boutique", "Nettoyage", "—"),
     ("Porte vente → cuisson (bas de la verrière)", "Produits chauds et personnel uniquement", "Aucun", "—"),
     ("Sols, plafonds", "Conservés", "Reprises ponctuelles : joints, plinthes à gorge, dalles abîmées", "État en cuisson / plonge"),
     ("Extraction : conduit SF ¼ h, extracteur 400 °C ½ h, écran de cantonnement, arrêts d'urgence", "Gardés pour four mixte + friteuse", "Ramonage, contrôle, filtres à chocs, crédence inox", "Hotte encore en place ?"),
     ("Ligne électrique du four Wind", "Four mixte + friteuse (≈ 19 kW)", "Contrôle", "Section et protection"),
     ("Chambre froide 3 × 3 m négative + groupe", "Reste négative : surgelés et stock", "Enregistreur de température (obligatoire > 10 m³)", "Contrôle frigoriste"),
     ("Armoire positive + saladette 3 portes de la prépa", "Gardées", "Aucun", "Cédées avec le local ?"),
     ("Prise de l'armoire de pousse", "1 armoire positive plug-in (+ 1 dans le DEGT N°1)", "Prise à décaler d'environ 1 m", "—"),
     ("Alimentations des meubles bas turbochef / vitrine boissons (mur bas)", "Murale libre-service 4,80 m à portes vitrées, groupe logé", "Prises à adapter si besoin", "Puissance de la murale"),
     ("Lave-mains : prépa, DEGT N°1, plonge, WC", "Conservés", "Commande non manuelle si absente", "Type de robinet"),
     ("Plonge", "Conservée + lave-vaisselle frontal", "Raccordement sur les attentes", "Capacité eau chaude"),
     ("Éclairage, BAES, extincteurs, coupure enseigne", "Conservés", "Luminaires protégés en zones alimentaires, 1 ou 2 déplacements", "—"),
     ("Caisson d'enseigne bandeau 11,50 × 1,48 m", "Conservé, nouvelles faces", "Faces et lettres seulement", "Charte du centre"),
     ("Banquette de l'alcôve, mange-debout en vitrine", "Conservés", "Aucun", "Cédés avec le local ?"),
    ]
    y = table(c, 40, H - 70, cols, rows, 7.3)
    para(c, 40, y - 18, 1100,
         "**Le levier n°1 sur l'investissement reste la reprise du matériel. Avant de signer, il faut un inventaire contradictoire de ce que La Mie Câline laisse (hotte, chambre froide et groupe, saladette, armoire positive, banquette, mange-debout, lave-mains) et de son état. Chaque équipement manquant redevient un achat.", 8.2)
    cartouche(c, "RÉEMPLOI DE L'EXISTANT", phase=PH, ech="—", num=2)

def page_plan(c):
    draw_shell(c); draw_equipment(c); dims(c)
    scale_bar(c, 150, 120)
    c.setFont("FB", 12); c.setFillColor(NAVY); c.drawString(40, H - 40, "03 — Plan RDC projeté : existant conservé + corrections DDPP (magenta)")
    X = 905; y = H - 75
    c.setFont("FB", 9); c.setFillColor(NAVY); c.drawString(X, y, "Parcours client"); y -= 14
    y = para(c, X, y, 272,
             "1. Entrée face à l'îlot « L'Arbre » (produits phares + retail).\n"
             "2. Murale libre-service à portes vitrées le long du mur bas.\n"
             "3. Caisse devant la verrière de la prépa : 2 postes dont 1 PMR, retrait chaud en bout de comptoir.\n"
             "4. Places en salle et dans l'alcôve ; desserte des plateaux vers la passe de la plonge.", 7.3)
    y -= 6
    c.setFont("FB", 9); c.setFillColor(NAVY); c.drawString(X, y, "Trois circuits séparés"); y -= 14
    y = para(c, X, y, 272,
             "• Froid : armoires positives → passage par l'ex-niche → zone de service → murale.\n"
             "• Chaud : cuisson → porte existante → retrait au comptoir.\n"
             "• Sale : salle → passe desserte → plonge → conteneurs → P2.\n"
             "• Ajouts : 2 lave-mains (comptoir, cuisson), crédence inox derrière la cuisson, armoire à produits d'entretien, bas de porte à brosse sur P1 / P2.", 7.3)
    y -= 8
    y = legend_box(c, X, y, [("box", WALL, "Cloisons / murs existants conservés"), ("box", HexColor("#bfe0f5"), "Verrières existantes"),
                             ("box", MAG, "Créé (cloisons légères, lave-mains, crédence…)"),
                             ("box", HexColor("#f6f1e7"), "Espace public (vente + salle)"), ("box", HexColor("#eef3e6"), "Zone service derrière comptoir"),
                             ("box", HexColor("#e3f0fb"), "Préparation froide / passage froid"), ("box", HexColor("#fde9e3"), "Cuisson (zone existante)"),
                             ("box", HexColor("#efe7f7"), "Plonge"), ("box", HexColor("#dcecff"), "Chambre froide négative"),
                             ("box", HexColor("#fff6d9"), "Réserve sèche"), ("box", HexColor("#efe2d3"), "Conteneurs déchets"),
                             ("dot", BLUE, "Lave-mains existant")], "Légende")
    cartouche(c, "PLAN RDC PROJETÉ", phase=PH, num=3)

def tag(c, x, y, s, col):
    X, Y = P(x, y); c.saveState(); c.setFillColor(white); c.setStrokeColor(col)
    wdt = pdfmetrics.stringWidth(s, "FB", 6) + 6; c.roundRect(X - wdt / 2, Y - 5, wdt, 11, 3, fill=1, stroke=1)
    c.setFillColor(col); c.setFont("FB", 6); c.drawCentredString(X, Y - 2, s); c.restoreState()

def flows(c):
    G = HexColor("#2e8b57")
    arrow_path(c, [(DEPTH + 40, 65), (1460, 65), (1460, 760), (1250, 760), (1250, 840)], G)
    arrow_path(c, [(1460, 585), (1400, 585)], G, lw=1.2)
    arrow_path(c, [(1200, 760), (1020, 775), (925, 790)], G)
    arrow_path(c, [(1110, 700), (1120, 385)], G, lw=1.2)
    arrow_path(c, [(845, 780), (720, 785), (610, 790), (600, 990), (440, 990), (300, 1050)], G, dash=(5, 2))
    arrow_path(c, [(820, 600), (955, 690), (955, 745), (880, 760)], G, lw=1.2)
    arrow_path(c, [(760, 1040), (690, 1095), (600, 1095), (580, 900), (548, 860)], HexColor("#c0392b"))
    arrow_path(c, [(1100, 210), (1100, 718), (1460, 718), (1460, 815)], BROWN, dash=(2, 2))
    arrow_path(c, [(960, 900), (1020, 800), (1080, 760)], BROWN, dash=(2, 2), head=False)
    arrow_path(c, [(1530, 900), (1530, 700), (DEPTH + 45, 700)], BROWN, dash=(2, 2))
    arrow_path(c, [(400, 200), (600, 160), (930, 120), (1015, 130)], ORANGE, dash=(6, 2))
    arrow_path(c, [(DEPTH + 40, 40), (1420, 40), (1420, 190), (1370, 190)], BLUE, lw=1.2)
    arrow_path(c, [(-60, 575), (60, 575), (60, 960), (420, 1000)], GREY, lw=1.2)
    arrow_path(c, [(420, 1000), (400, 900), (420, 760), (465, 640)], GREY, lw=1.2)

def page_hygiene(c):
    draw_shell(c, terrace_text=False); draw_equipment(c, labels=False)
    label_min(c, [(290, 1107, "MURALE LS"), (220, 735, "ÎLOT"), (507, 640, "CAISSE"), (840, 560, "PRÉPA FROIDE"),
                  (790, 930, "CUISSON"), (1072, 120, "PLONGE"), (1215, 990, "CH. NÉGATIVE"), (1277, 572, "RÉSERVE"),
                  (1277, 250, "VESTIAIRES / WC"), (1470, 960, "DÉCHETS")])
    flows(c)
    for (x, y, s, col) in [(290, 1020, "0/+3 °C", BLUE), (1215, 1070, "−18 °C", BLUE), (880, 830, "0/+3 °C", BLUE),
                           (902, 515, "0/+3 °C", BLUE), (760, 1015, "≥ 63 °C", RED)]:
        tag(c, x, y, s, col)
    for (x, y, s) in [(1500, 110, "1"), (1440, 600, "2"), (1250, 900, "3"), (930, 765, "3'"), (820, 660, "4"), (870, 1000, "4'"),
                      (690, 760, "5"), (500, 940, "6"), (1050, 120, "7"), (1490, 840, "8")]:
        badge(c, x, y, s, NAVY)
    c.setFont("FB", 12); c.setFillColor(NAVY); c.drawString(40, H - 40, "04 — Plan hygiène : marche en avant, flux et températures")
    X = 905; y = H - 70
    y = legend_box(c, X, y, [("line", HexColor("#2e8b57"), "Produits froids (labo → stockage → prépa → vitrine)"),
                             ("line", HexColor("#c0392b"), "Produits chauds (cuisson → retrait)"),
                             ("dash", BROWN, "Déchets (→ conteneurs → P2)"), ("dash", ORANGE, "Vaisselle + déchets de salle (passe desserte)"),
                             ("line", BLUE, "Personnel"), ("line", GREY, "Clients")], "Flux")
    y -= 4
    c.setFont("FB", 9); c.setFillColor(NAVY); c.drawString(X, y, "Étapes"); y -= 13
    y = para(c, X, y, 272,
             "1 Réception à P1 : T° à cœur, DLC, étiquetage, décartonnage, bacs navettes du labo.\n"
             "2 Retail et sec en réserve CF.  3 Surgelés en chambre négative.  3' Frais du jour en armoires positives.\n"
             "4 Prépa froide : assemblage, étiquetage.  4' Cuisson minute / remise en T°.\n"
             "5 Passage froid (ex-niche) vers la zone de service.\n"
             "6 Réassort de la murale par le portillon, retrait chaud au comptoir.\n"
             "7 Plonge (vaisselle reçue par la passe).  8 Déchets en sacs fermés → conteneurs → P2.", 7.1)
    y -= 4
    c.setFont("FB", 9); c.setFillColor(RED); c.drawString(X, y, "Ce qui reste à cadrer dans le PMS"); y -= 13
    para(c, X, y, 272,
         "• Couloir des rampes partagé livraisons / déchets : livraisons le matin, déchets après le service, nettoyage entre les deux.\n"
         "• Réassort de la murale en bacs fermés, hors coup de feu.\n"
         "• Aucun lavage de légumes sur place (tout arrive prêt à l'emploi) : sinon un évier dédié est obligatoire en prépa.\n"
         "• Pas de volaille crue manipulée en boutique : poulet livré cuit (ou pané précuit surgelé).\n"
         "• Conteneurs à couvercle et pédale, sortis chaque jour vers l'aire du centre.", 7.1)
    cartouche(c, "HYGIÈNE — MARCHE EN AVANT", phase=PH, num=4)

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
    R(655, 733, 741, 837, fill=HexColor("#e3f0fb"), stroke=None)
    R(640, 1150, 1075, 1175, fill=RED, stroke=None)
    for (x1, y1, x2, y2) in [(655, 727, 930, 739), (655, 831, 741, 843), (887, 948, 899, 1150)]:
        R(x1, y1, x2, y2, fill=WALL, stroke=None)
    R(651, 837, 659, 1053, fill=HexColor("#bfe0f5"), stroke=BLUE)
    R(1058, 830, 1066, 1150, fill=BLUE, stroke=None)
    R(650, 845, 1063, 1148, stroke=RED, lw=1.2, dash=(5, 3))
    # crédence inox
    R(690, 1143, 900, 1150, fill=MAG, stroke=None)
    R(700, 1060, 790, 1145, fill=HexColor("#f6c9bd")); T(745, 1102, "Four mixte\n6 GN 1/1\n≈ 10 kW", 6.3)
    R(797, 1060, 842, 1145, fill=HexColor("#f6c9bd")); T(820, 1102, "Fri-\nteuse\n10 L\n≈ 9 kW", 6)
    R(900, 1075, 1050, 1145, fill=HexColor("#cfe6f7")); T(975, 1110, "Plan réfrigéré\n(garnitures baos)", 6.3)
    R(984, 856, 1058, 973, fill=HexColor("#dddddd"), stroke=GREY); T(1021, 915, "Dressage\n(ex-table\nà plaquer)", 6)
    R(900, 975, 940, 1013, fill=white, stroke=MAG, lw=1.2); T(920, 994, "LM", 6, "FB", MAG)
    R(845, 745, 915, 815, fill=HexColor("#cfe6f7")); T(880, 780, "armoire +", 5.5, "FB", NAVY)
    # passage froid : porte va-et-vient dans le fond de niche
    X1, Y1 = Q(741, 745); X2, Y2 = Q(741, 830)
    c.saveState(); c.setStrokeColor(MAG); c.setLineWidth(1.6); c.line(X1, Y1, X2, Y2); c.restoreState()
    T(698, 785, "passage\nfroid\n(ex-niche)", 5.8, "FB", MAG)
    T(790, 800, "porte\nva-et-vient", 5.5, "FI", MAG)
    X1, Y1 = Q(696, 1046); X2, Y2 = Q(842, 1046)
    c.setStrokeColor(RED); c.setLineWidth(0.6); c.line(X1, Y1, X2, Y2); c.line(X1, Y1 - 3, X1, Y1 + 3); c.line(X2, Y2 - 3, X2, Y2 + 3)
    T(769, 1036, "emprise ex-four Wind 1,46 m", 6, "FB", RED)
    T(795, 1192, "crédence inox h 1,50 m derrière la ligne de cuisson", 6.5, "FB", MAG)
    T(800, 900, "ZONE CUISSON EXISTANTE (≈ 12,6 m²)", 8.5, "FB", RED)
    T(800, 925, "écran de cantonnement, conduit et extracteur conservés", 6.5, "FI", RED)
    T(600, 1094, "porte\nexistante\n(chaud)", 6, "FI", GREY)
    T(600, 940, "verrière\nexistante", 6, "FI", BLUE)
    T(1000, 760, "DEGT / ex-pousse", 6, "FI", GREY)
    X, Y = Q(1035, 1060); c.setFillColor(RED); c.circle(X, Y, 6, fill=1, stroke=0); c.setFillColor(white); c.setFont("FB", 5); c.drawCentredString(X, Y - 2, "F")
    c.setFont("FI", 7); c.setFillColor(GREY); c.drawString(ox, oy - 470 * s2 - 12, "Zoom échelle 1/25 — gris foncé = existant conservé ; magenta = créé ; F = extincteur classe F + couverture anti-feu")
    X = 690; y = H - 80
    rows = [("Four mixte 6 niveaux GN 1/1", "10", "Baos (vapeur), remise en T° gyozas, karaage, plats chauds du labo"),
            ("Friteuse électrique 1 bac 10 L", "9", "Poulet croustillant (pané précuit surgelé), gyozas frits"),
            ("Plan réfrigéré", "—", "Garnitures et sauces des baos (0/+3 °C)"),
            ("Rampe chauffante au retrait (comptoir)", "≈ 1", "Maintien ≥ 63 °C, durée limitée"),
            ("TOTAL cuisson", "≈ 19", "Sous le seuil de 20 kW : pas de « grande cuisine »", "B")]
    c.setFont("FB", 10); c.setFillColor(NAVY); c.drawString(X, y, "Équipement (électrique, posé, aucun gros œuvre)")
    y = table(c, X, y - 10, [("Appareil", 160), ("kW", 35), ("Usage", 265)], rows, 7.4)
    y -= 18
    c.setFont("FB", 10); c.setFillColor(NAVY); c.drawString(X, y, "Pourquoi exactement à cet endroit"); y -= 14
    y = para(c, X, y, 460,
             "• Four mixte (90 cm) + friteuse (45 cm) = 1,35 m : ça tient dans les 1,46 m du four Wind.\n"
             "• Ils restent sous l'extraction existante (conduit, extracteur et arrêts d'urgence acceptés en 2015).\n"
             "• La ligne électrique du four à sole alimente les deux appareils (à vérifier sur la plaque du four ou au TGBT).\n"
             "• La verrière existante montre la cuisson depuis la boutique, sans percement.\n"
             "• Sous 20 kW, l'écran de cantonnement n'est plus obligatoire : on le garde (coût zéro).", 7.8)
    y -= 4
    c.setFont("FB", 10); c.setFillColor(NAVY); c.drawString(X, y, "Exigences hygiène de la zone (audit DDPP)"); y -= 14
    para(c, X, y, 460,
         "• Crédence inox lisse derrière four mixte + friteuse (projections de graisse), joint étanche avec le plan et le sol.\n"
         "• Lave-mains à commande non manuelle dans la zone, avec savon, essuie-mains papier et poubelle à pédale.\n"
         "• Hotte : filtres à chocs démontables (lavables au lave-vaisselle), nettoyage chaque semaine, ramonage du conduit au moins une fois par an. Si la hotte du four Wind a été déposée, en racheter une d'environ 1,80 m raccordée au conduit existant.\n"
         "• Sol : carrelage sans joints creusés, pente vers la bonde existante, plinthes à gorge.\n"
         "• Luminaire étanche et protégé au-dessus de la ligne de cuisson.\n"
         "• Thermomètre sonde étalonné (cuisson à cœur, maintien chaud), testeur d'huile (seuil 25 % de composés polaires) et registre.\n"
         "• Eau et vidange du four mixte : à piquer sur l'arrivée de l'ex-four Wind ou de la prépa, évacuation sur la bonde.\n"
         "• Ne pas ajouter d'appareil sans refaire le compte des 20 kW.", 7.8)
    cartouche(c, "ESPACE CUISSON", phase=PH, ech="1/25", num=5)

def page_ddpp(c):
    h1(c, 40, H - 50, "08 — Notice hygiène : synthèse DDPP (le détail point par point est dans le document « Audit DDPP »)")
    para(c, 40, H - 72, 1100, "Cadre : règlement (CE) 852/2004 (annexe II), règlement (CE) 853/2004, règlement (CE) 178/2002, règlement (UE) 1169/2011, "
         "arrêté du 21/12/2009 (températures, commerce de détail), règlement (CE) 37/2005 (surgelés), décret 2008-184 (huiles), décret 2011-731 (formation), GBPH restaurateur.", 8)
    cols = [("Thème", 150), ("Exigence", 360), ("Réponse dans le projet V3", 470), ("Statut", 90)]
    rows = [
     ("Déclaration", "Déclarer l'établissement avant l'ouverture (Cerfa 13984)", "Activité « restauration commerciale + commerce de détail »", "À faire"),
     ("Fournisseur", "Agrément CE ou dérogation pour livrer un autre établissement", "Statut du labo de Maulévrier et volumes livrés à vérifier", "Bloquant"),
     ("Formation", "1 personne formée 14 h en restauration commerciale", "Responsable + un remplaçant", "À faire"),
     ("PMS / HACCP", "Plan de maîtrise sanitaire écrit", "PMS boutique adossé au GBPH et au PMS du labo", "À rédiger"),
     ("Circuits", "Éviter les contaminations croisées (852/2004 ann. II ch. I §2)", "Trois circuits : froid par l'ex-niche, chaud par la porte de la cuisson, sale par la passe desserte", "Travaux"),
     ("Lavage des mains", "Lavabos suffisants, eau chaude, savon, séchage hygiénique", "4 existants + 2 créés (comptoir, cuisson), commande non manuelle partout", "Travaux"),
     ("Revêtements", "Sols, murs, plafonds lisses et lavables", "Existants + crédence inox en cuisson, plinthes à gorge et joints repris si besoin", "Travaux"),
     ("Produits d'entretien", "Stockés hors des zones de manipulation", "Armoire fermée dans le couloir DEGT N°2", "Équipement"),
     ("Froid", "Enceintes capables de tenir les T° ; enregistrement pour les surgelés > 10 m³", "Murale à portes vitrées classe M0, armoires 0/+3 °C, chambre négative avec enregistreur, sondes connectées partout", "Équipement"),
     ("Nuisibles", "Protection des ouvertures, plan de lutte", "Bas de porte à brosse + ferme-portes P1 / P2, contrat 3D, piège à plaque engluée", "Travaux"),
     ("Déchets", "Conteneurs fermés, aire propre ; tri des biodéchets", "Poubelles à pédale à chaque poste ; conteneurs à couvercle derrière P2, évacuation quotidienne", "Prévu"),
     ("Températures", "Arrêté du 21/12/2009 : 0/+2 °C poisson frais, +3 °C préparations, ≥ 63 °C chaud, remise en T° < 1 h", "T° fixées par le labo sur l'étiquette ; cible matériel 0/+3 °C ; pas de refroidissement sur place", "Procédure"),
     ("Poisson cru", "Traitement antiparasitaire par congélation ou justificatif d'exemption", "Attestation du labo dans le classeur", "Document"),
     ("Huiles", "≤ 25 % de composés polaires", "Testeur + registre + collecte agréée", "Procédure"),
     ("Allergènes", "Information écrite sur les 14 allergènes", "Étiquettes labo + classeur / affichage pour les produits chauds ; arachide stockée à part", "Procédure"),
     ("Origine des viandes", "Pays d'élevage et d'abattage", "Afficher l'origine du poulet", "Procédure"),
    ]
    table(c, 40, H - 92, cols, rows, 7.1)
    cartouche(c, "NOTICE HYGIÈNE — DDPP", phase=PH, ech="—", num=8)

def page_travaux(c):
    h1(c, 40, H - 50, "09 — Travaux strictement nécessaires (aucun gros œuvre)")
    cols = [("Niveau", 150), ("Poste", 300), ("Nature", 330), ("Pourquoi", 290)]
    rows = [
     ("A — Obligatoire", "Passage froid par l'ex-niche vitrine", "Dépose de la vitrine encastrée, ouverture du fond de niche (cloison légère ≈ 1 m), bloc-porte va-et-vient lisse à hublot", "Audit DDPP B1 : sépare le froid du chaud"),
     ("A — Obligatoire", "Passe desserte salle → plonge", "Ouverture ≈ 80 × 60 cm dans la cloison légère + encadrement inox", "Audit DDPP B1 : la vaisselle sale ne traverse plus la cuisson"),
     ("A — Obligatoire", "Lave-mains comptoir + cuisson", "Plomberie : piquage sur les réseaux de la prépa et de l'ex-four Wind, commande non manuelle, savon, essuie-mains", "Audit DDPP B2"),
     ("A — Obligatoire", "Robinets des lave-mains existants", "Passage en commande non manuelle (fémorale, pédale ou détection) si ce n'est pas déjà le cas", "Audit DDPP B2"),
     ("A — Obligatoire", "Crédence inox derrière la ligne de cuisson", "Panneau inox ≈ 2,10 × 1,50 m collé, joints silicone alimentaire", "Audit DDPP B10"),
     ("A — Obligatoire", "Extraction", "Ramonage + contrôle, filtres à chocs (hotte à racheter seulement si elle a été déposée)", "Hygiène + sécurité incendie"),
     ("A — Obligatoire", "Portes arrière P1 / P2", "Ferme-portes + bas de porte à brosse", "Audit DDPP B12 : nuisibles"),
     ("A — Obligatoire", "Électricité / sécurité / enseigne", "Contrôle ligne cuisson, prise armoire déplacée, extincteur F, 1-2 BAES, faces d'enseigne", "—"),
     ("B — Selon état des lieux", "Revêtements", "Joints de carrelage, plinthes à gorge en cuisson / prépa / plonge, dalles de plafond abîmées, luminaires non protégés", "Audit DDPP B5, B9 à B11"),
     ("B — Selon état des lieux", "Séparateur à graisses", "Seulement si le gestionnaire du réseau l'exige", "Assainissement"),
     ("C — Matériel", "Froid", "Murale 4,80 m à portes vitrées classe M0, groupe logé ; 2 armoires positives ; sondes connectées + alarme (enregistrement obligatoire pour la chambre négative)", "Audit DDPP C1 à C3"),
     ("C — Matériel", "Cuisson / contrôle", "Four mixte, friteuse, plan réfrigéré, lave-vaisselle frontal, thermomètre sonde, testeur d'huile", "Audit DDPP C4, C5"),
     ("C — Matériel", "Hygiène", "Armoire fermée produits d'entretien, poubelles à pédale, conteneurs à couvercle, bac biodéchets, bacs GN à couvercle, planches code couleur", "Audit DDPP B8, C6, D1 à D4"),
     ("C — Matériel", "Agencement", "Comptoir caisse, îlot « L'Arbre », mobilier, desserte plateaux", "Décor classé M1"),
    ]
    y = table(c, 40, H - 70, cols, rows, 7.4)
    para(c, 40, y - 18, 1080,
         "**Ce qui peut encore faire grimper la facture, et qu'il faut savoir avant de signer : une hotte déposée, un groupe froid hors service, une ligne électrique insuffisante, des revêtements dégradés en cuisson, une cloison de fond de niche qui ne serait pas légère, un séparateur à graisses exigé. Une seule visite avec un frigoriste / cuisiniste, un électricien et un plaquiste suffit à le savoir.", 8.2)
    cartouche(c, "TRAVAUX STRICTEMENT NÉCESSAIRES", phase=PH, ech="—", num=9)

def page_demarches(c):
    h1(c, 40, H - 50, "11 — Démarches, calendrier et points à valider")
    cols = [("Démarche", 220), ("Auprès de", 170), ("Contenu", 380), ("Délai indicatif", 140)]
    rows = [
     ("Inventaire de reprise + état des lieux technique", "La Mie Câline / bailleur + frigoriste, électricien, plaquiste", "Équipements laissés et leur état, conduit, ligne cuisson, nature de la cloison de fond de niche, revêtements", "Avant toute offre"),
     ("Statut sanitaire du labo", "DDPP du lieu du labo", "Agrément CE ou dérogation (Cerfa 13982) couvrant la livraison de la boutique et les volumes", "À sécuriser avant engagement"),
     ("Avis informel sur plans", "DDPP de Maine-et-Loire", "Envoyer le plan hygiène (planche 04) et la synthèse de l'audit, demander un retour avant travaux", "Dès le plan arrêté"),
     ("Accord du bailleur / du centre", "Marques Avenue", "Plan, enseigne (faces seules), cuisson électrique < 20 kW, terrasse, sanitaires publics, aire de déchets", "Avant signature"),
     ("Autorisation de travaux ERP (art. L122-3 CCH)", "Mairie de La Séguinière (SDIS 49 + commission accessibilité)", "Dossier léger : mêmes cloisons porteuses et même recoupement, effectif en baisse. À confirmer en mairie", "Jusqu'à 4 mois : se renseigner tout de suite"),
     ("Déclaration d'activité", "DDPP de Maine-et-Loire", "Cerfa 13984 (en ligne)", "Avant ouverture"),
     ("Audit blanc", "Laboratoire d'analyses ou consultant hygiène", "Visite à blanc avant ouverture puis 1 mois après, avec prélèvements de surface", "J−15 et J+30"),
     ("Licence boissons (si bière / saké)", "Mairie + permis d'exploitation", "Petite licence restaurant ou licence restaurant", "≈ 1 mois + formation"),
    ]
    y = table(c, 40, H - 70, cols, rows, 7.6)
    para(c, 40, y - 18, 520,
         "**Points ouverts\n"
         "1. Ce que La Mie Câline laisse réellement (c'est ce qui fixe le budget).\n"
         "2. Cotes : relevé sur site (plan à ± 10 cm).\n"
         "3. Puissance de la ligne du four Wind et état de l'extraction.\n"
         "4. Statut du labo et volumes livrés (seul point vraiment bloquant).\n"
         "5. Loi AGEC : cas des produits préemballés consommés sur place.\n"
         "6. Accord écrit du centre pour les sanitaires publics et l'aire de déchets.\n"
         "7. Séparateur à graisses : exigence du gestionnaire du réseau.", 8.2)
    para(c, 600, y - 18, 520,
         "**À garder en tête : la cuisson reste le poste qui change le modèle\n"
         "Même sans gros œuvre, la cuisson minute ajoute du personnel au poste chaud pendant le rush, l'entretien de l'extraction et des huiles, et des points de contrôle DDPP. Le repli le moins cher reste de supprimer la friteuse et de garder le four mixte seul (≈ 10 kW, pas d'huile), sans rien changer au plan.\n"
         "Le chiffrage de la boutique avec et sans cuisson reste à faire.", 8.2, col=HexColor("#7a1f1f"))
    cartouche(c, "DÉMARCHES ET POINTS À VALIDER", phase=PH, ech="—", num=11)

# =========================================================================== AUDIT DDPP
OUT_AUDIT = os.path.join(HERE, "Audit_DDPP_LAM_La_Seguiniere_cellule09.pdf")
TYPE_COL = {"Conforme": HexColor("#2e7d32"), "Travaux": MAG, "Équipement": BLUE, "Procédure": ORANGE,
            "Document": HexColor("#8a6d00"), "Bloquant": RED, "À vérifier": GREY}

def audit_cart(c, titre, num):
    cartouche(c, titre, phase="AUDIT DDPP", ech="—", num=num)

def table_paged(c, X, Y, cols, rows, size, header_fn, bottom=92, pad=3, lead=1.25):
    """rows : tuples ; ('§', titre) = ligne de section. Dernière colonne colorée selon TYPE_COL."""
    total = sum(w for _, w in cols)
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
    def head(y):
        hh = size * lead + 2 * pad
        c.setFillColor(NAVY); c.rect(X, y - hh, total, hh, fill=1, stroke=0)
        c.setFillColor(white); c.setFont("FB", size); x = X
        for t, w in cols: c.drawString(x + pad, y - hh + pad + 1, t); x += w
        return y - hh
    y = head(Y)
    for i, r in enumerate(rows):
        if r[0] == "§":
            rh = size * 1.6 + 2 * pad
            if y - rh - 30 < bottom:
                y = head(header_fn())
            c.setFillColor(HexColor("#dfe7d3")); c.rect(X, y - rh, total, rh, fill=1, stroke=0)
            c.setFillColor(NAVY); c.setFont("FB", size + 1); c.drawString(X + pad, y - rh + pad + 2, r[1]); y -= rh; continue
        cells = [wrap(v, w, "FB" if j in (0, len(cols) - 1) else "F") for j, (v, (_, w)) in enumerate(zip(r, cols))]
        n = max(len(cc) for cc in cells); rh = n * size * lead + 2 * pad
        if y - rh < bottom:
            y = head(header_fn())
        if i % 2 == 0:
            c.setFillColor(HexColor("#f2f4f8")); c.rect(X, y - rh, total, rh, fill=1, stroke=0)
        x = X
        for j, (cc, (_, w)) in enumerate(zip(cells, cols)):
            last = j == len(cols) - 1
            c.setFillColor(TYPE_COL.get(r[-1], black) if last else black)
            c.setFont("FB" if (j == 0 or last) else "F", size)
            for k, l in enumerate(cc): c.drawString(x + pad, y - pad - size * (k + 1) * lead + size * 0.25, l)
            x += w
        c.setStrokeColor(HexColor("#cccccc")); c.setLineWidth(0.3); c.line(X, y - rh, X + total, y - rh)
        y -= rh
    return y

GRILLE = [
 ("§", "A — Statut, documents et information du consommateur"),
 ("A1", "Déclarer l'établissement avant l'ouverture — règl. 852/2004 art. 6, Cerfa 13984", "À faire", "Déclaration en ligne au moins 1 mois avant l'ouverture ; récépissé au classeur", "Document"),
 ("A2", "Un établissement qui livre un autre établissement doit être agréé CE ou bénéficier d'une dérogation (Cerfa 13982 : rayon de 80 km, plafonds de quantités par catégorie de produits) — règl. 853/2004 art. 4, arrêté du 8 juin 2006", "Labo de Maulévrier à ≈ 15 km (distance compatible). Statut actuel du labo et volumes poisson / volaille livrés non vérifiés", "Vérifier le statut du labo et calculer les kg / semaine livrés par catégorie. Si les plafonds de la dérogation sont dépassés : agrément CE avant l'ouverture", "Bloquant"),
 ("A3", "Au moins une personne formée à l'hygiène en restauration commerciale (14 h) — décret 2011-731", "À prévoir", "Former le responsable + un remplaçant ; attestations au classeur", "Document"),
 ("A4", "Plan de maîtrise sanitaire écrit : bonnes pratiques, HACCP, traçabilité, non-conformités — règl. 852/2004 art. 5", "À rédiger", "PMS de la boutique adossé au GBPH restaurateur et au PMS du labo, avec les règles de circulation de la planche 04 du dossier", "Document"),
 ("A5", "Traçabilité amont — règl. 178/2002 art. 18", "Produits du labo étiquetés (lot, DLC)", "Conserver bons de livraison et étiquettes ; registre des lots reçus", "Procédure"),
 ("A6", "Retrait / rappel et information des autorités — règl. 178/2002 art. 19", "Non prévu", "Procédure écrite + contacts DDPP 49 et labo affichés au bureau", "Document"),
 ("A7", "Information écrite sur les 14 allergènes, y compris pour les produits non préemballés — règl. 1169/2011, décret 2015-447", "Préemballés étiquetés au labo ; baos chauds servis non emballés. Arachide (sauce cacahuète, cacahuètes wasabi), sésame, poisson, soja et gluten très présents", "Classeur ou affichage des allergènes par produit à la caisse ; équipe formée ; produits à l'arachide stockés à part", "Procédure"),
 ("A8", "Étiquetage complet des préemballés (dénomination, ingrédients, allergènes mis en évidence, quantité, DLC, T° de conservation, lot, exploitant, marque sanitaire si agrément) — règl. 1169/2011", "Étiquettes faites par le labo", "Faire valider le modèle d'étiquette ; vérifier si la dispense de déclaration nutritionnelle s'applique (fabricant livrant ses propres points de vente locaux)", "À vérifier"),
 ("A9", "Origine des viandes servies (pays d'élevage et d'abattage)", "Poulet des baos livré par le labo", "Afficher l'origine du poulet. L'obligation pour une viande livrée déjà préparée est à confirmer, mais l'afficher ne coûte rien", "Procédure"),
 ("§", "B — Locaux et circuits (règl. 852/2004, annexe II, chapitres I et II)"),
 ("B1", "Agencement qui évite les contaminations croisées entre opérations (ch. I §2)", "V2 : une seule porte avant / arrière, dans la cuisson ; vaisselle sale, déchets de salle et réassort froid y passaient", "V3 : passage froid par l'ex-niche vitrine (fond de niche ouvert + porte va-et-vient) et passe desserte salle → plonge. La porte de la cuisson ne sert plus qu'au chaud et au personnel", "Travaux"),
 ("B2", "Lavabos en nombre suffisant et bien placés, eau chaude et froide, savon, séchage hygiénique (ch. I §4)", "4 existants (prépa, DEGT N°1, plonge, WC) ; aucun en cuisson ni au comptoir", "Créer 2 lave-mains (cuisson, comptoir) ; commande non manuelle sur tous ; savon, essuie-mains papier, poubelle à pédale à chaque poste", "Travaux"),
 ("B3", "Toilettes sans ouverture directe sur un local de manipulation, lavabo à proximité (ch. I §3)", "WC du personnel ouvrant sur les vestiaires, eux-mêmes sur le couloir DEGT N°2", "Conforme ; vérifier ferme-portes et ventilation mécanique des WC", "Conforme"),
 ("B4", "Ventilation adaptée, filtres accessibles (ch. I §5-6)", "Extraction cuisson existante, état inconnu", "Contrôle et ramonage, filtres à chocs démontables, air de compensation vérifié (sinon condensation et graisses)", "Travaux"),
 ("B5", "Éclairage suffisant (ch. I §7)", "Plan d'éclairage 2015 conservé", "Luminaires étanches et protégés au-dessus de la prépa, de la cuisson et de la plonge ; remplacer ceux qui ne le sont pas", "À vérifier"),
 ("B6", "Évacuation des eaux résiduaires (ch. I §8)", "Bonde de sol existante en cuisson", "Siphons et grilles démontables vérifiés ; séparateur à graisses si le réseau l'exige", "À vérifier"),
 ("B7", "Vestiaires adaptés (ch. I §9)", "Vestiaires H/F existants avec casiers", "Conforme", "Conforme"),
 ("B8", "Produits de nettoyage hors des zones de manipulation (ch. I §10)", "Aucun emplacement prévu en V2", "Armoire fermée dédiée dans le couloir DEGT N°2", "Équipement"),
 ("B9", "Sols en bon état, lavables, évacuation des eaux (ch. II §1a)", "Carrelage existant", "État des lieux : carreaux cassés, joints creusés, pente vers la bonde ; reprise ponctuelle", "À vérifier"),
 ("B10", "Murs lisses et lavables jusqu'à une hauteur adaptée (ch. II §1b)", "Revêtement de la cuisson inconnu ; friteuse prévue", "Crédence inox derrière four mixte + friteuse ; plinthes à gorge ou joint sol / mur étanche en cuisson, prépa, plonge", "Travaux"),
 ("B11", "Plafonds sans condensation ni écaillage (ch. II §1c)", "Dalles métalliques existantes", "Nettoyage, remplacement des dalles abîmées", "À vérifier"),
 ("B12", "Ouvertures vers l'extérieur protégées des insectes (ch. II §1d)", "Portes arrière P1 / P2", "Ferme-portes + bas de porte à brosse ; portes fermées en exploitation (sinon moustiquaire ou rideau à lanières)", "Travaux"),
 ("B13", "Portes lisses et lavables (ch. II §1e)", "Portes existantes", "État à vérifier ; porte du passage froid lisse, avec hublot", "Conforme"),
 ("B14", "Surfaces en contact avec les denrées lisses, lavables, non toxiques (ch. II §1f)", "Plans de la prépa et ex-table à plaquer réutilisés", "Inox ou stratifié alimentaire en bon état ; changer le plateau de l'ex-table à plaquer s'il est en bois", "À vérifier"),
 ("B15", "Nettoyage et désinfection des ustensiles, eau chaude (ch. II §2)", "Plonge 2 bacs + lave-vaisselle frontal", "Conforme si l'eau chaude suffit pour plonge + lave-vaisselle + 6 lave-mains", "Conforme"),
 ("B16", "Lavage des denrées séparé du lavage des mains (ch. I §4, ch. II §3)", "Pas d'évier dédié en prépa", "Règle : aucun lavage de légumes sur place, tout arrive prêt à l'emploi du labo. Sinon, évier dédié en prépa", "Procédure"),
 ("§", "C — Équipements, froid et mesure (ch. V et IX ; arrêté du 21/12/2009 ; règl. 37/2005)"),
 ("C1", "Enceintes capables de maintenir les températures (ch. IX §5)", "V2 : murale ouverte à groupe logé, près d'une façade vitrée. C'est le défaut le plus fréquent en libre-service", "Murale à portes vitrées, classe M0 (−1 / +4 °C, norme EN ISO 23953), air réglé à 0/+2 °C, ligne de charge respectée", "Équipement"),
 ("C2", "Thermomètre lisible sur chaque enceinte froide", "À prévoir", "Afficheur sur la murale, les armoires et la chambre", "Équipement"),
 ("C3", "Surgelés : enregistrement de la T° de l'air (dispense seulement sous 10 m³) — règl. 37/2005", "Chambre négative ≈ 21 m³ (3 × 3 × 2,40 m)", "Enregistreur obligatoire : sondes connectées avec alarme, sur toutes les enceintes", "Équipement"),
 ("C4", "Mesure des T° des produits", "—", "Thermomètre sonde étalonné (réception, cuisson à cœur, maintien chaud)", "Équipement"),
 ("C5", "Huiles de friture : au plus 25 % de composés polaires — décret 2008-184", "Friteuse prévue", "Testeur électronique + registre des changements d'huile", "Équipement"),
 ("C6", "Matériel en contact alimentaire adapté", "—", "Bacs GN à couvercle, planches et ustensiles code couleur (cru / cuit / allergènes)", "Équipement"),
 ("§", "D — Déchets (ch. VI ; code de l'environnement)"),
 ("D1", "Conteneurs fermés dans les locaux de manipulation", "—", "Poubelle à pédale à chaque poste (cuisson, prépa, plonge, comptoir)", "Équipement"),
 ("D2", "Aire de stockage propre, à l'abri des nuisibles", "Recoin derrière P2, sans local maçonné", "Conteneurs à couvercle, sol lavable, sortie quotidienne vers l'aire du centre, nettoyage planifié", "Procédure"),
 ("D3", "Huiles usagées", "—", "Collecteur agréé, bordereaux conservés", "Document"),
 ("D4", "Tri à la source des biodéchets — art. L541-21-1 C. env.", "—", "Bac biodéchets dédié + collecte", "Équipement"),
 ("§", "E — Eau (ch. VII) et F — Personnel (ch. VIII et XII)"),
 ("E1", "Eau potable chaude et froide", "Réseau public", "Conforme ; vérifier la capacité du ballon d'eau chaude", "Conforme"),
 ("F1", "Tenue propre, coiffe, hygiène des mains", "—", "Tenues fournies, consignes affichées aux lave-mains", "Procédure"),
 ("F2", "Personnel malade : signalement et éviction", "—", "Procédure d'aptitude et de déclaration dans le PMS", "Procédure"),
 ("§", "G — Denrées et températures (ch. IX ; arrêté du 21/12/2009)"),
 ("G1", "Réception : T°, DLC, intégrité, étiquetage", "Table de réception à P1", "Fiche de réception ; T° relevée à chaque livraison ; refus si non conforme", "Procédure"),
 ("G2", "Transport labo → boutique en froid maîtrisé", "Non défini", "Véhicule frigorifique ou caisses isothermes avec plaques eutectiques ; T° relevée au départ et à l'arrivée", "Procédure"),
 ("G3", "Conservation : produits de la pêche frais 0/+2 °C, préparations culinaires élaborées à l'avance +3 °C max, sauf T° justifiée par l'analyse des dangers du fabricant", "Sushis, rolls, bowls", "T° fixée par le labo et imprimée sur l'étiquette ; cible matériel 0/+3 °C", "Procédure"),
 ("G4", "Surgelés à −18 °C ou moins", "Chambre négative existante", "Conforme si le groupe est en état ; enregistrement (C3)", "Conforme"),
 ("G5", "Décongélation en enceinte froide ou cuisson directe, jamais à l'ambiante", "Baos, gyozas, poulet pané", "Cuisson directe depuis le surgelé ; sinon décongélation en armoire positive, bac identifié et daté", "Procédure"),
 ("G6", "Cuisson à cœur suffisante (point critique)", "Poulet, gyozas", "T° à cœur par produit fixée par le labo, contrôlée à la sonde ; poulet livré cuit (pas de volaille crue manipulée en boutique)", "Procédure"),
 ("G7", "Remise en température : +63 °C à cœur en moins d'1 h ; maintien chaud à +63 °C minimum", "Four mixte, rampe chauffante", "Fiche de remise en T° ; durée maximale en rampe ; invendus chauds jetés", "Procédure"),
 ("G8", "Refroidissement rapide (+63 → +10 °C en moins de 2 h)", "Pas de cellule de refroidissement", "Interdit sur place : aucune préparation chaude refroidie pour être revendue", "Procédure"),
 ("G9", "Poisson consommé cru : traitement antiparasitaire (−20 °C 24 h ou −35 °C 15 h) ou justificatif d'exemption — règl. 853/2004, ann. III, section VIII", "Assuré au labo", "Attestation du labo au classeur (ou justificatif d'exemption pour la truite d'élevage)", "Document"),
 ("G10", "Riz vinaigré : acidification maîtrisée (Bacillus cereus)", "Fait au labo", "Fiche de validation de la recette et DLC validée par le labo", "Document"),
 ("G11", "Produits en vitrine : DLC, rotation, protection", "Murale", "Contrôle des DLC à l'ouverture et à la fermeture, premier entré premier sorti, ligne de charge respectée", "Procédure"),
 ("G12", "Stockage séparé cru / cuit, allergènes, retail", "Réserve, armoires", "Étagères identifiées, arachide à part, rien au sol (étagères à 15 cm minimum)", "Procédure"),
 ("G13", "Invendus et dons", "Fin de journée", "Uniquement avant la DLC, avec traçabilité (anti-gaspi, dons)", "Procédure"),
 ("§", "H — Nuisibles, nettoyage, vaisselle"),
 ("H1", "Lutte contre les nuisibles", "—", "Contrat de dératisation / désinsectisation avec plan des postes ; piège à insectes à plaque engluée", "Document"),
 ("H2", "Plan de nettoyage et désinfection", "—", "Plan écrit (quoi, quand, qui, produit, dosage) + fiches techniques ; nettoyages tracés", "Document"),
 ("H3", "Vaisselle réutilisable (AGEC) : propreté et stockage", "Lave-vaisselle frontal", "Rangement fermé de la vaisselle propre, loin du retour sale", "Procédure"),
]

def audit_synthese(c):
    h1(c, 40, H - 50, "Audit DDPP — synthèse et verdict", size=17)
    para(c, 40, H - 80, 540,
         "**Verdict\n"
         "Le local peut être aux normes DDPP sans aucun gros œuvre. La V2 telle quelle aurait exposé à plusieurs écarts lors d'une inspection, tous corrigeables par de petits travaux et du matériel. Avec les corrections de la V3, l'agencement ne présente plus d'écart identifiable sur plan.\n"
         "\n"
         "Il reste trois choses à sécuriser :\n"
         "1. Le statut sanitaire du labo (agrément CE ou dérogation). C'est le seul point vraiment bloquant : sans lui, la boutique ne peut pas être livrée.\n"
         "2. L'état réel de l'existant (revêtements, extraction, groupe froid, cloison du fond de niche), à vérifier lors d'une visite sur site.\n"
         "3. Le fonctionnement au quotidien : documents, relevés de température, nettoyage, allergènes. C'est sur ce terrain que se jouent la plupart des remarques d'inspection et la note Alim'confiance.\n"
         "\n"
         "**Méthode et limites\n"
         "• Audit sur plans et sur programme, point par point, d'après le règlement (CE) 852/2004 annexe II (chapitres I à XII), les règlements 853/2004, 178/2002, 1169/2011 et 37/2005, l'arrêté du 21 décembre 2009, les décrets 2008-184 et 2011-731 et le GBPH restaurateur.\n"
         "• Ce n'est pas une visite sur site : l'état des sols, murs, plafonds, réseaux et équipements laissés n'a pas pu être constaté.\n"
         "• Pour une boutique en vente directe, la DDPP n'approuve pas les plans à l'avance : elle reçoit une déclaration puis inspecte, en général sans prévenir. Personne ne peut donc garantir « zéro remarque ». En revanche, on peut retirer tous les écarts de conception et préparer les preuves attendues.\n"
         "• Deux réflexes pour être tranquille : envoyer le plan hygiène à la DDPP 49 pour un avis informel avant travaux, et faire un audit blanc (consultant ou laboratoire) juste avant l'ouverture puis un mois après.", 8.6)
    rows = [
     ("Vaisselle sale et déchets de la salle traversaient la cuisson", "Passe desserte salle → plonge (ouverture en cloison légère)", "Travaux"),
     ("Réassort froid par la cuisson (seule liaison avant / arrière)", "Passage froid par l'ex-niche vitrine (fond de niche ouvert, porte va-et-vient)", "Travaux"),
     ("Pas de lave-mains en cuisson ni au comptoir", "2 lave-mains créés + commande non manuelle partout", "Travaux"),
     ("Murale ouverte : risque de T° > +3 °C en vitrine", "Murale à portes vitrées classe M0", "Équipement"),
     ("Chambre négative > 10 m³ sans enregistrement", "Sondes connectées avec enregistrement et alarme", "Équipement"),
     ("Pas de rangement des produits d'entretien", "Armoire fermée dans le couloir DEGT N°2", "Équipement"),
     ("Murs de la cuisson non garantis lavables (friteuse)", "Crédence inox + plinthes à gorge", "Travaux"),
     ("Portes arrière sans protection contre les nuisibles", "Ferme-portes + bas de porte à brosse", "Travaux"),
     ("Statut du labo non vérifié", "Agrément CE ou dérogation à confirmer avant engagement", "Bloquant"),
    ]
    c.setFont("FB", 11); c.setFillColor(NAVY); c.drawString(620, H - 80, "Écarts trouvés dans la V2 → correction V3")
    y = table_paged(c, 620, H - 92, [("Écart V2", 210), ("Correction V3", 220), ("Type", 70)], rows, 7.4, lambda: H - 60)
    para(c, 620, y - 16, 500,
         "**Les 4 situations qui font fermer un établissement à l'inspection — et la parade prévue\n"
         "• Rupture de la chaîne du froid → murale fermée, enregistreurs avec alarme, relevés.\n"
         "• Produits périmés ou sans traçabilité → contrôle des DLC deux fois par jour, étiquettes labo, registre de réception.\n"
         "• Locaux sales, nuisibles → plan de nettoyage, contrat 3D, portes arrière protégées.\n"
         "• Absence de maîtrise du chaud (cuisson, maintien, huiles) → sonde, fiches, testeur d'huile.", 8.2)
    audit_cart(c, "AUDIT DDPP — SYNTHÈSE", 1)

def audit_plan(c):
    draw_shell(c, terrace_text=False); draw_equipment(c, labels=False)
    label_min(c, [(290, 1107, "MURALE LS"), (220, 735, "ÎLOT"), (507, 640, "CAISSE"), (840, 560, "PRÉPA"),
                  (790, 930, "CUISSON"), (1072, 120, "PLONGE"), (1215, 990, "CH. NÉGATIVE"), (1277, 572, "RÉSERVE"),
                  (1277, 250, "VESTIAIRES / WC"), (1470, 960, "DÉCHETS")])
    pts = [(1, 698, 700, "Passage froid par l'ex-niche : dépose vitrine, ouverture du fond de niche, porte va-et-vient"),
           (2, 920, 240, "Passe desserte salle → plonge (cloison légère)"),
           (3, 590, 520, "Lave-mains comptoir (commande non manuelle)"),
           (4, 960, 1010, "Lave-mains cuisson (commande non manuelle)"),
           (5, 770, 1010, "Crédence inox derrière four mixte + friteuse"),
           (6, 290, 1020, "Murale à portes vitrées classe M0 + afficheur T°"),
           (7, 1450, 470, "Armoire fermée produits d'entretien"),
           (8, 1040, 335, "Armoire positive déplacée dans le DEGT N°1"),
           (9, 1500, 30, "P1 / P2 : ferme-portes + bas de porte à brosse"),
           (10, 1300, 1070, "Chambre négative : enregistreur + alarme (et sondes sur toutes les enceintes)"),
           (11, 880, 640, "Prépa / cuisson / plonge : luminaires protégés, joints, plinthes à gorge (selon état)"),
           (12, 1500, 740, "Conteneurs à couvercle, bac biodéchets, huiles usagées")]
    for n, x, y, _ in pts: badge(c, x, y, str(n), MAG, 7)
    badge(c, 1500, 655, "9", MAG, 7)
    c.setFont("FB", 12); c.setFillColor(NAVY); c.drawString(40, H - 40, "Audit DDPP — plan des corrections (V3)")
    X = 905; y = H - 75
    c.setFont("FB", 9); c.setFillColor(MAG); c.drawString(X, y, "Corrections à réaliser"); y -= 14
    for n, _, _, s in pts:
        c.setFillColor(MAG); c.setFont("FB", 7.4); c.drawString(X, y, f"{n}.")
        y = para(c, X + 14, y, 258, s, 7.4)
        y -= 3
    y -= 6
    para(c, X, y, 272, "Aucune de ces corrections ne touche à la structure : deux ouvertures dans des cloisons légères existantes (1 et 2), de la plomberie (3 et 4), de la finition (5, 9, 11) et du matériel (6, 7, 8, 10, 12).", 7.4)
    flows(c)
    cartouche(c, "AUDIT DDPP — PLAN DES CORRECTIONS", phase="AUDIT DDPP", ech="1/75", num=2)

def audit_grille(c):
    def hdr():
        h1(c, 40, H - 50, "Audit DDPP — grille point par point")
        c.setFont("F", 7.5); c.setFillColor(GREY)
        c.drawString(40, H - 68, "Type d'action : Conforme · Travaux · Équipement · Procédure (à écrire dans le PMS et appliquer) · Document (à avoir au classeur) · À vérifier (sur site) · Bloquant")
        return H - 78
    state = {"n": 3}
    def new_page():
        audit_cart(c, "AUDIT DDPP — GRILLE", state["n"]); state["n"] += 1
        c.showPage()
        return hdr()
    y0 = hdr()
    cols = [("Réf.", 40), ("Exigence (texte)", 320), ("Situation du projet", 280), ("Action pour être tranquille", 350), ("Type", 80)]
    table_paged(c, 40, y0, cols, GRILLE, 7.2, new_page)
    audit_cart(c, "AUDIT DDPP — GRILLE", state["n"])
    return state["n"]

def audit_temperatures(c, num):
    h1(c, 40, H - 50, "Audit DDPP — températures et points critiques à surveiller")
    cols = [("Produit / étape", 230), ("Stockage", 170), ("Vitrine / service", 190), ("Contrôle", 230), ("Si hors limite", 250)]
    rows = [
     ("Sushis, makis, rolls (poisson cru)", "0/+3 °C (T° de l'étiquette labo)", "Murale fermée 0/+3 °C", "Enregistreur + relevé produit à la sonde 2 fois/jour", "Produit au-dessus de la T° de l'étiquette : retiré et noté ; vérifier l'enceinte"),
     ("Bowls, salades, baos froids, desserts", "0/+3 °C", "Murale fermée 0/+3 °C", "Idem", "Idem"),
     ("Garnitures et sauces des baos", "0/+3 °C", "Plan réfrigéré", "Relevé à l'ouverture et au service", "Garniture jetée"),
     ("Surgelés (baos, gyozas, poulet pané)", "−18 °C ou moins", "—", "Enregistreur de la chambre (obligatoire > 10 m³)", "Remontée au-dessus de −15 °C : produits à évaluer, ne pas recongeler"),
     ("Réception des livraisons du labo", "—", "—", "T° de chaque livraison à la sonde, DLC, étiquettes", "Livraison refusée ou isolée, labo prévenu"),
     ("Cuisson / remise en température", "—", "+63 °C à cœur en moins d'1 h", "Sonde, fiche par produit (T° à cœur fixée par le labo)", "Prolonger la cuisson ; sinon jeter"),
     ("Maintien chaud au retrait", "—", "+63 °C minimum, durée maximale écrite au PMS", "Sonde au service", "Produit jeté, jamais refroidi ni remis en vente"),
     ("Huile de friture", "—", "—", "Testeur chaque jour de friture", "20 % de composés polaires : prévoir le changement ; 25 % : changer immédiatement"),
     ("Retail sec (sauces, chips, cacahuètes, thés)", "Ambiante, au sec, à 15 cm du sol", "Îlot", "Dates (DLC / DDM) chaque semaine", "Produit retiré"),
    ]
    y = table(c, 40, H - 70, cols, rows, 7.4)
    para(c, 40, y - 18, 1080,
         "**Base réglementaire : l'arrêté du 21/12/2009 fixe 0/+2 °C pour les produits de la pêche frais et +3 °C pour les préparations culinaires élaborées à l'avance, mais il autorise une autre température si l'analyse des dangers du fabricant la justifie. Pour les sushis, c'est donc la température et la DLC validées par le labo, imprimées sur l'étiquette, qui font foi : il faut qu'elles soient écrites et justifiées dans le PMS du labo. Le matériel de la boutique est dimensionné pour tenir 0/+3 °C afin de couvrir tous les cas.", 8.2)
    audit_cart(c, "AUDIT DDPP — TEMPÉRATURES", num)

def audit_classeur(c, num):
    h1(c, 40, H - 50, "Audit DDPP — classeur à présenter le jour de l'inspection et questions au labo")
    para(c, 40, H - 80, 540,
         "**Classeur DDPP de la boutique (à tenir à jour, au bureau)\n"
         "• Récépissé de déclaration d'activité (Cerfa 13984).\n"
         "• Attestations de formation hygiène (14 h) du responsable et du remplaçant.\n"
         "• Plan de maîtrise sanitaire : bonnes pratiques, analyse des dangers, procédures, plan de nettoyage et fiches techniques des produits d'entretien.\n"
         "• Relevés de température : export des enregistreurs (chambre, murale, armoires), fiches de réception, fiches de cuisson et de maintien chaud.\n"
         "• Registre des huiles (mesures, changements) et bordereaux de collecte.\n"
         "• Traçabilité : bons de livraison et étiquettes des lots, conservés au moins jusqu'à la DLC + 6 mois.\n"
         "• Fiches produits du labo : composition, allergènes, T° de conservation, DLC.\n"
         "• Statut sanitaire du labo : numéro d'agrément CE ou copie de la dérogation.\n"
         "• Attestation du traitement antiparasitaire du poisson cru (ou justificatif d'exemption).\n"
         "• Procédure de retrait / rappel, contacts DDPP 49 et labo.\n"
         "• Contrat de lutte contre les nuisibles et rapports de passage.\n"
         "• Tableau des allergènes par produit.\n"
         "• Résultats d'autocontrôles (prélèvements de surface et de produits, au moins à l'ouverture puis périodiquement).\n"
         "• Attestations d'entretien de l'extraction et de vérification des équipements froids.", 8.4)
    para(c, 620, H - 80, 500,
         "**Questions à poser au labo de Maulévrier (avant de figer l'offre)\n"
         "1. Quel est son statut sanitaire aujourd'hui (agrément CE, dérogation, simple déclaration) et couvre-t-il la livraison d'un autre établissement ?\n"
         "2. Combien de kg par semaine de produits à base de poisson et de volaille la boutique recevra-t-elle ? Est-ce sous les plafonds de la dérogation ?\n"
         "3. Comment le poisson cru est-il assaini (congélation −20 °C 24 h, ou exemption documentée pour la truite d'élevage) ?\n"
         "4. Quelles DLC et quelles T° de conservation sont validées pour chaque produit, et sur quelles études ?\n"
         "5. Le riz vinaigré est-il acidifié selon une recette validée ?\n"
         "6. Le poulet peut-il être livré cuit (sous vide) pour éviter toute volaille crue en boutique ?\n"
         "7. Les légumes et garnitures peuvent-ils arriver prêts à l'emploi (pas de lavage sur place) ?\n"
         "8. Comment seront faites les livraisons (véhicule, caisses isothermes, T° au départ) ?\n"
         "9. Les étiquettes sont-elles complètes (allergènes en évidence, lot, T°, marque sanitaire le cas échéant) ?\n"
         "\n"
         "**Après l'ouverture\n"
         "Faire relire le PMS par un consultant ou un laboratoire, puis un audit blanc à J+30 avec prélèvements de surface. Les premières semaines (rush, nouvelle équipe) sont celles où la DDPP trouve le plus d'écarts de pratique.", 8.4)
    audit_cart(c, "AUDIT DDPP — CLASSEUR ET LABO", num)

def main():
    c = canvas.Canvas(OUT, pagesize=(W, H))
    c.setTitle("Dossier d'adaptation V3 — L'Arbre à Makis — Cellule 09 La Séguinière")
    c.setAuthor("L'Arbre à Makis")
    for f in (page_cover, page_programme, page_reemploi, page_plan, page_hygiene, page_cuisson, page_incendie, page_pmr,
              page_ddpp, page_travaux, page_facade, page_demarches):
        f(c); c.showPage()
    c.save()
    a = canvas.Canvas(OUT_AUDIT, pagesize=(W, H))
    a.setTitle("Audit DDPP — L'Arbre à Makis — Cellule 09 La Séguinière")
    a.setAuthor("L'Arbre à Makis")
    audit_synthese(a); a.showPage()
    audit_plan(a); a.showPage()
    n = audit_grille(a); a.showPage()
    audit_temperatures(a, n + 1); a.showPage()
    audit_classeur(a, n + 2); a.showPage()
    a.save()
    print("OK", OUT); print("OK", OUT_AUDIT)
    tot = 0
    for lab, r in SURF:
        ar = area(r); tot += ar; print(f"{lab:55s} {ar:6.1f}")
    print("TOTAL", round(tot, 1))

if __name__ == "__main__":
    main()
