from unittest import TestCase
from dyntree import DynTree


class TestDynTree(TestCase):

    def test_build_and_order(self):
        t1 = DynTree()
        self.assertIsNone(t1.get_deep(5))
        t1.insert(1, 1)
        t1.insert(2, 2)
        t1.insert(11, 11, 2)
        t1.insert(30, 30, 20)
        t1.insert(20, 20, 2)
        t1.insert(13, 13, 15)
        t1.insert(15, 15)
        t1.finalize()
        self.assertDictEqual(t1.get_deep(15), {'value': 15, 'parent': None,
                                               'children': {13: {'value': 13, 'parent': 15, 'children': {}}}})
        items = t1.items()
        self.assertEqual(items[0], ('1', 1))
        self.assertEqual(items[1], ('2', 2))
        self.assertEqual(items[2], ('2.1', 11))
        self.assertEqual(items[3], ('2.2', 20))
        self.assertEqual(items[4], ('2.2.1', 30))
        self.assertEqual(items[5], ('3', 15))
        self.assertEqual(items[6], ('3.1', 13))
