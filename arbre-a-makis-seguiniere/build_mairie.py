# -*- coding: utf-8 -*-
"""Dossier de demande d'autorisation de travaux (ERP, Cerfa 13824*04) à déposer en mairie de La Séguinière.
Réutilise la géométrie et les tracés de build_dossier.py (plan V3)."""
import os, math
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, A3, landscape
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfbase import pdfmetrics
import build_dossier as bd
from build_dossier import para, table, P, rect, line, txt, circle, arrow_path, badge

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "Dossier_Mairie_AT_LAM_La_Seguiniere.pdf")
A4W, A4H = A4
A3W, A3H = landscape(A3)
INK = HexColor("#1b1f27"); GRY = HexColor("#666b73"); LGR = HexColor("#eef0f2"); NAVY = bd.NAVY; RED = bd.RED; BLUE = bd.BLUE
GG = HexColor("#1a9e3f"); BLANK = "……………………………………"
ETAB = "L'Arbre à Makis — Cellule n°09 — Espace commercial Marques Avenue — Rue du Bocage — 49280 La Séguinière"
DATE = "17/11/2026"

# ----------------------------------------------------------------------------------------------- mise en page A4
def a4(c):
    c.setPageSize(A4)

def a3(c):
    c.setPageSize((A3W, A3H))

def a4_head(c, piece, titre, sous=None):
    c.setFillColor(INK); c.setFont("FB", 8); c.drawString(50, A4H - 40, f"DEMANDE D'AUTORISATION DE TRAVAUX — ERP — PIÈCE {piece}")
    c.setStrokeColor(INK); c.setLineWidth(0.6); c.line(50, A4H - 46, A4W - 50, A4H - 46)
    c.setFont("FB", 15); c.drawString(50, A4H - 74, titre)
    y = A4H - 92
    if sous:
        c.setFont("F", 9); c.setFillColor(GRY); c.drawString(50, y, sous); y -= 14
    return y - 6

def a4_foot(c, piece, n):
    c.setFillColor(GRY); c.setFont("F", 7)
    c.drawString(50, 30, "L'Arbre à Makis — cellule n°09, espace commercial Marques Avenue, La Séguinière")
    c.drawRightString(A4W - 50, 30, f"Pièce {piece} — page {n} — {DATE}")
    c.setStrokeColor(HexColor("#c9ccd1")); c.setLineWidth(0.4); c.line(50, 40, A4W - 50, 40)

def h2(c, x, y, s, size=10.5):
    c.setFillColor(NAVY); c.setFont("FB", size); c.drawString(x, y, s); return y - size * 1.5

def field_rows(c, x, y, rows, w1=170, w2=325, size=8.6):
    for lab, val in rows:
        c.setFillColor(INK); c.setFont("FB", size); c.drawString(x, y, lab)
        yy = para(c, x + w1, y, w2, val, size)
        y = min(y - size * 1.55, yy - 2)
        c.setStrokeColor(HexColor("#dfe2e6")); c.setLineWidth(0.3); c.line(x, y + size * 0.7, x + w1 + w2, y + size * 0.7)
    return y

# ----------------------------------------------------------------------------------------------- cartouche A3 (plans)
def cart_a3(c, piece, titre, ech, note="Cotes issues des plans de l'aménagement 2015 — à confirmer par relevé avant dépôt"):
    c.setStrokeColor(INK); c.setLineWidth(0.8); c.rect(20, 18, A3W - 40, 58)
    for x in (300, 640, 900, 1010, 1090): c.line(x, 18, x, 76)
    c.setFillColor(INK); c.setFont("F", 6.5); c.drawString(26, 66, "Demandeur (exploitant)")
    c.setFont("FB", 8.5); c.drawString(26, 52, "Raison sociale : " + BLANK)
    c.setFont("F", 7.5); c.drawString(26, 40, "Représentée par : " + BLANK)
    c.drawString(26, 28, "Enseigne : L'Arbre à Makis")
    c.setFont("F", 6.5); c.drawString(306, 66, "Établissement")
    c.setFont("FB", 8.5); c.drawString(306, 52, "Cellule n°09 — Espace commercial Marques Avenue")
    c.setFont("F", 7.5); c.drawString(306, 40, "Rue du Bocage — 49280 La Séguinière")
    c.drawString(306, 28, "ERP type N + M — 5e catégorie — sans locaux à sommeil")
    c.setFont("F", 6.5); c.drawString(646, 66, f"Pièce {piece}")
    c.setFont("FB", 11); c.drawString(646, 46, titre)
    c.setFont("F", 6.5); c.setFillColor(GRY); c.drawString(646, 26, note)
    c.setFillColor(INK); c.setFont("F", 6.5); c.drawString(906, 66, "Échelle"); c.setFont("FB", 10); c.drawString(906, 44, ech)
    c.setFont("F", 6.5); c.drawString(1016, 66, "Date / indice"); c.setFont("FB", 9); c.drawString(1016, 46, DATE); c.drawString(1016, 30, "Indice A")
    c.setFont("F", 6.5); c.drawString(1096, 66, "Signature"); c.setStrokeColor(HexColor("#aaaaaa")); c.rect(1096, 22, 66, 38)

def north_arrow(c, X, Y):
    c.saveState(); c.setStrokeColor(INK); c.setFillColor(INK); c.setFont("FB", 7)
    c.drawString(X, Y, "← FAÇADE (allée du village)"); c.drawRightString(X + 640, Y, "FOND DE CELLULE (couloir de service) →"); c.restoreState()

def scale_bar(c, X, Y):
    bd.scale_bar(c, X, Y)

def cote(c, x1, y1, x2, y2, label, off=0, col=INK, size=5.5):
    """cote linéaire entre deux points plan (cm)."""
    line(c, x1, y1, x2, y2, col, 0.5)
    for (x, y) in ((x1, y1), (x2, y2)):
        if x1 == x2: line(c, x - 12, y, x + 12, y, col, 0.5)
        else: line(c, x, y - 12, x, y + 12, col, 0.5)
    if x1 == x2: txt(c, x1 + 14 + off, (y1 + y2) / 2, label, size, "FB", col, rot=90)
    else: txt(c, (x1 + x2) / 2, y1 - 14 + off, label, size, "FB", col)

# ----------------------------------------------------------------------------------------------- données
EFFECTIF = [
    ("Zones de restauration assise (salle 20,2 m² + alcôve 14,0 m²)", "34,2 m²", "1 pers./m²", "35"),
    ("Zone de vente et d'attente accessible au public", "47,2 m²", "1 pers./m² (valeur majorante)", "48"),
    ("Terrasse sous auvent, si exploitée (places déclarées)", "—", "places assises", "16"),
    ("EFFECTIF PUBLIC MAXIMAL RETENU", "", "", "99"),
    ("Personnel (n'intervient pas dans le classement en 5e catégorie)", "", "", "6 max."),
]

