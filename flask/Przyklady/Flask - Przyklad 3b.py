
# Dołączanie modułu flask 
from flask import Flask
from flask import render_template, request, redirect, url_for, flash

# Tworzenie aplikacji
app = Flask("Flask - Lab")

# Endpoint dla konkretnego zapytania HTTP  
@app.route('/', methods=['GET'])
def index_get():
    form='''
       <form method=post action="/login">
       Imie: <input type=text name=imie>
       Nazwisko: <input type=text name=nazwisko>
       <input type=submit>
       </form>
    '''
    return form

@app.route('/login', methods=['GET','POST'])
def login():
    # Sprawdzenie jakiego typu przyszło zapytanie
    if request.method == 'POST':
        # pobranie danych z przesłanego formularza metodą POST
        resposne_form = request.form
        if resposne_form['imie'] and resposne_form['nazwisko']:
            return "POST: Czesc "+resposne_form['imie']+" "+resposne_form['nazwisko']
        else: 
            return "Brak danych dla zapytania POST"

    elif request.method == 'GET':

        # odczyt danych przesłanych w postaci zapytania GET
        if request.args.get("imie") and request.args.get("nazwisko"):
            return "GET: Czesc "+request.args.get("imie") + " " + request.args.get("nazwisko")
        else: 
            return "Brak danych dla zapytania GET"
    else: 
        return "Dane w postaci zapytania GET lub POST"

# Uruchomienie applikacji w trybie debug
app.debug = True
app.run()

