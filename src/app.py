from flask import Flask, make_response
from flask import request, jsonify
from flask_expects_json import expects_json
import jwt 
import datetime
from functools import wraps 
from db_functions import Database
import os

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['JSON_SORT_KEYS'] = False
app.secret_key = os.environ.get('SECRET_KEY','dev')

@app.route('/login')
def login():
    auth = request.authorization

    if auth and auth.password == 'password':
        token = jwt.encode({'user' : auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})
if __name__ == "__main__":


    app.run(host='0.0.0.0', port=80)

