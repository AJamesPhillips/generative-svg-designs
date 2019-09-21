
from svg_lib import SVG, Path

svg = SVG()
layer1 = svg.create_layer()

for i in range(10):
  points = [
    [10 * i, 10 * i],
    [100, 0],
    [0, 100],
    [-100, 0],
  ]
  svg.add_path(Path(layer1, points, True))

svg_string = svg.make_svg()

with open("./demo-squares.svg", "w") as f:
  f.write(svg_string)
