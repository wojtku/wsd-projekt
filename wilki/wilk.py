import logging
import multiprocessing
import random
import threading
import time
from threading import Timer

from algorytm import GreyWolfOptimizer

class Wilk():
    def __init__(self, id, x=None, y=None):
        self.id = id
        self.x = x
        self.y = y
        self.h = self._jaka_wysokosc()
        self._wyslij_pozycje()
        # poczekajmy az kazdy wilk zaraportuje
        Timer(0.001, self._czolowka).start()

        logging.debug("utworzono " + str(self))

    def _jaka_wysokosc(self):
        # TODO
        return 8848

    def _wyslij_pozycje(self):
        logging.debug(" ".join(["wysylam pozycje:", str(self.x), str(self.y)]))
        # todo request http

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

        for a in range(5):
            self.x, self.y = self.gwo.krok()
            logging.info('hasam krok' + str(a) + " " + str(self))
            self._wyslij_pozycje()
            time.sleep(random.randint(2,5)/10)
            self._czolowka()
            self.gwo.update(self.alfa, self.beta, self.delta)

    def __str__(self):
        return " ".join(["wilk", str(self.id), "x=", str(self.x),"y=", str(self.y), 'h=', str(self.h)])


class RownoleglyWilk(Wilk):
    def __init__(self):
        super(Wilk, self).__init__()

    def run(self):
        self.wio()


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


