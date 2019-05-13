import unittest
from stack.stack import Stack


class StackTest(unittest.TestCase):
    def setUp(self):
        self.intStack = Stack([1, 2, 3])
        self.emptyStack = Stack([])
        self.stringStack = Stack(["a", "b", "c"])

    def test_push(self):
        self.intStack.push(4)
        self.assertEqual([1, 2, 3, 4], self.intStack.getArray())

        self.emptyStack.push(100)
        self.assertEqual([100], self.emptyStack.getArray())

        self.stringStack.push("hola")
        self.assertEqual(["a", "b", "c", "hola"], self.stringStack.getArray())

    def test_get(self):
        self.assertEqual(1, self.intStack.get())
        self.assertEqual([2, 3], self.intStack.getArray())
        self.assertEqual(2, self.intStack.get())
        self.assertEqual([3], self.intStack.getArray())
        self.assertEqual(3, self.intStack.get())
        self.assertEqual([], self.intStack.getArray())

        self.assertEqual(None, self.intStack.get())
        self.assertEqual([], self.intStack.getArray())


if __name__ == "__main__":
    unittest.main()
