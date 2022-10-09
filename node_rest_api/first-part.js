const WebSocket = require('ws');

// pobranie modułu (include z c w nodejs)
var express = require('express');

//dołączanie modułu ORM 
const Sequelize = require('sequelize')

// dołączenie modułu usuwającego problem z zabezpieczeniem CORS
const cors = require('cors');

// dołączenie modułu obsługi sesji
var session = require('express-session');
const e = require('express');

//Inicjalizacja aplikacji
var app             = express();
//process.env.PORT - pobranie portu z danych środowiska np. jeżeli aplikacja zostanie uruchomiona na zewnętrznej platformie np. heroku
var PORT            = process.env.PORT || 8080;
//uruchomienie serwera
var server          = app.listen(PORT,() => console.log(`Listening on ${ PORT }`));

const wss = new WebSocket.Server({
    noServer: true,
});

const sequelize = new Sequelize('database', 'root', 'root', {
    dialect: 'sqlite',
    storage: 'orm-db.sqlite',
});

const sessionParser = session({
    saveUninitialized: false,
    secret: '$secret',
    resave: false
});

// dołączenie modułu ułatwiającego przetwarzanie danych pochodzących z ciała zaytania HTTP (np. POST)
app.use(express.json());

// dołączenie modułu CORS do serwera
app.use(cors());

// dołączenie obslugi sesji do aplikacji 
app.use(sessionParser);

//dołączenie folderu public ze statycznymi plikami aplikacji klienckiej
app.use(express.static(__dirname + '/second-part/'));

// Stworzenie modelu - tabeli User
const User = sequelize.define('user', {
    user_id: {
      type: Sequelize.INTEGER,
      primaryKey: true,
      autoIncrement: true
    },
    user_name: Sequelize.STRING,
    user_password: Sequelize.STRING
})

const Message = sequelize.define('message', {
    message_id: {
      type: Sequelize.INTEGER,
      primaryKey: true,
      autoIncrement: true
    },
    message_from_user_id: Sequelize.INTEGER,
    message_to_user_id: Sequelize.INTEGER,
    message_text: Sequelize.STRING
})


let onlineUsers = {};

// synchroniznacja bazy danych - np. tworzenie tabel
sequelize.sync({}).then(() => {
  console.log(`Database & tables created!`)
})


function testGet(request, response){
    response.send("testGet working");
}

// rejestrowanie użytkownika
function register(request, response) {
    console.log(request.body)
    var user_name = request.body.user_name;
    var user_password = request.body.user_password;
    if (user_name && user_password) {

        User.count({ where: { user_name: user_name } }).then(
            count => {
                if (count != 0) {
                    response.send({ register: false });
                } else {
                    User.create({user_name: user_name, user_password: user_password})
                        .then(() => response.send({ register: true }))
                        .catch(function (err) { response.send({ register: true })
                      });
                }
            })
    } else {
        response.send({ register: false });
    }
}

// logowanie uzytkownika
function login(request, response) {
    const login = request.body.user_name;
    const password = request.body.user_password;
    User.findAll({where:{user_name:login},raw:true})
    .then((row) => {
        if(row[0].user_password === password){
            request.session.user_id = row[0].user_id;
            console.log(row[0].user_id);
            request.session.user_name = row[0].user_name;
            request.session.loggedin = true;
            response.send({loggedin: request.session.loggedin, user_id: request.session.user_id,
            user_name: request.session.user_name });
        }
        else{
            request.session.loggedin = false;
            response.send({ loggedin: request.session.loggedin });
        }
    })
    .catch((error) => {
        console.log(error);
    })
}

// sprawdzenie logowania jeżeli funkcja checkSessions nie zwróci błędu
function loginTest(request, response) {
    response.send({ loggedin: true });
}

function logout(request, response) {
    request.session.destroy()
    // TODO: niszczenie sesji
    response.send({ loggedin: false });
}

function checkSessions(request, response, next) {
    if (request.session.loggedin) {
        next();
    } else {
        response.send({ loggedin: false });
    }
}

function getUsers(request, response) {
    const usersList = [];
    const users =  User.findAll().then((users => {
        users.forEach(element => {
            const oneUser = {user_id:element.dataValues.user_id,user_name:element.dataValues.user_name};
            if(onlineUsers[element.user_id]){
            oneUser.online = true;
            }else{
            oneUser.online = false;
            }
            usersList.push(oneUser);
        });
        response.send({ data: usersList });
    }));
}

function getMessages(request, response){
    const user_id = request.session.user_id;
    const target_id = request.params.id;
    
    //const message = [{"message_text": []}]
    
    const message = [];
    const messages = Message.findAll({where:{message_from_user_id:user_id, message_to_user_id: target_id}, raw:true}).then(( row ) => {
        row.forEach(element => {
            const allMessages = {message_text: element.message_text}
            message.push(allMessages);
            
            //message[0]['message_text'].push(element.message_text);
        })
        response.send({data: message});
    }) 
}

function sendMessages(request, response) {
    var message_text = request.body.message_text;
    var to = request.body.message_to_user_id;
    console.log(`Received message => ${message_text} from ${request.session.user_id} to ${to}`);

    User.findAll({ where: { user_id: to } }).then(
        users => {
            if (users.length >= 1) {
                var mes = {
                    message_from_user_id: request.session.user_id,//TODO
                    message_to_user_id: users[0].user_id,
                    message_text: `${message_text}`, //TODO
                }
                var user = users[0];
                Message.create(mes)
                        .then((mes) => 
                        {
                            if (user.user_id in onlineUsers) {
                                // Wysyłanie wiadomości do odiorcy
                                onlineUsers[user.user_id].send(JSON.stringify(mes.message_text));

                            }
                            if (mes.message_from_user_id !== mes.message_to_user_id) {
                                if (mes.message_from_user_id in onlineUsers) {
                                     // Wysyłanie wiadomości do nadawcy jeżeli odbiorca nie jest nadawca
                                     onlineUsers[user.user_id].send(JSON.stringify(mes.message_text));
                                }
                            }

                            response.send({ sending: true })
                        })
                        .catch(function (err) { console.log(err); response.send({ error: err })
                      });

            } else {
                response.send({ error: "User not exists" });
            }
        })
}


server.on('upgrade', function (request, socket, head) {
    // Sprawdzenie czy dla danego połączenia istnieje sesja

    sessionParser(request, {}, () => {
        console.log(request.session.user_id);
        if (!request.session.user_id) {
            socket.destroy();
            return;
        }
        wss.handleUpgrade(request, socket, head, function (ws) {
            wss.emit('connection', ws, request);
        });
    });
});



wss.on('connection', function (ws, request) {

    wss.clients.forEach(function each(client) {
        if (client.readyState === WebSocket.OPEN) {
            client.send(JSON.stringify({ status: 2 }));
        }
    });
    onlineUsers[request.session.user_id] = ws;
    //console.log(onlineUsers);
    ws.on('message', function (message) {
        console.log(String(message))

        // parsowanie wiadomosci z JSONa na obiekt
        try {
            var data = JSON.parse(message);
        } catch (error) {
            return;
        }
    });

    ws.on('close', () => {
        delete onlineUsers[request.session.user_id];
    })

});



app.get('/api/test-get', testGet);

app.post('/api/register/', [register]);

app.post('/api/login/', [login]);

app.get('/api/login-test/', [checkSessions, loginTest]);

app.get('/api/logout/', [checkSessions, logout]);

app.get('/api/users/', [checkSessions, getUsers]);

app.get('/api/messages/:id', [checkSessions, getMessages]);

app.post('/api/messages/', [checkSessions, sendMessages]);

