"""Équipement Police Nationale par grade (grades du mod minenorth-police : Commissaire, Officier, Sous-officier).
Génère, à partir des textures PN existantes (brassard_pn, armorrig_jpc_2v_pn) et du casque Bastion :
  - brassards BAC (brassard orange porté en civil) : textures/models/armband/brassard_pn_<grade>.png (bande orange POLICE + écusson de grade) ;
  - gilets pare-balles : textures/models/armorrig/armorrig_jpc_2v_pn_<grade>.png (POLICE sur les poches avant et dans le dos, écusson de grade sur la poitrine) ;
  - casques balistiques : textures/models/helmet/helmet_pn_<grade>.png (Bastion repeint bleu nuit, POLICE à l'arrière, bandeau de grade) ;
  - modèles d'objet (rendu GeckoLib) et noms en français dans en_us.json ET fr_fr.json.
Écussons : créations originales simplifiées (chevrons / barrettes), pas d'insigne officiel.
Usage : python tools/minenorth/gen_police_pn.py   (depuis la racine du dépôt). Idempotent.
Les objets Java correspondants sont dans forge_registries/item (Armbands, Armors, Helmets)."""
import json
import os

from PIL import Image, ImageDraw

A = 'common/src/main/resources/assets/zerocontact/'
TEX = A + 'textures/models/'

NAVY = (14, 16, 44)
NAVY_HELMET = (24, 28, 62)
WHITE = (240, 240, 236)
SILVER, SILVER_D = (205, 210, 218), (128, 134, 146)
GOLD, GOLD_D = (226, 182, 72), (150, 112, 36)

# id, nom affiché, écusson
GRADES = [
    ('sous_officier', 'Sous-officier', 'chevrons'),
    ('officier', 'Officier', 'barrettes'),
    ('commissaire', 'Commissaire', 'barrettes_or'),
]

# police 5 x 7 pour le lettrage « POLICE »
FONT = {'P': ["XXXX.", "X...X", "X...X", "XXXX.", "X....", "X....", "X...."],
        'O': [".XXX.", "X...X", "X...X", "X...X", "X...X", "X...X", ".XXX."],
        'L': ["X....", "X....", "X....", "X....", "X....", "X....", "XXXXX"],
        'I': ["XXX", ".X.", ".X.", ".X.", ".X.", ".X.", "XXX"],
        'C': [".XXXX", "X....", "X....", "X....", "X....", "X....", ".XXXX"],
        'E': ["XXXXX", "X....", "X....", "XXXX.", "X....", "X....", "XXXXX"],
        'R': ["XXXX.", "X...X", "X...X", "XXXX.", "X.X..", "X..X.", "X...X"],
        'A': [".XXX.", "X...X", "X...X", "XXXXX", "X...X", "X...X", "X...X"],
        'D': ["XXXX.", "X...X", "X...X", "X...X", "X...X", "X...X", "XXXX."]}


def text_w(s, k):
    return sum(len(FONT[c][0]) * k + k for c in s) - k


def text(d, cx, y, s, k, col):
    """Lettrage centré sur cx, points de k pixels."""
    x = cx - text_w(s, k) // 2
    for c in s:
        for j, row in enumerate(FONT[c]):
            for i, ch in enumerate(row):
                if ch == 'X':
                    d.rectangle((x + i * k, y + j * k, x + (i + 1) * k - 1, y + (j + 1) * k - 1), fill=col)
        x += len(FONT[c][0]) * k + k


