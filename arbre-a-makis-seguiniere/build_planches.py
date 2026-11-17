# -*- coding: utf-8 -*-
"""Planches d'ambiance (rendus 3D de la maquette maquette3d/index.html) - L'Arbre à Makis, cellule 09 La Séguinière."""
import os
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from build_dossier import (W, H, NAVY, GREEN, GREY, MAG, LOGO, cartouche, para, h1, table, badge)

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, "maquette3d", "rendus")
OUT = os.path.join(HERE, "Planches_ambiance_LAM_La_Seguiniere.pdf")
PH = "AMBIANCE V3"

def img(c, name, x, y, w, frame=True):
    h = w / 1.6
    c.drawImage(os.path.join(R, name + ".jpg"), x, y, w, h)
    if frame:
        c.setStrokeColor(HexColor("#d9d3c7")); c.setLineWidth(0.6); c.rect(x, y, w, h)
    return h

def caption(c, x, y, s, size=7.5):
    c.setFillColor(GREY); c.setFont("FI", size); c.drawString(x, y, s)

def cart(c, titre, num, ech="—"):
    cartouche(c, titre, phase=PH, ech=ech, num=num)

def p_cover(c):
    c.setFillColor(HexColor("#e8ebee")); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.drawImage(os.path.join(R, "axo.jpg"), 0, 0, W, H - 175, preserveAspectRatio=True, anchor="c")
    c.setFillColor(NAVY); c.rect(0, H - 175, W, 175, fill=1, stroke=0)
    c.setFillColor(white); c.roundRect(40, H - 158, 150, 140, 8, fill=1, stroke=0)
    c.drawImage(LOGO, 48, H - 152, 134, 128, preserveAspectRatio=True, mask="auto")
    c.setFillColor(white); c.setFont("FB", 28); c.drawString(215, H - 70, "PLANCHES D'AMBIANCE")
    c.setFont("F", 14); c.drawString(215, H - 96, "La salle et le laboratoire, vus comme un architecte d'intérieur les présenterait")
    c.setFont("F", 11); c.drawString(215, H - 120, "Cellule n°09 — Marques Avenue — La Séguinière · maquette 3D d'intention construite sur le plan V3 (cotes du DAT 2015)")
    c.setFillColor(HexColor("#b8c2d6")); c.setFont("FI", 9)
    c.drawString(215, H - 142, "Images de principe : volumes, implantation et matériaux sont fidèles au plan V3 ; les finitions exactes seront arrêtées avec l'agenceur.")

def p_plan(c):
    h1(c, 40, H - 50, "01 — Plan d'aménagement rendu")
    ix, iy, iw = 30, 112, 860
    ih = img(c, "plan", ix, iy, iw)
    def pt(xc, yc):
        return ix + ((xc / 100) + 3.45) / 20 * iw, iy + ih - ((yc / 100) + 0.5) / 12.5 * ih
    L = [(-40, 575, "Entrée clients (porte 2 vantaux)"), (220, 735, "Îlot « L'Arbre » : produits phares + retail"),
         (290, 1105, "Murale libre-service à portes vitrées 4,80 m"), (507, 660, "Comptoir caisse (2 postes dont 1 PMR) + retrait chaud"),
         (620, 545, "Écrans menus + logo sur la verrière"), (300, 200, "Salle : banquette, tables, chaises"),
         (25, 240, "Mange-debout en vitrine"), (800, 200, "Espace détente (banquette existante)"),
         (956, 130, "Desserte + passe vers la plonge"), (820, 590, "Préparation froide (existante)"),
         (698, 785, "Passage froid (ex-niche vitrine)"), (780, 960, "Cuisson : four mixte + friteuse sous hotte"),
         (1070, 110, "Plonge + lave-vaisselle"), (1215, 990, "Chambre froide négative (existante)"),
         (1277, 572, "Réserve sèche coupe-feu"), (1277, 250, "Vestiaires H/F, WC, bureau"),
         (1470, 300, "Couloir arrière : réception, entretien"), (1470, 930, "Conteneurs déchets → porte P2"),
         (-330, 300, "Terrasse sous auvent (saisonnière)")]
    for i, (x, y, _) in enumerate(L):
        X, Y = pt(x, y); c.setFillColor(NAVY); c.circle(X, Y, 8, fill=1, stroke=0)
        c.setFillColor(white); c.setFont("FB", 7.5); c.drawCentredString(X, Y - 2.7, str(i + 1))
    caption(c, ix, iy - 12, "Vue de dessus de la maquette, murs coupés à 1,60 m. Façade à gauche, fond de cellule à droite (même orientation que le dossier).")
    X0, y = 910, H - 82
    c.setFont("FB", 9.5); c.setFillColor(NAVY); c.drawString(X0, y, "Repères"); y -= 15
    for i, (_, _, s) in enumerate(L):
        c.setFillColor(NAVY); c.circle(X0 + 6, y + 2.5, 6, fill=1, stroke=0)
        c.setFillColor(white); c.setFont("FB", 6.5); c.drawCentredString(X0 + 6, y, str(i + 1))
        c.setFillColor(HexColor("#222222")); c.setFont("F", 7.6); c.drawString(X0 + 17, y, s); y -= 14.5
    y -= 6
    para(c, X0, y, 255, "**Les deux mondes\nÀ l'avant, une salle chaleureuse (bois clair, bleu marine, végétal) organisée autour de l'arbre. À l'arrière, un laboratoire blanc et inox, entièrement logé dans les cloisons existantes, qui se laisse voir à travers les verrières.", 7.6)
    cart(c, "PLAN D'AMÉNAGEMENT RENDU", 1, "≈ 1/90")

