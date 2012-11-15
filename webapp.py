from flask import Flask
from flask import render_template
from flask import request
from socketio.namespace import BaseNamespace
from socketio import socketio_manage
from socketio.server import SocketIOServer

app = Flask(__name__)
app.debug = True

class PingPong(BaseNamespace):
    def on_ping(self,attack):
        if attack['type'] == 'fireball':
            for i in range(10):
                self.emit('pong',{'sound':'bang!'})
        else:
            self.emit('pong',{'sound':'pong'})

@app.route('/socket.io/<path:remaining>')
def pingpong(remaining):
    socketio_manage(request.environ,{'/pingpong':PingPong},request)
    return 'done'

@app.route('/')
def main_page():
    return render_template('main_page.html')

def main():
    SocketIOServer(('',5000),app,resource="socket.io").serve_forever() 

if __name__ == "__main__":
    main()
