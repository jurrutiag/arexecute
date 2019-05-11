
class Stack():
    def __init__(self, array, fifo=True):
        self._array = array

    def push(self, item):
        self._array.append(item)

    def get(self):
        if (len(self._array) > 0):
            return self._array.pop(0)
        else:
            return None

    def getArray(self):
        return self._array