def p_axo(c):
    h1(c, 40, H - 50, "02 — Axonométrie d'ensemble")
    ih = img(c, "axo", 30, 100, 870)
    caption(c, 30, 88, "Maquette coupée à 1,70 m, vue depuis l'angle façade / mur haut. Silhouettes à l'échelle.")
    para(c, 915, H - 82, 245,
         "**Le parti pris\n"
         "Une boutique lisible en un coup d'œil : on entre face à l'arbre, les frigos libre-service courent sur tout le mur de droite, la caisse attend au fond dans l'axe de la porte. Les places assises occupent l'autre moitié, au calme, en deux ambiances : les tables le long de la vitrine et l'alcôve du fond.\n"
         "\n"
         "**L'arbre, signature du lieu\n"
         "Un tronc habillé de lattes de chêne sort de l'îlot central et se déploie en branches lumineuses sous le plafond, d'où retombe un feuillage stabilisé. Il porte le nom de la marque, guide le regard et cache les volumes techniques du plafond.\n"
         "\n"
         "**Ce que l'on voit du laboratoire\n"
         "Les verrières existantes de la prépa et de la cuisson sont gardées : le client voit les équipes travailler en tenue blanche, dans un espace inox et blanc. C'est la meilleure publicité pour le « frais, préparé ici ».\n"
         "\n"
         "**Fidélité au plan\n"
         "Toutes les cloisons, portes et équipements sont à la position du plan V3 ; seules les finitions décoratives sont des intentions.", 8)
    cart(c, "AXONOMÉTRIE D'ENSEMBLE", 2)

def p_view(c, num, titre, name, cap, text):
    h1(c, 40, H - 50, titre)
    img(c, name, 30, 100, 870)
    caption(c, 30, 88, cap)
    para(c, 915, H - 82, 245, text, 8)
    cart(c, titre.split(" — ", 1)[1].upper(), num)

def p_labo2(c):
    h1(c, 40, H - 50, "07 — Laboratoire : cuisson & préparation")
    w = 560
    img(c, "hotline", 30, H - 80 - w / 1.6, w)
    img(c, "cuisson", 30 + w + 14, H - 80 - w / 1.6, w)
    caption(c, 30, H - 92 - w / 1.6, "À gauche : maquette rapprochée (prépa froide, armoires positives, cuisson). À droite : la ligne de cuisson vue depuis l'ex-zone pousse.")
    para(c, 30, H - 120 - w / 1.6, 560,
         "**Ligne de cuisson\n"
         "Four mixte 6 niveaux + friteuse sur les 1,46 m de l'ancien four Wind, sous la hotte existante, devant une crédence inox. Le muret existant sépare le chaud du plan réfrigéré à garnitures. L'ex-table à plaquer devient le plan de dressage, avec planches code couleur.\n"
         "**Lumière et matières\n"
         "Dalles LED étanches 4000 K, murs blancs lessivables, sol grès gris antidérapant, inox brossé partout où l'on travaille. Aucun bois ni textile côté laboratoire.", 8)
    para(c, 30 + w + 14, H - 120 - w / 1.6, 560,
         "**Préparation froide\n"
         "La pièce vitrée existante garde sa saladette 3 portes et son armoire positive. Elle sert à assembler, étiqueter et préparer le réassort, qui part directement vers la zone de service par le passage froid (ex-niche).\n"
         "**Lisibilité depuis la salle\n"
         "Les verrières laissent voir la prépa et la cuisson derrière les écrans menus. Gardez-les propres et bien éclairées : c'est une vitrine.", 8)
    cart(c, "LABORATOIRE — CUISSON & PRÉPA", 7)

