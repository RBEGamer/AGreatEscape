import json

import typer
import bleach
import signal
import typer
from flask import Flask, request, jsonify, make_response, redirect, render_template, Response
from flask_cors import CORS, cross_origin
import time
import multiprocessing
from flask_socketio import SocketIO, emit
from flask_sock import Sock
from waitress import serve



STATIC_FOLDER="./static"
TEMPLATE_FOLDER = "./templates"

terminate_flask: bool = False

app_typer = typer.Typer(add_completion=True)
app_flask = Flask(__name__, static_url_path='/static', static_folder=STATIC_FOLDER, template_folder=TEMPLATE_FOLDER)
cors = CORS(app_flask)
app_flask.config['CORS_HEADERS'] = 'Content-Type'


app_flask.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app_flask)

def signal_andler(signum, frame):
    global terminate_flask
    terminate_flask = True
    time.sleep(4)
    exit(1)
signal.signal(signal.SIGINT, signal_andler)


@socketio.event
def my_event(message):
    emit('my response', {'data': 'got it!'})

@app_flask.errorhandler(404)
def frontend_page_not_found(e):
    return redirect('/')

@app_flask.route("/")
def frontend_index():


    return redirect("/static/index.html?api=127.0.0.1:5557")


@app_flask.route("/launch")
def frontend_launch():
    user = bleach.clean(request.args.get('user', ''))



@app_flask.route("/api/checkuser")
def api_checkuser():
    user = bleach.clean(request.args.get('user', ''))

    return jsonify({'exists': True}), 200


@app_flask.route("/api/register")
def api_register():
    user = bleach.clean(request.args.get('user', ''))

    return jsonify({})

def flask_server_task(_config: dict):
    host:str = _config.get("host", "0.0.0.0")
    port: int = _config.get("port", 5557)
    debug: bool = _config.get("debug", False)


    #if debug:
    #    #app_flask.run(host=host, port=port, debug=debug)
    socketio.run(app_flask, host=host, port=port, allow_unsafe_werkzeug=True)
    #else:
    #    serve(app_flask, host=host, port=port)


@app_typer.command()
def launch(ctx: typer.Context, port: int = 5557, host: str = "0.0.0.0", debug: bool = False):
    global terminate_flask

    flask_config = {"port": port, "host": host, "debug": debug}
    flask_server: multiprocessing.Process = multiprocessing.Process(target=flask_server_task, args=(flask_config,))
    flask_server.start()

    time.sleep(3)
    while( not terminate_flask):
        print("Editor started. Please open http://{}:{}/".format(host, port))
        if typer.prompt("Terminate  [Y/n]", 'y') == 'y':
            break


    # STOP
    flask_server.terminate()
    flask_server.join()



@app_typer.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    pass






def run():
    app_typer()

if __name__ == "__main__":
    app_typer()



if __name__ == "__main__":
    run()