class CoordonatesScaler:
    def get_scaled(self, coordonates: tuple, initial_width: int, resize_width: int) -> tuple:
        (p1x, p1y), (p2x, p2y) = coordonates
        scale_factor = initial_width / resize_width

        return (int(p1x * scale_factor), int(p1y * scale_factor)), (int(p2x * scale_factor), int(p2y * scale_factor))