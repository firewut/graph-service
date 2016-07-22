import datetime
import pdb

from flask import Flask, jsonify, request, render_template
from pydeform import Client

from functions import *
from settings import *

app = Flask(__name__)

# Deform init
client = Client(host="deform.io")
token_client = client.auth(
    'token',
    auth_key=DEFORM_TOKEN,
    project_id=DEFORM_PROJECT_ID,
)


# # Graph Shema Sync
# token_client.collection.save(
#     data={
#         "_id": GRAPH_COLLECTION_ID,
#         "name": 'Graph',
#         "schema": GRAPH_COLLECTION_SCHEMA
#     }
# )

@app.route("/")
def index_page():
    return render_template('index.html')

@app.route("/graph/", methods=["POST"])
def create_graph():
    """
       Create a graph for a customer
    """
    request_data, error = parseHTTPRequest(request, ["name", "units"])
    if error:
        response = jsonify({
            "error": error
        })
        return response, 422
    
    try:
        # Deform save a graph
        deform_response = token_client.document.create(
            collection=GRAPH_COLLECTION_ID,
            data={
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

   

@app.route("/graph/<graph_id>/", methods=["POST"])
def push_point_to_graph(graph_id):
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
            operation.update({
                "date": request_data["date"]
            })

        deform_response = token_client.documents.update(
            collection=GRAPH_COLLECTION_ID,
            filter={
                "_id": graph_id
            },
            operation=operation
        )
        response = jsonify({
            "point": deform_response
        })
        return response, 201
    except Exception as e:
        response = jsonify({
            "error": str(e)
        })
        return response, 422
        

@app.route("/graph/<graph_id>/", methods=["GET"])
def get_graph(graph_id):
    """
        Get a graph by Identifier
    """
    graph = token_client.document.get(
        collection=GRAPH_COLLECTION_ID,
        identity=graph_id,
    )
    return render_template('chart.html', graph=graph)


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=8888
    )