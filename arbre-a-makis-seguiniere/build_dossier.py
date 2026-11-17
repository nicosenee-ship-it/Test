# -*- coding: utf-8 -*-
"""Dossier d'adaptation - L'Arbre à Makis - Cellule 09 Marques Avenue La Séguinière.
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
OUT = os.path.join(HERE, "Dossier_LAM_La_Seguiniere_cellule09.pdf")
LOGO = os.path.join(HERE, "logo_lam.png")

pdfmetrics.registerFont(TTFont("F", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("FB", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("FI", "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"))

W, H = landscape(A3)
NAVY = HexColor("#13213c"); GREEN = HexColor("#8cc63f"); SALMON = HexColor("#e8765a")
BLUE = HexColor("#2f6db5"); RED = HexColor("#d0312d"); GREY = HexColor("#777777")
LGREY = HexColor("#e9e9e9"); WALL = HexColor("#3a3a3a"); WOOD = HexColor("#d9b98a")
ORANGE = HexColor("#f29c1f"); BROWN = HexColor("#8b5a2b"); PURPLE = HexColor("#7d4fb3")

# --------------------------------------------------------------------------- géométrie
DEPTH, WIDTH = 1545, 1150
S = 28.3465 / 75.0          # 1/75 : points par cm réel
OX, OY = 150, 735           # origine page (x=0 vitrage, y=0 mur haut)

def P(x, y):
    return OX + x * S, OY - y * S

ZONES = {  # nom: (x1, y1, x2, y2, couleur de fond, libellé)
 "vente":   (0, 0, 655, 1150, HexColor("#f6f1e7"), None),
 "alcove":  (655, 0, 983, 427, HexColor("#f6f1e7"), None),
 "service": (545, 330, 655, 1150, HexColor("#eef3e6"), None),
 "prep":    (655, 427, 983, 736, HexColor("#e3f0fb"), None),
 "cuisson": (655, 820, 1060, 1150, HexColor("#fde9e3"), None),
 "plonge":  (983, 0, 1160, 280, HexColor("#efe7f7"), None),
 "degt1a":  (983, 280, 1160, 736, HexColor("#f4f4f4"), None),
 "degt1b":  (655, 736, 1060, 820, HexColor("#f4f4f4"), None),
 "degt1c":  (1060, 700, 1395, 830, HexColor("#f4f4f4"), None),
 "vest":    (1160, 0, 1395, 445, HexColor("#f4f4f4"), None),
 "reserve": (1160, 445, 1395, 700, HexColor("#fff6d9"), None),
 "cf":      (1060, 830, 1370, 1150, HexColor("#dcecff"), None),
 "cfgap":   (1370, 830, 1395, 1150, HexColor("#f4f4f4"), None),
 "degt2":   (1395, 0, 1545, 790, HexColor("#f4f4f4"), None),
 "dechets": (1395, 790, 1545, 1040, HexColor("#efe2d3"), None),
 "tgbt":    (1395, 1040, 1545, 1150, HexColor("#f4f4f4"), None),
}

SURF = [  # (libellé, liste de rectangles) -> surfaces calculées
 ("Espace vente libre-service + caisse + salle", [(0, 0, 545, 1150), (545, 0, 655, 330), (655, 0, 983, 427)]),
 ("Zone service derrière le comptoir (personnel)", [(545, 330, 655, 1150)]),
 ("Cuisson (terminal chaud)", [(655, 820, 1060, 1150)]),
 ("Préparation froide / assemblage", [(655, 427, 983, 736)]),
 ("Plonge", [(983, 0, 1160, 280)]),
 ("Chambre froide positive (ex-négative)", [(1060, 830, 1370, 1150)]),
 ("Réserve sèche (CF) + armoires négatives", [(1160, 445, 1395, 700)]),
 ("Vestiaires H/F, WC personnel, bureau", [(1160, 0, 1395, 445)]),
 ("Local déchets", [(1395, 790, 1545, 1040)]),
 ("Circulations arrière + réception + TGBT", [(983, 280, 1160, 736), (655, 736, 1060, 820), (1060, 700, 1395, 830),
                                            (1370, 830, 1395, 1150), (1395, 0, 1545, 790), (1395, 1040, 1545, 1150)]),
]

def area(rects):
    return sum((x2 - x1) * (y2 - y1) for x1, y1, x2, y2 in rects) / 1e4

# cloisons (x1,y1,x2,y2) en ligne médiane ; épaisseur 10 cm
PARTS = [
 (983, 0, 983, 427),                      # salle / plonge
 (655, 427, 983, 427), (655, 427, 655, 736), (655, 736, 983, 736), (983, 427, 983, 736),   # prépa froide
 (655, 820, 655, 1150), (655, 820, 1060, 820), (1060, 820, 1060, 1150),                   # cuisson
 (983, 280, 1160, 280), (1160, 0, 1160, 700),                                              # plonge / bloc vest+réserve
 (1395, 0, 1395, 700), (1160, 445, 1395, 445), (1160, 700, 1395, 700),                    # bloc vestiaires / réserve
 (1160, 110, 1395, 110), (1160, 275, 1395, 275), (1280, 110, 1280, 445),                  # bureau / vest / WC
 (1395, 790, 1545, 790), (1395, 1040, 1545, 1040), (1395, 790, 1395, 1150),              # local déchets + TGBT
]
CF_PARTS = [(1160, 445, 1395, 445), (1160, 700, 1395, 700), (1160, 445, 1160, 700), (1395, 445, 1395, 700),
            (1395, 790, 1545, 790), (1395, 1040, 1545, 1040), (1395, 790, 1395, 1040)]
# ouvertures (x1,y1,x2,y2) : portes -> (axe, a, b, sens)
DOORS = [
 ("v", 655, 470, 550), ("v", 983, 600, 690), ("v", 655, 1050, 1140), ("h", 820, 960, 1050),
 ("h", 280, 1050, 1140), ("v", 1395, 540, 630), ("v", 1395, 150, 230), ("v", 1395, 320, 400),
 ("v", 1395, 20, 100), ("h", 790, 1420, 1520), ("v", 1160, 610, 690),
]
WINDOWS = [("v", 655, 850, 990, "Passe chaude"), ("v", 983, 195, 270, "Passe desserte")]

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
def draw_shell(c, cf=False):
    # terrasse (début)
    rect(c, -330, 0, 0, WIDTH, fill=HexColor("#f3f3f3"), stroke=None)
    for yy in (0, WIDTH):
        line(c, -330, yy, 0, yy, GREY, 0.5)
    line(c, -330, -25, -330, WIDTH + 25, GREY, 0.6, dash=(4, 2, 1, 2))
    txt(c, -170, 575, "TERRASSE EXTÉRIEURE\nCOUVERTE (sous auvent)\nprofondeur totale 10,60 m\n→ terrasse saisonnière\n≈ 16 places (à valider\navec le centre)", 6.5, "F", GREY, rot=90)
    # zones
    for k, (x1, y1, x2, y2, col, _) in ZONES.items():
        rect(c, x1, y1, x2, y2, fill=col, stroke=None)
    # murs latéraux mitoyens + fond
    wc = RED if cf else WALL
    rect(c, -20, -25, DEPTH + 25, 0, fill=wc, stroke=None)
    rect(c, -20, WIDTH, DEPTH + 25, WIDTH + 25, fill=wc, stroke=None)
    rect(c, DEPTH, 0, DEPTH + 25, WIDTH, fill=WALL, stroke=None)
    for (a, b) in [(15, 115), (640, 740)]:
        rect(c, DEPTH - 1, a, DEPTH + 26, b, fill=white, stroke=None)
        X, Y = P(DEPTH + 25, a)
        c.saveState(); c.setStrokeColor(black); c.setLineWidth(0.4)
        c.arc(X - (b - a) * S, Y - (b - a) * S, X + (b - a) * S, Y + (b - a) * S, 90, -90) if False else None
        c.restoreState()
        line(c, DEPTH + 25, a, DEPTH + 25 + (b - a), a, black, 0.5)
    # poteaux
    for xp in (-20, 622, 1225, DEPTH):
        for yp in (-35, WIDTH - 5):
            rect(c, xp - 18, yp, xp + 22, yp + 40, fill=HexColor("#555555"), stroke=black, lw=0.3)
    # façade vitrée
    rect(c, -6, 0, 6, 455, fill=HexColor("#bfe0f5"), stroke=BLUE, lw=0.4)
    rect(c, -6, 695, 6, WIDTH, fill=HexColor("#bfe0f5"), stroke=BLUE, lw=0.4)
    for a, b in [(455, 575), (695, 575)]:
        X, Y = P(0, a); r = abs(b - a) * S
        c.saveState(); c.setStrokeColor(black); c.setLineWidth(0.4); c.setDash(2, 1.5)
        if a < b: c.arc(X - r, Y - r, X + r, Y + r, 180, 90)
        else: c.arc(X - r, Y - r, X + r, Y + r, 180, -90)
        c.restoreState()
        line(c, 0, a, -abs(b - a), a, black, 0.6)
    # cloisons
    for (x1, y1, x2, y2) in PARTS:
        is_cf = cf and (x1, y1, x2, y2) in CF_PARTS
        t = 6
        if x1 == x2: rect(c, x1 - t, y1, x1 + t, y2, fill=RED if is_cf else WALL, stroke=None)
        else: rect(c, x1, y1 - t, x2, y1 + t, fill=RED if is_cf else WALL, stroke=None)
    # chambre froide (panneaux)
    rect(c, 1060, 830, 1370, 1150, fill=None, stroke=BLUE, lw=2.2)
    # portes
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
    # porte chambre froide coulissante
    rect(c, 1200, 822, 1310, 838, fill=white, stroke=BLUE, lw=0.8)
    for ax, k, a, b, lab in WINDOWS:
        rect(c, k - 7, a, k + 7, b, fill=HexColor("#ffe7a8"), stroke=ORANGE, lw=0.8)

def draw_equipment(c, labels=True):
    # --- murale libre-service
    mods = ["Sushis\n& makis", "Rolls\n& plateaux", "Bowls\n& salades", "Baos & snacks\nfroids", "Desserts\n& boissons"]
    for i, m in enumerate(mods):
        x1 = 40 + i * 120
        rect(c, x1, 0, x1 + 120, 85, fill=HexColor("#cfe6f7"), stroke=NAVY, lw=0.6)
        if labels: txt(c, x1 + 60, 42, m, 5.2, "F", NAVY)
    if labels: txt(c, 360, 103, "MURALE RÉFRIGÉRÉE LIBRE-SERVICE  5 × 1,20 m  (0/+3 °C, rideaux de nuit)", 5.6, "FB", NAVY)
    # --- îlot retail "L'Arbre"
    rect(c, 110, 250, 350, 470, fill=WOOD, stroke=BROWN, lw=0.8, r=12)
    circle(c, 230, 360, 32, fill=HexColor("#6aa84f"), stroke=HexColor("#38761d"))
    if labels:
        txt(c, 230, 282, "ÎLOT « L'ARBRE »  retail", 5.4, "FB", black)
        txt(c, 230, 432, "sauces, chips d'algues,\ncacahuètes wasabi, thés…", 4.8, "F", black)
    # --- comptoir caisse
    rect(c, 470, 330, 545, 820, fill=WOOD, stroke=BROWN, lw=0.8)
    rect(c, 470, 380, 500, 470, fill=HexColor("#ffffff"), stroke=BROWN, lw=0.4)
    if labels:
        txt(c, 507, 425, "CAISSE 1\nPMR h 0,80", 4.6, "FB", black, rot=90)
        txt(c, 507, 560, "CAISSE 2", 4.8, "FB", black, rot=90)
        txt(c, 507, 655, "impulse retail", 4.4, "F", black, rot=90)
        txt(c, 507, 765, "RETRAIT\nCHAUD", 4.6, "FB", black, rot=90)
    rect(c, 470, 300, 545, 330, fill=None, stroke=BROWN, lw=0.4, dash=(2, 1.5))
    if labels: txt(c, 507, 315, "portillon", 4, "F", BROWN)
    # lave-mains zone service + écrans menu
    rect(c, 612, 340, 652, 378, fill=white, stroke=BLUE, lw=0.6); circle(c, 632, 359, 10, stroke=BLUE)
    if labels:
        txt(c, 600, 640, "ZONE SERVICE\n(personnel)", 5.2, "FB", HexColor("#4f7a28"), rot=90)
        txt(c, 645, 600, "écrans menu au-dessus", 4.2, "FI", GREY, rot=90)
    # --- places assises
    def tabouret(x, y): circle(c, x, y, 17, fill=white, stroke=GREY, lw=0.5)
    for (a, b) in [(110, 430), (735, 1110)]:
        rect(c, 0, a, 45, b, fill=WOOD, stroke=BROWN, lw=0.5)
        n = 5 if a == 110 else 6
        for i in range(n): tabouret(75, a + (b - a) * (i + 0.5) / n)
    if labels:
        txt(c, 22, 270, "mange-debout vitrine", 4.2, "F", BROWN, rot=90)
        txt(c, 22, 922, "mange-debout vitrine", 4.2, "F", BROWN, rot=90)
    # banquette bas + 4 tables
    rect(c, 125, 1095, 470, 1150, fill=HexColor("#2c3e5c"), stroke=None)
    for i, xt in enumerate((135, 220, 305, 390)):
        rect(c, xt, 1025, xt + 65, 1085, fill=WOOD, stroke=BROWN, lw=0.5)
        if i != 3: rect(c, xt + 12, 975, xt + 53, 1015, fill=white, stroke=GREY, lw=0.5)
    if labels:
        txt(c, 422, 990, "table PMR", 4.2, "FB", BLUE)
        txt(c, 300, 1122, "banquette", 4.4, "F", white)
    # alcôve détente
    rect(c, 665, 0, 925, 55, fill=HexColor("#2c3e5c"), stroke=None)
    for xt in (675, 760, 845):
        rect(c, xt, 65, xt + 70, 130, fill=WOOD, stroke=BROWN, lw=0.5)
        rect(c, xt + 15, 140, xt + 55, 180, fill=white, stroke=GREY, lw=0.5)
    for xt in (680, 790):
        rect(c, xt, 260, xt + 80, 320, fill=WOOD, stroke=BROWN, lw=0.5)
        rect(c, xt + 20, 215, xt + 60, 252, fill=white, stroke=GREY, lw=0.5)
        if xt == 680: rect(c, xt + 20, 328, xt + 60, 365, fill=white, stroke=GREY, lw=0.5)
    rect(c, 935, 190, 977, 300, fill=HexColor("#ffe7a8"), stroke=ORANGE, lw=0.6)
    if labels:
        txt(c, 795, 27, "banquette", 4.4, "F", white)
        txt(c, 820, 395, "ESPACE DÉTENTE (calme)", 5.4, "FB", NAVY)
        txt(c, 956, 245, "desserte\nplateaux", 3.8, "F", BROWN, rot=90)
        txt(c, 842, 340, "PMR", 4.2, "FB", BLUE)
    # --- prépa froide
    rect(c, 820, 437, 975, 500, fill=HexColor("#cfe6f7"), stroke=NAVY, lw=0.5)
    rect(c, 665, 560, 730, 726, fill=HexColor("#cfe6f7"), stroke=NAVY, lw=0.5)
    rect(c, 860, 650, 975, 726, fill=HexColor("#dddddd"), stroke=GREY, lw=0.5)
    rect(c, 937, 560, 975, 600, fill=white, stroke=BLUE, lw=0.6); circle(c, 956, 580, 9, stroke=BLUE)
    if labels:
        txt(c, 897, 468, "armoire positive", 4.4)
        txt(c, 697, 643, "saladette\n/ plan réfrigéré", 4.2, rot=90)
        txt(c, 917, 688, "plan inox\nétiquetage", 4.2)
        txt(c, 820, 540, "PRÉPARATION FROIDE\nassemblage bowls,\nréassort vitrines", 5.2, "FB", NAVY)
    # --- cuisson
    rect(c, 665, 1035, 1052, 1145, fill=None, stroke=RED, lw=0.8, dash=(4, 2))
    eq = [(670, 760, "four mixte\n6 GN1/1"), (768, 830, "friteuse\n1×10 L"), (838, 900, "cuiseur\nvapeur\nbaos"),
          (908, 1050, "plan inox\nréfrigéré")]
    for x1, x2, lab in eq:
        rect(c, x1, 1055, x2, 1142, fill=HexColor("#f6c9bd") if "plan" not in lab else HexColor("#cfe6f7"), stroke=black, lw=0.5)
        if labels: txt(c, (x1 + x2) / 2, 1098, lab, 4.0)
    rect(c, 665, 850, 735, 990, fill=HexColor("#dddddd"), stroke=GREY, lw=0.5)
    rect(c, 1010, 960, 1050, 1000, fill=white, stroke=BLUE, lw=0.6); circle(c, 1030, 980, 9, stroke=BLUE)
    if labels:
        txt(c, 700, 920, "dressage\n+ lampe\nchauffante", 4.0)
        txt(c, 880, 925, "CUISSON", 6.5, "FB", RED)
        txt(c, 880, 960, "hotte 3,8 m (filtres à chocs)", 4.3, "FI", RED)
    # --- plonge
    rect(c, 995, 8, 1150, 70, fill=HexColor("#dddddd"), stroke=GREY, lw=0.5)
    rect(c, 1080, 80, 1150, 150, fill=HexColor("#cfcfe8"), stroke=GREY, lw=0.5)
    rect(c, 992, 160, 1050, 272, fill=HexColor("#dddddd"), stroke=GREY, lw=0.5)
    rect(c, 1100, 170, 1150, 272, fill=None, stroke=GREY, lw=0.5)
    if labels:
        txt(c, 1072, 39, "plonge 2 bacs + douchette", 4.0)
        txt(c, 1115, 115, "lave-\nvaisselle\ncapot", 3.8)
        txt(c, 1021, 216, "entrée\nsale", 3.8, rot=90)
        txt(c, 1125, 221, "sortie\npropre", 3.8, rot=90)
        txt(c, 1072, 110, "PLONGE", 5.5, "FB", PURPLE, rot=90)
    # --- réserve
    rect(c, 1170, 455, 1385, 490, fill=None, stroke=GREY, lw=0.5)
    rect(c, 1170, 655, 1385, 690, fill=None, stroke=GREY, lw=0.5)
    rect(c, 1170, 505, 1240, 640, fill=HexColor("#cfe6f7"), stroke=NAVY, lw=0.5)
    if labels:
        txt(c, 1277, 473, "étagères retail / emballages", 4.0)
        txt(c, 1205, 572, "2 armoires\nnégatives\n−18 °C", 3.8, rot=90)
        txt(c, 1312, 572, "RÉSERVE\nSÈCHE\n(existante CF)", 5.0, "FB", BROWN)
        txt(c, 1277, 673, "étagères (≥ 15 cm du sol)", 4.0)
    # --- vestiaires
    if labels:
        txt(c, 1277, 55, "BUREAU", 5, "FB")
        txt(c, 1220, 192, "VEST. H\ncasiers", 4.6, "FB"); txt(c, 1337, 192, "WC +\nlave-mains", 4.2)
        txt(c, 1220, 360, "VEST. F\ncasiers", 4.6, "FB"); txt(c, 1337, 360, "WC +\nlave-mains", 4.2)
    # --- chambre froide
    if labels:
        txt(c, 1215, 960, "CHAMBRE FROIDE\nPOSITIVE 0/+3 °C\n(ex-négative 3,00 × 3,00\nconservée, groupe\nà reconvertir)", 5.0, "FB", BLUE)
        txt(c, 1255, 760, "rampes (CF à +0,14)", 4.2, "FI", GREY)
    # --- réception / déchets / TGBT
    rect(c, 1488, 130, 1542, 330, fill=HexColor("#dddddd"), stroke=GREY, lw=0.5)
    rect(c, 1500, 345, 1540, 385, fill=white, stroke=BLUE, lw=0.6); circle(c, 1520, 365, 9, stroke=BLUE)
    for i, yb in enumerate((830, 888, 946)):
        rect(c, 1420, yb, 1480, yb + 52, fill=HexColor("#b9d7a8") if i == 2 else HexColor("#cccccc"), stroke=GREY, lw=0.4)
    rect(c, 1495, 840, 1540, 890, fill=HexColor("#f1d58a"), stroke=GREY, lw=0.4)
    circle(c, 1515, 1010, 22, fill=HexColor("#8b5a2b"), stroke=None)
    if labels:
        txt(c, 1515, 230, "RÉCEPTION\ncontrôle T°\ndécartonnage", 4.0, "FB", rot=90)
        txt(c, 1470, 450, "DEGT N°2", 5.4, "FB", GREY, rot=90)
        txt(c, 1517, 920, "huiles\nusagées", 3.6)
        txt(c, 1450, 1018, "OM / tri / bio", 3.6, "F", black)
        txt(c, 1470, 1095, "TGBT / EDF", 4.6, "FB")
        txt(c, 1470, 812, "LOCAL DÉCHETS", 4.4, "FB", BROWN)
        txt(c, 1075, 500, "DEGT N°1", 5.4, "FB", GREY, rot=90)
        txt(c, DEPTH + 60, 65, "P1\nentrée\npersonnel\n+ livraisons", 4.6, "FB", NAVY, "l")
        txt(c, DEPTH + 60, 690, "P2\nsortie déchets\n+ issue de\nsecours arrière", 4.6, "FB", BROWN, "l")
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
        cells = [wrap(v, w, "FB" if bold else "F") for v, (_, w) in zip(r, cols)]
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
def page_cover(c):
    c.setFillColor(NAVY); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(white); c.roundRect(W / 2 - 170, H - 330, 340, 240, 10, fill=1, stroke=0)
    c.drawImage(LOGO, W / 2 - 150, H - 320, 300, 220, preserveAspectRatio=True, mask="auto")
    c.setFillColor(white); c.setFont("FB", 24)
    c.drawCentredString(W / 2, H - 390, "DOSSIER D'ADAPTATION DU LOCAL")
    c.setFont("F", 14)
    c.drawCentredString(W / 2, H - 418, "Point de vente « prêt-à-manger » japonais — vitrines libre-service, retail, consommation sur place")
    c.drawCentredString(W / 2, H - 438, "avec terminal de cuisson à l'arrière")
    c.setStrokeColor(GREEN); c.setLineWidth(2); c.line(W / 2 - 200, H - 456, W / 2 + 200, H - 456)
    c.setFont("FB", 12)
    c.drawCentredString(W / 2, H - 484, "CELLULE N°09 — ESPACE COMMERCIAL MARQUES AVENUE — RUE DU BOCAGE — 49280 LA SÉGUINIÈRE")
    c.setFont("F", 10.5)
    c.drawCentredString(W / 2, H - 504, "Reprise du local exploité par La Mie Câline (DAT « terminal de cuisson », ChauvierePajot, 20/03/2015)")
    c.setFont("FB", 10); c.drawString(170, 300, "PIÈCES DU DOSSIER")
    pieces = ["01  Programme, principes et tableau des surfaces", "02  Plan RDC projeté — aménagement", "03  Plan hygiène — marche en avant, flux et températures (DDPP)",
              "04  Espace cuisson — définition, équipements, puissance, extraction", "05  Plan de sécurité incendie (ERP type N + M)",
              "06  Plan d'accessibilité PMR", "07  Notice hygiène — check-list de conformité DDPP", "08  Descriptif des travaux par lot (conservé / modifié / créé)",
              "09  Façade et enseigne projetées", "10  Démarches, calendrier et points à valider"]
    c.setFont("F", 9.5)
    for i, p in enumerate(pieces): c.drawString(170, 282 - i * 15, p)
    c.setFont("FB", 10); c.drawString(700, 300, "STATUT DU DOCUMENT")
    para(c, 700, 282, 330, "Esquisse et programme établis par L'Arbre à Makis pour cadrer le projet avec le bailleur, l'architecte / maître d'œuvre, le bureau de contrôle et la DDPP de Maine-et-Loire.\n"
         "Le fond de plan est redessiné à partir du DAT 2015 (cotes non relevées sur site).\n"
         "Les pièces réglementaires définitives (formulaire Cerfa 13824, notices sécurité et accessibilité signées, plans d'exécution) restent à produire par le maître d'œuvre à partir de ce programme.", 9, col=white)
    c.setFont("F", 8); c.setFillColor(HexColor("#b8c2d6")); c.drawString(170, 50, "L'Arbre à Makis — produits préparés à Maulévrier — version du 17/11/2026")

def page_programme(c):
    h1(c, 40, H - 50, "01 — Programme et principes d'adaptation")
    txt_l = (
        "**Ce que l'on reprend du local La Mie Câline\n"
        "• L'enveloppe : cellule de 11,50 × 15,45 m (≈ 178 m² intérieurs), murs mitoyens coupe-feu 1 h, façade vitrée avec porte 2 vantaux de 2,40 m, 2 portes arrière vers la circulation de service.\n"
        "• Le « back-office » déjà cloisonné : bloc vestiaires H/F + WC personnel + bureau, réserve coupe-feu, chambre froide 3 × 3 m sur rampes, plonge, local cuisson avec conduit d'extraction, écran de cantonnement et commandes d'arrêt d'urgence, TGBT.\n"
        "• Le principe sécurité incendie validé en 2015 pour un « terminal de cuisson » ouvert sur la vente.\n"
        "\n"
        "**Ce qui change\n"
        "• L'avant devient un espace libre-service : une murale réfrigérée de 6 m sur le mur latéral, un îlot central « L'Arbre » pour le retail (sauces, chips d'algues, cacahuètes wasabi, thés, baguettes…), une caisse centrale au fond face à l'entrée, avec retrait des produits chauds.\n"
        "• Les places assises sont regroupées côté opposé à la murale et dans l'alcôve du fond (espace détente au calme) : ≈ 30 places intérieures + terrasse saisonnière sous auvent.\n"
        "• L'ex-zone « pousse / plaquage » boulangerie est supprimée. Le local cuisson est recentré sur 3 appareils électriques (four mixte, friteuse, cuiseur vapeur) avec une passe chaude vers le comptoir.\n"
        "• La chambre froide négative devient positive (stock du jour livré par le labo) ; le surgelé (baos, gyozas, poulet pané) passe en 2 armoires négatives dans la réserve.\n"
        "• Création d'un local déchets fermé côté sortie P2, d'une zone de réception/décartonnage à l'entrée P1 et d'une passe « desserte » salle → plonge.\n"
        "\n"
        "**Principes retenus pour la DDPP\n"
        "• Marche en avant dans l'espace (et dans le temps quand l'espace est partagé) : livraison par P1, sortie des déchets par P2, vaisselle sale qui ne traverse pas les zones de préparation.\n"
        "• Les produits crus sensibles (poisson cru, riz vinaigré) arrivent finis et conditionnés du labo de Maulévrier : pas de découpe de poisson cru sur place. Sur place : remise en température, cuisson minute des produits chauds, assemblage simple et mise en vitrine.\n"
        "• Chaque zone de manipulation a son lave-mains à commande non manuelle ; chaque enceinte froide a son enregistreur de température.\n"
        "• Remise directe au consommateur : simple déclaration d'activité à la DDPP (pas d'agrément pour la boutique). C'est le labo qui doit être couvert (agrément CE ou dérogation) pour livrer la boutique."
    )
    para(c, 40, H - 80, 620, txt_l, 8.6)
    # tableau surfaces
    rows = []
    tot = 0
    for lab, rects in SURF:
        a = area(rects)
        tot += a
        rows.append((lab, f"{a:.1f} m²"))
    rows.append(("TOTAL intérieur (hors cloisons)", f"{tot:.1f} m²", "B"))
    c.setFont("FB", 10); c.setFillColor(NAVY); c.drawString(700, H - 80, "Tableau des surfaces (calculées sur le plan redessiné)")
    y = table(c, 700, H - 90, [("Zone", 300), ("Surface", 80)], rows, 7.6)
    rows2 = [("Mange-debout le long de la vitrine (5 + 6 tabourets)", "11"), ("Tables + banquette côté mur (dont 1 PMR)", "8"),
             ("Espace détente au fond (dont 1 PMR)", "10"), ("Total intérieur", "29", "B"), ("Terrasse sous auvent (saisonnier, accord centre)", "≈ 16")]
    c.setFont("FB", 10); c.setFillColor(NAVY); c.drawString(700, y - 22, "Places assises")
    y = table(c, 700, y - 32, [("Emplacement", 300), ("Places", 80)], rows2, 7.6)
    para(c, 700, y - 18, 400,
         "**À noter : au-delà de 20 personnes servies simultanément (assises ou debout, intérieur + terrasse), la loi AGEC impose la vaisselle réutilisable pour la consommation sur place (art. L541-15-10 du code de l'environnement, depuis le 01/01/2023). D'où la plonge équipée d'un lave-vaisselle et la passe desserte. Le cas des produits vendus préemballés en libre-service puis mangés sur place est à faire confirmer (DGCCRF / juriste).", 7.8)
    cartouche(c, "PROGRAMME ET SURFACES", ech="—", num=1)

def page_plan(c):
    draw_shell(c); draw_equipment(c); dims(c)
    scale_bar(c, 150, 120)
    c.setFont("FB", 12); c.setFillColor(NAVY); c.drawString(40, H - 40, "02 — Plan RDC projeté — aménagement L'Arbre à Makis")
    X = 905; y = H - 75
    c.setFont("FB", 9); c.setFillColor(NAVY); c.drawString(X, y, "Parcours client"); y -= 4
    y = para(c, X, y - 10, 270,
             "1. Entrée face à l'îlot « L'Arbre » (produits phares + retail).\n"
             "2. Murale libre-service sur le mur latéral, ordonnée sushis → rolls → bowls → baos → desserts/boissons.\n"
             "3. Caisse centrale au fond, dans l'axe de la porte : 2 postes dont 1 PMR, retrait des baos/chauds à la passe.\n"
             "4. Places : mange-debout en vitrine, tables côté mur, espace détente au calme dans l'alcôve.\n"
             "5. Desserte plateaux à côté de la plonge : la vaisselle sale ne revient pas par le comptoir.", 7.4)
    y -= 6
    c.setFont("FB", 9); c.setFillColor(NAVY); c.drawString(X, y, "Back-office"); y -= 14
    y = para(c, X, y, 270,
             "• Cloisons existantes conservées autant que possible (prépa froide, cuisson, plonge, vestiaires, réserve CF, chambre froide).\n"
             "• Cuisson redéfinie : 4,05 × 3,30 m, appareils électriques sous hotte le long du mur mitoyen, passe chaude vers le comptoir (voir planche 04).\n"
             "• Chambre froide existante passée en positive. Surgelés en armoires négatives.\n"
             "• Réception/décartonnage à P1, local déchets fermé à P2.", 7.4)
    y -= 8
    y = legend_box(c, X, y, [("box", HexColor("#f6f1e7"), "Espace public (vente + salle)"), ("box", HexColor("#eef3e6"), "Zone service derrière comptoir"),
                             ("box", HexColor("#e3f0fb"), "Préparation froide"), ("box", HexColor("#fde9e3"), "Cuisson"),
                             ("box", HexColor("#efe7f7"), "Plonge"), ("box", HexColor("#dcecff"), "Froid (chambre positive)"),
                             ("box", HexColor("#fff6d9"), "Stockage sec"), ("box", HexColor("#efe2d3"), "Déchets"),
                             ("box", HexColor("#ffe7a8"), "Passes (chaude / desserte)"), ("dot", BLUE, "Lave-mains à commande non manuelle")], "Légende")
    cartouche(c, "PLAN RDC PROJETÉ", num=2)

def page_hygiene(c):
    draw_shell(c); draw_equipment(c, labels=False)
    # étiquettes minimales
    for (x, y, s) in [(340, 45, "MURALE LS"), (230, 360, "ÎLOT"), (507, 575, "CAISSE"), (820, 560, "PRÉPA\nFROIDE"),
                      (880, 925, "CUISSON"), (1072, 120, "PLONGE"), (1215, 990, "CH. FROIDE +"), (1277, 572, "RÉSERVE"),
                      (1277, 250, "VESTIAIRES\n/ WC"), (1470, 990, "DÉCHETS")]:
        txt(c, x, y, s, 6, "FB", HexColor("#333333"))
    # Flux produits (vert)
    arrow_path(c, [(DEPTH + 40, 65), (1460, 65), (1460, 600), (1460, 760), (1250, 760), (1250, 840)], HexColor("#2e8b57"))
    arrow_path(c, [(1460, 600), (1400, 585)], HexColor("#2e8b57"), lw=1.2)
    arrow_path(c, [(1200, 760), (1110, 760), (1110, 650), (990, 645)], HexColor("#2e8b57"))
    arrow_path(c, [(1040, 778), (1005, 778), (1005, 830)], HexColor("#2e8b57"))
    arrow_path(c, [(700, 510), (620, 510), (600, 300), (520, 290), (520, 130), (450, 110)], HexColor("#2e8b57"), dash=(5, 2))
    arrow_path(c, [(700, 920), (610, 920), (560, 790)], HexColor("#c0392b"))
    # Déchets (marron)
    arrow_path(c, [(1100, 300), (1100, 718), (1420, 718), (1420, 800)], BROWN, dash=(2, 2))
    arrow_path(c, [(900, 800), (1085, 800), (1085, 718)], BROWN, dash=(2, 2), head=False)
    arrow_path(c, [(1530, 880), (1530, 700), (DEPTH + 45, 700)], BROWN, dash=(2, 2))
    # Vaisselle sale (orange)
    arrow_path(c, [(150, 990), (420, 880), (720, 400), (930, 240), (1010, 230)], ORANGE, dash=(6, 2))
    # Personnel (bleu)
    arrow_path(c, [(DEPTH + 40, 40), (1420, 40), (1420, 190), (1370, 190)], BLUE, lw=1.2)
    arrow_path(c, [(1370, 360), (1420, 360), (1420, 690), (1180, 760), (1000, 760), (950, 760)], BLUE, lw=1.2, dash=(1, 2))
    # Clients (gris)
    arrow_path(c, [(-60, 575), (60, 575), (60, 180), (560 - 100, 170)], GREY, lw=1.2)
    arrow_path(c, [(80, 520), (300, 560), (450, 560)], GREY, lw=1.2)
    # températures
    for (x, y, s, col) in [(340, 140, "0/+3 °C", BLUE), (1215, 1060, "0/+3 °C", BLUE), (1205, 640, "−18 °C", BLUE),
                           (900, 470, "armoire 0/+3 °C", BLUE), (700, 1010, "≥ 63 °C (maintien chaud)", RED)]:
        X, Y = P(x, y); c.saveState(); c.setFillColor(white); c.setStrokeColor(col)
        wdt = pdfmetrics.stringWidth(s, "FB", 6) + 6; c.roundRect(X - wdt / 2, Y - 5, wdt, 11, 3, fill=1, stroke=1)
        c.setFillColor(col); c.setFont("FB", 6); c.drawCentredString(X, Y - 2, s); c.restoreState()
    # étapes
    for (x, y, s) in [(1500, 110, "1"), (1440, 600, "2"), (1250, 900, "3"), (800, 650, "4"), (850, 1000, "4'"), (470, 230, "5"),
                      (560, 720, "6"), (1050, 120, "7"), (1470, 840, "8")]:
        badge(c, x, y, s, NAVY)
    c.setFont("FB", 12); c.setFillColor(NAVY); c.drawString(40, H - 40, "03 — Plan hygiène : marche en avant, flux et températures")
    X = 905; y = H - 70
    y = legend_box(c, X, y, [("line", HexColor("#2e8b57"), "Produits (labo → stockage → préparation → vitrine)"),
                             ("line", HexColor("#c0392b"), "Produits chauds (cuisson → passe → client)"),
                             ("dash", BROWN, "Déchets (→ local déchets → P2)"), ("dash", ORANGE, "Vaisselle sale (salle → desserte → plonge)"),
                             ("line", BLUE, "Personnel (P1 → vestiaires → lavage mains → zones)"), ("line", GREY, "Clients")], "Flux")
    y -= 6
    c.setFont("FB", 9); c.setFillColor(NAVY); c.drawString(X, y, "Étapes de la marche en avant"); y -= 14
    y = para(c, X, y, 272,
             "1 Réception par P1 : contrôle T° à cœur et DLC, décartonnage (aucun carton au-delà), bacs navettes du labo.\n"
             "2 Stockage sec / retail (réserve CF) et surgelés en armoires −18 °C.\n"
             "3 Stockage frais en chambre froide positive, rangement FIFO / DLC.\n"
             "4 Préparation froide : assemblage bowls, étiquetage. 4' Cuisson minute ou remise en température.\n"
             "5 Mise en vitrine par le portillon (réassort hors pic si possible).\n"
             "6 Vente : retrait des produits chauds à la passe.\n"
             "7 Plonge : vaisselle sale arrivée par la passe desserte, sortie propre côté opposé.\n"
             "8 Déchets en sacs fermés vers le local déchets, sortie par P2.", 7.2)
    y -= 6
    c.setFont("FB", 9); c.setFillColor(RED); c.drawString(X, y, "Croisements résiduels et parades"); y -= 14
    para(c, X, y, 272,
         "• Le couloir des rampes est partagé produits / déchets : séparation dans le temps (livraisons le matin avant 10 h 30, sortie des déchets après le service et en fin de journée) + nettoyage entre les deux, à écrire dans le PMS.\n"
         "• Le réassort de la murale traverse la vente : en bacs fermés, hors rush.\n"
         "• Températures à valider avec le labo : c'est lui qui fixe la T° de conservation et la DLC de chaque produit (sushis poisson cru en général 0/+3 °C).", 7.2)
    cartouche(c, "HYGIÈNE — MARCHE EN AVANT", num=3)

def page_cuisson(c):
    h1(c, 40, H - 50, "04 — Espace cuisson : définition")
    # zoom plan 1/25
    s2 = 28.3465 / 25.0
    ox, oy = 150, H - 120
    def Q(x, y): return ox + (x - 640) * s2, oy - (y - 800) * s2
    def R(x1, y1, x2, y2, fill=None, stroke=black, lw=0.6, dash=None):
        X1, Y1 = Q(x1, y1); X2, Y2 = Q(x2, y2); c.saveState(); c.setLineWidth(lw)
        if dash: c.setDash(list(dash))
        if fill is not None: c.setFillColor(fill)
        c.setStrokeColor(stroke if stroke is not None else black)
        c.rect(min(X1, X2), min(Y1, Y2), abs(X2 - X1), abs(Y2 - Y1), fill=1 if fill is not None else 0, stroke=1 if stroke is not None else 0)
        c.restoreState()
    def T(x, y, s, size=7, font="F", col=black, rot=0):
        X, Y = Q(x, y); c.saveState(); c.setFillColor(col); c.setFont(font, size); c.translate(X, Y); c.rotate(rot)
        ls = s.split("\n")
        for i, l in enumerate(ls): c.drawCentredString(0, (len(ls) - 1) * size * 0.6 - i * size * 1.2 - size * 0.35, l)
        c.restoreState()
    R(655, 820, 1060, 1150, fill=HexColor("#fde9e3"), stroke=None)
    R(640, 1150, 1075, 1175, fill=RED, stroke=None)
    for (x1, y1, x2, y2) in [(649, 820, 661, 1150), (655, 814, 1060, 826), (1054, 820, 1066, 1150)]:
        R(x1, y1, x2, y2, fill=WALL, stroke=None)
    R(649, 850, 661, 990, fill=HexColor("#ffe7a8"), stroke=ORANGE, lw=1)
    R(649, 1050, 661, 1140, fill=white, stroke=None); R(960, 814, 1050, 826, fill=white, stroke=None)
    R(665, 1035, 1052, 1148, fill=None, stroke=RED, lw=1.2, dash=(5, 3))
    eq = [(670, 760, "Four mixte\n6 GN 1/1\nélec.\n≈ 10 kW"), (768, 830, "Friteuse\n1 × 10 L\nélec.\n≈ 9 kW"),
          (838, 900, "Cuiseur\nvapeur\nbaos\n≈ 3 kW"), (908, 1050, "Plan inox réfrigéré\n(garnitures baos,\nsauces)\n≈ 0,5 kW")]
    for x1, x2, lab in eq:
        R(x1, 1055, x2, 1142, fill=HexColor("#f6c9bd") if "Plan" not in lab else HexColor("#cfe6f7"))
        T((x1 + x2) / 2, 1098, lab, 6.3)
    R(665, 850, 735, 990, fill=HexColor("#dddddd"), stroke=GREY); T(700, 920, "Plan de\ndressage\n+ rampe\nchauffante", 6.3)
    R(1010, 960, 1050, 1000, fill=white, stroke=BLUE, lw=1); T(1030, 980, "LM", 6, "FB", BLUE)
    T(700, 1000, "← passe chaude vers comptoir", 6, "FI", ORANGE)
    T(860, 1020, "HOTTE murale 3,80 × 1,10 m — filtres à chocs, débordement ≥ 15 cm", 6.5, "FB", RED)
    T(860, 900, "CUISSON  ≈ 13,4 m²\nsol grès antidérapant R12, siphon,\nmurs inox / PVC alimentaire h ≥ 2 m", 8, "FB", RED)
    T(1005, 800, "porte vers DEGT N°1 ↑", 6, "FI", GREY); T(610, 1095, "porte\n← zone\nservice", 6, "FI", GREY)
    X, Y = Q(1030, 1120); c.setFillColor(RED); c.circle(X, Y, 6, fill=1, stroke=0); c.setFillColor(white); c.setFont("FB", 5); c.drawCentredString(X, Y - 2, "F")
    X, Y = Q(640, 1030); c.setFillColor(RED); c.rect(X - 14, Y - 6, 12, 12, fill=1, stroke=0)
    c.setFillColor(black); c.setFont("F", 6); c.drawString(X - 70, Y - 20, "arrêts d'urgence (cuisson,")
    c.drawString(X - 70, Y - 28, "élec., ventilation) hors cuisine")
    c.setFont("FI", 7); c.setFillColor(GREY); c.drawString(ox, oy - 390 * s2 - 10, "Zoom échelle 1/25 — F = extincteur classe F (huiles) + couverture anti-feu ; LM = lave-mains à commande non manuelle")
    # Texte droite
    X = 690; y = H - 80
    rows = [("Four mixte 6 niveaux GN 1/1", "10", "Baos (vapeur), remise en T° gyozas, karaage, plats chauds labo"),
            ("Friteuse électrique 1 bac 10 L", "9", "Poulet croustillant, gyozas frits, tempura"),
            ("Cuiseur vapeur baos (paniers)", "3", "Option : supprimé si le four mixte suffit en pointe"),
            ("Plan inox réfrigéré", "—", "Garnitures et sauces des baos (froid, hors puissance de cuisson)"),
            ("Rampe chauffante à la passe", "≈1", "Maintien ≥ 63 °C quelques minutes avant remise"),
            ("TOTAL appareils de cuisson", "≈ 22", "Au-dessus de 20 kW → « grande cuisine » au sens du règlement ERP", "B")]
    c.setFont("FB", 10); c.setFillColor(NAVY); c.drawString(X, y, "Équipement proposé (électrique uniquement, pas de gaz)")
    y = table(c, X, y - 10, [("Appareil", 160), ("kW", 35), ("Usage", 265)], rows, 7.4)
    y -= 18
    c.setFont("FB", 10); c.setFillColor(NAVY); c.drawString(X, y, "Le choix qui conditionne tout : la puissance installée"); y -= 14
    y = para(c, X, y, 460,
             "**Option A — rester sous 20 kW (recommandée pour le pilote)\n"
             "Four mixte (10 kW) + friteuse (9 kW) = 19 kW, la vapeur des baos étant faite au four mixte. La cuisine n'est pas une « grande cuisine » : contraintes allégées, extraction et coût réduits. Limite : débit en pointe sur les baos.\n"
             "**Option B — dépasser 20 kW (cuiseur vapeur en plus, wok à induction…)\n"
             "Grande cuisine ouverte sur la vente : écran de cantonnement fixe E 15 / M1 descendant à au moins 0,50 m sous plafond (La Mie Câline en avait un de 60 cm), conduit d'extraction aux performances du règlement, arrêts d'urgence hors cuisine. C'est la configuration déjà acceptée en 2015 : si l'écran, le conduit et l'extracteur sont encore en place et en bon état, l'option B coûte surtout en vérifications.\n"
             "Dans les deux cas, le bureau de contrôle confirme le classement sur la liste réelle des appareils (puissances utiles des fiches techniques).", 7.8)
    y -= 4
    c.setFont("FB", 10); c.setFillColor(NAVY); c.drawString(X, y, "Extraction, réseaux, hygiène"); y -= 14
    para(c, X, y, 460,
         "• Réutiliser le conduit existant (classé M0/A2-s1,d0, SF ¼ h) et l'extracteur en toiture (400 °C ½ h) : à faire inspecter et ramoner avant travaux, vérifier le débit (≈ 3 000 à 4 000 m³/h pour 3,80 m de hotte avec friteuse, à dimensionner par le cuisiniste) et prévoir l'air de compensation.\n"
         "• Nettoyage des filtres chaque semaine, ramonage du conduit au moins une fois par an (attestation à garder pour la commission de sécurité et l'assureur).\n"
         "• Électricité : ≈ 22 kW de cuisson + froid (murale 6 m, chambre froide, armoires) + lave-vaisselle → vérifier l'abonnement et le TGBT existants (ordre de grandeur 60 à 72 kVA tri, à confirmer par l'électricien).\n"
         "• Huiles de friture : bidons fermés dans le local déchets, collecte par un prestataire agréé (bordereaux à conserver).\n"
         "• Eaux grasses : demander à l'Agglomération du Choletais si un séparateur à graisses est exigé ; le regard Ø 64 du fond de cellule peut servir de point de raccordement.\n"
         "• Lave-mains à commande non manuelle, distributeurs savon et essuie-mains à usage unique, poubelle à pédale, thermomètre sonde.", 7.8)
    cartouche(c, "ESPACE CUISSON", ech="1/25", num=4)

def page_incendie(c):
    draw_shell(c, cf=True); draw_equipment(c, labels=False)
    for (x, y, s) in [(340, 45, "MURALE LS"), (230, 360, "ÎLOT"), (507, 575, "CAISSE"), (820, 560, "PRÉPA FROIDE"),
                      (880, 925, "CUISSON"), (1072, 120, "PLONGE"), (1215, 990, "CH. FROIDE"), (1277, 572, "RÉSERVE"), (1470, 920, "DÉCHETS")]:
        txt(c, x, y, s, 6, "FB", HexColor("#333333"))
    # cantonnement
    rect(c, 640, 805, 1075, 1150, fill=None, stroke=RED, lw=1.2, dash=(6, 3))
    txt(c, 860, 790, "écran de cantonnement existant (h ≥ 0,50 m, E15 / M1) — à conserver si cuisson > 20 kW", 5, "FB", RED)
    # conduit extraction
    arrow_path(c, [(860, 1090), (1000, 900), (1250, 720), (1500, 330), (DEPTH, 300)], RED, lw=1, dash=(3, 2), head=False)
    txt(c, 1330, 460, "conduit d'extraction existant\nM0 / A2-s1,d0 – SF ¼ h", 5, "FI", RED)
    # dégagements
    arrow_path(c, [(200, 575), (-80, 575)], HexColor("#1a9e3f"), lw=3)
    arrow_path(c, [(1470, 700), (DEPTH + 70, 690)], HexColor("#1a9e3f"), lw=3)
    arrow_path(c, [(1470, 120), (DEPTH + 70, 65)], HexColor("#1a9e3f"), lw=2)
    txt(c, 150, 620, "dégagement principal 2 UP (2,40 m)", 5.5, "FB", HexColor("#1a9e3f"))
    # BAES / extincteurs / commandes
    for (x, y) in [(15, 420), (15, 730), (1530, 640), (1530, 120), (1100, 500), (800, 400), (600, 1100)]:
        X, Y = P(x, y); c.setFillColor(HexColor("#1a9e3f")); c.rect(X - 6, Y - 3, 12, 6, fill=1, stroke=0)
    for (x, y, k) in [(60, 700, "E"), (630, 420, "E"), (1030, 1120, "F"), (1180, 760, "C"), (1480, 1080, "C"), (1500, 450, "E")]:
        X, Y = P(x, y); c.setFillColor(RED); c.circle(X, Y, 6, fill=1, stroke=0); c.setFillColor(white); c.setFont("FB", 6); c.drawCentredString(X, Y - 2, k)
    X, Y = P(625, 1035); c.setFillColor(RED); c.rect(X - 7, Y - 7, 14, 14, fill=1, stroke=0)
    X, Y = P(20, 470); c.setFillColor(ORANGE); c.rect(X - 5, Y - 5, 10, 10, fill=1, stroke=0)
    c.setFont("FB", 12); c.setFillColor(NAVY); c.drawString(40, H - 40, "05 — Plan de sécurité incendie (ERP type N + M, 5e catégorie)")
    X = 905; y = H - 70
    y = legend_box(c, X, y, [("line", RED, "Parois coupe-feu (murs mitoyens CF 1 h, réserve, local déchets)"),
                             ("dash", RED, "Écran de cantonnement cuisson / conduit d'extraction"),
                             ("line", HexColor("#1a9e3f"), "Dégagements / sens d'évacuation"),
                             ("box", HexColor("#1a9e3f"), "Bloc autonome d'éclairage de sécurité (BAES)"),
                             ("dot", RED, "Extincteurs : E eau 6 L · C CO₂ 2 kg · F classe F"),
                             ("box", RED, "Arrêts d'urgence cuisson / élec. / ventilation"),
                             ("box", ORANGE, "Coupure d'urgence enseigne lumineuse")], "Légende sécurité")
    y -= 6
    para(c, X, y, 272,
         "**Classement (estimation à confirmer)\n"
         "Type N (restauration) + M (vente). Effectif public : 29 places assises + surface de vente ≈ 75 personnes au total, très en dessous du seuil de 200 → 5e catégorie, comme La Mie Câline.\n"
         "**Ce que l'on reprend tel quel\n"
         "• Murs mitoyens CF 1 h, réserve CF, porte arrière d'accès au couloir de service.\n"
         "• Écran de cantonnement, conduit d'extraction et extracteur, commandes d'arrêt d'urgence (à vérifier et faire attester).\n"
         "**Ce qui est nouveau\n"
         "• Local déchets : parois et bloc-porte à degré coupe-feu à faire valider par le bureau de contrôle.\n"
         "• Extincteur classe F + couverture anti-feu près de la friteuse.\n"
         "• BAES et extincteurs repositionnés selon le nouveau mobilier.\n"
         "• Mobilier et décor (arbre, végétal, bois) : réaction au feu M1 / B-s3,d0 minimum, végétal stabilisé ou artificiel classé ; à prévoir dès la consultation de l'agenceur.\n"
         "• Circulations ≥ 1,20 m (1,40 à 1,65 m sur les allées principales), porte d'entrée dégagée.\n"
         "• Vérifications périodiques : électricité, extraction, extincteurs, registre de sécurité.", 7.2)
    cartouche(c, "SÉCURITÉ INCENDIE", num=5)

def page_pmr(c):
    draw_shell(c); draw_equipment(c, labels=False)
    for (x, y, s) in [(340, 45, "MURALE LS"), (230, 360, "ÎLOT"), (820, 560, "PRÉPA FROIDE"), (880, 925, "CUISSON")]:
        txt(c, x, y, s, 6, "FB", HexColor("#333333"))
    G = HexColor("#1a9e3f")
    for (cx, cy) in [(400, 560), (250, 175), (280, 960), (840, 400)]:
        circle(c, cx, cy, 75, fill=None, stroke=G, lw=1)
    txt(c, 400, 640, "Ø 1,50 m", 5, "FB", G)
    for (a, b, xx, lab) in [(85, 250, 300, "1,65 m"), (470, 1025, 300, "≥ 1,40 m")]:
        line(c, xx, a, xx, b, G, 0.8); txt(c, xx + 25, (a + b) / 2, lab, 5.5, "FB", G, rot=90)
    line(c, 350, 380, 470, 380, G, 0.8); txt(c, 410, 368, "1,20 m", 5.5, "FB", G)
    arrow_path(c, [(-80, 575), (60, 575), (60, 180), (450, 170)], G, lw=1.6)
    arrow_path(c, [(60, 575), (400, 560), (465, 430)], G, lw=1.6)
    for (x, y, s) in [(507, 425, "caisse PMR"), (422, 1000, "table PMR"), (720, 345, "table PMR")]:
        badge(c, x, y, "♿", BLUE, 7); txt(c, x, y + 30, s, 5.2, "FB", BLUE)
    c.setFont("FB", 12); c.setFillColor(NAVY); c.drawString(40, H - 40, "06 — Plan d'accessibilité PMR (ERP existant)")
    # détail comptoir
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
         "**Exigences reprises (arrêté du 8 décembre 2014 — ERP existants)\n"
         "• Entrée de plain-pied, seuil ≤ 2 cm, porte 2,40 m.\n"
         "• Bandes de repérage contrastées sur la vitrine à 1,10 m et 1,60 m (déjà prévues en 2015, à intégrer au graphisme LAM).\n"
         "• Cheminement ≥ 1,20 m partout (1,20 m entre îlot et comptoir, point le plus serré), 1,40 à 1,65 m sur les allées principales ; aires de rotation Ø 1,50 m devant la caisse, l'îlot, les tables PMR.\n"
         "• Murale libre-service : une partie de chaque famille de produits à hauteur 0,40 à 1,30 m.\n"
         "• Îlot retail : tablettes basses accessibles, pas de produit uniquement en hauteur.\n"
         "• 2 emplacements de table accessibles (vide sous table h 0,70 m, prof. 0,30 m).\n"
         "• Éclairage ≥ 200 lux sur le cheminement, 300 lux à la caisse.\n"
         "• Écrans menu : prévoir une carte papier en gros caractères à la caisse.\n"
         "**Sanitaires clients\n"
         "Le local n'a pas de WC clients (La Mie Câline s'appuyait sur les sanitaires publics du centre, accessibles PMR). À faire confirmer par écrit par le centre et à mentionner dans la notice d'accessibilité.\n"
         "**Registre public d'accessibilité à tenir à disposition dès l'ouverture.", 7.2)
    cartouche(c, "ACCESSIBILITÉ PMR", num=6)

def page_ddpp(c):
    h1(c, 40, H - 50, "07 — Notice hygiène : check-list de conformité DDPP de Maine-et-Loire")
    para(c, 40, H - 72, 1100, "Cadre : règlement (CE) 852/2004 (hygiène), règlement (CE) 853/2004, arrêté du 21/12/2009 (commerce de détail, températures), "
         "GBPH restaurateur, décret 2011-731 (formation hygiène). La boutique vend directement au consommateur : déclaration d'activité, pas d'agrément.", 8)
    cols = [("Thème", 150), ("Exigence", 390), ("Réponse dans le projet", 420), ("Statut", 110)]
    rows = [
     ("Déclaration", "Déclarer l'établissement avant l'ouverture (formulaire Cerfa 13984, en ligne sur mesdemarches.agriculture.gouv.fr)", "Déclaration au nom de l'exploitant de la boutique, activité « restauration commerciale + commerce de détail »", "À faire J−30"),
     ("Approvisionnement", "Le fournisseur qui livre un autre établissement doit être agréé CE ou bénéficier d'une dérogation (quantités, distance ≤ 80 km)", "Labo de Maulévrier à ≈ 15 km : vérifier que son statut couvre ce flux et les volumes (poisson, volaille)", "Point bloquant"),
     ("Formation", "Au moins une personne formée à l'hygiène en restauration commerciale (14 h)", "Responsable de boutique + un second titulaire pour les absences", "À planifier"),
     ("PMS / HACCP", "Plan de maîtrise sanitaire écrit : BPH, HACCP, traçabilité, gestion des non-conformités, retraits/rappels", "Adapter le PMS du labo : réception, froid, cuisson minute, refroidissement interdit sur place, invendus", "À rédiger"),
     ("Marche en avant", "Pas de croisement propre/sale, ou séparation dans le temps documentée", "Voir planche 03 : P1 entrées, P2 déchets, passe desserte, horaires réception/déchets", "Prévu"),
     ("Locaux", "Sols, murs, plafonds lisses, lavables, imperméables ; angles arrondis ; siphons ; éclairage protégé", "Grès antidérapant R12 + plinthes à gorge (cuisson, plonge, prépa, déchets), panneaux PVC alimentaire/inox h 2 m, dalles de plafond lessivables, luminaires étanches", "Lot carrelage / doublage"),
     ("Lavage des mains", "Lave-mains à commande non manuelle, eau chaude, savon, essuie-mains à usage unique, près des postes", "6 lave-mains : cuisson, prépa froide, zone service caisse, plonge, réception, + WC personnel", "Prévu"),
     ("Personnel", "Vestiaires séparés des zones alimentaires, WC sans ouverture directe sur une zone de manipulation", "Bloc vestiaires H/F + WC existant ouvrant sur le couloir DEGT N°2", "Existant"),
     ("Froid", "Enceintes capables de tenir les T° réglementaires ou fixées par le fabricant ; contrôle et enregistrement", "Chambre positive 0/+3 °C, murale LS 0/+3 °C avec affichage T°, armoires −18 °C ; sondes connectées + alarme", "Prévu"),
     ("Vitrines libre-service", "Produits protégés, T° maîtrisée en façade, étiquetage complet (DLC, allergènes, lot)", "Produits préemballés et étiquetés au labo ; rideaux de nuit ; contrôle T° 2 fois/jour", "Prévu"),
     ("Chaîne chaude", "Cuisson à cœur, maintien ≥ 63 °C, pas de refroidissement de préparations chaudes sur place", "Cuisson minute, rampe chauffante courte à la passe, invendus chauds jetés", "Procédure"),
     ("Huiles de friture", "Contrôle des composés polaires, renouvellement, collecte des huiles usagées", "Testeur d'huile, registre, collecte par prestataire", "Procédure"),
     ("Allergènes", "Information écrite sur les 14 allergènes pour tout produit vendu, y compris non emballé", "Étiquettes labo + classeur/QR code allergènes en caisse pour les baos et produits chauds", "Prévu"),
     ("Origine des viandes", "Origine des viandes servies (bœuf, et porc/volaille/ovin) quand elles sont achetées crues", "Poulet livré mariné ou pané par le labo : vérifier si l'obligation s'applique ; l'afficher par précaution (« poulet élevé et abattu en France »)", "À vérifier"),
     ("Eau", "Eau potable, eau chaude sanitaire aux points de lavage", "Réseau existant ; préparateur ECS à dimensionner pour plonge + lave-vaisselle", "Lot plomberie"),
     ("Nuisibles", "Plan de lutte contre les nuisibles, protections", "Contrat dératisation/désinsectisation, désinsectiseur à plaque engluée (pas à grille), bas de portes arrière", "Contrat"),
     ("Déchets", "Stockage dans des conteneurs fermés, local lavable ; tri à la source des biodéchets (obligatoire depuis 2024)", "Local déchets fermé, siphon, point d'eau proche ; bacs OM / emballages / biodéchets / huiles", "Prévu"),
     ("Invendus", "Traçabilité des invendus, dons possibles sous conditions", "Destruction tracée ou anti-gaspi en fin de journée (Too Good To Go) dans la limite des DLC", "Procédure"),
    ]
    table(c, 40, H - 92, cols, rows, 7.1)
    cartouche(c, "NOTICE HYGIÈNE — DDPP", ech="—", num=7)

def page_travaux(c):
    h1(c, 40, H - 50, "08 — Descriptif des travaux par lot")
    cols = [("Lot", 140), ("Conservé", 300), ("Modifié", 320), ("Créé", 320)]
    rows = [
     ("Démolition", "—", "Dépose de l'ex-comptoir boulangerie, des vitrines La Mie Câline, du four à pain et de l'armoire de pousse", "Évacuation en filière, protection des sols conservés"),
     ("Cloisons / doublages", "Cloisons prépa froide, cuisson, plonge, vestiaires, réserve CF", "Cloison cuisson côté vente : création de la passe chaude (vitrée, cadre inox). Ouverture de la passe desserte salle → plonge", "Local déchets fermé (degré CF à valider). Habillage décor « Arbre » en bois classé M1"),
     ("Sols", "Carrelage arrière existant si en bon état", "Reprise des sols de la cuisson / plonge en grès R12 + plinthes à gorge + siphons", "Sol de la vente (grès cérame ou vinyle U4P3 aspect bois), traitement du local déchets"),
     ("Plafonds", "Dalles métalliques démontables (arrière), plafond plâtre de la salle", "Dalles lessivables en cuisson / prépa", "Faux plafond acoustique dans l'espace détente"),
     ("Froid", "Chambre froide 3 × 3 m (panneaux, porte coulissante)", "Reconversion en positive 0/+3 °C (groupe, régulation, évaporateur)", "Murale libre-service 6 m avec groupe déporté si possible (chaleur et bruit), 2 armoires négatives, sondes connectées"),
     ("Cuisson / extraction", "Conduit d'extraction, extracteur, écran de cantonnement, commandes d'arrêt d'urgence", "Hotte adaptée aux nouveaux appareils, air de compensation", "Four mixte, friteuse, (cuiseur vapeur), plan réfrigéré, rampe chauffante"),
     ("Plomberie", "Réseaux, WC et lave-mains du personnel", "Raccordements plonge, lave-vaisselle", "Lave-mains à commande non manuelle (×5), siphons, séparateur à graisses si exigé"),
     ("Électricité", "TGBT, alimentation générale (à vérifier)", "Puissance et distribution cuisson / froid, éclairage de sécurité", "Éclairage d'ambiance, éclairage des vitrines, écrans menu, caisses"),
     ("Agencement", "—", "—", "Îlot « L'Arbre » retail, comptoir caisse 2 postes (dont PMR) + retrait chaud, banquettes, tables, mange-debout, desserte plateaux"),
     ("Façade / enseigne", "Structure vitrée, porte 2 vantaux", "Dépose de l'enseigne La Mie Câline", "Bandeau L'Arbre à Makis, vitrophanie, bandes contrastées PMR (planche 09)"),
     ("Sécurité", "Murs CF, réserve CF", "BAES et extincteurs repositionnés", "Extincteur classe F, coupure enseigne, attestation conduit"),
    ]
    y = table(c, 40, H - 70, cols, rows, 7.4)
    para(c, 40, y - 20, 1080,
         "**Avant de chiffrer : faire un état des lieux contradictoire avec le bailleur et un frigoriste / cuisiniste. "
         "Le DAT de 2015 décrit ce qui était prévu, pas forcément ce qui reste. Il faut vérifier sur place : présence et état du conduit et de l'extracteur, groupe froid de la chambre (reconversion possible ou remplacement), "
         "état du carrelage arrière, puissance électrique souscrite, présence d'un séparateur à graisses. Ce sont les postes les plus chers à refaire.", 8.2)
    cartouche(c, "DESCRIPTIF DES TRAVAUX", ech="—", num=8)

def page_facade(c):
    h1(c, 40, H - 50, "09 — Façade et enseigne projetées")
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
         "• On garde l'emplacement et les dimensions de l'enseigne existante : bandeau 11,50 × 1,48 m au-dessus du vitrage (la structure et l'alimentation peuvent être réutilisées).\n"
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
    cartouche(c, "FAÇADE ET ENSEIGNE", ech="≈ 1/55", num=9)

def page_demarches(c):
    h1(c, 40, H - 50, "10 — Démarches, calendrier et points à valider")
    cols = [("Démarche", 220), ("Auprès de", 170), ("Contenu", 380), ("Délai indicatif", 140)]
    rows = [
     ("Accord du bailleur / du centre", "Marques Avenue", "Plans d'aménagement, enseigne, activité cuisson + terrasse, horaires, sanitaires publics utilisés par la clientèle", "Avant signature / avant AT"),
     ("Autorisation de travaux ERP (art. L122-3 CCH)", "Mairie de La Séguinière (avis SDIS 49 + commission accessibilité)", "Cerfa 13824 + plans + notice sécurité + notice accessibilité, à monter par le maître d'œuvre à partir de ce dossier", "Instruction 4 mois : à déposer au plus tôt"),
     ("Autorisation d'enseigne", "Mairie (si règlement local de publicité)", "Plan et vue d'insertion de l'enseigne", "≈ 2 mois"),
     ("Déclaration d'activité", "DDPP de Maine-et-Loire", "Cerfa 13984 (en ligne), activité restauration + vente au détail", "Avant ouverture"),
     ("Statut sanitaire du labo", "DDPP du lieu du labo", "Agrément CE ou dérogation couvrant la livraison de la boutique et les volumes", "À sécuriser avant engagement"),
     ("Licence boissons (si bière / saké)", "Mairie + formation permis d'exploitation", "Petite licence restaurant ou licence restaurant", "≈ 1 mois + formation"),
     ("Vérifications avant ouverture", "Bureau de contrôle / organismes agréés", "Électricité, extraction, désenfumage le cas échéant, extincteurs, registre de sécurité, attestation d'achèvement", "Fin de chantier"),
    ]
    y = table(c, 40, H - 70, cols, rows, 7.6)
    para(c, 40, y - 18, 520,
         "**Points ouverts qui peuvent changer le plan\n"
         "1. Cotes et état réel : relevé sur site (le plan est redessiné depuis le DAT 2015, précision ± 10 cm).\n"
         "2. Équipements laissés par La Mie Câline : conduit, extracteur, chambre froide, groupe, hotte, sols.\n"
         "3. Puissance de cuisson : option A < 20 kW ou option B > 20 kW (planche 04). À trancher avec la carte chaude définitive.\n"
         "4. Vaisselle réutilisable (loi AGEC) : avec 30 places + terrasse, l'obligation s'applique au service sur place. Reste à confirmer le cas des produits préemballés en libre-service.\n"
         "5. Sanitaires clients : confirmation écrite du centre pour l'usage des sanitaires publics.\n"
         "6. Séparateur à graisses : exigence du gestionnaire du réseau d'assainissement.\n"
         "7. Terrasse : emprise autorisée sous l'auvent et mobilier imposé par le centre.", 8.2)
    para(c, 600, y - 18, 520,
         "**Conséquence à ne pas sous-estimer : la cuisson change le modèle de la boutique\n"
         "Le concept boutique LAM était pensé sans cuisine : produits finis du labo, vitrines, un vendeur. Ici, on ajoute de la cuisson minute (baos, poulet croustillant). Cela demande du personnel formé au poste chaud pendant le rush, l'entretien de l'extraction et des huiles, plus de contrôles DDPP, plus de puissance électrique et un investissement plus lourd.\n"
         "Avant de figer le plan, il faut chiffrer la boutique avec et sans cuisson : CA attendu de l'offre chaude, heures de personnel en plus, investissement cuisson + extraction. Si l'offre chaude ne paie pas son poste, l'option « remise en température seule » (four mixte, sans friteuse) est un repli simple : moins de 20 kW, pas d'huile, même plan.", 8.2, col=HexColor("#7a1f1f"))
    cartouche(c, "DÉMARCHES ET POINTS À VALIDER", ech="—", num=10)

def main():
    c = canvas.Canvas(OUT, pagesize=(W, H))
    c.setTitle("Dossier d'adaptation — L'Arbre à Makis — Cellule 09 La Séguinière")
    c.setAuthor("L'Arbre à Makis")
    for f in (page_cover, page_programme, page_plan, page_hygiene, page_cuisson, page_incendie, page_pmr,
              page_ddpp, page_travaux, page_facade, page_demarches):
        f(c); c.showPage()
    c.save()
    print("OK", OUT)
    for lab, r in SURF: print(f"{lab:50s} {area(r):6.1f}")

if __name__ == "__main__":
    main()
