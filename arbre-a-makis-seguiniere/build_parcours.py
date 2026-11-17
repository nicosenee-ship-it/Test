# -*- coding: utf-8 -*-
"""Audit du parcours client par 8 clients-tests (ville et zone) - L'Arbre à Makis, cellule 09 La Séguinière.
Réutilise le plan V3 (build_dossier.py) et les rendus de la maquette 3D (maquette3d/rendus)."""
import os
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white, black, Color
from reportlab.pdfbase import pdfmetrics
import build_dossier as bd
from build_dossier import (W, H, NAVY, GREEN, GREY, MAG, RED, BLUE, ORANGE, WOOD, BROWN, P, rect, line, txt, circle,
                           arrow_path, badge, para, table, h1, legend_box, cartouche)

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, "maquette3d", "rendus")
OUT = os.path.join(HERE, "Parcours_clients_LAM_La_Seguiniere.pdf")
PH = "PARCOURS"
INK = HexColor("#1b1f27"); FLOOR = HexColor("#f6f1e7")
COL = {"G": (HexColor("#2e7d32"), HexColor("#dcefd9")), "O": (HexColor("#a35f00"), HexColor("#fde8c8")),
       "R": (HexColor("#c62828"), HexColor("#f8d3d0")), "-": (GREY, HexColor("#f0f0f0"))}
PTS = {"G": 2, "O": 1, "R": 0}

STEPS = ["Repérer", "Entrer", "Comprendre l'offre", "Choisir", "Attendre", "Payer", "Le chaud", "S'installer", "Débarrasser", "Revenir"]