def insignia(d, cx, cy, w, h, kind):
    """Écusson de grade : pastille bleu nuit très arrondie, chevrons ou barrettes."""
    r = min(w, h) // 2
    d.rounded_rectangle((cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2), radius=r, fill=NAVY, outline=(60, 66, 110), width=max(1, h // 18))
    gold = kind == 'barrettes_or'
    c, cd = (GOLD, GOLD_D) if gold else (SILVER, SILVER_D)
    t = max(2, h // 7)                     # épaisseur d'un galon
    if kind == 'chevrons':
        for k in (0, 1):
            y = cy - h // 4 + k * (t + t // 2 + 1)
            half = w // 2 - r // 2 - 2
            d.line([(cx - half, y), (cx, y + h // 4), (cx + half, y)], fill=cd, width=t + 1, joint='curve')
            d.line([(cx - half, y - 1), (cx, y + h // 4 - 1), (cx + half, y - 1)], fill=c, width=t, joint='curve')
    else:
        n = 3 if gold else 2
        gap = t + max(2, t // 2)
        y0 = cy - (n * t + (n - 1) * (gap - t)) // 2
        half = w // 2 - r // 2 - 2
        for k in range(n):
            y = y0 + k * gap
            d.rounded_rectangle((cx - half, y, cx + half, y + t), radius=t // 2, fill=cd)
            d.rounded_rectangle((cx - half, y, cx + half, y + t - 1), radius=t // 2, fill=c)



def detoure(lg):
    """Logo PN sans son fond blanc : blanc -> transparent, lettrage noir -> blanc brodé (lisible sur le bleu nuit), bleu éclairci, rouge gardé."""
    import colorsys
    out = Image.new('RGBA', lg.size)
    for y in range(lg.height):
        for x in range(lg.width):
            r, g, b, a = lg.getpixel((x, y))
            hh, ll, ss = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
            if ss > .35 and .15 < ll < .9:                         # bleu / rouge du ruban tricolore
                if .5 < hh < .75:
                    r, g, b = [int(v * 255) for v in colorsys.hls_to_rgb(hh, max(ll, .55), ss)]
                out.putpixel((x, y), (r, g, b, a))
            else:                                                   # gris / noir = lettrage, blanc = fond
                k = 1 - ll
                if k > .12:
                    out.putpixel((x, y), (240, 240, 236, int(a * min(1, k * 1.6))))
    return out

# ---------------------------------------------------------------- brassards

ARMBAND_FACES = [(320, 320, 160, 122), (320, 448, 160, 122), (0, 480, 160, 122), (480, 0, 160, 122)]


def brassard(g, kind):
    im = Image.open(TEX + 'armband/brassard_pn.png').convert('RGBA')
    d = ImageDraw.Draw(im)
    for (x, y, w, h) in ARMBAND_FACES:
        insignia(d, x + w // 2, y + 93, 74, 34, kind)
    im.save(TEX + 'armband/brassard_pn_%s.png' % g)


# ---------------------------------------------------------------- gilets pare-balles (JPC PN, texture 2048 = 32 px par unité)

# Zones visibles une fois le gilet monté (vérifiées avec apercu_geo.py) : les sangles élastiques couvrent les poches à 21-38 % et 64-81 %
# de leur largeur, le bas du dos est caché de la même façon, le centre du haut de la poitrine (cube 48) est masqué.
POUCH_FRONT = (512, 320, 225, 118)      # face avant des porte-chargeurs (cube 8) : écusson dans la colonne du milieu
UPPER = (448, 576, 231, 107)            # bande au-dessus des poches (cube 51, moitié haute visible) : POLICE
BACK = (256, 192, 231, 170)             # dos (cube 46) : lettrage en haut, logo MineNorth dessous
RAID_BLACK = (24, 24, 27)


def noircit(im):
    """Tenue RAID : le bleu nuit du gilet passe en noir (le logo et les détails clairs ne bougent pas)."""
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a and b < 90 and r < 50 and g < 50:
                f = (r + g + b + 30) / 90
                px[x, y] = tuple(min(255, int(c * f)) for c in RAID_BLACK) + (a,)
    return im


def gilet(g, kind):
    im = Image.open(TEX + 'armorrig/armorrig_jpc_2v_pn.png').convert('RGBA')
    if kind == 'raid':
        im = noircit(im)
    d = ImageDraw.Draw(im)
    x, y, w, h = UPPER
    text(d, x + w // 2, y + 10, 'POLICE', 4, WHITE)
    x, y, w, h = POUCH_FRONT
    if kind == 'raid':
        text(d, x + 115, y + 46, 'RAID', 2, WHITE)
    else:
        insignia(d, x + 115, y + 58, 52, 34, kind)
    x, y, w, h = BACK
    text(d, x + w // 2, y + 3, 'RAID' if kind == 'raid' else 'POLICE', 4, WHITE)
    im.save(TEX + 'armorrig/armorrig_jpc_2v_pn_%s.png' % g)


# ---------------------------------------------------------------- casques balistiques (Bastion 64 px -> 1024 px, 16 px par texel)

# Faces 8 x 2 texels du bandeau du casque (cube 27 : n, e, s, w) et des plaques avant / latérales (cubes 26, 14, 25 : n et s).
BAND_FACES = [(24, 4), (24, 6), (8, 24), (24, 8), (24, 16), (24, 18), (24, 14), (16, 24)]
FRONT = (24, 10)      # plaque avant (cube 26, face extérieure) : écusson POLICE NATIONALE
NAPE = (8, 30)        # plaque de nuque (cube 1, face extérieure) : lettrage POLICE
K = 16


def casque(g, kind):
    src = Image.open(TEX + 'helmet/helmet_bastion_black.png').convert('RGBA')
    px = list(src.get_flattened_data()) if hasattr(src, 'get_flattened_data') else list(src.getdata())
    lum = [sum(p[:3]) / 3 for p in px if p[3]]
    avg = sum(lum) / len(lum)
    out = Image.new('RGBA', src.size)
    for i, p in enumerate(px):
        if p[3]:
            f = min(1.6, (sum(p[:3]) / 3) / avg)
            out.putpixel((i % src.width, i // src.width), tuple(min(255, int(c * f)) for c in (RAID_BLACK if kind == 'raid' else NAVY_HELMET)) + (p[3],))
    im = out.resize((64 * K, 64 * K), Image.NEAREST)
    deco = Image.new('RGBA', im.size)
    d = ImageDraw.Draw(deco)
    band, band_d = (GOLD, GOLD_D) if kind == 'barrettes_or' else (SILVER, SILVER_D)
    rows = [] if kind == 'raid' else [12] if kind == 'chevrons' else [7, 19]
    for (u, v) in BAND_FACES:                                    # bandeau(x) de grade tout autour
        x0, y0 = u * K, v * K
        for y in rows:
            d.rectangle((x0, y0 + y, x0 + 8 * K - 1, y0 + y + 6), fill=band_d)
            d.rectangle((x0, y0 + y, x0 + 8 * K - 1, y0 + y + 4), fill=band)
    text(d, NAPE[0] * K + 4 * K, NAPE[1] * K + 5, 'RAID' if kind == 'raid' else 'POLICE', 3, WHITE)
    lg = Image.open(TEX + 'armorrig/armorrig_jpc_2v_pn.png').convert('RGBA').crop((897, 192, 1005, 249))
    lg = detoure(lg).resize((56, 30), Image.LANCZOS)
    deco.alpha_composite(lg, (FRONT[0] * K + 36, FRONT[1] * K + 1))           # même écusson que le gilet PN
    mask = im.getchannel('A')                                    # rien sur les texels transparents de la coque
    im.paste(deco, (0, 0), Image.composite(deco.getchannel('A'), Image.new('L', im.size), mask))
    im.save(TEX + 'helmet/helmet_pn_%s.png' % g)


# ---------------------------------------------------------------- modèles d'objet et noms

def item_model(src, dst, tex):
    m = json.load(open(A + 'models/item/%s.json' % src, encoding='utf-8'))
    m['textures']['layer0'] = 'zerocontact:' + tex
    json.dump(m, open(A + 'models/item/%s.json' % dst, 'w', encoding='utf-8'), indent=2)


def main():
    names = {                    # le béret et le gilet « gs » gardent leur nom du pack (default_armor)
        'item.zerocontact.brassard_pn': 'Brassard Police Nationale',
        'item.zerocontact.uniform_pn_haut': 'Haut Police Nationale',
        'item.zerocontact.uniform_pn_bas': 'Pantalon Police Nationale',
    }
    for g, fr, kind in GRADES:
        brassard(g, kind)
        gilet(g, kind)
        casque(g, kind)
        item_model('brassard_pn', 'brassard_pn_' + g, 'models/armband/brassard_pn_' + g)
        item_model('armor_jpc_v2_pn_gs', 'armor_jpc_v2_pn_' + g, 'models/armorrig/armorrig_jpc_2v_pn_' + g)
        item_model('helmet_berret_pn', 'helmet_pn_' + g, 'models/helmet/helmet_pn_' + g)
        names['item.zerocontact.brassard_pn_' + g] = 'Brassard BAC - ' + fr
        names['item.zerocontact.armor_jpc_v2_pn_' + g] = 'Gilet pare-balles Police - ' + fr
        names['item.zerocontact.helmet_pn_' + g] = 'Casque balistique Police - ' + fr
    gilet('raid', 'raid')                # RAID : gilet et casque noirs, pas de brassard (unité d'intervention en tenue)
    casque('raid', 'raid')
    item_model('armor_jpc_v2_pn_gs', 'armor_jpc_v2_pn_raid', 'models/armorrig/armorrig_jpc_2v_pn_raid')
    item_model('helmet_berret_pn', 'helmet_pn_raid', 'models/helmet/helmet_pn_raid')
    names['item.zerocontact.armor_jpc_v2_pn_raid'] = 'Gilet pare-balles RAID'
    names['item.zerocontact.helmet_pn_raid'] = 'Casque balistique RAID'
    for lg in ('en_us', 'fr_fr'):
        p = A + 'lang/%s.json' % lg
        d = json.load(open(p, encoding='utf-8-sig')) if os.path.exists(p) else {}
        d.update(names)
        json.dump(d, open(p, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
    print('ok : %d grades' % len(GRADES))


if __name__ == '__main__':
    main()
