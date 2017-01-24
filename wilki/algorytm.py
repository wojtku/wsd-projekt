import json
import random
from math import sin, radians

import time


class GreyWolfOptimizer():
    def __init__(self, x, y, alfa, beta, delta, wilk):
        self.wilk = wilk
        self.alfa = alfa
        self.beta = beta
        self.delta = delta
        self.model_a = 2
        self.a_decr = 0.1
        self.A = None  # random.uniform(-self.model_a, self.model_a)


    def krok(self):
        self.A = random.uniform(-self.model_a, self.model_a)
        if abs(self.A) > 1:
            new_x, new_y = self.nowa_pozycja_gdy_atak()
        else:
            new_x, new_y = self.nowa_pozycja_gdy_nie_atak()

        self.model_a = self.model_a - self.a_decr
        if self.model_a < 0:
            self.model_a = 2

        return new_x, new_y

    def update(self, alfa, beta, delta):
        self.alfa = alfa
        self.beta = beta
        self.delta = delta

    def nowa_pozycja_gdy_atak(self):
        c1 = random.uniform(0, 2)
        c2 = random.uniform(0, 2)
        c3 = random.uniform(0, 2)

        da = abs(c1 * self.alfa.x - self.wilk.x)
        db = abs(c2 * self.beta.x - self.wilk.x)
        dd = abs(c3 * self.delta.x - self.wilk.x)

        A1 = random.uniform(-self.model_a, self.model_a)
        A2 = random.uniform(-self.model_a, self.model_a)
        A3 = random.uniform(-self.model_a, self.model_a)

        x1 = self.alfa.x - A1 * da
        x2 = self.beta.x - A2 * db
        x3 = self.delta.x - A3 * dd

        new_x = (x1 + x2 + x3) / 3.0

        da = abs(c1 * self.alfa.y - self.wilk.y)
        db = abs(c2 * self.beta.y - self.wilk.y)
        dd = abs(c3 * self.delta.y - self.wilk.y)

        A1 = random.uniform(-self.model_a, self.model_a)
        A2 = random.uniform(-self.model_a, self.model_a)
        A3 = random.uniform(-self.model_a, self.model_a)

        y1 = self.alfa.y - A1 * da
        y2 = self.beta.y - A2 * db
        y3 = self.delta.y - A3 * dd

        new_y = (y1 + y2 + y3) / 3.0

        return new_x, new_y

    def nowa_pozycja_gdy_nie_atak(self):
        c = random.uniform(0, 2)
        x_ofiara = (self.alfa.x * self.alfa.h +
                    self.beta.x * self.beta.h +
                    self.delta.x * self.delta.h) / (self.alfa.h + self.beta.h + self.delta.h)
        d = abs(c * x_ofiara - self.wilk.x)
        new_x = x_ofiara - self.A * d

        y_ofiara = (self.alfa.y * self.alfa.h +
                    self.beta.y * self.beta.h +
                    self.delta.y * self.delta.h) / (self.alfa.h + self.beta.h + self.delta.h)
        d = abs(c * y_ofiara - self.wilk.y)
        new_y = y_ofiara - self.A * d

        return new_x, new_y


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
