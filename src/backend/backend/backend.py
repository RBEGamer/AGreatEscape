import json
import os
import random

import bson
import pymongo.database
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
from pymongo import MongoClient
from waitress import serve
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo
from pymongo.errors import DuplicateKeyError, OperationFailure
from flask import current_app, g
import DBModelUser
import Floorplan
import ai

MONGO_COLLECTION = "AGreatEscapeCollection"
MONGO_USERSDB = "users"

STATIC_FOLDER = "./static"
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


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        urli: str = current_app.config['MONGO_URI']
        db = g._database = MongoClient(urli)

    return db


def get_floorplan():
    floorplan = getattr(g, "_floorplan", None)
    if floorplan is None:
        floorplan = g._floorplan = Floorplan.Floorplan()
    return floorplan


def init_db(_mongodb_uri: str):
    client = MongoClient(_mongodb_uri)
    db = client[MONGO_COLLECTION]
    userdb = db[MONGO_USERSDB]

    res = list(userdb.find({'operator': False}, {'_id': 1}))

    f = Floorplan.Floorplan()
    w: int = f.properties_to_json()['width']
    h: int = f.properties_to_json()['height']
    ext_count: int = len(f.properties_to_json()['exits'])


    for r in res:
        userdb.update_one({"_id": r['_id']},
                      {"$set": {
                          "current_postion_on_map_x": random.randint(20, w - 20),
                          "current_postion_on_map_y": random.randint(20, h - 20),
                          'target_exit': random.randint(0, ext_count)}})

    print(userdb)


def get_userdb():
    db = get_db()[MONGO_COLLECTION]
    userdb = db[MONGO_USERSDB]
    return userdb
    #    userdb = db["users"]


# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)
floorplan = LocalProxy(get_floorplan)


@socketio.event
def my_event(message):
    emit('my response', {'data': 'got it!'})


@app_flask.errorhandler(404)
def frontend_page_not_found(e):
    return redirect('/')


@app_flask.route("/")
def frontend_index():
    return redirect("/static/index.html?api=127.0.0.1:5557")


@app_flask.route("/api/get_person_state")
def api_getpersonstate():
    username: str = bleach.clean(request.args.get('username', ''))

    # TODO GET ALL PERSONS FROM DATABASE
    # GET CURRENT POSITIONS
    query: dict = {}
    # if 'operator' not in username:
    #    query['username'] = {'$regex': username}

    query['exit_reached'] = False

    res = list(get_userdb().find(query, {'_id': 0, 'current_postion_on_map_x': 1, 'current_postion_on_map_y': 1,
                                         'username': 1, 'target_exit': 1}))

    return jsonify({
        'positions': res
    })


@app_flask.route("/api/initsystem")
def api_initsystem():
    get_floorplan()
    return jsonify({'register_user_operator': register_user(_username="operator", _operator=True)})


@app_flask.route("/api/checkuser/<username>")
def api_checkuser(username: str):
    assert username == request.view_args['username']
    username = bleach.clean(username)

    if (get_userdb().find_one({"username": username})) is not None:
        return jsonify({'exists': True}), 200
    return jsonify({'exists': False}), 200


@app_flask.route("/api/floorplan")
def api_floorplan():
    fp = get_floorplan()
    return jsonify(fp.properties_to_json())


def register_user(_username: str, _walkfast: int = 5, _climbrange: int = 5, _widthrange: int = 5,
                  _operator: bool = False) -> bool:
    user: DBModelUser.DBModelUser = DBModelUser.DBModelUser()
    user.username = _username
    user.walkfast = _walkfast
    user.climbrange = _climbrange
    user.operator = _operator

    user_j: dict = user.to_json()
    update_result = get_userdb().insert_one(user_j)

    return update_result.acknowledged


