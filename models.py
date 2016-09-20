
class Point(object):

    def __init__(self, index, value):
        self.index = index
        self.value = value


class Metric(object):

    def __init__(self, name, points):
        self.name = name
        self.points = self._build_point_list(points)

    def _build_point_list(self, points):
        return [Point(point[1], point[0]) for point in points if point[0]]
