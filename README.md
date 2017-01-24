## wymagania:
- python3 requests *pip3 install requests*
- nodejs
- w folderze visualization : *npm install*
    
    
##DEMO
- 10 wilków
- 15 iteracji
- co krok wilki losowo 1-3 sekund czekają
- mapa nr 0: sin(x*y)
- min_x=-2, min_y=-2, max_x=2, max_y=2

start backendu wizualizacyjnego:

    nodejs visulization/server.js 8080

start wilków:

    python3 wilki/test.py
    
podgląd wszystkich wilków:

    GET http://localhost:8080/api/wolf