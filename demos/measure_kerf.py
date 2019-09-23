import math
import os
import sys

sys.path.insert(1, os.path.realpath(os.path.pardir))
from svg_lib import SVG, Path

svg = SVG()
layer1 = svg.create_layer()
cuts = 20
increment = 15
offset = 10
height = 15
for i in range(cuts):
  points = [
    [offset + increment * i, offset],
    [0, height],
  ]
  svg.add_path(Path(layer1, points, False))

points_for_bottom = [
  [offset, offset],
  [increment * (cuts - 1), 0],
]
svg.add_path(Path(layer1, points_for_bottom, False))
points_for_top = [
  [offset, offset + height],
  [increment * (cuts - 1), 0],
]
svg.add_path(Path(layer1, points_for_top, False))

svg_string = svg.make_svg()
with open("./images/measure-kerf.svg", "w") as f:
  f.write(svg_string)