# ----------------------------------------------------------------------------------------------- pages
def p_mode_emploi(c):
    a4(c)
    c.setFillColor(HexColor("#fff6d9")); c.rect(0, 0, A4W, A4H, fill=1, stroke=0)
    c.setFillColor(INK); c.setFont("FB", 9); c.drawString(50, A4H - 40, "PAGE D'INSTRUCTIONS — À RETIRER AVANT L'ENVOI")
    c.setFont("FB", 17); c.drawString(50, A4H - 70, "Mode d'emploi du dossier mairie")
    y = para(c, 50, A4H - 96, 495,
        "**Ce que vous déposez\n"
        "Une demande d'autorisation de travaux pour un établissement recevant du public (ERP). Elle est obligatoire avant d'aménager un local qui reçoit de la clientèle, même sans permis de construire. La mairie la transmet pour avis à la commission de sécurité (SDIS 49) et à la commission d'accessibilité. Vous ne touchez ni à la façade ni à la structure : un permis de construire n'est donc pas nécessaire.\n"
        "\n"
        "**Ce que je n'ai pas pu faire à votre place\n"
        "1. Télécharger et remplir le formulaire officiel Cerfa 13824*04 (sur service-public.fr). La pièce 02 vous dit quoi écrire dans chaque rubrique.\n"
        "2. Compléter les champs en pointillés (raison sociale, SIRET, représentant), puis dater et signer le Cerfa, le courrier et les deux notices.\n"
        "3. Joindre un extrait de plan cadastral (cadastre.gouv.fr, gratuit) et un plan de situation (geoportail.gouv.fr) à la pièce 03.\n"
        "4. Prendre les photos listées en pièce 12 et les coller dans les cadres.\n"
        "5. Joindre l'accord écrit du bailleur / de la direction du centre (pièce 13).\n"
        "6. Faire vérifier les cotes principales sur place : les plans sont redessinés d'après les plans de l'aménagement de 2015 (précision d'environ 10 cm).\n"
        "\n"
        "**Combien d'exemplaires, où, quand\n"
        "• En général 3 exemplaires complets (certaines mairies en demandent 4) : appelez le service urbanisme de La Séguinière pour confirmer, et demandez s'il accepte le dépôt en ligne.\n"
        "• Dépôt en mairie contre récépissé, ou par lettre recommandée avec accusé de réception. Gardez un exemplaire complet.\n"
        "• Délai d'instruction : plusieurs mois (4 mois en pratique courante, plus si la mairie demande des pièces). Ne commencez pas les travaux avant d'avoir reçu l'accord.\n"
        "• Si la mairie demande des pièces complémentaires, le délai repart à leur réception : répondez vite.\n"
        "\n"
        "**Ce que ce dossier ne couvre pas\n"
        "• L'enseigne : si la commune ou l'agglomération a un règlement local de publicité, il faut en plus une autorisation d'enseigne (Cerfa 14798*01). La pièce 11 (façades) peut y être jointe. Je n'ai pas trouvé de règlement publié pour La Séguinière : posez la question en mairie.\n"
        "• La déclaration d'activité alimentaire à la DDPP, qui se fait à part, en ligne, avant l'ouverture.\n"
        "• L'accord du centre Marques Avenue sur l'aménagement et l'enseigne, qui reste à obtenir de votre côté (souvent avant même le dépôt).\n"
        "\n"
        "**Droits sur les plans de 2015\n"
        "Les plans du dossier La Mie Câline de 2015 appartiennent à leur cabinet d'architecture et portent une mention interdisant leur diffusion. Ce dossier n'en reproduit aucune page : tous les plans ont été redessinés. N'y ajoutez pas de copies de ces anciens plans sans l'accord du cabinet.\n"
        "\n"
        "**Après l'accord\n"
        "Faites réaliser les travaux, puis les vérifications prévues dans la notice de sécurité (électricité, extincteurs, extraction). Ouvrez le registre de sécurité et le registre public d'accessibilité. Gardez les attestations : la commission de sécurité peut passer.", 8.8)

def p_garde(c):
    a4(c)
    c.setFillColor(INK); c.setFont("F", 10); c.drawString(50, A4H - 70, "Mairie de La Séguinière — Service urbanisme")
    c.setStrokeColor(INK); c.setLineWidth(1.2); c.line(50, A4H - 84, A4W - 50, A4H - 84)
    c.setFont("FB", 22); c.drawString(50, A4H - 140, "DEMANDE D'AUTORISATION")
    c.drawString(50, A4H - 168, "DE TRAVAUX")
    c.setFont("F", 13); c.drawString(50, A4H - 196, "Établissement recevant du public — articles L.122-3 et suivants")
    c.drawString(50, A4H - 214, "du code de la construction et de l'habitation")
    c.setFont("FB", 12); c.drawString(50, A4H - 270, "Aménagement intérieur d'une cellule commerciale existante")
    c.setFont("F", 11); c.drawString(50, A4H - 288, "en point de vente de restauration rapide (vente à emporter et consommation sur place)")
    y = A4H - 340
    y = field_rows(c, 50, y, [
        ("Établissement", "L'Arbre à Makis"),
        ("Adresse", "Cellule n°09 — Espace commercial Marques Avenue — Rue du Bocage — 49280 La Séguinière"),
        ("Références cadastrales", "Section AX, parcelle n°48 (d'après le dossier 2015, à vérifier sur l'extrait cadastral joint)"),
        ("Classement", "ERP de type N (restauration) avec activité M (vente), 5e catégorie, sans locaux à sommeil"),
        ("Demandeur", "Raison sociale : " + BLANK + "\nSIRET : " + BLANK + "\nReprésentée par : " + BLANK),
        ("Contact", "Téléphone : " + BLANK + "\nCourriel : " + BLANK),
        ("Précédent exploitant", "La Mie Câline (terminal de cuisson et restauration), aménagement autorisé en 2015"),
        ("Nature des travaux", "Aucune modification de structure, de façade ni du recoupement coupe-feu. Remplacement du mobilier et des équipements, deux ouvertures dans des cloisons légères existantes, ajout de deux lave-mains, changement des faces de l'enseigne."),
        ("Date", DATE),
    ], w1=150, w2=345, size=9.2)
    c.setFillColor(GRY); c.setFont("FI", 8); c.drawString(50, 70, "Dossier composé de 14 pièces — voir le bordereau (pièce 00).")

def p_bordereau(c):
    a4(c); y = a4_head(c, "00", "Bordereau des pièces")
    rows = [("00", "Bordereau des pièces", "Joint"), ("01", "Courrier de demande adressé au maire", "Joint — à signer"),
            ("02", "Formulaire Cerfa 13824*04 + aide au remplissage", "Cerfa à télécharger, remplir et signer"),
            ("03", "Plan de situation et extrait cadastral", "À joindre (cadastre.gouv.fr / geoportail)"),
            ("04", "Notice descriptive de sécurité incendie", "Jointe — à signer"),
            ("05", "Plan de l'état existant (avant travaux)", "Joint — A3"),
            ("06", "Plan de l'état projeté — sécurité incendie", "Joint — A3"),
            ("07", "Coupe longitudinale AA", "Jointe — A3"),
            ("08", "Notice d'accessibilité (ERP existant)", "Jointe — à signer"),
            ("09", "Plan de l'état projeté — accessibilité, coté", "Joint — A3"),
            ("10", "Notice descriptive des travaux et des matériaux", "Jointe"),
            ("11", "Façades état actuel / état projeté (enseigne)", "Jointe — A3"),
            ("12", "Photographies de l'état actuel", "À compléter (cadres prévus)"),
            ("13", "Accord du bailleur / de la direction du centre", "À joindre")]
    yy = table(c, 50, y, [("Pièce", 50), ("Intitulé", 285), ("État", 160)], rows, 8.6)
    para(c, 50, yy - 20, 495,
         "**Demande de dérogation\nAucune dérogation aux règles de sécurité ou d'accessibilité n'est demandée.\n\n"
         "**Permis de construire\nLes travaux ne relèvent d'aucune autre autorisation d'urbanisme : ni modification de façade, ni création de surface, ni changement de destination (le local reste un commerce de restauration, comme précédemment).", 8.8)
    a4_foot(c, "00", 1)

