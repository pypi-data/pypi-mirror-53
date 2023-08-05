
class Type1:

    def __init__(self):
        self.x = 1
        self.y = 2


class Type2:

    def __init__(self):
        self.x = 1
        self.y = 2


def eins(a: Type1, b: Type1):
    return a.x + b.y


print(eins(Type1(), Type2()))