@app_flask.route("/api/trigger_emergency")
def api_triggeremergency():
    res = get_userdb().update_many({"exit_reached": True},
                                   {"$set": {
                                       "exit_reached": False,
                                       "target_exit": -1}})

    res = get_userdb().update_many({"username": "operator"},
                                   {"$set": {
                                       "exit_reached": True,
                                       "target_exit": 0}})

    return redirect('/static/map.html?user=operator')


@app_flask.route("/api/register")
def api_register():
    username: str = bleach.clean(request.args.get('username', ''))
    walkfast: int = 5
    climbrange: int = 5
    widthrange: int = 5
    operator: bool = False

    if 'operator' in username:
        operator = True
    try:
        walkfast = int(bleach.clean(request.args.get('walkfast', '5'))) % 10
        climbrange = int(bleach.clean(request.args.get('climbrange', '5'))) % 10
        widthrange = int(bleach.clean(request.args.get('widthrange', '5'))) % 10

    except Exception as e:
        pass

    if not username or len(username) <= 0:
        return jsonify({'error': True, 'reason': 'username is empty'}), 500

    if (get_userdb().find_one({"username": username})) is not None:
        return jsonify({'error': True, 'reason': 'username exists'}), 500

    if register_user(username, walkfast, climbrange, widthrange, operator):
        return redirect('/index.html?user=' + username)

    return jsonify({'success': register_user(username, walkfast, climbrange, widthrange, operator)}), 500


def flask_server_task(_config: dict):
    host: str = _config.get("host", "0.0.0.0")
    port: int = _config.get("port", 5557)
    debug: bool = _config.get("debug", False)
    mongodb: bool = _config.get("mongodb", "mongodb://localhost:27017")
    if not mongodb:
        mongodb = "mongodb://localhost:27017"

    init_db(mongodb)

    # TEST
    f = Floorplan.Floorplan()

    app_flask.config['_config'] = _config
    app_flask.config['MONGO_URI'] = mongodb

    socketio.run(app_flask, host=host, port=port, allow_unsafe_werkzeug=True)


@app_typer.command()
def launch(ctx: typer.Context, port: int = 5557, host: str = "0.0.0.0", debug: bool = False):
    global terminate_flask

    flask_config = {"port": port, "host": host, "debug": debug, "mongodb": os.environ.get('MONGO_IP')}
    flask_server: multiprocessing.Process = multiprocessing.Process(target=flask_server_task, args=(flask_config,))
    flask_server.start()

    print("Editor started. Please open http://{}:{}/".format(host, port))
    time.sleep(3)



    ##### secondary logic  ##########
    #res = list(get_userdb().find({}, {'_id': 0, 'current_postion_on_map_x': 1, 'current_postion_on_map_y': 1,'username': 1, 'target_exit': 1}))

    fp: Floorplan.Floorplan = Floorplan.Floorplan()

    while (not terminate_flask):

        time.sleep(1)
        print(".")

        try:

            db = MongoClient(flask_config['mongodb'])
            userdb = db[MONGO_COLLECTION][MONGO_USERSDB]
            users: [DBModelUser.DBModelUser] = []
            for u in list(userdb.find({'exit_reached': False}, {'_id': 0})):
                users.append(DBModelUser.DBModelUser(u))

            # FIND CORRESPONDING ENTRY IN TO INDEX
            exists: [dict] = ai.compute_new_people_exit_target(users, fp.EXIT_LOCATIONS, fp.loaded_floorplan_matrix)
            for uidx, u in enumerate(users):
                for eidx, e in enumerate(fp.EXIT_LOCATIONS):
                    if e['x'] == exists[uidx]['x'] and e['y'] == exists[uidx]['y']:
                        if users[uidx].target_exit != eidx:
                            users[uidx].target_exit = eidx
                            print("updated user target {} -> {}".format(users[uidx].username, eidx))



            # UPDATE ALL USERS
            for u in users:
                userdb.update_one({"username": u.username},{"$set": {"target_exit": u.target_exit}})
            #print(users)
        except Exception as e:
            raise Exception(str(e))



        #if typer.prompt("Terminate  [Y/n]", 'y') == 'y':
        #    break

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
