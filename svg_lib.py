import math
import sys


def pol2cart(radius, angle):
  x = radius * math.cos(angle)
  y = radius * math.sin(angle)
  return (x, y)


def add_cart(coord1, coord2):
  return (
    coord1[0] + coord2[0],
    coord1[1] + coord2[1],
  )


def diff_cart(coord1, coord2):
  return (
    coord2[0] - coord1[0],
    coord2[1] - coord1[1],
  )


def cart2pol(x, y):
  radius = (x**2 + y**2)**0.5
  angle = math.atan(y / x)
  if (x < 0):
    angle = math.pi + angle
  elif (y < 0):
    angle = (math.pi * 2) + angle
  return (radius, angle)


def project(point, angle, distance):
  projected_x, projected_y = pol2cart(distance, angle)
  projected_x += point[0]
  projected_y += point[1]
  return (projected_x, projected_y)


class _Layer:
  def __unicode__(self):
    return "Layer {}".format(self.id)
  def __str__(self):
    return self.__unicode__()

  def __init__(self, layer_id):
    self.id = layer_id


class Path:
  next_id = 1

  def __unicode__(self):
    return "Path {}, layer: {}, close_path: {}, points: {}".format(self.id, self.layer, self.close_path, self.points)
  def __str__(self):
    return self.__unicode__()

  def __init__(self, layer, points, close_path):
    self.id = Path.next_id
    Path.next_id += 1

    self.layer = layer
    self.points = points
    self.close_path = close_path

    if not isinstance(points, (tuple, list)):
      raise Exception("points must be a tuple or list")
    for point in points:
      if not isinstance(point, (tuple, list)):
        raise Exception("point must be a tuple or list")

    self.min_x =  sys.maxsize
    self.max_x = -sys.maxsize - 1
    self.min_y =  sys.maxsize
    self.max_y = -sys.maxsize - 1

    pos_x = 0
    pos_y = 0
    for x, y in self.points:
      pos_x += x
      pos_y += y

      self.min_x = min(self.min_x, pos_x)
      self.min_y = min(self.min_y, pos_y)
      self.max_x = max(self.max_x, pos_x)
      self.max_y = max(self.max_y, pos_y)

  def to_svg(self):

    coords = "m"
    for point in self.points:
      coords += " {},{}".format(*point)

    if self.close_path:
      coords += " z"

    svg = "\n".join([
      "    <path",
      "       id=\"path{}\"".format(self.id),
      "       style=\"fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1\"",
      "       d=\"{}\"".format(coords),
      "    />",
      "",
    ])

    return svg


class SVG:
  @staticmethod
  def points_to_path(points):
    path = []
    for i, point in enumerate(points):
      if (i == 0):
        path.append(point)
      else:
        last_point = points[i - 1]
        diff = diff_cart(last_point, point)
        path.append(diff)

    return path

  def __unicode__(self):
    return "yo"
  def __str__(self):
    return self.__unicode__()

  def __init__(self):
    self.next_layer_id = 1

    self.paths = []
    self.layers = []

    self.min_x =  sys.maxsize
    self.max_x = -sys.maxsize - 1
    self.min_y =  sys.maxsize
    self.max_y = -sys.maxsize - 1

  def create_layer(self):
    layer = _Layer(self.next_layer_id)
    self.next_layer_id += 1
    self.layers.append(layer)
    return layer

  def add_path(self, path):
    layers = [layer for layer in self.layers if layer.id == path.layer.id]
    if (len(layers) != 1):
      raise Exception("Layer {} does not exist".format(path.layer.id))
    self.paths.append(path)

    self.min_x = min(self.min_x, path.min_x)
    self.min_y = min(self.min_y, path.min_y)
    self.max_x = max(self.max_x, path.max_x)
    self.max_y = max(self.max_y, path.max_y)

  def _svg_header(self):
    width = self.max_x - self.min_x
    height = self.max_y - self.min_y

    return """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
  xmlns:svg="http://www.w3.org/2000/svg"
  xmlns="http://www.w3.org/2000/svg"
  version="1.1"
  viewBox="{view_x} {view_y} {view_width} {view_height}"
  width="{width}mm"
  height="{height}mm"
>
  <defs id="defs4215" />
""".format(
    view_x = self.min_x - width * 0.1,
    view_y = self.min_y - height * 0.1,
    view_width = width * 1.2,
    view_height = height * 1.2,
    width = width,
    height = height,
  )

  def make_svg(self):
    svg = self._svg_header()

    paths_by_layer = dict()

    for layer in self.layers:
      paths_by_layer[layer.id] = []

    for path in self.paths:
      paths_by_layer[path.layer.id].append(path)

    for layer in self.layers:
      svg += """  <g id="layer{}">\n""".format(layer.id)
      for path in paths_by_layer[layer.id]:
        svg += path.to_svg()
      svg += "  </g>\n"

    svg += "</svg>\n"

    return svg
