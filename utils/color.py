from dto.svg_picture import SvgPicture
from tqdm import tqdm


def fix_init_colors(picture: SvgPicture):
    for p in picture.paths:
        for j in range(3):
            best_color = p.colors[0][j]
            best_loss = picture.culc_fitness_function()
            for i in tqdm(range(256)):
                p.colors[0][j] = i
                loss = picture.culc_fitness_function()
                if loss < best_loss:
                    best_loss = loss
                    best_color = i
            p.colors[0][j] = best_color
