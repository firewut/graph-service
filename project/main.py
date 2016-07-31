import datetime
import os  
import pytz
import logging
import random
import re
import string
import tempfile

from functions import *
from raven.contrib.flask import Sentry
from flask import Flask, jsonify, request, render_template, send_from_directory
from pydeform import Client
import schemas
import settings

import requests.packages.urllib3

requests.packages.urllib3.disable_warnings()

host = os.getenv('IP', '0.0.0.0')  
port = int(os.getenv('PORT', 8080))

START_TIME = datetime.datetime.utcnow()
DATES=[
    START_TIME.strftime("%Y-%m-%dT%H:%M:%S.")+START_TIME.strftime("%f")[0:3]+"+00",
]

for i in xrange(5):
    new_date = START_TIME + datetime.timedelta(seconds=1*(i+1))
    DATES.append(
        new_date.strftime("%Y-%m-%dT%H:%M:%S.")+new_date.strftime("%f")[0:3]+"+03",
    )

app = Flask(__name__)

# Deform init
client = Client(host="deform.io")
token_client = client.auth(
    'token',
    auth_key=settings.DEFORM_TOKEN,
    project_id=settings.DEFORM_PROJECT_ID,
)
collections = [
    schemas.graph_schema
]

for collection in collections:
    try:
        token_client.collection.save(data=collection)
    except Exception as e:
        print(str(e))


app.config['token_client'] = token_client

@app.route("/", methods=["GET"])
def index():
    return render_template(
        'index.html', 
        DATES=DATES,
        VIRTUAL_HOST=os.getenv('VIRTUAL_HOST', "%s:%d" % (host, port)),
        EXAMPLE_GRAPH_DOC_ID=os.getenv('EXAMPLE_GRAPH_DOC_ID', settings.EXAMPLE_GRAPH_ID)
    )

@app.route("/graph/", methods=["POST"])
def graph_create():
    request_data, error = parseHTTPRequest(request, ["name", "units"])
    if error:
        response = jsonify({
            "error": error
        })
        return response, 422
    
    try:
        # Deform save a graph
        deform_response = token_client.document.create(
            collection=schemas.GRAPH_COLLECTION_ID,
            data={
                "_id": ''.join(random.choice(string.ascii_letters) for x in range(40)),
                "name": request_data["name"],
                "units": request_data["units"]
            },
        )
        
        CREATED_GRAPH_KEY = deform_response.get('_id')
        response = jsonify({
            "graph-key": CREATED_GRAPH_KEY
        })
        return response, 201
    except Exception as e:
        response = jsonify({
            "error": str(e)
        })
        return response, 422


@app.route("/graph/<graph_id>/", methods=["GET"])
def graph_get(graph_id):
    response = token_client.document.get(
        collection=schemas.GRAPH_COLLECTION_ID,
        identity=graph_id,
    )

    return render_template(
        'graph.html', 
        graph=response, 
    )

@app.route("/graph/<graph_id>.json/", methods=["GET"])
def graph_get_chart(graph_id):
    try:
        response = token_client.document.get(
            collection=schemas.GRAPH_COLLECTION_ID,
            identity=graph_id,
        )
        return jsonify(response)
    except:
     return page_not_found(None)

@app.route("/graph/<graph_id>/", methods=["POST", "PUT"])
def graph_push_point(graph_id):
    """
        Push points to graph
    """
    request_data, error = parseHTTPRequest(request, ["value"])
    if error:
        response = jsonify({
            "error": error
        })
        return response, 422
    
    try:
        # data = {"value":10, "date": datetime.datetime.utcnow()}
        operation = {
            "$push": {
                "points": {
                    "value": request_data["value"],
                }
            }
        }
        if "date" in request_data:
            operation["$push"]["points"].update({
                "date": request_data["date"]
            })

        deform_response = token_client.documents.update(
            collection=schemas.GRAPH_COLLECTION_ID,
            filter={
                "_id": graph_id
            },
            operation=operation
        )
        response = jsonify({
            "point": operation["$push"]["points"]
        })
        return response, 201
    except Exception as e:
        response = jsonify({
            "error": str(e)
        })
        return response, 422


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    sentry = Sentry(app, dsn=os.getenv("SENTRY_DSN"))  
    sentry_errors_log = logging.getLogger("sentry.errors")
    sentry_errors_log.addHandler(logging.StreamHandler())

    app.run(  
        host=host,
        port=port,
        debug=os.getenv("MODE")!="prod"
    )