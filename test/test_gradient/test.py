import os
from cairosvg import svg2png
import config
from vectorize_by_algo import get_initial_svg

filename = "gradient_2"
test_dir = os.path.join("test", "test_gradient")
path_tmp_svg = os.path.join(test_dir, f'{filename}.svg')
path_tmp_png = os.path.join(test_dir, f'{filename}.png')
with open(path_tmp_svg, 'r') as f:
    svg_str = f.read()
    svg2png(svg_str, write_to=str(path_tmp_png))
p = get_initial_svg(path_tmp_png)
# need add to config right mutation
mutation = config.MUTATION_TYPE[0]
for i in range(4):
    mutation.mutate(p, 0)
p.save_as_svg(os.path.join(test_dir, "gradient_updated.svg"))
