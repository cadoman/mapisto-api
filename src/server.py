import logging
import os
from datetime import datetime
from pprint import pprint
from resources.BoundingBox import BoundingBox
from dateutil.parser import parse, ParserError
from flask import Flask, jsonify, redirect, request, send_from_directory
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.exceptions import BadRequest, InternalServerError, HTTPException

from json_encoder import MapistoObjectsEncoder
from resources.Land import Land
import pytz
from resources.State import State
from land_tag import LandTag
from territory_tag import TerritoryTag
from map_tag import MapTag
from resources.Territory import Territory
from state_tag import StateTag


logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'
app.json_encoder = MapistoObjectsEncoder

SWAGGER_URL = '/docs'  # URL for exposing Swagger UI (without trailing '/')
OPENAPI_PATH = '/static/openapi.yaml'
API_DOC_URL = '/docs'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    OPENAPI_PATH,
    config={  # Swagger UI config overrides
        'app_name': "Mapisto"
    },
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


@app.route('/map', methods=['GET'])
def get_states():
    date = date_from_request('date')
    precision, bbox = extract_map_request()
    return jsonify(MapTag.get(bbox, date, precision))


@app.route('/state', methods=['POST'])
def post_state():
    return jsonify(StateTag.post(State.from_dict(request.json)))

@app.route('/territory', methods=['POST'])
def post_territory():
    return jsonify(TerritoryTag.post(Territory.from_dict(request.json)))


@app.route('/land', methods=['POST'])
def post_land():
    land = Land.from_dict(request.json)
    return jsonify(LandTag.post_land(land))


@app.route('/land', methods=['GET'])
def get_land():
    precision, bbox = extract_map_request()
    return jsonify(LandTag.get_lands(bbox, precision))

@app.route('/', methods=['GET'])
def redirectDoc():
    return redirect(API_DOC_URL)


def date_from_request(*identifiers):
    res = []
    try:
        for id in identifiers:
            res.append(parse(request.args.get(id)).replace(tzinfo=None))
    except (TypeError, ParserError):
        if request.args.get(id) == None:
            raise BadRequest("Missing parameter : "+id)
        else:
            raise BadRequest('Wrong format for '+id+' : '+request.args.get(id))
    if len(res) == 1:
        return res[0]
    else:
        return res


def extract_map_request():
    precision = float(request.args.get('precision_in_km'))
    bbmin_x = int(float(request.args.get('min_x')))
    bbmax_x = int(float(request.args.get('max_x')))
    bbmin_y = int(float(request.args.get('min_y')))
    bbmax_y = int(float(request.args.get('max_y')))
    logging.debug(bbmax_x)
    bbox = BoundingBox(bbmin_x, bbmin_y, bbmax_x-bbmin_x, bbmax_y-bbmin_y)
    return (precision, bbox)


@app.errorhandler(HTTPException)
def handle_http(e: HTTPException):
    return e.description, e.code


@app.errorhandler(Exception)
def handle_500(e):
    logging.info("SERVER ERROR caught : ")
    logging.exception(e)
    return "Internal Server Error", 500
