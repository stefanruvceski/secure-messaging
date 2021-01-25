from flask import Flask
import socket

app = Flask(__name__)
@app.route('/')
def index():
    return "Laaav juuu!"

if __name__ == '__main__':
    #app.run(debug=True)
    
    host = socket.gethostbyname(socket.gethostname())
    app.run( host='192.168.1.3',port=12000)