PERSONAS = [
 dict(key="sandrine", nom="Sandrine, 46 ans", qui="Vendeuse dans une boutique de Marques Avenue", tag="ZONE",
      quand="Du lundi au samedi, pause à 12h30 ou 14h", temps="30 min, dont 10 pour acheter",
      veut="Manger vite, varier, ≈ 10 €, emporter en salle de pause", fuit="Une file visible depuis la porte",
      revient="Commander à l'avance, carte de fidélité, offre « personnel du centre »",
      quote="« Je passe devant tous les jours. Si je vois la queue depuis la porte, je ne rentre pas : j'ai 30 minutes, pas une de plus. »",
      recit="Elle voit l'arbre depuis l'allée et entre… droit dans la file, qui part de la caisse et arrive à la porte. Elle prend un bowl dans la murale, revient se placer au milieu de l'entrée, gênée par ceux qui entrent. Sept minutes plus tard, elle paie. Une fois, ça passe ; tous les jours, non.",
      besoin="Commander sur son téléphone à 12h15 et passer directement au retrait ; une formule à prix fixe ; une carte de fidélité ; une remise pour le personnel du centre, à négocier avec la direction.",
      v3=[("G", "passe devant chaque jour"), ("R", "file jusqu'à la porte"), ("G", "connaît l'offre"), ("G", "murale lisible"), ("R", "7 min sur 30 de pause"),
          ("O", "pas de paiement express"), ("O", "attente debout"), ("-", "à emporter"), ("-", "—"), ("O", "ni fidélité, ni commande en ligne")],
      v4=[("G", "passe devant chaque jour"), ("G", "entrée dégagée"), ("G", "connaît l'offre"), ("G", "se sert en avançant"), ("O", "file, sauf click & collect"),
          ("G", "retrait direct"), ("G", "prêt au retrait"), ("-", "à emporter"), ("-", "—"), ("G", "fidélité + offre centre")]),
 dict(key="karim", nom="Karim, 31 ans, et 4 collègues", qui="Techniciens d'une entreprise de la ZI de la Ménardière", tag="ZONE",
      quand="Vendredi midi, sur place", temps="45 min",
      veut="Manger chaud et copieux, s'asseoir ensemble, payer chacun", fuit="Attendre debout, tables trop petites",
      revient="Un plat chaud copieux, une table de 6, être servis",
      quote="« On est cinq, on veut manger chaud et s'asseoir ensemble. Les sushis, d'accord, mais il nous faut un vrai plat. »",
      recit="Ils ne découvrent les baos qu'en arrivant devant la caisse, sur l'écran au-dessus du comptoir. Chacun commande et paie à son tour : cinq paiements d'affilée bloquent la caisse. Puis ils attendent debout devant la rampe chaude, au milieu de ceux qui font la queue. Dans l'alcôve, ils rapprochent trois tables de deux.",
      besoin="Voir l'offre chaude dès l'entrée de la file ; un bowl chaud copieux ; une table de 6 toute prête ; qu'on leur apporte les plats à table avec un numéro.",
      v3=[("G", "sur leur trajet"), ("G", "vitrine, arbre"), ("O", "chaud vu en caisse seulement"), ("G", "large choix"), ("O", "file à cinq"),
          ("R", "5 paiements d'affilée"), ("R", "5 baos, attente debout"), ("O", "tables de 2 à rapprocher"), ("O", "desserte au fond"), ("G", "si c'est copieux")],
      v4=[("G", "sur leur trajet"), ("G", "vitrine, arbre"), ("G", "panneau « Envie de chaud ? »"), ("G", "large choix"), ("O", "file à cinq"),
          ("O", "paiements séparés"), ("G", "servis à table"), ("G", "table de 6 prête"), ("G", "desserte de l'alcôve"), ("G", "si c'est copieux")]),
 dict(key="famille", nom="Claire et Julien, Léo (8 ans), Jade (3 ans)", qui="Famille de La Séguinière, avec poussette", tag="VILLE",
      quand="Samedi 12h30, avant le shopping", temps="1 h",
      veut="Manger assis ensemble, quelque chose pour les enfants", fuit="Pas de toilettes, pas de chaise haute",
      revient="Box enfant, chaise haute, accueil des familles",
      quote="« La première chose que demande Léo, ce sont les toilettes. La deuxième, s'il peut prendre les cacahuètes. »",
      recit="L'arbre émerveille les enfants. Mais les sachets de cacahuètes wasabi et de chips sont à hauteur d'enfant sur l'îlot : risqué pour un enfant allergique à l'arachide. La poussette ne passe pas dans la file qui coupe l'entrée. Il n'y a pas de chaise haute, les tables sont des tables de deux, et personne ne leur indique les toilettes du centre.",
      besoin="Une box enfant (makis concombre, onigiri, compote), deux chaises hautes, une table de 4, un coin poussette, un panneau clair vers les toilettes du centre, l'arachide rangée en hauteur.",
      v3=[("O", "boutique peu signalée"), ("G", "l'arbre plaît aux enfants"), ("O", "rien pour les enfants"), ("R", "arachide à hauteur d'enfant"), ("O", "poussette dans la file"),
          ("G", "simple"), ("O", "attente avec 2 enfants"), ("R", "ni chaise haute, ni WC"), ("O", "plateaux à rapporter"), ("O", "si accueil famille")],
      v4=[("O", "dépend du centre"), ("G", "l'arbre plaît aux enfants"), ("G", "box enfant"), ("G", "arachide en hauteur"), ("O", "file le long des frigos"),
          ("G", "simple"), ("G", "servi à table"), ("O", "chaise haute ; WC du centre"), ("G", "tri près de la sortie"), ("G", "accueil famille")]),
 dict(key="seniors", nom="Monique (72 ans) et Bernard (75 ans)", qui="Retraités choletais", tag="VILLE",
      quand="Mardi 12h, journée shopping", temps="1 h, sans se presser",
      veut="Comprendre, être conseillés, s'asseoir au calme", fuit="Ne pas comprendre l'offre, rester debout",
      revient="Conseil, carte lisible, dégustation",
      quote="« C'est quoi, un bao ? On aimerait goûter, mais sans se tromper. Et on ne lit rien sur l'écran là-bas. »",
      recit="Ils hésitent devant la murale : étiquettes petites, portes vitrées à ouvrir pour lire. Les écrans menus sont à 5 m, au-dessus du comptoir. Ils font la queue debout. En revanche, l'alcôve calme du fond leur plaît beaucoup : ils y resteraient une heure.",
      besoin="Un menu papier en gros caractères, un petit lexique « Le Japon en 6 mots » (bao, gyoza, onigiri, maki, california, mochi), des étiquettes de rayon avec photo, un conseil du vendeur, une dégustation en heure creuse.",
      v3=[("G", "plan du centre"), ("G", "accueil visible"), ("R", "« bao ? » écrans à 5 m"), ("O", "petites étiquettes, portes"), ("O", "debout dans la file"),
          ("G", "caissier"), ("O", "attente au comptoir"), ("G", "alcôve calme"), ("G", "desserte proche"), ("O", "si on les conseille")],
      v4=[("G", "plan du centre"), ("G", "accueil visible"), ("G", "lexique, menu papier"), ("G", "étiquettes avec photo"), ("O", "debout dans la file"),
          ("G", "caissier"), ("G", "servi à table"), ("G", "alcôve calme"), ("G", "desserte proche"), ("G", "conseil, dégustation")]),
 dict(key="etudiantes", nom="Léa, 19 ans, et deux amies", qui="Étudiantes à Cholet", tag="VILLE",
      quand="Samedi 15h30, pause goûter", temps="1 h",
      veut="Un dessert ou une boisson originale, une photo sous l'arbre", fuit="Un lieu sans âme, trop cher",
      revient="Boisson signature, coin photo, wifi",
      quote="« On vient pour la photo sous l'arbre et un dessert. Si c'est joli et pas trop cher, on revient avec les autres. »",
      recit="À 15h30 il n'y a pas de file : le parcours est fluide et l'arbre est très photogénique. Mais il n'y a rien à boire de chaud ou de préparé sur place (thé matcha, thé glacé maison), et les desserts sont tout au bout de la murale.",
      besoin="Une boisson signature, des mochis, le wifi, un hashtag sous l'arbre. Pour le centre, ce sont elles qui feront connaître le lieu sur les réseaux.",
      v3=[("G", "réseaux sociaux"), ("G", "arbre photogénique"), ("G", "visuels clairs"), ("O", "desserts au fond"), ("G", "pas de file à 15h30"),
          ("G", "sans contact"), ("-", "—"), ("G", "banquette"), ("O", "tri peu clair"), ("O", "pas de boisson signature")],
      v4=[("G", "réseaux sociaux"), ("G", "arbre photogénique"), ("G", "visuels clairs"), ("G", "desserts près des caisses"), ("G", "pas de file à 15h30"),
          ("G", "sans contact"), ("-", "—"), ("G", "banquette"), ("G", "station de tri"), ("O", "boisson : à décider")]),
 dict(key="thomas", nom="Thomas, 35 ans", qui="Artisan plombier à Cholet, en camionnette", tag="VILLE",
      quand="Mercredi 12h10, à emporter", temps="10 min chrono",
      veut="Se garer, prendre, payer, repartir", fuit="Chercher la boutique, attendre un plat chaud",
      revient="Click & collect, retrait immédiat",
      quote="« Je me gare, je prends, je repars. Si je dois chercher la boutique ou attendre un bao cinq minutes, je vais au drive. »",
      recit="Depuis le parking, il ne voit pas forcément l'enseigne : tout dépend de l'emplacement de la cellule dans le centre. Une fois dedans, pas de commande à l'avance, la file, puis l'attente du bao. Il compte douze minutes. Il ne reviendra pas.",
      besoin="Click & collect avec retrait immédiat à l'entrée du comptoir, paiement sans contact, enseigne drapeau visible depuis l'allée.",
      v3=[("R", "peu visible du parking"), ("O", "file visible"), ("G", "offre claire"), ("G", "rapide en murale"), ("R", "file + chaud = 12 min"),
          ("O", "pas d'express"), ("R", "bao à attendre"), ("-", "à emporter"), ("-", "—"), ("R", "pas de commande à l'avance")],
      v4=[("O", "drapeau, plan du centre"), ("G", "entrée dégagée"), ("G", "offre claire"), ("G", "rapide en murale"), ("G", "click & collect"),
          ("G", "déjà payé"), ("G", "commandé à l'avance"), ("-", "à emporter"), ("-", "—"), ("G", "commande en ligne")]),
 dict(key="visiteuses", nom="Nathalie (52 ans) et Sophie (55 ans)", qui="Venues de Nantes pour une journée outlet", tag="ZONE",
      quand="Samedi 13h30, chargées de sacs", temps="45 min",
      veut="Poser les sacs, souffler, découvrir", fuit="Pas de place, pas de toilettes",
      revient="Elles reviennent rarement : c'est l'avis qu'elles laissent qui compte",
      quote="« On cherche un endroit pour poser nos sacs et souffler. On ne connaît pas la marque, on a regardé les avis Google avant d'entrer. »",
      recit="Elles trouvent le lieu joli et s'installent, sacs coincés entre les chaises. Elles demandent les toilettes. Elles ne reviendront peut-être que dans six mois : ce qui compte, c'est la note qu'elles laisseront et ce qu'elles raconteront.",
      besoin="Des crochets à sacs sous les tables, la terrasse aux beaux jours, l'histoire de la marque racontée (atelier de Maulévrier), un QR code pour laisser un avis.",
      v3=[("O", "dépend du plan du centre"), ("G", "vitrine attirante"), ("G", "enseigne explicite"), ("G", "découverte"), ("O", "file debout"),
          ("G", "sans contact"), ("O", "attente"), ("O", "pas de crochets, WC ?"), ("O", "desserte loin"), ("O", "reviennent rarement")],
      v4=[("O", "dépend du plan du centre"), ("G", "vitrine attirante"), ("G", "enseigne explicite"), ("G", "découverte"), ("O", "file debout"),
          ("G", "sans contact"), ("G", "servi à table"), ("O", "crochets ; WC du centre"), ("G", "tri près de la sortie"), ("O", "QR code avis")]),
 dict(key="marc", nom="Marc, 58 ans, en fauteuil, et son épouse", qui="Habitants de Cholet", tag="VILLE",
      quand="Samedi 12h15", temps="1 h",
      veut="Tout faire seul : se servir, payer, s'installer", fuit="Être coincé, devoir demander de l'aide",
      revient="Passages larges, chaud servi à table",
      quote="« Je veux tout faire seul : prendre mon plateau, payer, m'installer. Dès qu'il y a du monde debout dans l'allée, je suis coincé. »",
      recit="L'entrée de plain-pied est parfaite. Mais la file debout dans l'axe de la porte lui barre le passage, et le côté vitrine de l'îlot ne fait que 1,10 m. Il doit récupérer un plat chaud sur un comptoir à 1 m et le porter sur ses genoux. La desserte est au fond de l'alcôve.",
      besoin="Une file qui ne coupe pas l'entrée, 1,40 m de passage partout, le chaud apporté à table, une station de tri à hauteur près de la sortie.",
      v3=[("G", "accès de plain-pied"), ("G", "porte 2,40 m"), ("O", "écrans hauts"), ("O", "portes vitrées à ouvrir"), ("R", "file en travers de l'allée"),
          ("G", "tablette adaptée"), ("R", "plat chaud à 1 m de haut"), ("G", "place adaptée"), ("R", "desserte au fond"), ("O", "si autonome")],
      v4=[("G", "accès de plain-pied"), ("G", "porte 2,40 m"), ("G", "menu papier"), ("O", "portes vitrées à ouvrir"), ("G", "file le long des frigos"),
          ("G", "tablette adaptée"), ("G", "servi à table"), ("G", "place adaptée"), ("G", "tri à hauteur"), ("G", "autonome")]),
]

