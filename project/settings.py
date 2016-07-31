import os

# Vars and Constants
AVAILABLE_CONTENT_TYPES = [
    "application/json",
    "application/x-www-form-urlencoded"
]

DEFORM_PROJECT_ID = os.getenv('DEFORM_PROJECT_ID', 'my-steam-graph')
DEFORM_TOKEN = os.getenv('DEFORM_TOKEN', 'VWgIyzOsDDjqTGMG')
EXAMPLE_GRAPH_ID='CUxHCtsjezgWDNIIuDbmDJHqosjxuQRqbokygpHG'
