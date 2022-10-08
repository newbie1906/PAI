# Dołączanie modułu flask 
from flask import Flask

# Tworzenie aplikacji
app = Flask("Flask - Lab")

@app.route('/')
def users():
    return 'Users'

# Endpoint umożliwiający podanie parametru w postaci string'a
@app.route('/<username>')
def user_by_name(username):
    return 'User name: %s' % username

# Endpoint umożliwiający podanie parametru w postaci int'a
@app.route('/<int:get_id>')
def user_by_id(get_id):
    return 'User id: %d' % get_id

# Uruchomienie applikacji w trybie debug
app.debug = True
app.run()