def score(cells):
    pts = [PTS[c] for c, _ in cells if c != "-"]
    return round(10 * sum(pts) / (2 * len(pts)), 1)

def cart(c, titre, num, ech="—"):
    cartouche(c, titre, phase=PH, ech=ech, num=num)

def tagbox(c, x, y, tag):
    col = HexColor("#2f6db5") if tag == "VILLE" else HexColor("#7d4fb3")
    w = pdfmetrics.stringWidth(tag, "FB", 6.5) + 8
    c.setFillColor(col); c.roundRect(x, y - 2, w, 10, 2, fill=1, stroke=0)
    c.setFillColor(white); c.setFont("FB", 6.5); c.drawString(x + 4, y + 0.5, tag); return w

# ------------------------------------------------------------------------------------------ page 1
def p_synthese(c):
    h1(c, 40, H - 50, "Parcours clients — l'avis de 8 clients-tests de la ville et de la zone")
    y = para(c, 40, H - 82, 560,
        "**Verdict\n"
        "Le parcours de la V3 fonctionne bien en heure creuse et pour les clients qui ont le temps : l'arbre et la vitrine attirent, la murale est lisible, l'alcôve calme plaît. "
        "Il casse au coup de feu de midi, et précisément pour les clients qui viendraient tous les jours : le personnel du centre, les salariés de la zone, les artisans pressés. "
        "Le défaut vient de l'implantation, pas des travaux : on peut le corriger sans rien construire, en redessinant le comptoir et l'îlot avant leur fabrication.\n"
        "\n"
        "**Les 5 points qui cassent le parcours (V3)\n"
        "1. La file se forme dans l'axe de l'entrée. À partir de 7 ou 8 personnes, elle atteint la porte : celui qui arrive voit une file, pas l'arbre, et une partie des clients repart.\n"
        "2. Quatre flux se croisent devant le comptoir : sortie de la murale, file d'attente, attente du chaud, départ avec le plateau vers la salle.\n"
        "3. Le chaud est invisible et lent : on découvre les baos en caisse, puis on attend debout à la rampe, au milieu de la file.\n"
        "4. Rien pour les clients pressés : ni commande à l'avance, ni retrait direct, ni fidélité.\n"
        "5. Le confort des familles et des groupes : tables de deux, pas de chaise haute, pas de toilettes dans la boutique sans panneau vers celles du centre, arachide à hauteur d'enfant, une seule desserte au fond.\n"
        "\n"
        "**Ce qui marche déjà, à garder\n"
        "• La vitrine et l'arbre : tous les profils les remarquent, les enfants et les étudiantes en premier.\n"
        "• La murale à droite de l'entrée, avec les desserts et boissons en dernier, juste avant les caisses : bon pour l'achat d'impulsion.\n"
        "• L'alcôve du fond, au calme, qui plaît aux seniors et aux groupes.\n"
        "• La place adaptée, la tablette de caisse basse et l'entrée de plain-pied.", 8.6)
    # scores
    X0, Y0 = 640, H - 82
    c.setFont("FB", 10); c.setFillColor(NAVY); c.drawString(X0, Y0, "Note du parcours par client-test (sur 10)")
    c.setFont("F", 7.2); c.setFillColor(GREY); c.drawString(X0, Y0 - 12, "Calculée sur les 10 étapes de la carte d'expérience : vert = 2, orange = 1, rouge = 0.")
    y = Y0 - 32; bw = 260
    for p in PERSONAS:
        s3, s4 = score(p["v3"]), score(p["v4"])
        c.setFillColor(INK); c.setFont("FB", 7.6); c.drawString(X0, y, p["nom"][:42])
        tagbox(c, X0 + 200, y, p["tag"])
        bx = X0 + 250
        c.setFillColor(HexColor("#eceff2")); c.rect(bx, y - 1, bw, 7, fill=1, stroke=0); c.rect(bx, y - 10, bw, 7, fill=1, stroke=0)
        c.setFillColor(HexColor("#9aa3ad")); c.rect(bx, y - 1, bw * s3 / 10, 7, fill=1, stroke=0)
        c.setFillColor(HexColor("#5f9a3a")); c.rect(bx, y - 10, bw * s4 / 10, 7, fill=1, stroke=0)
        c.setFont("FB", 7); c.setFillColor(INK); c.drawString(bx + bw + 6, y, f"{s3:.1f}".replace(".", ",")); c.setFillColor(HexColor("#2e7d32")); c.drawString(bx + bw + 6, y - 9, f"{s4:.1f}".replace(".", ","))
        y -= 27
    c.setFillColor(HexColor("#9aa3ad")); c.rect(X0 + 250, y + 2, 10, 6, fill=1, stroke=0); c.setFillColor(INK); c.setFont("F", 7.2); c.drawString(X0 + 264, y + 3, "V3 (plan actuel)")
    c.setFillColor(HexColor("#5f9a3a")); c.rect(X0 + 350, y + 2, 10, 6, fill=1, stroke=0); c.setFillColor(INK); c.drawString(X0 + 364, y + 3, "V4 (proposition, sans travaux)")
    c.setFillColor(GREY); c.setFont("FI", 7); c.drawString(X0, y - 10, "Notes V4 = projection si toutes les mesures sont appliquées, avec deux caisses et une personne en salle au coup de feu.")
    y -= 12
    para(c, X0, y - 18, 510,
        "**Ce que je propose (V4), sans aucun travaux\n"
        "• Une boucle à sens unique : on entre, on longe la vitrine, on se sert le long de la murale en avançant dans la file, on remonte le long du comptoir vers les caisses, on récupère au retrait, on s'installe ou on ressort. La file ne touche plus la porte.\n"
        "• Le comptoir redessiné avant fabrication : retrait et click & collect au bout visible depuis la porte, caisses au milieu, entrée de file en bas.\n"
        "• L'îlot ramené à 1,90 m de large : 1,40 m de passage de chaque côté.\n"
        "• Le chaud annoncé dès l'entrée de la file et servi à table avec un numéro.\n"
        "• Click & collect, fidélité, chaises hautes, tables jumelables, station de tri près de la sortie, panneaux vers les toilettes du centre.\n"
        "\n"
        "**Méthode\nHuit profils de clients construits à partir de ce que l'on sait du site (centre de magasins d'usine de la ZI de la Ménardière, commune de 4 365 habitants à côté de Cholet, zones d'activités voisines) et de comportements courants en restauration rapide. Chaque profil parcourt le plan V3 étape par étape, à son heure de visite. Ce ne sont pas des clients interrogés : la planche 09 dit comment le vérifier sur place.", 8.2)
    cart(c, "SYNTHÈSE", 1)

