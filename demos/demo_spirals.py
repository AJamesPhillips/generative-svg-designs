import math
import os
import sys

sys.path.insert(1, os.path.realpath(os.path.pardir))
from svg_lib import SVG, Path, add_cart, pol2cart


def spiral(
  segments=100,
  interspiral_size=0.1,
  stop_radius_size=100,
  radius_function=None,
  angle_function=None,
  terminate_tail=False,
):
  svg = SVG()
  layer1 = svg.create_layer()

  origin = (100, 100)
  points = [
    origin,
  ]

  category_total = segments
  segment_increment = round(segments/10) * 2 # x2 ensures it's always even
  i = 0
  stop_next = False
  while True:
    if (i == category_total):
      if stop_next:
        if terminate_tail:
          points.append(points[i - segments])
        break
      segments += segment_increment
      category_total += segments

    angle = ((i - (category_total - segments)) / segments) * 2 * math.pi
    radius = i * interspiral_size

    final_angle = angle_function(i, angle, radius, category_total, segments) if angle_function else angle
    final_radius = radius_function(i, angle, radius, category_total, segments) if radius_function else radius

    if (final_radius > stop_radius_size):
      stop_next = True

    new_coord = pol2cart(final_radius, final_angle)
    new_coord = add_cart(origin, new_coord)
    points.append(new_coord)
    i += 1

  path = SVG.points_to_path(points)

  svg.add_path(Path(layer1, path, False))

  return svg


def spiral_flower():
  def radius_function(i, angle, radius, category_total, segments):
    return radius + 2 + (math.cos(angle * 6) * (max(100, i) / 30))

  return spiral(radius_function=radius_function)


def spiral_steps():
  def radius_function(i, angle, radius, category_total, segments):
    return radius + (0.8 * (i % 10))

  return spiral(radius_function=radius_function)


def spiral_sails():
  def sign(v):
    return -1 if v < 0 else 1

  def radius_function(i, angle, radius, category_total, segments):
    partial_i = i - (category_total - segments)
    i_progress = partial_i % (segments / 6)
    return radius + i_progress * 0.4

  def angle_function(i, angle, radius, category_total, segments):
    return angle - (math.cos(angle * 6) * 0.4)

  return spiral(radius_function=radius_function, angle_function=angle_function)


def spiral_whirlpool():
  def radius_function(i, angle, radius, category_total, segments):
    partial_i = i - (category_total - segments)
    seg6 = segments / 6
    i_progress = abs((partial_i % seg6) - (seg6 / 2))
    return radius + i_progress * 0.4

  def angle_function(i, angle, radius, category_total, segments):
    d60 = (math.pi * 2) / 6
    angle_progress = abs((angle % d60) - (d60 / 2))
    return angle - (angle_progress * 2)

  return spiral(radius_function=radius_function, angle_function=angle_function)

# def spiral_whirlpool_2():
#   def angle_function(i, angle, radius, category_total, segments):
#     a = math.cos(angle * 1 * 4) * 0.7
#     return angle + a

#   return spiral(angle_function=angle_function)


def spiral_loop_back():
  def radius_function(i, angle, radius, category_total, segments):
    a = 1 + (math.sin(angle * 11.7) * 0.2)
    return radius * a

  def angle_function(i, angle, radius, category_total, segments):
    a = math.cos(angle * 2 * 4) * 0.3
    return angle + a

  return spiral(radius_function=radius_function, angle_function=angle_function)


def spiral_fireball():
  def radius_function(i, angle, radius, category_total, segments):
    a = 1 + (math.sin(angle * 11) * 0.2)
    return radius * a

  def angle_function(i, angle, radius, category_total, segments):
    a = math.cos(angle * 12 + math.pi) * 0.3
    return angle + a

  return spiral(radius_function=radius_function, angle_function=angle_function)


def spiral_squid():
  def radius_function(i, angle, radius, category_total, segments):
    a = 1 + (math.sin(angle * 12) * 0.1)
    return radius * a

  def angle_function(i, angle, radius, category_total, segments):
    a = math.cos(angle * 12) * 0.3
    return angle + a

  return spiral(radius_function=radius_function, angle_function=angle_function)


def spiral_spiky():
  def radius_function(i, angle, radius, category_total, segments):
    angle = math.cos(angle * 12) * 0.1
    a = 1 + (math.sin(angle * 12) * 0.3)
    return radius * a

  def angle_function(i, angle, radius, category_total, segments):
    a = math.cos(angle * 12) * 0.3
    return angle + a

  return spiral(radius_function=radius_function, angle_function=angle_function)


def spiral_club():
  def radius_function(i, angle, radius, category_total, segments):
    d60 = (math.pi * 2) / 6
    d40 = (math.pi * 2) / 9

    a1 = angle % d60
    fudge = 1
    if (a1 < d40):
      fudge = math.sin(a1 * 4.5)
    else:
      fudge = math.sin(a1 * 9 + math.pi)

    return (radius ** 1.3) * (1 + (fudge * 0.3))

  def angle_function(i, angle, radius, category_total, segments):
    d60 = (math.pi * 2) / 6
    d40 = (math.pi * 2) / 9
    d30 = (math.pi * 2) / 12
    d10 = (math.pi * 2) / 36

    a1 = angle % d60
    fudge = 1
    if (a1 < d40):
      fudge = math.sin(a1 * 9 + math.pi)
    else:
      fudge = math.sin((angle % d30) * 18)

    return angle + (fudge * d10)

  return spiral(segments=200, interspiral_size=0.05,
    radius_function=radius_function, angle_function=angle_function)


def save_svg(svg, file_name):
  svg_string = svg.make_svg()
  with open(file_name, "w") as f:
    f.write(svg_string)


if __name__  == "__main__":
  save_svg(spiral(), file_name="./images/spiral.svg")
  save_svg(spiral_flower(), file_name="./images/spiral-flower.svg")
  save_svg(spiral_steps(), file_name="./images/spiral-steps.svg")
  save_svg(spiral_sails(), file_name="./images/spiral-sails.svg")
  save_svg(spiral_whirlpool(), file_name="./images/spiral-whirlpool.svg")
  save_svg(spiral_loop_back(), file_name="./images/spiral-loop-back.svg")
  save_svg(spiral_fireball(), file_name="./images/spiral-fireball.svg")
  save_svg(spiral_squid(), file_name="./images/spiral-squid.svg")
  save_svg(spiral_spiky(), file_name="./images/spiral-spiky.svg")
  save_svg(spiral_club(), file_name="./images/spiral-club.svg")
