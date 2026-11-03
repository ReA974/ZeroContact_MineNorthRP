"""Aperçu hors jeu d'un modèle GeckoLib (.geo.json) texturé : rendu 3D simple (projection orthographique, tri des facettes).
Usage : python tools/minenorth/apercu_geo.py <sortie.png> <geo> <texture> [<geo> <texture> ...] [--angles 25,205] [--peau]
--peau : dessine une tête / un buste de joueur gris sous l'équipement (repère d'échelle)."""
import json
import math
import sys

from PIL import Image, ImageDraw

FACES = ('north', 'south', 'east', 'west', 'up', 'down')


def rot(p, r, c):
    """Rotation GeckoLib (x et y inversés), ordre Z puis Y puis X autour du pivot c."""
    x, y, z = p[0] - c[0], p[1] - c[1], p[2] - c[2]
    rx, ry, rz = math.radians(-r[0]), math.radians(-r[1]), math.radians(r[2])
    x, y, z = x, y * math.cos(rx) - z * math.sin(rx), y * math.sin(rx) + z * math.cos(rx)
    x, y, z = x * math.cos(ry) + z * math.sin(ry), y, -x * math.sin(ry) + z * math.cos(ry)
    x, y, z = x * math.cos(rz) - y * math.sin(rz), x * math.sin(rz) + y * math.cos(rz), z
    return (x + c[0], y + c[1], z + c[2])


def box_uv(u, v, w, h, d):
    return {'west': (u, v + d, d, h), 'north': (u + d, v + d, w, h), 'east': (u + d + w, v + d, d, h), 'south': (u + 2 * d + w, v + d, w, h),
            'up': (u + d, v, w, d), 'down': (u + d + w, v + d, w, -d)}


def face_quad(o, s, f):
    """Coins (haut-gauche, haut-droit, bas-droit, bas-gauche) de la face vue de l'extérieur, alignés sur l'UV."""
    x0, y0, z0 = o
    x1, y1, z1 = o[0] + s[0], o[1] + s[1], o[2] + s[2]
    return {'north': [(x1, y1, z0), (x0, y1, z0), (x0, y0, z0), (x1, y0, z0)],
            'south': [(x0, y1, z1), (x1, y1, z1), (x1, y0, z1), (x0, y0, z1)],
            'east': [(x0, y1, z0), (x0, y1, z1), (x0, y0, z1), (x0, y0, z0)],
            'west': [(x1, y1, z1), (x1, y1, z0), (x1, y0, z0), (x1, y0, z1)],
            'up': [(x1, y1, z1), (x0, y1, z1), (x0, y1, z0), (x1, y1, z0)],
            'down': [(x1, y0, z0), (x0, y0, z0), (x0, y0, z1), (x1, y0, z1)]}[f]


def quads(geo, tex):
    d = json.load(open(geo, encoding='utf-8'))['minecraft:geometry'][0]
    tw, th = d['description']['texture_width'], d['description']['texture_height']
    im = Image.open(tex).convert('RGBA')
    kx, ky = im.width / tw, im.height / th
    bones = {b['name']: b for b in d['bones']}

    def chain(b):
        out = []
        while b:
            out.append(b)
            b = bones.get(b.get('parent'))
        return out

    res = []
    for b in d['bones']:
        for c in b.get('cubes', []):
            inf = c.get('inflate', 0)
            o = [c['origin'][i] - inf for i in range(3)]
            s = [c['size'][i] + 2 * inf for i in range(3)]
            uvs = c['uv']
            if isinstance(uvs, list):
                uvs = {k: v for k, v in zip(FACES, [None] * 6)} | {k: {'uv': v[:2], 'uv_size': v[2:]} for k, v in
                                                                    box_uv(uvs[0], uvs[1], *[math.floor(x) for x in c['size']]).items()}
            for f in FACES:
                fu = uvs.get(f)
                if not fu:
                    continue
                pts = face_quad(o, s, f)
                if 'rotation' in c:
                    pts = [rot(p, c['rotation'], c.get('pivot', [0, 0, 0])) for p in pts]
                for bb in chain(b):
                    if 'rotation' in bb:
                        pts = [rot(p, bb['rotation'], bb.get('pivot', [0, 0, 0])) for p in pts]
                u, v = fu['uv']
                w, h = fu['uv_size']
                res.append((pts, (u * kx, v * ky, w * kx, h * ky), im))
    return res


