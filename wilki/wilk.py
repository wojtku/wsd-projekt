import logging
import multiprocessing
import random
import threading
import time
from threading import Timer
import requests

from algorytm import GreyWolfOptimizer

class Wilk():
    def __init__(self, id, x=None, y=None):
        self.id = id
        self.x = x
        self.y = y
        self.h = self._jaka_wysokosc(self.x, self.y)
        self.gwo = None
        self._wyslij_pozycje()
        # poczekajmy az kazdy wilk zaraportuje
        Timer(0.001, self._czolowka).start()

        logging.debug("utworzono " + str(self))

    def _jaka_wysokosc(self, x, y):
        # TODO
        return 8848

    def _wyslij_pozycje(self):
        logging.debug(" ".join(["wysylam pozycje:", str(self.x), str(self.y)]))
        try:
            requests.post('http://localhost:8080/api/wolf/' + str(self.id),
                          json={'id': self.id, 'x': self.x, 'y': self.y, 'h': self.h, 'type': 'OMEGA'})
        except Exception as e:
            print('nie mogę wysłać pozycji do backendu wizualizacyjnego', e)


    def __kto_alfa(self):
        # todo
        return 1

    def __kto_beta(self):
        # todo
        return 2

    def __kto_delta(self):
        # todo
        return 3

    def _czolowka(self):
        self.alfa = self.__kto_alfa()
        self.beta = self.__kto_beta()
        self.delta = self.__kto_delta()
        return self.alfa, self.beta, self.delta

    def wio(self):
        logging.debug(str(self.id) + " wio")
        time.sleep(0.0001)
        try:
            self.gwo = GreyWolfOptimizer(x=self.x, y=self.y, alfa=self.alfa,
                                         beta=self.beta, delta=self.delta, wilk=self)
        except AttributeError:
            time.sleep(0.01)
            self._czolowka()
            self.gwo = GreyWolfOptimizer(x=self.x, y=self.y, alfa=self.alfa,
                                         beta=self.beta, delta=self.delta, wilk=self)
        # GLOWNA PETLA HASANIA
        for a in range(15):
            self.x, self.y = self.gwo.krok()
            self.h = self._jaka_wysokosc(self.x, self.y)
            logging.info('hasam krok' + str(a) + " " + str(self))
            self._wyslij_pozycje()
            time.sleep(random.randint(1, 3))
            self._czolowka()
            self.gwo.update(self.alfa, self.beta, self.delta)

    def __str__(self):
        return " ".join(["wilk", str(self.id), "x=", str(self.x),"y=", str(self.y), 'h=', str(self.h)])


class RownoleglyWilk(Wilk):
    def __init__(self):
        super(Wilk, self).__init__()

    def run(self):
        self.wio()
        print("najwyższy szczyt: ", self.alfa.h)


class WilkThread(RownoleglyWilk, threading.Thread):
    def __init__(self, id, x, y):
        super(WilkThread, self).__init__()
        super(RownoleglyWilk, self).__init__(id=id, x=x, y=y)
        logging.debug('WilkThread utworzono: ' + Wilk.__str__(self))


class WilkProcess(RownoleglyWilk, multiprocessing.Process):
    def __init__(self, id, x, y):
        super(WilkProcess, self).__init__()
        super(RownoleglyWilk, self).__init__(id=id, x=x, y=y)
        logging.debug('WilkProces utworzono: ' + Wilk.__str__(self))



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG ,format='%(levelname)s: %(message)s')
    wilk = WilkThread(4, 1.5, 1.9)
    wilk.start()