def p_courrier(c):
    a4(c)
    c.setFillColor(INK); c.setFont("F", 9.5)
    y = A4H - 70
    for l in ["Raison sociale : " + BLANK, "Adresse du siège : " + BLANK, BLANK + BLANK, "SIRET : " + BLANK, "Téléphone / courriel : " + BLANK]:
        c.drawString(50, y, l); y -= 14
    y -= 10
    for l in ["Madame, Monsieur le Maire", "Mairie de La Séguinière", "Service urbanisme", "49280 La Séguinière"]:
        c.drawString(330, y, l); y -= 14
    y -= 14; c.drawString(330, y, "À " + "……………………" + ", le " + "……………………"); y -= 34
    c.setFont("FB", 9.5); c.drawString(50, y, "Objet : demande d'autorisation de travaux — établissement recevant du public"); y -= 13
    c.setFont("F", 9.5); c.drawString(50, y, "Cellule n°09, Espace commercial Marques Avenue, rue du Bocage"); y -= 13
    c.drawString(50, y, "Pièces jointes : dossier en 14 pièces (bordereau en pièce 00)"); y -= 30
    para(c, 50, y, 495,
         "Madame, Monsieur le Maire,\n\n"
         "Nous reprenons la cellule n°09 de l'espace commercial Marques Avenue, précédemment exploitée par La Mie Câline, pour y ouvrir un point de vente de restauration rapide à l'enseigne L'Arbre à Makis : sushis, bowls et baos préparés dans notre laboratoire de Maulévrier, vendus en vitrines réfrigérées en libre-service, avec une offre de produits d'épicerie et une salle pour consommer sur place.\n\n"
         "Conformément à l'article L.122-3 du code de la construction et de l'habitation, nous avons l'honneur de solliciter l'autorisation de réaliser les travaux d'aménagement intérieur décrits dans le dossier ci-joint.\n\n"
         "L'établissement reste classé en type N avec activité M, en 5e catégorie, sans locaux à sommeil. Les travaux conservent l'enveloppe, la façade, les cloisons et le recoupement coupe-feu existants. Ils consistent pour l'essentiel à remplacer le mobilier et les équipements, à créer deux ouvertures dans des cloisons légères, à ajouter deux lave-mains et à changer les faces de l'enseigne. L'effectif maximal du public passe de 53 places assises à 29 places intérieures et 16 places en terrasse, pour un effectif total retenu de 99 personnes. Les appareils de cuisson sont électriques, d'une puissance totale inférieure à 20 kW.\n\n"
         "Nous restons à la disposition de vos services et de la commission de sécurité et d'accessibilité pour tout complément d'information ou visite du local.\n\n"
         "Nous vous prions d'agréer, Madame, Monsieur le Maire, l'expression de nos salutations distinguées.", 9.5, lead=1.4)
    c.setFont("F", 9.5); c.drawString(330, 150, "Nom, qualité : " + "……………………………"); c.drawString(330, 132, "Signature et cachet :")
    a4_foot(c, "01", 1)

def p_cerfa(c):
    a4(c); y = a4_head(c, "02", "Formulaire Cerfa 13824*04 — aide au remplissage", "Le formulaire officiel est à télécharger sur service-public.fr (« Autorisation de travaux ERP »), à remplir et à signer.")
    rows = [
     ("Identité du demandeur", "Personne morale : dénomination, raison sociale, n° SIRET, type de société, nom et qualité du représentant légal."),
     ("Coordonnées", "Adresse du siège ; téléphone et courriel où la mairie peut vous joindre."),
     ("Localisation de l'établissement", "Cellule n°09, Espace commercial Marques Avenue, rue du Bocage, 49280 La Séguinière ; cadastre section AX n°48 (à vérifier sur l'extrait cadastral)."),
     ("Nom et activité de l'établissement", "L'Arbre à Makis — restauration rapide (vente à emporter et consommation sur place), vente de produits alimentaires préemballés."),
     ("Type et catégorie", "Type N (restauration) avec activité de type M (vente) ; 5e catégorie ; pas de locaux à sommeil."),
     ("Effectif", "Public : 99 personnes au maximum (détail en pièce 04) ; personnel : 6 au maximum."),
     ("Nature des travaux", "Aménagement intérieur d'une cellule existante, sans modification de structure, de façade ni du recoupement coupe-feu (détail en pièce 10)."),
     ("Permis de construire", "Non, les travaux ne sont soumis à aucune autre autorisation d'urbanisme."),
     ("Demande de dérogation", "Aucune (ne rien remplir dans le cadre « dérogation »)."),
     ("Pièces jointes", "Cocher les pièces correspondant au bordereau (pièce 00) : plans, notice de sécurité, notice d'accessibilité."),
     ("Engagement", "Date, lieu, nom, qualité et signature du représentant légal."),
    ]
    yy = table(c, 50, y, [("Rubrique", 150), ("À indiquer", 345)], rows, 8.5)
    para(c, 50, yy - 18, 495, "Les intitulés des rubriques peuvent légèrement différer selon la version imprimée du formulaire : reportez-vous au sens indiqué ci-dessus. En cas de doute, le service urbanisme peut vous aider à le remplir lors du dépôt.", 8.2, col=GRY)
    a4_foot(c, "02", 1)

def p_situation(c):
    a4(c); y = a4_head(c, "03", "Plan de situation et extrait cadastral")
    for i, (t, how) in enumerate([("PLAN DE SITUATION", "À imprimer depuis geoportail.gouv.fr : centrer sur l'espace commercial Marques Avenue (rue du Bocage, La Séguinière), échelle 1/5 000 à 1/25 000, repérer la cellule par une flèche."),
                                  ("EXTRAIT DU PLAN CADASTRAL", "À imprimer depuis cadastre.gouv.fr : section AX, parcelle n°48 (référence du dossier 2015, à vérifier), repérer le bâtiment et la cellule n°09.")]):
        top = y - i * 330
        c.setStrokeColor(GRY); c.setDash(4, 3); c.rect(50, top - 300, 495, 290); c.setDash()
        c.setFillColor(INK); c.setFont("FB", 10); c.drawCentredString(A4W / 2, top - 140, t)
        para(c, 110, top - 160, 375, how, 8.6, col=GRY)
    a4_foot(c, "03", 1)

