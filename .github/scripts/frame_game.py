"""Coloca uma moldura (retângulo com contorno verde e cantos arredondados) no
GIF do space shooter, no mesmo estilo dos cards do README.

O GitHub não aceita CSS no README, então a borda precisa ser desenhada dentro
da própria imagem. Uso: python frame_game.py entrada.gif saida.gif
"""
import sys

import numpy as np
from PIL import Image, ImageDraw

BORDER = (0, 255, 102)      # #00FF66, o mesmo verde das bordas dos cards
CARD_BG = (6, 11, 8)        # #060B08, fundo dos cards
SOURCE_BG = (13, 17, 23)    # fundo original do GIF gerado pela action
BORDER_WIDTH = 0.75   # o GIF é exibido em escala maior que os cards; isso iguala a espessura visível
RADIUS = 13
PAD = 6                     # respiro entre a moldura e o jogo
SCALE = 4                   # supersampling para suavizar a borda


def build_masks(size):
    """Máscara do retângulo arredondado e do anel da borda, já suavizadas."""
    w, h = size
    big = (w * SCALE, h * SCALE)
    outer = Image.new("L", big, 0)
    ImageDraw.Draw(outer).rounded_rectangle(
        (0, 0, big[0] - 1, big[1] - 1), RADIUS * SCALE, fill=255)
    inner = Image.new("L", big, 0)
    inset = round(BORDER_WIDTH * SCALE)
    ImageDraw.Draw(inner).rounded_rectangle(
        (inset, inset, big[0] - 1 - inset, big[1] - 1 - inset),
        (RADIUS - BORDER_WIDTH) * SCALE, fill=255)
    outer = outer.resize(size, Image.LANCZOS)
    inner = inner.resize(size, Image.LANCZOS)
    return np.asarray(outer, dtype=np.float32) / 255, np.asarray(inner, dtype=np.float32) / 255


def main(src, dst):
    game = Image.open(src)
    gw, gh = game.size
    size = (gw + 2 * PAD, gh + 2 * PAD)
    outer, inner = build_masks(size)
    ring = (outer - inner)[..., None]
    border = np.array(BORDER, dtype=np.float32)

    frames, durations = [], []
    for i in range(game.n_frames):
        game.seek(i)
        durations.append(game.info.get("duration", 50))
        rgb = np.asarray(game.convert("RGB"))
        rgb = np.where((rgb == SOURCE_BG).all(axis=-1, keepdims=True), CARD_BG, rgb)
        canvas = np.empty((size[1], size[0], 3), dtype=np.uint8)
        canvas[:] = CARD_BG
        canvas[PAD:PAD + gh, PAD:PAD + gw] = rgb
        out = canvas.astype(np.float32) * (1 - ring) + border * ring
        # GIF só tem transparência de 1 bit: fora do retângulo fica transparente.
        alpha = np.where(outer > 0.5, 255, 0).astype(np.uint8)
        img = Image.fromarray(out.astype(np.uint8), "RGB").convert("P", palette=Image.ADAPTIVE, colors=255)
        mask = Image.fromarray(alpha == 0)
        img.paste(255, mask=mask)
        img.info["transparency"] = 255
        frames.append(img)

    frames[0].save(
        dst, save_all=True, append_images=frames[1:], duration=durations,
        loop=0, transparency=255, optimize=False)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
