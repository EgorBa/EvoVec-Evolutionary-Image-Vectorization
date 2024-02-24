import os.path

from PIL import Image
from cairosvg import svg2png

folder = "../my algo"

for image in os.listdir(folder):
    path = os.path.join(folder, image)
    png_path = f'my_algo_{image.split(".")[0]}.png'
    with open(path, 'r') as f:
        svg_str = f.read()
        svg2png(svg_str, write_to=str(png_path))
    im = Image.open(png_path)

    (w, h) = im.size
    ratio = float(w) / float(h)
    new_h = 256
    new_w = ratio * new_h

    im = im.resize((int(new_w), int(new_h)))
    im.save(png_path)

folder = "../init"

for image in os.listdir(folder):
    path = os.path.join(folder, image)
    png_path = f'init_{image.split(".")[0]}.png'
    im = Image.open(path)

    (w, h) = im.size
    ratio = float(w) / float(h)
    new_h = 256
    new_w = ratio * new_h

    im = im.resize((int(new_w), int(new_h)))
    im.save(png_path)