# ------------------------------------------------------------------------------------------ page 2
def p_personas(c):
    h1(c, 40, H - 50, "Les 8 clients-tests")
    para(c, 40, H - 70, 1100, "Quatre profils de la ville (La Séguinière, Cholet) et quatre de la zone (le centre de magasins d'usine, les entreprises voisines, la clientèle de passage venue pour l'outlet). Chacun vient à un moment différent de la semaine.", 8.4)
    rows = []
    for p in PERSONAS:
        rows.append((p["nom"] + "\n" + p["qui"], p["tag"], p["quand"], p["temps"], p["veut"], p["fuit"], p["revient"]))
    yt = table(c, 40, H - 92, [("Client-test", 215), ("Origine", 50), ("Quand", 140), ("Temps", 90), ("Vient chercher", 215), ("Le fait fuir", 190), ("Le fera revenir", 210)], rows, 8, lead=1.3, pad=5)
    para(c, 40, yt - 24, 1100,
         "**Deux clientèles, deux logiques\n"
         "• La clientèle de la zone qui vient tous les jours (personnel du centre, salariés des zones d'activités) fera le chiffre d'affaires de la semaine. Elle juge sur la vitesse et la régularité : c'est elle que le coup de feu de midi met le plus en échec.\n"
         "• La clientèle du samedi (familles, visiteuses venues de loin, étudiantes) juge sur le confort, la découverte et l'ambiance. Elle fait la réputation du lieu (avis, réseaux sociaux) mais revient moins souvent.\n"
         "Le parcours doit servir les deux sans les mélanger : rapide au comptoir, confortable en salle.", 8.4)
    cart(c, "LES 8 CLIENTS-TESTS", 2)

