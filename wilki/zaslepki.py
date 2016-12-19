import threading


class Wszechwiedzacy():
    def __init__(self):
        self.d = {}
        self.lock = threading.Lock()

    def najlepsi(self):
        with self.lock:
            l = [wilk for wilk in self.d.values()]
            l.sort(key=lambda wilk: wilk.h, reverse=True)
            return l[:3]

    def setWilk(self, wilk):
        with self.lock:
            self.d[wilk.id] = wilk

    def getWilk(self, id):
        with self.lock:
            return self.d[id]