def notice_securite(c):
    a4(c); y = a4_head(c, "04", "Notice descriptive de sécurité incendie", "Règlement de sécurité ERP (arrêté du 25 juin 1980 modifié) — petits établissements (PE)")
    y = h2(c, 50, y, "1. Renseignements généraux")
    y = field_rows(c, 50, y, [
        ("Établissement", "L'Arbre à Makis — cellule n°09, Espace commercial Marques Avenue, rue du Bocage, 49280 La Séguinière"),
        ("Exploitant", BLANK),
        ("Activité", "Restauration rapide : vente à emporter de produits frais préparés par le laboratoire de l'exploitant, cuisson minute de quelques produits chauds, consommation sur place, vente de produits d'épicerie préemballés."),
        ("Situation", "Cellule en rez-de-chaussée d'un bâtiment de l'espace commercial, ouverte sur l'allée piétonne par sa façade vitrée (sous auvent) et sur le couloir de service par deux portes à l'arrière. Cellules voisines mitoyennes de part et d'autre."),
        ("Surface", "≈ 178 m² intérieurs, dont ≈ 81 m² accessibles au public, + terrasse sous auvent."),
        ("Nature des travaux", "Aménagement intérieur sans modification de la structure, de la façade ni des parois coupe-feu (détail en pièce 10)."),
    ])
    y = h2(c, 50, y - 4, "2. Classement et effectif")
    y = table(c, 50, y, [("Zone", 255), ("Surface", 60), ("Densité", 120), ("Effectif", 60)],
              [r if i != 3 else r + ("B",) for i, r in enumerate(EFFECTIF)], 8)
    y = para(c, 50, y - 8, 495,
        "Densités de l'article N 2 pour la restauration assise ; pour la zone de vente, une densité majorante d'une personne par m² est retenue. L'effectif de 99 personnes est inférieur au seuil de la 5e catégorie : l'établissement relève des dispositions particulières aux petits établissements (articles PE). Le précédent aménagement comptait 53 places assises : l'effectif diminue.", 8.4)
    y = h2(c, 50, y - 6, "3. Isolement et construction (PE 5 à PE 8)")
    y = para(c, 50, y, 495,
        "• Structure, couverture et façade existantes, non modifiées.\n"
        "• Murs mitoyens avec les cellules voisines : coupe-feu 1 h existants, conservés sans percement.\n"
        "• Réserve existante à parois et bloc-porte coupe-feu, conservée ; local TGBT existant conservé.\n"
        "• Les deux ouvertures créées concernent des cloisons légères intérieures sans rôle d'isolement (fond de l'ancienne niche de vitrine, passe entre salle et plonge).", 8.4)
    a4_foot(c, "04", 1); c.showPage()

    a4(c); y = a4_head(c, "04", "Notice descriptive de sécurité incendie (suite)")
    y = h2(c, 50, y, "4. Dégagements (PE 11)")
    y = para(c, 50, y, 495,
        "• Sortie principale : porte vitrée à 2 vantaux de 2,40 m (4 unités de passage) donnant directement sur l'allée extérieure, ouvrant vers l'extérieur.\n"
        "• Issue arrière P2 : porte de 1,00 m (1 unité de passage) donnant sur le couloir de service, accessible depuis la zone de vente par la zone de service et le laboratoire.\n"
        "• Porte arrière P1 (1,00 m) : entrée du personnel et des livraisons, utilisable en évacuation par le personnel.\n"
        "• Circulations de la zone publique d'au moins 1,20 m (1,40 m à 2,15 m sur les allées principales) ; aucun obstacle sur le cheminement vers la sortie.\n"
        "Pour un effectif de 99 personnes, les dégagements existants (4 UP en façade + 1 UP à l'arrière) sont supérieurs au nombre et à la largeur requis. Distance maximale à parcourir pour rejoindre une sortie : environ 10 m depuis le point le plus éloigné de la salle.", 8.4)
    y = h2(c, 50, y - 4, "5. Aménagements intérieurs, décoration, mobilier (PE 13)")
    y = table(c, 50, y, [("Élément", 175), ("Matériau", 210), ("Réaction au feu", 110)], [
        ("Plafonds", "Existants (plafond plâtre en salle, dalles métalliques en laboratoire)", "Existant, M1 / A2-s1,d0"),
        ("Revêtements muraux", "Existants (peinture, panneaux lisses) + crédence inox en cuisson", "M2 minimum / inox A1"),
        ("Sols", "Existants (carrelage)", "M4 / existant"),
        ("Habillages bois (lattes du comptoir, de l'arbre, des banquettes)", "Panneaux et lattes ignifugés", "M1 ou B-s3,d0 (PV à fournir)"),
        ("Décor végétal de l'arbre central", "Végétal stabilisé ou artificiel", "M1 (PV à fournir)"),
        ("Mobilier (tables, chaises, banquettes, comptoir)", "Bois, métal, tissu", "Non réglementé (rembourrage M3 souhaité)"),
    ], 7.8)
    y = h2(c, 50, y - 10, "6. Désenfumage")
    y = para(c, 50, y, 495, "Sans objet : locaux en rez-de-chaussée de moins de 300 m², largement vitrés en façade. Aucune modification par rapport à l'existant.", 8.4)
    y = h2(c, 50, y - 4, "7. Chauffage, ventilation, conditionnement d'air")
    y = para(c, 50, y, 495, "Installations existantes conservées, avec leur commande d'arrêt d'urgence. Extraction de la cuisson : hotte raccordée au conduit existant (classé M0 / A2-s1,d0, stable au feu ¼ h) et à l'extracteur de toiture existant (400 °C ½ h) ; ramonage et contrôle avant mise en service, puis au moins une fois par an.", 8.4)
    y = h2(c, 50, y - 4, "8. Appareils de cuisson (PE 15 / GC)")
    y = para(c, 50, y, 495,
        "Appareils électriques uniquement, aucun gaz : four mixte (≈ 10 kW) et friteuse (≈ 9 kW), soit une puissance utile totale d'environ 19 kW, inférieure à 20 kW : la cuisine n'est pas une « grande cuisine » au sens de l'article GC 3. Les appareils sont installés à l'emplacement de l'ancien four de cuisson, sous l'extraction existante. L'écran de cantonnement existant est conservé. Coupure d'urgence de l'alimentation électrique des appareils (existante) placée hors de la zone de cuisson.", 8.4)
    a4_foot(c, "04", 2); c.showPage()

    a4(c); y = a4_head(c, "04", "Notice descriptive de sécurité incendie (suite)")
    y = h2(c, 50, y, "9. Installations électriques et éclairage de sécurité")
    y = para(c, 50, y, 495,
        "• Installation existante conforme à la norme NF C 15-100, adaptée aux nouveaux équipements ; vérification par un technicien compétent avant ouverture.\n"
        "• Éclairage de sécurité d'évacuation par blocs autonomes (BAES) au-dessus des sorties et sur le cheminement (repérés sur le plan, pièce 06).\n"
        "• Coupure d'urgence de l'enseigne lumineuse conservée.", 8.4)
    y = h2(c, 50, y - 4, "10. Moyens de secours (PE 26 et PE 27)")
    y = para(c, 50, y, 495,
        "• Extincteurs : 3 extincteurs à eau pulvérisée 6 L (salle, zone de service, couloir arrière), 2 extincteurs CO₂ 2 kg (près du tableau électrique et du laboratoire), 1 extincteur classe F + couverture anti-feu près de la friteuse.\n"
        "• Alarme : équipement d'alarme de type 4 (ou équipement existant conservé), audible dans tout l'établissement.\n"
        "• Consignes de sécurité et plan d'évacuation affichés ; téléphone permettant d'appeler les secours (18 / 112).\n"
        "• Personnel informé du maniement des extincteurs et des consignes.", 8.4)
    y = h2(c, 50, y - 4, "11. Stockage")
    y = para(c, 50, y, 495, "Stocks limités au besoin courant : emballages et épicerie en réserve coupe-feu existante ; produits froids en chambre froide et armoires réfrigérées ; aucun stockage de produits inflammables hormis les produits d'entretien courants, rangés dans une armoire fermée.", 8.4)
    y = h2(c, 50, y - 4, "12. Vérifications techniques et registre (PE 4)")
    y = para(c, 50, y, 495, "Vérifications par un technicien compétent : installations électriques, éclairage de sécurité, extincteurs, alarme, hotte et conduit d'extraction. Registre de sécurité tenu à jour et présenté à toute visite.", 8.4)
    y -= 16
    c.setFont("F", 9); c.setFillColor(INK)
    c.drawString(50, y, "Fait à …………………………, le ………………………"); c.drawString(320, y, "Signature de l'exploitant :")
    a4_foot(c, "04", 3)