# ------------------------------------------------------------------------------------------ matrices
def matrix(c, X, Y, key, title, rh=50, fs=6.4):
    pw, sw, scw = 165, 88, 52
    c.setFillColor(NAVY); c.rect(X, Y - 26, pw + sw * 10 + scw, 26, fill=1, stroke=0)
    c.setFillColor(white); c.setFont("FB", 7.6); c.drawString(X + 6, Y - 16, title)
    for i, s in enumerate(STEPS):
        c.drawCentredString(X + pw + sw * i + sw / 2, Y - 11, f"{i + 1}")
        c.setFont("FB", 7); c.drawCentredString(X + pw + sw * i + sw / 2, Y - 21, s); c.setFont("FB", 7.6)
    c.drawCentredString(X + pw + sw * 10 + scw / 2, Y - 16, "/ 10")
    y = Y - 26
    for p in PERSONAS:
        c.setFillColor(HexColor("#f6f7f9")); c.rect(X, y - rh, pw, rh, fill=1, stroke=0)
        c.setFillColor(INK); c.setFont("FB", 7.2)
        nm = p["nom"]; lines = []
        cur = ""
        for wd in nm.split(" "):
            t = (cur + " " + wd).strip()
            if pdfmetrics.stringWidth(t, "FB", 7.2) < pw - 12: cur = t
            else: lines.append(cur); cur = wd
        lines.append(cur)
        for k, l in enumerate(lines[:2]): c.drawString(X + 6, y - 12 - k * 9, l)
        tagbox(c, X + 6, y - rh + 7, p["tag"])
        for i, (code, note) in enumerate(p[key]):
            fg, bg = COL[code]
            cx = X + pw + sw * i
            c.setFillColor(bg); c.rect(cx + 1, y - rh + 1, sw - 2, rh - 2, fill=1, stroke=0)
            c.setFillColor(fg); c.circle(cx + 8, y - 9, 3.2, fill=1, stroke=0)
            c.setFont("F", fs); c.setFillColor(INK)
            ws = note.split(" "); cur = ""; ls = []
            for wd in ws:
                t = (cur + " " + wd).strip()
                if pdfmetrics.stringWidth(t, "F", fs) < sw - 10: cur = t
                else: ls.append(cur); cur = wd
            ls.append(cur)
            for k, l in enumerate(ls[:4]): c.drawString(cx + 5, y - 20 - k * fs * 1.25, l)
        sc = score(p[key])
        c.setFillColor(HexColor("#f6f7f9")); c.rect(X + pw + sw * 10, y - rh, scw, rh, fill=1, stroke=0)
        c.setFillColor(HexColor("#2e7d32") if sc >= 8 else (HexColor("#a35f00") if sc >= 6 else HexColor("#c62828")))
        c.setFont("FB", 12); c.drawCentredString(X + pw + sw * 10 + scw / 2, y - rh / 2 - 4, f"{sc:.1f}".replace(".", ","))
        c.setStrokeColor(white); c.setLineWidth(1); c.line(X, y - rh, X + pw + sw * 10 + scw, y - rh)
        y -= rh
    return y

def legend_codes(c, X, Y):
    for i, (code, lab) in enumerate([("G", "fluide, agréable"), ("O", "gêne, ralentit"), ("R", "point de rupture : le client renonce ou ne revient pas"), ("-", "sans objet")]):
        fg, bg = COL[code]; x = X + i * 175 if i < 3 else X + 525 + 170
        if i == 2: x = X + 350
        c.setFillColor(bg); c.rect(x, Y - 3, 22, 11, fill=1, stroke=0); c.setFillColor(fg); c.circle(x + 6, Y + 2.5, 3, fill=1, stroke=0)
        c.setFillColor(INK); c.setFont("F", 7.4); c.drawString(x + 28, Y, lab)

def p_matrix_v3(c):
    h1(c, 40, H - 50, "Carte d'expérience — parcours actuel (V3)")
    para(c, 40, H - 70, 1100, "Chaque client-test parcourt la boutique à son heure de visite. Une case par étape : ce qu'il vit, en quelques mots.", 8.4)
    y = matrix(c, 40, H - 84, "v3", "Client-test · étape du parcours")
    legend_codes(c, 40, y - 18)
    para(c, 40, y - 40, 1100,
         "**Lecture\nLes ruptures (rouge) se concentrent sur trois étapes : attendre, le chaud et, pour les familles et le client en fauteuil, s'installer et débarrasser. Ce sont des questions d'implantation et de service, pas de produit : les étapes « Choisir » et « Entrer » sont presque toutes vertes.", 8.2)
    cart(c, "CARTE D'EXPÉRIENCE — V3", 3)

# ------------------------------------------------------------------------------------------ plans
def hot(c, x, y, n, r=48):
    X, Y = P(x, y); c.saveState(); c.setFillColor(Color(0.85, 0.15, 0.15, alpha=0.16)); c.setStrokeColor(RED); c.setLineWidth(0.8)
    c.circle(X, Y, r * bd.S, fill=1, stroke=1); c.restoreState(); badge(c, x, y, str(n), RED, 7)

def plan_labels(c):
    bd.label_min(c, [(290, 1107, "MURALE"), (840, 560, "PRÉPA"), (790, 930, "CUISSON"), (300, 120, "SALLE"), (820, 120, "ALCÔVE")])

