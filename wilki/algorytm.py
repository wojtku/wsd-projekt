import json
from math import sin, radians


class GreyWolfOptimizer():
    def __init__(self, x, y, alfa, beta, delta, wilk):
        self.wilk = wilk
        self.x = x
        self.y = y
        self.alfa = alfa
        self.beta = beta
        self.delta = delta

    def krok(self):
        # todo
        self.x = self.x + 0.01
        self.y = self.y + 0.01
        return self.x, self.y

    def update(self, alfa, beta, delta):
        self.alfa = alfa
        self.beta = beta
        self.delta = delta


class Mapy():
    def __init__(self):
        self.mapy = [(self.przestrzen1, 'sin(x,y)'),
                     (self.przestrzen2, '-pow(1-x, 2)-100*pow((y-pow(x,2)),2)')]

    def oblicz(self, numer_mapy, x, y):
        fun = self.mapy[numer_mapy][0]
        return fun(x, y)

    @staticmethod
    def przestrzen1(x, y):
        return sin(radians(x * y))

    @staticmethod
    def przestrzen2(x, y):
        return -pow(1 - x, 2) - 100 * pow((y - pow(x, 2)), 2)

    def json(self):
        l = [m[1] for m in self.mapy]
        d = {key: value for key, value in enumerate(l)}
        return json.dumps(d, sort_keys=True, indent=4)

    def zapisz_jsona(self):
        with open('mapy.json', 'wt') as f:
            f.write(self.json())


if __name__ == "__main__":
    mapy = Mapy()
    mapy.zapisz_jsona()
