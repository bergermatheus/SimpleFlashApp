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



schema = {
    'type': 'object',
    'properties': {
        'id': {"type": "string","pattern": "^[1-9]\d*$"},
        'name': {'type': 'string',"minLenght":1,"maxLenght":50},
        'email': { "type": "string", "pattern": "^.+@ssys.com.br$"},
        'department': {'type': 'string', "minLenght": 1, "maxLenght":50},
        'salary': {"type": "string","pattern": "^\$?(([1-9]\d{0,2}(\d{3})*)|0)?\.\d{1,2}$"},
        'birth_date': {'type': 'string', "pattern":"^(0?[1-9]|[12][0-9]|3[01])[\/\-](0?[1-9]|1[012])[\/\-]\d{4}$"}
    },
    'required': ['id', 'name', 'email', 'department','salary','birth_date']
}

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token:
            #bearer token
            token = token.split(" ")[1]

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 403

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated


@token_required
def protected():
    return jsonify({'message' : 'This is only available for people with valid tokens.'})

@app.route('/login')
def login():
    auth = request.authorization

    if auth and auth.password == 'password':
        token = jwt.encode({'user' : auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})


@app.route('/employees/',methods =['GET', 'POST'])
@token_required
@expects_json(schema, ignore_for=['GET'])
def employee_list():
    if request.method == 'POST':
        
        employees_details = dict(request.json)
        response = database.create(employees_details)
        return response

    else:
        response = jsonify(database.show_employees_details())
        response.headers.set('Content-Type', 'application/json')
        return response



@app.route('/employees/<ID>', methods = ['GET','PUT','DELETE'])
@expects_json(schema, ignore_for=['GET','DELETE'])
@token_required
def employee_details(ID):
    
    if request.method == 'GET':
        response = jsonify(database.show_employees_details(ID))
        response.headers.set('Content-Type', 'application/json')
        return response  

    elif request.method == 'PUT':
        employees_details = dict(request.json)
        response = jsonify(database.update(employees_details, ID))
        response.headers.set('Content-Type', 'application/json')
        return response  
    elif request.method == 'DELETE':

        response = jsonify(database.delete(ID))
        response.headers.set('Content-Type', 'application/json')
        return response

if __name__ == "__main__":

    # Call database class and create dataset if doesn't exist
    database = Database()

    app.run(host='0.0.0.0', port=80)