def p_v3_rush(c):
    bd.draw_shell(c, terrace_text=False); bd.draw_equipment(c, labels=False); plan_labels(c)
    txt(c, 220, 700, "ÎLOT", 6, "FB"); txt(c, 507, 515, "CAISSE 1", 5, "FB", rot=90); txt(c, 507, 640, "CAISSE 2", 5, "FB", rot=90); txt(c, 507, 845, "RETRAIT", 5, "FB", rot=90)
    BL = HexColor("#2f6db5"); GR = HexColor("#2e8b57")
    arrow_path(c, [(-80, 590), (90, 610), (90, 930), (200, 990)], BL, lw=1.6)
    arrow_path(c, [(400, 1000), (405, 900), (410, 690)], GR, lw=1.6)
    arrow_path(c, [(445, 515), (90, 520)], RED, lw=4.5, dash=(5, 3), head=False)
    arrow_path(c, [(445, 600), (520, 420), (720, 300)], BROWN, lw=1.4, dash=(3, 2))
    arrow_path(c, [(420, 560), (200, 570), (-80, 565)], GREY, lw=1.4)
    for (x, y) in [(425, 820), (380, 862), (440, 880)]: circle(c, x, y, 18, fill=ORANGE, stroke=None)
    for n, (x, y) in enumerate([(250, 520), (395, 780), (60, 760), (640, 580), (220, 680), (300, 290), (956, 130)], start=1): hot(c, x, y, n)
    bd.scale_bar(c, 150, 120)
    c.setFont("FB", 12); c.setFillColor(NAVY); c.drawString(40, H - 40, "12h45, un jour de semaine : le parcours actuel (V3)")
    y = legend_box(c, 40, 262, [("line", BL, "Clients qui entrent (vers la murale)"), ("line", GR, "Clients qui vont payer"),
                                 ("dash", RED, "File d'attente (8 personnes)"), ("dot", ORANGE, "Attente debout du chaud"),
                                 ("dash", BROWN, "Plateau vers la salle"), ("line", GREY, "Départ à emporter")], "Flux")
    para(c, 330, 262, 420,
         "**Points chauds\n"
         "1. La file de la caisse 1 part vers la porte : 8 personnes l'atteignent.\n"
         "2. Croisement de la file, de la sortie de murale et de l'attente du chaud.\n"
         "3. Côté vitrine de l'îlot : 1,10 m seulement (moins que 1,20 m), poussette et fauteuil y passent mal.\n"
         "4. Écrans menus à 5 m, au-dessus du comptoir : illisibles depuis la murale.\n"
         "5. Produits à l'arachide à hauteur d'enfant sur l'îlot.\n"
         "6. Tables de deux, pas de chaise haute, pas de crochets à sacs.\n"
         "7. Une seule desserte, au fond de l'alcôve.", 7.6)
    w = 405; h = w / 1.6
    c.drawImage(os.path.join(R, "rush_v3_entree.jpg"), 765, H - 75 - h, w, h)
    c.drawImage(os.path.join(R, "rush_v3_vente.jpg"), 765, H - 100 - 2 * h, w, h)
    c.setFillColor(GREY); c.setFont("FI", 6.8)
    c.drawString(765, H - 84 - h, "Ce que voit le client qui arrive à la porte : un mur de dos, pas l'arbre.")
    c.drawString(765, H - 109 - 2 * h, "Même instant, maquette coupée : la file barre l'entrée, l'attente du chaud bloque le bas du comptoir.")
    para(c, 765, H - 128 - 2 * h, 405,
         "**Hypothèse du coup de feu\nSi 40 clients arrivent entre 12h30 et 13h et qu'un passage en caisse dure 45 secondes, une caisse sert exactement ce qui arrive : la moindre vague fait monter la file à 8-10 personnes. Avec deux caisses ouvertes, elle redescend vite, à condition qu'elle ne bloque pas l'entrée entre-temps.", 7.6)
    cart(c, "COUP DE FEU — V3", 4, "1/75")

def p_v4(c):
    bd.draw_shell(c, terrace_text=False); bd.draw_equipment(c, labels=False); plan_labels(c)
    # îlot redessiné 1,90 m
    rect(c, 104, 612, 336, 858, fill=FLOOR, stroke=None)
    rect(c, 140, 620, 330, 850, fill=WOOD, stroke=BROWN, lw=0.8, r=12); circle(c, 235, 735, 28, fill=HexColor("#6aa84f"), stroke=HexColor("#38761d"))
    txt(c, 235, 650, "ÎLOT 1,90 m", 5.2, "FB")
    # comptoir réorganisé
    rect(c, 471, 465, 501, 566, fill=WOOD, stroke=None)
    rect(c, 470, 600, 500, 690, fill=white, stroke=BROWN, lw=0.4)
    txt(c, 507, 500, "RETRAIT\nC&C", 4.6, "FB", rot=90); txt(c, 507, 645, "CAISSE 1\nadaptée", 4.4, "FB", rot=90)
    txt(c, 507, 775, "CAISSE 2", 4.6, "FB", rot=90); txt(c, 507, 875, "entrée\nde file", 4.2, "F", rot=90)
    # station de tri, totem, marquage
    rect(c, 0, 345, 100, 430, fill=FLOOR, stroke=None)
    rect(c, 0, 355, 55, 445, fill=HexColor("#eadcf2"), stroke=MAG, lw=0.9); txt(c, 27, 400, "TRI", 4.6, "FB", MAG)
    rect(c, 20, 925, 58, 975, fill=NAVY, stroke=None)
    GR = HexColor("#2e8b57")
    arrow_path(c, [(-80, 600), (70, 640), (70, 960)], HexColor("#2f6db5"), lw=1.6)
    arrow_path(c, [(70, 985), (400, 985), (410, 900), (420, 700)], GR, lw=4, dash=(5, 3))
    arrow_path(c, [(440, 600), (440, 520)], GR, lw=1.6)
    arrow_path(c, [(420, 500), (200, 520), (-80, 525)], GREY, lw=1.4)
    arrow_path(c, [(470, 470), (560, 400), (720, 300)], BROWN, lw=1.4, dash=(3, 2))
    for (a, b, xx, lab) in [(0, 140, 760, "1,40"), (330, 470, 760, "1,40")]:
        line(c, a, xx, b, xx, MAG, 0.6); txt(c, (a + b) / 2, xx - 12, lab, 5.5, "FB", MAG)
    for n, (x, y) in enumerate([(240, 985), (507, 700), (235, 735), (40, 1010), (420, 470), (27, 400), (300, 200)], start=0):
        badge(c, x, y, "ABCDEFGH"[n], MAG, 7)
    bd.scale_bar(c, 150, 120)
    c.setFont("FB", 12); c.setFillColor(NAVY); c.drawString(40, H - 40, "Parcours proposé (V4) : une boucle à sens unique, sans travaux")
    para(c, 40, 262, 700,
         "**Ce qui change (lettres sur le plan)\n"
         "A. File le long de la murale : on se sert en avançant ; 11 personnes tiennent avant d'approcher la porte (contre 8 en V3).\n"
         "B. Comptoir redessiné : retrait et click & collect en haut, visibles depuis la porte ; caisse adaptée puis caisse 2 au milieu ; entrée de file en bas.\n"
         "C. Îlot ramené à 1,90 m : 1,40 m côté vitrine (nouvel accès à la murale) et 1,40 m côté comptoir.\n"
         "D. Totem à l'entrée de la file : « Ici, on se sert en avançant » et « Envie de chaud ? Commandez en caisse ».\n"
         "E. Retrait unique (click & collect et plats chauds à emporter) avec écran « commandes prêtes » ; sur place, le chaud est servi à table.\n"
         "F. Station de tri et retour des plateaux à la sortie (un tabouret en moins : 28 places).\n"
         "G. Tables de deux jumelables (4 et 6 places), deux chaises hautes, crochets à sacs, coin poussette dans l'alcôve.", 7.6)
    w = 405; h = w / 1.6
    c.drawImage(os.path.join(R, "rush_v4_entree.jpg"), 765, H - 75 - h, w, h)
    c.drawImage(os.path.join(R, "rush_v4_vente.jpg"), 765, H - 100 - 2 * h, w, h)
    c.setFillColor(GREY); c.setFont("FI", 6.8)
    c.drawString(765, H - 84 - h, "Même coup de feu, même nombre de clients : l'entrée et l'arbre restent dégagés.")
    c.drawString(765, H - 109 - 2 * h, "La file longe les frigos puis remonte le comptoir ; le retrait est en haut.")
    para(c, 765, H - 128 - 2 * h, 405,
         "**Pourquoi c'est gratuit\nLe comptoir et l'îlot ne sont pas encore fabriqués : il suffit de les dessiner ainsi pour l'agenceur. Le reste est du mobilier, de la signalétique et des règles de service. À reporter dans le dossier mairie avant dépôt (position de la caisse adaptée et cotes de passage, pièces 06 et 09).", 7.6)
    cart(c, "PARCOURS PROPOSÉ — V4", 7, "1/75")

