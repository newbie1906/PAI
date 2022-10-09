
# Dołączanie modułu flask 
from flask import Flask
from flask import render_template, request, redirect, url_for, flash

# Tworzenie aplikacji
app = Flask("Flask - Lab")


@app.route('/', methods=['GET', 'POST'])
def index():
    # Przesłanie w odpowiedzi stworzonego widoku z pliku HTML (pliki muszą znajdować w folderze "templates")
    return render_template('t1.html')

@app.route('/login', methods=['POST'])
def login(methods=['POST']):
    if request.method == 'POST':
        
        # Pobranie danych z przesłanego formularza metodą POST i konwersja ich do słownika
        req_form = request.form.to_dict()
        
        # Przesłanie w odpowiedzi stworzonego widoku z pliku HTML 
        # Podczas renderowania szablonu (template) można wykorzytywać dane z funkcji dodając kolejne argumenty
        # do wywołania funkcji render_template i wykorzystując w kodzie html.    
        return "Template przesyłany jest w formie string'a więc można dodawać np. kolejne szablony" + \
                render_template('t2.html', userdata=req_form)


# Uruchomienie applikacji w trybie debug
app.debug = True
app.run()

