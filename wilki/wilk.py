import logging
import multiprocessing
import random
import threading
import time


class Wilk():
    def __init__(self, id, x=None, y=None):
        self.id = id
        self.x = x
        self.y = y
        self.h = self.__jaka_wysokosc()
        self.__wyslij_pozycje()
        self.alfa, self.beta, self.delta = self.__czolowka()

        logging.debug("utworzono " + str(self))

    def __jaka_wysokosc(self):
        # TODO
        return 8848

    def __wyslij_pozycje(self):
        logging.debug(" ".join(["wysylam pozycje:", str(self.x), str(self.y)]))
        # todo

    def __kto_alfa(self):
        # todo
        return 1

    def __kto_beta(self):
        # todo
        return 2

    def __kto_delta(self):
        # todo
        return 3

    def __czolowka(self):
        alfa = self.__kto_alfa()
        beta = self.__kto_beta()
        delta = self.__kto_delta()
        return alfa, beta, delta

    def wio(self):
        logging.debug("wio")
        for a in range(3):
            print('hasam krok'+ str(a) +" "+ str(self))
            time.sleep(random.randint(2,5)/10)


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
    # wilk = WilkProcess(7, 0.2, 0.3)
    wilk.start()

    # print(wilk)

