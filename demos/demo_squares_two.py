import math
import os
import sys

sys.path.insert(1, os.path.realpath(os.path.pardir))
from svg_lib import SVG, Path

svg = SVG()
layer1 = svg.create_layer()
def make_points(x, y):
  return [
    [0 + x, 5 + y],
    [0, 15],
    [15, 0],
    [0, -15],
    [-15, 0],
    [5, 0],
    [0, -5],
    [0, 15],
    [15, 0],
    [0, -15],
    [-15, 0],
  ]
svg.add_path(Path(layer1, make_points(10, 10), False))
svg.add_path(Path(layer1, make_points(50, 10), False))
svg.add_path(Path(layer1, make_points(90, 10), False))

svg_string = svg.make_svg()
with open("./images/squares-two.svg", "w") as f:
  f.write(svg_string)
