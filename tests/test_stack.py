import unittest
import stack

class StackTest(unittest.TestCase):

    def setUp(self):
        self.intStack = Stack([1, 2, 3])
        self.emptyStack = Stack([])
        self.stringStack = Stack(["a", "b", "c"])

    # def test_push(self):
        

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