def p_palette(c):
    h1(c, 40, H - 50, "08 — Palette des matériaux, mobilier et lumière")
    sw = [("#13213C", "Bleu marine L'Arbre à Makis", "Banquettes, bandeaux de la murale, enseigne, cadres"),
          ("#D8B98A", "Chêne clair", "Lattes du comptoir et de l'arbre, îlot, plateaux de tables, mange-debout (panneaux classés M1)"),
          ("#F2EFE9", "Quartz blanc", "Plans du comptoir, de l'îlot et de la desserte"),
          ("#E6DCCB", "Crème chaud", "Murs de la salle (peinture lessivable mate)"),
          ("#D4CCBC", "Sol clair existant", "Conservé ; rendu proche d'un grès aspect pierre beige"),
          ("#4C8A2E", "Vert végétal", "Feuillage stabilisé de l'arbre, plantes en pot (artificiel ou stabilisé classé)"),
          ("#1D1F22", "Noir mat", "Piètements, chaises, menuiseries de la murale, suspensions"),
          ("#A3AAB0", "Inox brossé", "Équipements du laboratoire, crédence, plans de travail"),
          ("#ECEDEB", "Blanc laboratoire", "Panneaux muraux lisses et lessivables (existants)"),
          ("#9A9EA3", "Grès gris antidérapant", "Sol du laboratoire (existant, joints à reprendre si besoin)")]
    x, y = 40, H - 85
    for i, (col, name, use) in enumerate(sw):
        cx = x + (i % 2) * 560; cy = y - (i // 2) * 62
        c.setFillColor(HexColor(col)); c.setStrokeColor(HexColor("#cccccc")); c.roundRect(cx, cy - 44, 70, 48, 5, fill=1, stroke=1)
        c.setFillColor(NAVY); c.setFont("FB", 9.5); c.drawString(cx + 84, cy - 8, name)
        c.setFillColor(HexColor("#333333")); c.setFont("F", 8); c.drawString(cx + 84, cy - 22, use)
        c.setFillColor(GREY); c.setFont("FI", 7); c.drawString(cx + 84, cy - 34, col)
    yy = y - 5 * 62 - 10
    rows = [("Places assises", "29 à l'intérieur (5 mange-debout, 14 en salle, 10 dans l'alcôve, dont 2 PMR) + ≈ 16 en terrasse"),
            ("Mobilier salle", "Banquettes marine sur socle noir, tables chêne 65-80 cm sur pied central noir, chaises noires empilables, tabourets hauts chêne"),
            ("Comptoir", "Façade en lattes de chêne verticales, plan quartz, tablette PMR à 0,80 m, rampe chauffante au retrait"),
            ("Îlot « L'Arbre »", "Socle chêne arrondi à deux gradins, produits retail en couronne, tronc en lattes, branches avec LED intégrée"),
            ("Murale", "4 modules à portes vitrées, intérieur blanc LED 4000 K, bandeaux marine lettrés SUSHIS / ROLLS & BOWLS / BAOS / DESSERTS"),
            ("Lumière salle", "Suspensions globes opalins 2700 K au-dessus des tables, spots encastrés, LED linéaire dans les branches de l'arbre"),
            ("Lumière laboratoire", "Dalles LED étanches 4000 K, luminaires protégés au-dessus des postes"),
            ("Graphisme", "Citations manuscrites au mur (« Des produits frais, préparés à Maulévrier. », « Une pause gourmande qui a du sens. », « Le goût du bon sens. »), bandes vitrophanie PMR marine")]
    table(c, 40, yy, [("Poste", 150), ("Intention", 930)], rows, 7.8)
    para(c, 40, 100, 1080, "Rappels : tout le décor (bois, végétal, textiles) doit être classé au feu M1 / B-s3,d0 (ERP) ; côté laboratoire, uniquement des matériaux lisses et lessivables (audit DDPP).", 7.6, col=GREY)
    cart(c, "PALETTE MATÉRIAUX & MOBILIER", 8)

def main():
    c = canvas.Canvas(OUT, pagesize=(W, H))
    c.setTitle("Planches d'ambiance — L'Arbre à Makis — Cellule 09 La Séguinière"); c.setAuthor("L'Arbre à Makis")
    p_cover(c); c.showPage()
    p_plan(c); c.showPage()
    p_axo(c); c.showPage()
    p_view(c, 3, "03 — Salle : l'arrivée", "salle", "Vue depuis le coin mange-debout, à hauteur d'œil (1,60 m) : tables, comptoir, arbre et murale au fond.",
           "**Première impression\nDepuis la vitrine, on voit l'arbre et la murale éclairée dès le seuil : le client sait tout de suite où se servir.\n\n"
           "**Le comptoir\nUne façade en lattes de chêne, un plan quartz blanc et deux caisses. Au-dessus, trois écrans menus (Sushis & Rolls, Baos, Bowls) et le logo, posés sur la verrière de la prépa, qui reste visible.\n\n"
           "**Les tables\nPlateaux chêne et chaises noires, suspensions globes en lumière chaude : l'ambiance d'un café plus que d'un fast-food.")
    c.showPage()
    p_view(c, 4, "04 — Salle : l'îlot et la murale", "murale", "Vue depuis la salle vers le mur des frigos : l'îlot « L'Arbre » au centre, la caisse à gauche, la vitrine à droite.",
           "**L'îlot « L'Arbre »\nDeux gradins en chêne arrondis : la couronne basse présente le retail (sauces, chips d'algues, cacahuètes wasabi, thés), le gradin haut les produits phares. Bandeau marine « NOS INCONTOURNABLES » côté entrée.\n\n"
           "**La murale\nQuatre modules noirs à portes vitrées, intérieur blanc très éclairé : les couleurs des sushis, rolls et bowls ressortent. Un bandeau marine lettré par famille, et la citation « Le goût du bon sens. » au-dessus.\n\n"
           "**La circulation\nAu moins 1,40 m autour de l'îlot et 2,15 m devant la murale : on se sert sans gêner la file de la caisse.")
    c.showPage()
    p_view(c, 5, "05 — Salle : l'espace détente", "detente", "Vue depuis le fond de l'alcôve vers la façade : banquette, tables, lattes de bois et lumière du jour.",
           "**Une pause au calme\nL'alcôve du fond reprend la banquette existante, retapissée en marine, avec un habillage de lattes de chêne et la citation « Une pause gourmande qui a du sens. ».\n\n"
           "**La lumière\nLa grande façade vitrée sous l'auvent éclaire toute la salle. Les suspensions globes donnent une lumière chaude et basse au-dessus de chaque table.\n\n"
           "**La desserte\nUn meuble en chêne pour déposer les plateaux, adossé à la passe de la plonge : la vaisselle sale ne retraverse jamais la salle.")
    c.showPage()
    p_view(c, 6, "06 — Laboratoire : maquette d'ensemble", "labo", "Maquette coupée à 1,70 m, vue depuis le fond de cellule : réserve, chambre froide, vestiaires, plonge, prépa, cuisson.",
           "**Un laboratoire dans les murs existants\nAucune cloison n'est déplacée. On retrouve la réserve coupe-feu (étagères retail), la chambre froide négative (surgelés), le bloc vestiaires / WC, la plonge, la prépa froide vitrée et la zone de cuisson.\n\n"
           "**Le couloir arrière\nRéception des livraisons à la porte P1, armoire à produits d'entretien, conteneurs à couvercle près de la porte P2.\n\n"
           "**Hygiène\nMurs blancs lisses, sol grès gris, inox : tout se lave à grande eau, conformément à l'audit DDPP.")
    c.showPage()
    p_labo2(c); c.showPage()
    p_palette(c); c.showPage()
    c.save(); print("OK", OUT)

if __name__ == "__main__":
    main()