# ------------------------------------------------------------------------------------------ récits
def card(c, x, y, w, h, p):
    c.setFillColor(HexColor("#f6f7f9")); c.rect(x, y - h, w, h, fill=1, stroke=0)
    c.setFillColor(NAVY); c.rect(x, y - 30, w, 30, fill=1, stroke=0)
    c.setFillColor(white); c.setFont("FB", 10); c.drawString(x + 10, y - 13, p["nom"])
    c.setFont("F", 7.6); c.drawString(x + 10, y - 24, p["qui"] + " · " + p["quand"])
    tw = tagbox(c, x + w - 120, y - 14, p["tag"])
    s3, s4 = score(p["v3"]), score(p["v4"])
    c.setFillColor(white); c.setFont("FB", 8); c.drawString(x + w - 112 + tw, y - 13, f"{s3:.1f} → {s4:.1f}".replace(".", ","))
    c.setFillColor(HexColor("#2e8b57")); c.setFont("FI", 9.6)
    yy = para(c, x + 12, y - 48, w - 24, p["quote"], 9.2, font="FI", col=HexColor("#1f5f3a"))
    yy = para(c, x + 12, yy - 6, w - 24, "**Son parcours aujourd'hui (V3)\n" + p["recit"], 8.2)
    para(c, x + 12, yy - 4, w - 24, "**Ce qui le ferait revenir\n" + p["besoin"], 8.2)
    cw = (w - 70) / 10
    c.setFont("FB", 6.6); c.setFillColor(INK)
    SH = ["Repérer", "Entrer", "Comprendre", "Choisir", "Attendre", "Payer", "Chaud", "S'installer", "Débarrasser", "Revenir"]
    for i, st in enumerate(SH): c.drawCentredString(x + 50 + cw * i + cw / 2, y - h + 62, st)
    for r_, key in enumerate(["v3", "v4"]):
        yy0 = y - h + 34 - r_ * 22
        c.setFillColor(INK); c.setFont("FB", 7.4); c.drawString(x + 14, yy0 + 5, key.upper())
        for i, (code, note) in enumerate(p[key]):
            fg, bg = COL[code]; c.setFillColor(bg); c.rect(x + 50 + cw * i + 1, yy0, cw - 2, 18, fill=1, stroke=0)
            c.setFillColor(fg); c.circle(x + 50 + cw * i + cw / 2, yy0 + 9, 3.5, fill=1, stroke=0)

