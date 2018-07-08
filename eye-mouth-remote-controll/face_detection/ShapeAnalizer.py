class ShapeAnalizer:
    def get_height(self, points) -> int:
        return self.__do_get_dimensions(points, 1)

    def get_width(self, points) -> int:
        return self.__do_get_dimensions(points, 0)

    def __do_get_dimensions(self, points, axis: int) -> int:
        min_height = min(points, key=lambda coordonates: coordonates[axis])[axis]
        max_height = max(points, key=lambda coordonates: coordonates[axis])[axis]

        return max_height - min_height