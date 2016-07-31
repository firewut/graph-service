GRAPH_COLLECTION_ID = 'graphs'
GRAPH_COLLECTION_NAME = 'graphs'
GRAPH_SCHEMA = {
    "type": "object",
    "description": "Graph Schema",
    "properties": {
        "name": {
            "type": "string"
        },
        "units": {
            "type": "string",
            "required": True
        },
        "points": {
            "type": "array",
            "items": {
                "type": "object",
                "description": "point of a graph",
                "properties": {
                    "value": {
                    "type": "number",
                    "description": "value of a point"
                    },
                    "date": {
                        "type": "datetime",
                        "description": "point date"
                    }
                }
            }
        },
        "date": {
            "type": "datetime",
            "description": "date when graph was created"
        }
    }
}

graph_schema = {
    "_id": GRAPH_COLLECTION_ID,
    "name": GRAPH_COLLECTION_NAME,
    "schema": GRAPH_SCHEMA,
    "indexes": [
        {
            "type": "simple",
            "property": "points"
        },
        {
            "type": "simple",
            "property": "date"
        },
    ]
}