def p_recits(c, idx, num):
    h1(c, 40, H - 50, "Récits des clients-tests (%d/2)" % (num - 4))
    w, h = 545, 330
    for k, i in enumerate(idx):
        card(c, 40 + (k % 2) * (w + 20), H - 72 - (k // 2) * (h + 14), w, h, PERSONAS[i])
    cart(c, "RÉCITS DES CLIENTS-TESTS", num)

# ------------------------------------------------------------------------------------------ page 8
def p_mesures(c):
    h1(c, 40, H - 50, "Carte d'expérience avec la V4 et liste des mesures")
    y = matrix(c, 40, H - 70, "v4", "Client-test · étape du parcours (V4)", rh=34, fs=6.0)
    rows = [
     ("A. Boucle à sens unique, file le long de la murale", "Personnel du centre, salariés, artisan, client en fauteuil", "Marquage au sol + 1 totem : < 500 €", "Plan d'agencement"),
     ("B. Comptoir redessiné (retrait en haut, caisses au milieu)", "Tous", "0 € (pas encore fabriqué)", "Dossier mairie pièces 06 et 09"),
     ("C. Îlot ramené à 1,90 m", "Familles, client en fauteuil", "0 € (pas encore fabriqué)", "Dossier mairie pièce 09"),
     ("D. Chaud annoncé à l'entrée de la file, servi à table avec un numéro", "Salariés, familles, seniors, client en fauteuil", "Chevalets numérotés : < 500 €", "Procédure de service"),
     ("L. Deux caisses ouvertes et une personne en salle de 12h15 à 13h30", "Tous au coup de feu", "Temps de personnel : à intégrer au prévisionnel", "Planning"),
     ("E. Au coup de feu (12h15-13h30), baos en petites séries au retrait", "Personnel du centre, artisan", "0 € ; invendus à surveiller", "PMS : maintien ≥ 63 °C, durée limitée, invendus jetés"),
     ("F. Click & collect + carte de fidélité + offre personnel du centre", "Personnel du centre, artisan, salariés", "Module du logiciel de caisse : à comparer", "Accord du centre pour l'offre personnel"),
     ("G. Familles et groupes : tables jumelables, 2 chaises hautes, crochets, box enfant", "Familles, visiteuses, salariés", "< 500 € (hors carte)", "—"),
     ("H. Lisibilité : menu papier gros caractères, lexique « Le Japon en 6 mots », étiquettes avec photo, arachide en hauteur", "Seniors, familles, visiteuses", "< 500 €", "Audit DDPP : allergènes"),
     ("I. Station de tri à la sortie (28 places au lieu de 29)", "Tous, client en fauteuil", "Meuble : < 2 000 €", "Effectif ERP inchangé"),
     ("J. Panneaux « Toilettes du centre », enseigne drapeau, présence sur le plan du centre", "Familles, visiteuses, artisan", "Panneaux < 500 € ; drapeau en option", "Accord du centre"),
     ("K. Option si la file dépasse 8 personnes plusieurs jours : borne de paiement express", "Personnel du centre, salariés", "> 2 000 € : à décider après 1 mois", "—"),
    ]
    table(c, 40, y - 14, [("Mesure", 400), ("Pour qui", 270), ("Coût (ordre de grandeur, à chiffrer)", 210), ("À reporter dans", 220)], rows, 7.2, pad=3)
    cart(c, "MESURES ET EFFET ATTENDU", 8)

# ------------------------------------------------------------------------------------------ page 9
def p_tests(c):
    h1(c, 40, H - 50, "Vérifier avant et après l'ouverture")
    para(c, 40, H - 82, 540,
        "**Avant de signer : observer le vrai site (2 midis)\n"
        "• Un mardi et un samedi, de 12h à 14h, devant la cellule : compter les passants, noter d'où ils arrivent (parking, allée) et s'ils portent déjà un repas.\n"
        "• Parler à une dizaine de vendeurs du centre : heure et durée de pause, budget, où ils mangent aujourd'hui. C'est le test du profil « Sandrine », le plus important pour la semaine.\n"
        "• Demander à la direction du centre la fréquentation par jour et par heure, et le nombre de salariés sur le site.\n"
        "• Vérifier ce qu'on voit de la cellule depuis le parking et l'entrée du centre (profil « Thomas »).\n"
        "\n"
        "**Avant d'ouvrir : une répétition à blanc\n"
        "• Dans le local vide, tracer au scotch l'îlot, le comptoir et la murale.\n"
        "• Faire jouer un coup de feu de 20 minutes à 15 personnes (équipe, amis) avec paniers et plateaux, dont une poussette et un fauteuil roulant.\n"
        "• Chronométrer et filmer depuis la porte ; corriger l'implantation avant de commander le comptoir.\n"
        "\n"
        "**Après l'ouverture : client mystère\n"
        "À J+15 et J+45, faire jouer chacun des 8 profils par une personne différente, avec la grille de la carte d'expérience (planche 03).", 8.4)
    rows = [("Temps entre la porte et le paiement au coup de feu", "≤ 4 min", "Chronomètre, 10 clients par jour la 1re semaine"),
            ("Longueur maximale de la file", "≤ 8 personnes", "Comptage à 12h30, 12h45, 13h"),
            ("Attente d'un plat chaud", "≤ 5 min (0 au retrait en série)", "Heure de commande / heure de remise"),
            ("Clients qui entrent et repartent sans acheter", "< 5 %", "Comptage 30 min par jour"),
            ("Part des commandes en click & collect", "Suivre la tendance", "Logiciel de caisse"),
            ("Note Google", "≥ 4,5", "Chaque semaine"),
            ("Panier moyen et part du retail", "Suivre", "Logiciel de caisse"),
            ("Places occupées à 12h45 / 15h30", "Suivre", "Comptage")]
    c.setFont("FB", 10); c.setFillColor(NAVY); c.drawString(620, H - 82, "Indicateurs à suivre et seuils d'alerte")
    yy = table(c, 620, H - 92, [("Indicateur", 230), ("Seuil", 120), ("Comment le mesurer", 180)], rows, 7.6, pad=4)
    para(c, 620, yy - 18, 530,
         "**Limites de cet exercice\n"
         "• Les profils sont construits, pas interrogés : leurs attentes sont plausibles mais à confirmer sur place.\n"
         "• Je n'ai trouvé aucune donnée publique de fréquentation du centre, ni l'emplacement exact de la cellule par rapport au parking.\n"
         "• Le départ de l'ancien exploitant (boulangerie-snacking) est un signal à comprendre : demander au centre et au bailleur pourquoi il est parti.\n"
         "• L'hypothèse de coup de feu (40 clients en 30 minutes) sert à tester l'implantation, pas à prévoir le chiffre d'affaires.", 8)
    cart(c, "TESTS ET INDICATEURS", 9)

def main():
    c = canvas.Canvas(OUT, pagesize=(W, H))
    c.setTitle("Parcours clients — L'Arbre à Makis — Cellule 09 La Séguinière"); c.setAuthor("L'Arbre à Makis")
    p_synthese(c); c.showPage()
    p_personas(c); c.showPage()
    p_matrix_v3(c); c.showPage()
    p_v3_rush(c); c.showPage()
    p_recits(c, [0, 1, 5, 7], 5); c.showPage()
    p_recits(c, [2, 3, 4, 6], 6); c.showPage()
    p_v4(c); c.showPage()
    p_mesures(c); c.showPage()
    p_tests(c); c.showPage()
    c.save(); print("OK", OUT)
    for p in PERSONAS: print(f"{p['nom'][:40]:42s} V3 {score(p['v3'])}  V4 {score(p['v4'])}")

if __name__ == "__main__":
    main()
