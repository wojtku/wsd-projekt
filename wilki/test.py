import logging
from threading import Timer
from unittest.mock import patch
import requests

import time

from menager import MenagerThread
from wilk import Wilk
from menager import Menager
from algorytm import Mapy
from zaslepki import Wszechwiedzacy

global wszechwiedzacy, mapy, wybrana_mapa
wszechwiedzacy = Wszechwiedzacy()
mapy = Mapy()


def _init_mapa_mock(self, nr_mapy):
    global wybrana_mapa
    wybrana_mapa = nr_mapy


def _wyslij_pozycje_mock(self):
    logging.debug(" ".join([str(self.id), "wysylam pozycje: ", str(self.x), str(self.y)]))
    requests.post('http://localhost:8080/api/wolf/' + str(self.id),
                  json={'id': self.id, 'x': self.x, 'y': self.y, 'h': self.h, 'type': 'OMEGA'})
    wszechwiedzacy.setWilk(self)


def _jaka_wysokosc_mock(self, x, y):
    return mapy.oblicz(numer_mapy=wybrana_mapa, x=self.x, y=self.y)


def _czolowka_mock(self):
    naj = wszechwiedzacy.najlepsi()
    while (len(naj) < 3):
        logging.debug("czekam az wszystkie watki wysla pozycje, sa " + str(len(naj)))
        naj = wszechwiedzacy.najlepsi()
    self.alfa = naj[0]
    self.beta = naj[1]
    self.delta = naj[2]
    return naj[0], naj[1], naj[2]


if __name__ == "__main__":
    # logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    patchery = [patch('__main__.Wilk._wyslij_pozycje', _wyslij_pozycje_mock),
                patch('__main__.Wilk._jaka_wysokosc', _jaka_wysokosc_mock),
                patch('__main__.Menager._init_mapa', _init_mapa_mock),
                patch('__main__.Wilk._czolowka', _czolowka_mock)
                ]
    for patch in patchery:
        patch.start()

    menager = MenagerThread(liczba_wilkow=10)
    menager.start()

    for patch in patchery:
        patch.stop()