def notice_access(c):
    a4(c); y = a4_head(c, "08", "Notice d'accessibilité aux personnes handicapées", "ERP situé dans un cadre bâti existant — arrêté du 8 décembre 2014")
    y = para(c, 50, y, 495, "L'établissement est situé en rez-de-chaussée, de plain-pied avec l'allée piétonne de l'espace commercial. Les travaux portent sur l'aménagement intérieur. Aucune dérogation n'est demandée.", 8.6)
    rows = [
     ("Cheminement extérieur", "Depuis l'allée piétonne du centre : sol dur et non glissant, sans ressaut, sous auvent. Places de stationnement adaptées : celles du parc de stationnement de l'espace commercial (gestion par le centre).", "Existant, conservé"),
     ("Entrée", "Porte vitrée à 2 vantaux de 1,20 m chacun (passage utile > 0,90 m sur un seul vantail), ressaut ≤ 2 cm, poignées contrastées, effort d'ouverture ≤ 50 N, espaces de manœuvre devant et derrière la porte. Vitrage repéré par deux bandes contrastées à 1,10 m et 1,60 m.", "Existant + bandes"),
     ("Accueil / caisse", "Comptoir visible depuis l'entrée ; une caisse équipée d'une tablette à 0,80 m maximum, vide en dessous de 0,70 m de haut, 0,60 m de large et 0,30 m de profondeur ; terminal de paiement et écran client entre 0,90 et 1,30 m. Menu imprimé en gros caractères disponible à la caisse.", "Créé"),
     ("Circulations intérieures", "Largeur ≥ 1,20 m sur tout le cheminement public (1,40 m entre îlot et comptoir, 1,65 m entre comptoir et frigos, 2,15 m devant les frigos) ; sol carrelé non glissant, sans ressaut ; aires de rotation de Ø 1,50 m devant la caisse, les frigos et les tables adaptées.", "Conforme"),
     ("Libre-service", "Frigos à portes vitrées : pour chaque famille de produits, une partie de l'offre est placée entre 0,40 et 1,30 m. Îlot central : tablettes basses accessibles.", "Créé"),
     ("Places assises", "2 places adaptées (une en salle, une dans l'alcôve) : table à 0,80 m maximum, vide en dessous de 0,70 m × 0,60 m × 0,30 m, chaise amovible, accès par une circulation de 1,20 m minimum.", "Créé"),
     ("Sanitaires", "Pas de sanitaires ouverts au public dans l'établissement (comme précédemment). Le public dispose des sanitaires publics de l'espace commercial, dont un sanitaire adapté.", "Accord du centre joint"),
     ("Éclairage", "≥ 200 lux sur le cheminement intérieur, ≥ 300 lux à la caisse ; pas d'éblouissement ni de zones d'ombre.", "Conforme"),
     ("Signalétique", "Informations lisibles et contrastées (familles de produits, caisse, sortie) ; écrans menus doublés d'un menu imprimé.", "Créé"),
     ("Registre public", "Registre public d'accessibilité tenu à disposition à l'accueil dès l'ouverture.", "À l'ouverture"),
    ]
    yy = table(c, 50, y - 8, [("Point", 95), ("Dispositions", 310), ("Statut", 90)], rows, 7.9)
    c.setFont("F", 9); c.setFillColor(INK)
    c.drawString(50, yy - 30, "Fait à …………………………, le ………………………"); c.drawString(320, yy - 30, "Signature de l'exploitant :")
    a4_foot(c, "08", 1)

def notice_travaux(c):
    a4(c); y = a4_head(c, "10", "Notice descriptive des travaux et des matériaux")
    y = para(c, 50, y, 495, "Les travaux se limitent à l'aménagement intérieur de la cellule. La structure, la façade, la couverture, les murs mitoyens coupe-feu, la réserve coupe-feu, les sanitaires du personnel, l'extraction de la cuisson et la chambre froide sont conservés.", 8.6)
    rows = [
     ("Dépose", "Mobilier et comptoirs de l'ancien exploitant, four de cuisson et armoire de pousse, vitrine boissons encastrée dans sa niche.", "—"),
     ("Cloisons (légères, non porteuses)", "Ouverture du fond de l'ancienne niche de vitrine (≈ 1 m, cloison légère) avec pose d'un bloc-porte va-et-vient. Passe de ≈ 0,80 × 0,60 m entre la salle et la plonge, avec encadrement inox. Aucune autre modification.", "Plaque de plâtre existante, A2-s1,d0"),
     ("Plomberie", "Deux lave-mains (comptoir et cuisson) ; raccordement du four mixte et d'un lave-vaisselle sur les réseaux existants.", "—"),
     ("Électricité", "Adaptation des circuits aux nouveaux équipements (ligne existante de l'ancien four réutilisée), repositionnement de blocs d'éclairage de sécurité, éclairage décoratif LED.", "NF C 15-100"),
     ("Ventilation / extraction", "Conservation de la hotte (ou remplacement à l'identique), du conduit et de l'extracteur existants ; filtres à chocs ; ramonage.", "Conduit M0 / A2-s1,d0 existant"),
     ("Revêtements", "Crédence inox derrière les appareils de cuisson ; reprises ponctuelles de joints et de plinthes ; peinture lessivable en salle.", "Inox A1 ; peinture M1"),
     ("Agencement", "Comptoir caisse, îlot central de présentation (« arbre » décoratif en lattes de bois et végétal stabilisé), banquettes, tables, chaises, mange-debout, desserte.", "Bois ignifugé M1 / B-s3,d0 ; végétal M1"),
     ("Froid et cuisson", "Frigos libre-service à portes vitrées (groupe intégré), armoires réfrigérées, four mixte et friteuse électriques (≈ 19 kW au total), plan réfrigéré.", "Matériel posé"),
     ("Enseigne", "Remplacement des faces et des lettres sur le caisson d'enseigne existant (11,50 × 1,48 m) ; vitrophanie partielle.", "Voir pièce 11"),
    ]
    yy = table(c, 50, y - 8, [("Lot", 95), ("Travaux", 290), ("Matériaux / classement", 110)], rows, 7.9)
    para(c, 50, yy - 18, 495, "Les procès-verbaux de réaction au feu des habillages et éléments décoratifs seront tenus à la disposition de la commission de sécurité.", 8.2, col=GRY)
    a4_foot(c, "10", 1)

