# Vars and Constants
AVAILABLE_CONTENT_TYPES = [
    "application/json",
    "application/x-www-form-urlencoded"
]

DEFORM_PROJECT_ID = 'my-steam-graph'
DEFORM_TOKEN = 'VWgIyzOsDDjqTGMG'

GRAPH_COLLECTION_ID = 'graphs'
GRAPH_COLLECTION_NAME = 'graphs'
GRAPH_COLLECTION_SCHEMA = {
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
#