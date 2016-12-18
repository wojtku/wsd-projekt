import logging
import random

from wilki.wilk import WilkThread, WilkProcess


class Menager():
    def __init__(self, liczba_wilkow, mapa=None, min_x=-2, min_y=-2, max_x=2, max_y=2, rozdzielczosc=100):
        self.__init_mapa()
        self.liczba_wilkow = liczba_wilkow
        self.mapa = mapa
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y
        self.rozdzielczosc = rozdzielczosc

    def __init_mapa(self):
        logging.debug("init_mapa")

    def _wylosuj_wspolrzedna(self, min, max):
        return random.randint(min*self.rozdzielczosc, max*self.rozdzielczosc)/self.rozdzielczosc

    def start(self):
        raise NotImplementedError


class MenagerThread(Menager):
    def start(self):
        threads = [WilkThread(id=id, x=self._wylosuj_wspolrzedna(self.min_x, self.max_x),
                              y=self._wylosuj_wspolrzedna(self.min_y, self.max_y)) for id in range(self.liczba_wilkow)]
        for wilkthread in threads:
            wilkthread.start()
        for wilkthread in threads:
            wilkthread.join()

class MenagerProcess(Menager):
    def start(self):
        procesy = [WilkProcess(id=id, x=self._wylosuj_wspolrzedna(self.min_x, self.max_x),
                              y=self._wylosuj_wspolrzedna(self.min_y, self.max_y)) for id in range(self.liczba_wilkow)]
        for wilkproces in procesy:
            wilkproces.start()
        for wilkproces in procesy:
            wilkproces.join()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
    menager = MenagerThread(liczba_wilkow=3)
    # menager = MenagerProcess(liczba_wilkow=3)
    menager.start()