def p_photos(c):
    a4(c); y = a4_head(c, "12", "Photographies de l'état actuel", "À prendre au moment du dépôt et à coller dans les cadres (ou à imprimer à la place de cette page)")
    labels = ["Photo 1 — Façade de la cellule, vue rapprochée depuis l'allée", "Photo 2 — Façade dans son environnement (vue lointaine)",
              "Photo 3 — Intérieur : salle depuis l'entrée", "Photo 4 — Intérieur : zone de cuisson et extraction existantes",
              "Photo 5 — Niche de l'ancienne vitrine boissons (ouverture prévue)", "Photo 6 — Cloison salle / plonge (passe prévue)"]
    w, h = 240, 175
    for i, l in enumerate(labels):
        x = 50 + (i % 2) * 255; yy = y - 10 - (i // 2) * 215
        c.setStrokeColor(GRY); c.setDash(4, 3); c.rect(x, yy - h, w, h); c.setDash()
        c.setFillColor(GRY); c.setFont("F", 7.8); c.drawString(x, yy - h - 12, l)
    a4_foot(c, "12", 1)

def p_bailleur(c):
    a4(c); y = a4_head(c, "13", "Accord du bailleur / de la direction de l'espace commercial")
    y = para(c, 50, y, 495, "Joindre ici le courrier ou l'extrait du bail par lequel le propriétaire de la cellule et la direction de l'espace commercial Marques Avenue autorisent :", 8.8)
    y = para(c, 50, y - 4, 495,
        "• l'exploitation d'une activité de restauration rapide dans la cellule n°09 ;\n"
        "• les travaux d'aménagement intérieur décrits en pièce 10 ;\n"
        "• le changement des faces de l'enseigne (pièce 11) ;\n"
        "• l'utilisation, par la clientèle de l'établissement, des sanitaires publics de l'espace commercial (dont un sanitaire adapté) ;\n"
        "• le cas échéant, l'exploitation d'une terrasse sous l'auvent devant la cellule.", 8.8)
    c.setStrokeColor(GRY); c.setDash(4, 3); c.rect(50, 120, 495, y - 140); c.setDash()
    c.setFillColor(GRY); c.setFont("F", 9); c.drawCentredString(A4W / 2, (y + 120) / 2 - 10, "Document à joindre")
    a4_foot(c, "13", 1)

# ----------------------------------------------------------------------------------------------- plans A3
EXIST_ZONES = [(0, 0, 655, 1150, HexColor("#f7f7f5")), (655, 0, 983, 427, HexColor("#f7f7f5")), (655, 427, 1545, 1150, HexColor("#f1f2f3")),
               (983, 0, 1545, 427, HexColor("#f1f2f3"))]

def plan_existant(c):
    a3(c)
    saved = bd.ZONES; bd.ZONES = EXIST_ZONES
    bd.draw_shell(c, terrace_text=False)
    bd.ZONES = saved
    # remettre l'existant : cloison de fond de niche et cloison pleine salle / plonge
    rect(c, 977, 90, 989, 170, fill=bd.WALL, stroke=None)
    rect(c, 747, 738, 832, 834, fill=HexColor("#f1f2f3"), stroke=None)
    rect(c, 735, 733, 747, 837, fill=bd.WALL, stroke=None)
    rect(c, 662, 742, 735, 828, fill=None, stroke=GRY, lw=0.6)
    labels = [(300, 600, "VENTE / FILE D'ATTENTE"), (420, 200, "SALLE DE RESTAURATION\n(53 places assises)"), (820, 200, "SALLE (suite)"),
              (820, 580, "PRÉPARATION\nFROIDE"), (698, 785, "niche\nvitrine\nboissons"), (870, 785, "POUSSE"), (760, 960, "CUISSON\n(four de cuisson)"),
              (975, 960, "PLAQUAGE"), (1072, 110, "PLONGE"), (1075, 450, "DEGT N°1"), (1277, 572, "RÉSERVE\n(coupe-feu)"),
              (1215, 990, "CHAMBRE\nFROIDE\nNÉGATIVE"), (1277, 55, "BUREAU"), (1220, 192, "VEST. H"), (1337, 192, "WC"), (1220, 360, "VEST. F"),
              (1337, 360, "WC"), (1470, 450, "DEGT N°2"), (1470, 1110, "TGBT"), (-170, 575, "TERRASSE SOUS AUVENT")]
    for x, y, s in labels: txt(c, x, y, s, 6.4 if len(s) < 30 else 6, "FB", INK, rot=90 if x < 0 or s in ("DEGT N°1", "DEGT N°2") else 0)
    # légende des éléments supprimés
    for (x1, y1, x2, y2) in [(160, 860, 650, 970), (700, 1053, 842, 1145), (755, 749, 875, 815)]:
        rect(c, x1, y1, x2, y2, fill=None, stroke=RED, lw=0.8, dash=(3, 2))
    txt(c, 405, 915, "comptoir et vitrines de l'ancien exploitant (déposés)", 5.5, "FI", RED)
    for (x1, y1, x2, y2) in [(977, 90, 989, 170), (735, 742, 747, 830)]:
        rect(c, x1 - 6, y1, x2 + 6, y2, fill=None, stroke=bd.MAG, lw=1.2)
    bd.dims(c); scale_bar(c, 150, 120)
    c.setFont("FB", 12); c.setFillColor(INK); c.drawString(40, A3H - 40, "Plan de l'état existant (avant travaux) — rez-de-chaussée")
    X = 905; y = A3H - 80
    para(c, X, y, 270,
         "**Lecture du plan\nAménagement réalisé par le précédent exploitant (autorisation de 2015), tel qu'il existe aujourd'hui.\n\n"
         "**Éléments déposés (tireté rouge)\nComptoir et vitrines de vente, four de cuisson, armoire de pousse, vitrine boissons de la niche.\n\n"
         "**Cloisons concernées par les travaux (cadre magenta)\n1. Fond de la niche de la vitrine boissons : ouverture d'environ 1 m (cloison légère).\n2. Cloison entre la salle et la plonge : passe de 0,80 × 0,60 m (cloison légère).\n\n"
         "**Tout le reste est conservé\nMurs, façade, cloisons, portes, réserve et local TGBT coupe-feu, chambre froide, sanitaires et vestiaires du personnel, extraction de la cuisson.\n\n"
         "**Hauteurs sous plafond\nSalle 2,80 m ; laboratoire 2,80 m ; chambre froide 2,40 m (plancher à +0,14).", 8)
    cart_a3(c, "05", "PLAN DE L'ÉTAT EXISTANT", "1/75")

ROOMS_PROJ = [(300, 640, "VENTE / LIBRE-SERVICE"), (300, 160, "SALLE"), (820, 395, "ALCÔVE"), (600, 700, "ZONE\nSERVICE"),
              (820, 560, "PRÉPA\nFROIDE\n10,0 m²"), (790, 930, "CUISSON\n12,6 m²"), (1072, 120, "PLONGE"), (1215, 990, "CHAMBRE\nNÉGATIVE\n10,0 m²"),
              (1277, 572, "RÉSERVE\nCF 6,0 m²"), (1277, 250, "VESTIAIRES\nWC\n10,5 m²"), (1470, 960, "DÉCHETS")]

def plan_securite(c):
    a3(c)
    bd.draw_shell(c, cf=True, terrace_text=False); bd.draw_equipment(c, labels=False)
    for x, y, s in ROOMS_PROJ: txt(c, x, y, s, 6, "FB", INK)
    txt(c, 300, 690, "public : 81,4 m²", 5.5, "FI", INK)
    rect(c, 650, 830, 1063, 1150, fill=None, stroke=RED, lw=1.0, dash=(6, 3))
    txt(c, 860, 1178, "écran de cantonnement existant conservé", 5, "FB", RED)
    arrow_path(c, [(770, 1090), (900, 900), (1250, 720), (1500, 330), (bd.DEPTH, 300)], RED, lw=1, dash=(3, 2), head=False)
    txt(c, 1230, 765, "conduit d'extraction existant M0 / A2-s1,d0 – SF ¼ h", 4.6, "FI", RED)
    arrow_path(c, [(250, 575), (-90, 575)], GG, lw=3)
    arrow_path(c, [(1470, 690), (bd.DEPTH + 75, 690)], GG, lw=3)
    arrow_path(c, [(1470, 65), (bd.DEPTH + 75, 65)], GG, lw=2)
    txt(c, -60, 470, "SORTIE PRINCIPALE\n4 UP — 2,40 m", 5.8, "FB", GG, rot=90)
    txt(c, bd.DEPTH + 120, 760, "P2 — 1 UP\n1,00 m", 5.5, "FB", GG, "l")
    txt(c, bd.DEPTH + 120, 130, "P1 — 1,00 m\n(personnel)", 5.5, "FB", GG, "l")
    for (x, y) in [(15, 420), (15, 730), (1530, 640), (1530, 120), (1100, 500), (800, 400), (600, 1100)]:
        X, Y = P(x, y); c.setFillColor(GG); c.rect(X - 6, Y - 3, 12, 6, fill=1, stroke=0)
    for (x, y, k) in [(60, 700, "E"), (630, 560, "E"), (870, 1030, "F"), (1000, 790, "C"), (1480, 1100, "C"), (1500, 450, "E")]:
        X, Y = P(x, y); c.setFillColor(RED); c.circle(X, Y, 6, fill=1, stroke=0); c.setFillColor(white); c.setFont("FB", 6); c.drawCentredString(X, Y - 2, k)
    X, Y = P(620, 1040); c.setFillColor(RED); c.rect(X - 7, Y - 7, 14, 14, fill=1, stroke=0)
    X, Y = P(20, 470); c.setFillColor(bd.ORANGE); c.rect(X - 5, Y - 5, 10, 10, fill=1, stroke=0)
    bd.dims(c); scale_bar(c, 150, 120)
    c.setFont("FB", 12); c.setFillColor(INK); c.drawString(40, A3H - 40, "Plan de l'état projeté — sécurité incendie — rez-de-chaussée")
    X = 905; y = A3H - 75
    y = bd.legend_box(c, X, y, [("line", RED, "Parois coupe-feu existantes (mitoyens CF 1 h, réserve, TGBT)"),
                                ("dash", RED, "Écran de cantonnement / conduit d'extraction existants"),
                                ("line", GG, "Sens d'évacuation"), ("box", GG, "Bloc autonome d'éclairage de sécurité"),
                                ("dot", RED, "Extincteurs : E eau 6 L · C CO₂ 2 kg · F classe F"),
                                ("box", RED, "Coupure d'urgence cuisson / électricité / ventilation"),
                                ("box", bd.ORANGE, "Coupure d'urgence de l'enseigne")], "Légende")
    y -= 6
    c.setFont("FB", 8.5); c.setFillColor(INK); c.drawString(X, y, "Effectif du public"); y -= 6
    y = table(c, X, y, [("Zone", 190), ("Effectif", 70)], [("Restauration assise (34,2 m², 1/m²)", "35"), ("Vente / attente (47,2 m², 1/m²)", "48"),
                                                            ("Terrasse (places déclarées)", "16"), ("Total public — 5e catégorie", "99", "B")], 7.4)
    para(c, X, y - 12, 270, "Établissement de type N avec activité M, 5e catégorie, sans locaux à sommeil. Cuisson électrique ≈ 19 kW (< 20 kW). Aucune modification des parois coupe-feu ni des dégagements.", 7.6)
    cart_a3(c, "06", "ÉTAT PROJETÉ — SÉCURITÉ INCENDIE", "1/75")

def plan_access(c):
    a3(c)
    bd.draw_shell(c, terrace_text=False); bd.draw_equipment(c, labels=False)
    for x, y, s in ROOMS_PROJ[:4]: txt(c, x, y, s, 6, "FB", INK)
    G = GG
    for (cx, cy) in [(400, 530), (420, 985), (330, 410), (860, 415)]:
        circle(c, cx, cy, 75, fill=None, stroke=G, lw=1)
    txt(c, 400, 612, "Ø 1,50", 5, "FB", G)
    cote(c, 330, 760, 470, 760, "1,40", col=G)
    cote(c, 220, 850, 220, 1065, "2,15", col=G)
    cote(c, 507, 900, 507, 1065, "1,65", col=G)
    cote(c, 90, 430, 90, 620, "1,90", col=G)
    cote(c, 0, 455, 0, 695, "", col=G)
    txt(c, -40, 575, "porte 2 × 1,20 m\nressaut ≤ 2 cm", 5.5, "FB", G, rot=90)
    arrow_path(c, [(-110, 575), (60, 575), (60, 960), (420, 1000)], G, lw=1.6)
    arrow_path(c, [(60, 575), (380, 560), (465, 515)], G, lw=1.6)
    arrow_path(c, [(380, 560), (560, 470), (620, 300), (830, 330)], G, lw=1.2, dash=(4, 2))
    for (x, y, s) in [(507, 515, "caisse adaptée"), (415, 345, "place adaptée"), (830, 345, "place adaptée")]:
        badge(c, x, y, "♿", BLUE, 7); txt(c, x, y + 30, s, 5.2, "FB", BLUE)
    bd.dims(c); scale_bar(c, 150, 120)
    c.setFont("FB", 12); c.setFillColor(INK); c.drawString(40, A3H - 40, "Plan de l'état projeté — accessibilité — rez-de-chaussée (coté)")
    X0, Y0 = 905, A3H - 85
    c.setFont("FB", 9); c.setFillColor(INK); c.drawString(X0, Y0, "Détail de la caisse adaptée")
    k = 1.25; bx, by = X0 + 90, Y0 - 150
    c.setStrokeColor(black); c.setLineWidth(0.8); c.line(bx - 60, by, bx + 160, by)
    c.setFillColor(bd.WOOD); c.rect(bx + 30 * k, by, 75 * k, 95 * k, fill=1, stroke=1)
    c.setFillColor(white); c.rect(bx, by + 70 * k, 30 * k, 10 * k, fill=1, stroke=1)
    c.setDash(2, 2); c.line(bx, by + 70 * k, bx, by); c.setDash()
    c.setFont("F", 6); c.setFillColor(black)
    c.drawString(bx + 105 * k + 6, by + 92 * k, "comptoir h 0,95"); c.drawRightString(bx - 4, by + 77 * k, "tablette h 0,80 max")
    c.drawRightString(bx - 4, by + 35 * k, "vide h 0,70 mini"); c.drawString(bx, by + 84 * k, "prof. 0,30 · larg. 0,60")
    c.drawString(X0, by - 12, "Terminal de paiement et écran client entre 0,90 et 1,30 m")
    para(c, X0, by - 34, 270,
         "**Légende\n"
         "• Trait vert : cheminement accessible depuis l'entrée vers les frigos, la caisse et les places adaptées.\n"
         "• Cercles : aires de rotation de Ø 1,50 m.\n"
         "• Cotes en mètres : largeurs de passage libres.\n"
         "• ♿ : caisse et places adaptées (table à 0,80 m max., vide 0,70 × 0,60 × 0,30 m).\n\n"
         "**Rappels\nEntrée de plain-pied existante (ressaut ≤ 2 cm), vitrage repéré par deux bandes contrastées à 1,10 m et 1,60 m. Pas de sanitaires ouverts au public dans l'établissement : sanitaires publics adaptés de l'espace commercial.", 7.6)
    cart_a3(c, "09", "ÉTAT PROJETÉ — ACCESSIBILITÉ", "1/75")

def coupe(c):
    a3(c)
    s = 28.3465 / 100.0  # 1/100 : pt par cm
    ox, oy = 120, 250
    def Q(x, z): return ox + (x + 1060) * s, oy + z * s
    def R(x1, z1, x2, z2, fill=None, stroke=INK, lw=0.6, dash=None):
        X1, Y1 = Q(x1, z1); X2, Y2 = Q(x2, z2); c.saveState(); c.setLineWidth(lw); c.setStrokeColor(stroke or INK)
        if dash: c.setDash(*dash)
        if fill is not None: c.setFillColor(fill)
        c.rect(min(X1, X2), min(Y1, Y2), abs(X2 - X1), abs(Y2 - Y1), fill=1 if fill is not None else 0, stroke=1 if stroke is not None else 0); c.restoreState()
    def L(x1, z1, x2, z2, col=INK, lw=0.6, dash=None):
        c.saveState(); c.setStrokeColor(col); c.setLineWidth(lw)
        if dash: c.setDash(*dash)
        X1, Y1 = Q(x1, z1); X2, Y2 = Q(x2, z2); c.line(X1, Y1, X2, Y2); c.restoreState()
    def T(x, z, t, size=7, font="F", col=INK, rot=0):
        X, Y = Q(x, z); c.saveState(); c.setFillColor(col); c.setFont(font, size); c.translate(X, Y); c.rotate(rot); c.drawCentredString(0, 0, t); c.restoreState()
    R(-1100, -40, 1600, 0, fill=HexColor("#d7d9dc"), stroke=None)                 # sol
    R(1545, 0, 1570, 1175, fill=HexColor("#555555"), stroke=None)                    # mur du fond
    L(-625, 1175, 1570, 1175, INK, 1.2); L(-625, 1150, 1570, 1150, INK, 0.6)        # couverture (faîtage)
    for x in (-625, 0): R(x - 10, 0, x + 10, 1150, fill=HexColor("#9a9fa6"), stroke=None)
    R(-4, 0, 4, 478, fill=HexColor("#bfe0f5"), stroke=BLUE)                          # façade vitrée
    R(-4, 478, 4, 626, fill=HexColor("#3b3f46"), stroke=None)                        # bandeau / enseigne
    L(0, 280, 1545, 280, INK, 1.0)                                                   # plafonds
    T(320, 295, "plafond existant — HSP 2,80 m", 6.5, "FI")
    T(1200, 295, "dalles métalliques existantes — HSP 2,80 m", 6.5, "FI")
    R(651, 0, 659, 280, fill=HexColor("#bfe0f5"), stroke=BLUE)                       # verrière prépa
    R(983 - 5, 0, 983 + 5, 280, fill=HexColor("#555555"), stroke=None)
    R(1160 - 5, 0, 1160 + 5, 280, fill=HexColor("#555555"), stroke=None); R(1395 - 5, 0, 1395 + 5, 280, fill=HexColor("#555555"), stroke=None)
    R(1058, 14, 1370, 240, fill=None, stroke=BLUE, lw=1.2); R(1058, 0, 1370, 14, fill=HexColor("#cfd3d6"), stroke=None)
    T(1214, 120, "chambre froide (existante) — HSP 2,40 m", 6.5, "FB", BLUE)
    T(1214, 4, "plancher +0,14", 5.5, "FI", BLUE)
    R(472, 0, 545, 100, fill=bd.WOOD, stroke=INK)
    T(508, 110, "comptoir", 6, "FI")
    R(110, 0, 330, 103, fill=bd.WOOD, stroke=INK); R(190, 103, 250, 280, fill=HexColor("#c9a777"), stroke=INK)
    T(220, 140, "îlot", 6, "FI", white)
    R(50, 0, 530, 205, fill=None, stroke=GRY, lw=0.4, dash=(2, 2)); T(290, 215, "frigos (en arrière-plan)", 6, "FI", GRY)
    T(-312, 560, "TERRASSE SOUS AUVENT (existante)", 7, "FB")
    T(320, 640, "SALLE / VENTE", 8, "FB"); T(820, 640, "PRÉPA", 8, "FB"); T(1070, 640, "LABO", 8, "FB"); T(1470, 640, "DEGT", 8, "FB")
    T(640, 1190, "couverture existante (bac acier) — faîtage +11,75", 7, "FI")
    for (z, lab) in [(0, "±0,00"), (280, "+2,80"), (478, "+4,78"), (1175, "+11,75")]:
        L(1600, z, 1650, z, INK, 0.6); T(1690, z - 3, lab, 7, "FB")
    c.setFont("FB", 12); c.setFillColor(INK); c.drawString(40, A3H - 40, "Coupe longitudinale AA (axe de la cellule) — état projeté")
    para(c, 40, A3H - 62, 1100, "Aucune modification des niveaux, des hauteurs, de la couverture ni de la façade. Seul le mobilier change. Coupe schématique à l'échelle 1/100, d'après la coupe de l'aménagement 2015.", 8.4)
    cart_a3(c, "07", "COUPE LONGITUDINALE AA", "1/100")

def facades(c):
    a3(c)
    s = 0.27  # pt par cm
    def elev(ox, oy, projete):
        def F(x, y): return ox + x * s, oy + y * s
        Wd = 1150; h_eg = 605; h_f = 1175
        c.saveState(); c.setFillColor(HexColor("#2b2f36")); p = c.beginPath()
        p.moveTo(*F(-40, h_eg)); p.lineTo(*F(Wd / 2, h_f)); p.lineTo(*F(Wd + 40, h_eg)); p.close(); c.drawPath(p, fill=1, stroke=0)
        c.setFillColor(HexColor("#c9ccd1"))
        for xx in (-40, Wd): X, Y = F(xx, 0); c.rect(X, Y, 40 * s, h_eg * s, fill=1, stroke=0)
        X, Y = F(0, 478); c.setFillColor(NAVY if projete else HexColor("#6f747c")); c.rect(X, Y, Wd * s, 148 * s, fill=1, stroke=0)
        if projete:
            c.setFillColor(white); bx, by = F(Wd / 2 - 75, 484); c.roundRect(bx, by, 150 * s, 136 * s, 3, fill=1, stroke=0)
            c.drawImage(bd.LOGO, bx + 2, by + 2, 150 * s - 4, 136 * s - 4, preserveAspectRatio=True, mask="auto")
            c.setFont("FB", 5.6); X, Y = F(30, 540); c.drawString(X, Y, "SUSHIS · BOWLS · BAOS")
            X, Y = F(Wd - 30, 540); c.drawRightString(X, Y, "FRAIS · RESPONSABLE")
        else:
            c.setFillColor(white); c.setFont("FI", 7); X, Y = F(Wd / 2, 545); c.drawCentredString(X, Y, "caisson d'enseigne existant (faces de l'ancien exploitant déposées)")
        c.setFillColor(HexColor("#cfe3ef")); X, Y = F(0, 0); c.rect(X, Y, Wd * s, 478 * s, fill=1, stroke=0)
        c.setStrokeColor(HexColor("#5a6b78")); c.setLineWidth(0.7)
        for xx in (Wd * .2, Wd * .4, Wd * .6, Wd * .8): c.line(*F(xx, 0), *F(xx, 478))
        c.setFillColor(HexColor("#b5d3e6")); X, Y = F(455, 0); c.rect(X, Y, 240 * s, 300 * s, fill=1, stroke=1)
        c.line(*F(575, 0), *F(575, 300))
        if projete:
            c.setStrokeColor(NAVY); c.setLineWidth(1.6)
            for hh in (110, 160): c.line(*F(0, hh), *F(Wd, hh))
        c.setFillColor(INK); c.setFont("F", 6.5)
        for (z, lab) in [(0, "±0,00"), (478, "+4,78"), (626, "+6,26"), (h_eg, ""), (h_f, "+11,75")]:
            if lab: X, Y = F(Wd + 60, z); c.drawString(X, Y - 2, lab)
        c.restoreState()
        X, Y = F(Wd / 2, -60); c.setFont("FB", 10); c.setFillColor(INK); c.drawCentredString(X, Y, "ÉTAT PROJETÉ" if projete else "ÉTAT ACTUEL")
    elev(80, 260, False); elev(560, 260, True)
    c.setFont("FB", 12); c.setFillColor(INK); c.drawString(40, A3H - 40, "Façade sur l'allée du village — état actuel / état projeté")
    para(c, 960, A3H - 80, 200,
         "**Modifications\n"
         "• Aucune modification de la façade, des menuiseries ni des volumes.\n"
         "• Enseigne : nouvelles faces et lettres sur le caisson existant (11,50 × 1,48 m) ; fond bleu marine, logo L'Arbre à Makis rétroéclairé au centre, lettres blanches de part et d'autre.\n"
         "• Vitrine : bandes contrastées à 1,10 m et 1,60 m (accessibilité), vitrophanie partielle, horaires sur la porte.\n"
         "• Coupure d'urgence de l'enseigne lumineuse conservée.\n\n"
         "**Enseigne\nSi la commune ou l'agglomération dispose d'un règlement local de publicité, cette pièce est aussi jointe à la demande d'autorisation d'enseigne (Cerfa 14798*01).", 7.8)
    cart_a3(c, "11", "FAÇADES — ÉTAT ACTUEL / PROJETÉ", "1/100 env.")

def main():
    c = canvas.Canvas(OUT, pagesize=A4)
    c.setTitle("Demande d'autorisation de travaux ERP — L'Arbre à Makis — Cellule 09 La Séguinière")
    c.setAuthor("L'Arbre à Makis")
    for f in (p_mode_emploi, p_garde, p_bordereau, p_courrier, p_cerfa, p_situation):
        f(c); c.showPage()
    notice_securite(c); c.showPage()
    for f in (plan_existant, plan_securite, coupe, notice_access, plan_access, notice_travaux, facades, p_photos, p_bailleur):
        f(c); c.showPage()
    c.save(); print("OK", OUT)

if __name__ == "__main__":
    main()
