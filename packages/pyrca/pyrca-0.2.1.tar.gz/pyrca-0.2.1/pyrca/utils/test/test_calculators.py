import unittest
from pyrca.properties.node import Node
from pyrca.utils.calculators import calculate_area, calculate_centroid_y, \
    get_centroid_above_axis, get_area_above_axis


class TestCalculators(unittest.TestCase):
    data = [Node(0, 0), Node(0, 400), Node(200, 400), Node(200, 0)]

    def test_area(self):
        data = [Node(0, 0), Node(0, 400), Node(200, 400), Node(200, 0)]
        result = calculate_area(data)
        self.assertEqual(result, 80000, msg='Error in calculation of area!')

    def test_centroid_y(self):
        data = [Node(0, 0), Node(0, 400), Node(200, 400), Node(200, 0)]
        result = calculate_centroid_y(data)
        self.assertEqual(result, 200, msg='Error in calculation of centroid y.')

    def test_centroid_above_axis(self):
        result = get_centroid_above_axis(200.0, self.data)
        self.assertEqual(result, 100, msg='Error in calculating centroid above axis')

    def test_area_above_axis(self):
        result = get_area_above_axis(200, self.data)
        self.assertEqual(result, 40000, msg='Error calculating area above axis!')


if __name__ == '__main__':
    unittest.main()