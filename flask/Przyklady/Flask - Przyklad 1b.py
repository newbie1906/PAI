# Dołączanie modułu flask 
from flask import Flask

# Tworzenie aplikacji
app = Flask("Flask - Lab")

# Anotacja funkcji @app.route() dodaje 
# endpoint - adres, pod który może odwołać się klient 
# podczas zapytania HTTP - pod adresem przekazanym w parametrach funkcji route
@app.route("/")
# Funkcja zwracająca napis
def index():
    return """Hello World!<br>
    <a href=/about>Przejdz do about</a>"""

@app.route("/about")
def about():
    return "<a href=/>Powrót</a>"
# Uruchomienie applikacji w trybie debug
app.debug = True
app.run()

