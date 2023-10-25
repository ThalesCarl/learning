import unittest
import math

class Vector():
    def __init__(self, x=0, y=0) -> None:
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Vector({self.x!r}, {self.y!r})'

    def __abs__(self):
        return math.hypot(self.x, self.y)
    
    def __bool__(self):
        return bool(abs(self)) # What does this mean? That if self != 0.0 then we have a Vector
    
    # This one I had to implement myself, in order to the unitest work
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

class TestVector(unittest.TestCase):
    def test_sum(self):
        v1 = Vector(2, 4)
        v2 = Vector(2, 1)
        self.assertEqual(v1 + v2, Vector(4, 5))

    def test_magnitude(self):
        v = Vector(3, 4)
        self.assertEqual(abs(v), 5.0)
    
    def test_scalar_multiply(self):
        v = Vector(3, 4)
        self.assertEqual(v * 3, Vector(9, 12))
        self.assertEqual(abs(v * 3), 15.0)



if __name__ == '__main__':
    unittest.main()