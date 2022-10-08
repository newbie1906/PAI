# Dołączanie modułu flask 
from flask import Flask
from flask import render_template, request, redirect, url_for, flash

# Tworzenie aplikacji
app = Flask("Flask - Lab")

# Endpoint dla konkretnego zapytania HTTP  
@app.route('/', methods=['GET'])
def index_get():
    form='''
       <form method=post action="/">
       Imie: <input type=text name=imie>
       Nazwisko: <input type=text name=nazwisko>
       <input type=submit>
       </form>
    '''
    return form


# Endpoint dla konkretnego zapytania HTTP  
@app.route('/', methods=['POST'])
def index_post():
    # pobranie danych z przesłanego formularza metodą POST
    resposne_form = request.form
    if resposne_form['imie'] and resposne_form['nazwisko']:
        return "<br> Czesc "+resposne_form['imie']+" "+resposne_form['nazwisko']
    else: 
        return "Dane w postaci zapytania GET lub POST"

# Uruchomienie applikacji w trybie debug
app.debug = True
app.run()