def sample(im, u, v):
    x, y = int(min(max(u, 0), im.width - 1)), int(min(max(v, 0), im.height - 1))
    return im.getpixel((x, y))


def render(items, yaw, pitch=18, size=520, peau=False):
    polys = []
    if peau:
        skin = Image.new('RGBA', (1, 1), (150, 150, 156, 255))
        for (o, s) in (((-4, 24, -4), (8, 8, 8)), ((-4, 12, -2), (8, 12, 4)), ((-8, 12, -2), (4, 12, 4)), ((4, 12, -2), (4, 12, 4))):
            for f in FACES:
                polys.append((face_quad(o, s, f), (0, 0, 1, 1), skin))
    for g, t in items:
        polys += quads(g, t)
    cy, sy, cp, sp = math.cos(math.radians(yaw)), math.sin(math.radians(yaw)), math.cos(math.radians(pitch)), math.sin(math.radians(pitch))

    def view(p):
        x, y, z = p
        x, z = x * cy - z * sy, x * sy + z * cy
        y, z = y * cp + z * sp, -y * sp + z * cp
        return x, y, z

    tris = []
    allv = []
    for pts, (u, v, w, h), im in polys:
        vp = [view(p) for p in pts]
        a, b, c = vp[0], vp[1], vp[3]
        nx = (b[1] - a[1]) * (c[2] - a[2]) - (b[2] - a[2]) * (c[1] - a[1])
        ny = (b[2] - a[2]) * (c[0] - a[0]) - (b[0] - a[0]) * (c[2] - a[2])
        nz = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
        n = math.sqrt(nx * nx + ny * ny + nz * nz) or 1
        shade = .62 + .38 * max(0, (-nz * .55 + ny * .65 - nx * .3) / n)
        allv += vp
        lu = math.dist(pts[0], pts[1]) * 3
        lv = math.dist(pts[0], pts[3]) * 3
        nu = max(1, min(int(max(abs(w), lu)), 160))
        nv = max(1, min(int(max(abs(h), lv)), 160))
        for i in range(nu):
            for j in range(nv):
                def at(s_, t_):
                    top = [vp[0][k] + (vp[1][k] - vp[0][k]) * s_ for k in range(3)]
                    bot = [vp[3][k] + (vp[2][k] - vp[3][k]) * s_ for k in range(3)]
                    return [top[k] + (bot[k] - top[k]) * t_ for k in range(3)]
                q = [at(i / nu, j / nv), at((i + 1) / nu, j / nv), at((i + 1) / nu, (j + 1) / nv), at(i / nu, (j + 1) / nv)]
                col = sample(im, u + (i + .5) / nu * w, v + (j + .5) / nv * h)
                if col[3] < 20:
                    continue
                tris.append((sum(p[2] for p in q) / 4, q, tuple(int(col[k] * shade) for k in range(3)) + (255,)))
    if not allv:
        return Image.new('RGBA', (size, size))
    mnx, mxx = min(p[0] for p in allv), max(p[0] for p in allv)
    mny, mxy = min(p[1] for p in allv), max(p[1] for p in allv)
    k = size * .86 / max(mxx - mnx, mxy - mny)
    cx, cyy = (mnx + mxx) / 2, (mny + mxy) / 2
    out = Image.new('RGBA', (size, size), (34, 36, 46, 255))
    dr = ImageDraw.Draw(out)
    for _, q, col in sorted(tris, key=lambda t: -t[0]):
        dr.polygon([(size / 2 - (p[0] - cx) * k, size / 2 - (p[1] - cyy) * k) for p in q], fill=col, outline=col)
    return out


def main():
    args = sys.argv[1:]
    angles, peau = [25, 205], False
    if '--angles' in args:
        i = args.index('--angles'); angles = [float(a) for a in args[i + 1].split(',')]; del args[i:i + 2]
    if '--peau' in args:
        args.remove('--peau'); peau = True
    out, rest = args[0], args[1:]
    items = list(zip(rest[0::2], rest[1::2]))
    ims = [render(items, a, peau=peau) for a in angles]
    sheet = Image.new('RGBA', (sum(i.width for i in ims), ims[0].height))
    x = 0
    for i in ims:
        sheet.paste(i, (x, 0)); x += i.width
    sheet.save(out)


if __name__ == '__main__':
    main()
