class Point(tuple):
    def __new__(self, x, y):
        return tuple.__new__(Point, (x,y))
    def __add__(self, other):
        return Point(*([sum(x) for x in zip(self, other)]))
    def __sub__(self, other):
        return self.__add__(-i for i in other)
