from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int


class Rectangular:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height

        self.top_right: Point = Point(x + width, y + height)
        self.top_left: Point = Point(x, y + height)
        self.bottom_right: Point = Point(x + width, y)
        self.bottom_left: Point = Point(x, y)

    def check_overlap(self, other: 'Rectangular') -> bool:
        """Check if there was an overlap between the two objects.
        If the rectangles do not intersect, then at least one of the right sides will be to the
        left of the left side of the other rectangle (i.e. it will be a separating axis), or vice versa,
        or one of the top sides will be below the bottom side of the other rectange, or vice versa.

        Parameters
        ----------
        other : Rectangular
           The other rectangular we want to check for overlapping.

        Returns
        -------
        bool
            Whether or not they overlap.
        """
        if not isinstance(other, Rectangular):
            raise Exception("You need to give a Rectangular you can't check for a Rectangular and a: ", type(other))
        return (
            self.top_right.x > other.bottom_left.x and self.bottom_left.x < other.top_right.x and self.top_right.y > other.bottom_left.y and self.bottom_left.y < other.top_right.y
        )
