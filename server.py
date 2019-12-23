from flask import Flask, send_from_directory, jsonify, request, redirect
from flask_swagger_ui import get_swaggerui_blueprint
from datetime import datetime
from werkzeug.exceptions import BadRequest
from flask_cors import CORS

from datasource.postgresql_source import PostgreSQLDataSource
from json_encoder import MapistoObjectsEncoder
from resources.State import State
from dateutil.parser import parse

datasource = PostgreSQLDataSource()

app = Flask(__name__)
CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'
app.json_encoder = MapistoObjectsEncoder

SWAGGER_URL = '/docs' # URL for exposing Swagger UI (without trailing '/')
OPENAPI_PATH = 'http://localhost:5000/static/openapi.yaml' # Our API url (can of course be a local resource)
API_DOC_URL = 'http://localhost:5000/docs'
# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
SWAGGER_URL, # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
OPENAPI_PATH,
config={ # Swagger UI config overrides
    'app_name': "Mapisto"
    },
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/state', methods=['GET'])
def get_states():
    print('GET STATES')
    try : 
        date = parse(request.args.get('date'))
    except TypeError:
        raise BadRequest('date param not valid')
    res = jsonify(datasource.get_states(date))
    # res = jsonify(['youhou'])
    return res

@app.route('/state', methods=['POST'])
def post_state():
    try :
        validity_start = parse(request.args.get('validity_start'))
        validity_end = parse(request.args.get('validity_end'))
    except TypeError:
        raise BadRequest('Wrong format for validity start or validity end')
    print('start', validity_start)
    print('got json')
    state = State.from_dict(request.json)
    return str(datasource.post_state(state, validity_start, validity_end))

@app.route('/', methods = ['GET'])
def redirectDoc():
    return redirect(API_DOC_URL)