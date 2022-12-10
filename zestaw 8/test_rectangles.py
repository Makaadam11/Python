print("\n-------------------zadanie 8.1 --------------------\n") 

import unittest
from rectangles import Rectangle
from points import Point



class TestRectangle(unittest.TestCase): 
    
    def setUp(self):
        self.rectangle1 = Rectangle()
        self.rectangle2 = Rectangle(2, 5, 6, 3)
        self.rectangle3 = Rectangle(3, 2, -6, 5)
        self.rectangle4 = Rectangle(2, 2, 8, 8)
        self.rectangle5 = Rectangle(1, 1, 10, 10)
        self.rectangle6 = Rectangle(2, 1, 10, 8)
        self.rectangle7 = Rectangle(1, 2, 8, 10)

    def test_str(self):
        self.assertEqual(self.rectangle2.__str__(), "[(2, 5), (6, 3)]")
        self.assertEqual(self.rectangle3.__str__(), "[(3, 2), (-6, 5)]")	

    def test_repr(self):
        self.assertEqual(self.rectangle2.__repr__(), "Rectangle(2, 5, 6, 3)")
        self.assertEqual(self.rectangle3.__repr__(), "Rectangle(3, 2, -6, 5)")

    def test_eq(self):
        self.assertEqual(self.rectangle3 == self.rectangle3, True)
        self.assertEqual(self.rectangle3 == self.rectangle2, False)

    def test_center(self):
        self.assertEqual(self.rectangle1.center(), Point())
        self.assertEqual(self.rectangle2.center(), Point(4, 4))
        self.assertEqual(self.rectangle3.center(), Point(-1.5,3.5))

    def test_area(self):
        self.assertEqual(self.rectangle1.area(), 0)
        self.assertEqual(self.rectangle2.area(), 8)
        self.assertEqual(self.rectangle3.area(), 27)

    def test_move(self):
        self.rectangle1.move(2, 1)
        self.rectangle2.move(2, 1)
        self.assertEqual(self.rectangle1, Rectangle(2, 1, 2, 1))
        self.assertEqual(self.rectangle2, Rectangle(4, 6, 8, 4))

    def test_intersection(self):
        self.assertEqual(self.rectangle6.intersection(self.rectangle7), Rectangle(2, 2, 8, 8))
        with self.assertRaises(ValueError):
            self.rectangle1.intersection(self.rectangle3)

    def test_cover(self):
        self.assertEqual(self.rectangle5.cover(self.rectangle4), self.rectangle5)
        self.assertEqual(self.rectangle6.cover(self.rectangle7), Rectangle(1, 1, 10, 10))

    def test_make4(self):
        self.assertEqual(self.rectangle4.make4(), [Rectangle(2, 2, 5, 5), 
            Rectangle(5, 2, 8, 5), Rectangle(2, 5, 5, 8), 
            Rectangle(5, 5, 8, 8)])
        with self.assertRaises(ValueError):
            self.rectangle1.make4()
        
        
    def test_from_points(self):
        self.assertEqual(self.rectangle2.from_points((2,3),(4,6)), "Rectangle(topleft (2,6), bottomleft (2,3), topright (4,6), bottomright (4,3))")

if __name__ == '__main__':
	unittest.main()