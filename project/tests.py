# -*- coding: utf-8 -*-
from main import app

import random
import datetime
import json
import nose
import unittest

from flask import Flask
from nose.tools import * # assert_equals, assert_greater, assert_in


class FlaskTestClientProxy(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.local_http_client = self.app.test_client()

    ####
    def test_create_a_demo_graph(self):
        data = {
            "name": "demo graph",
            "units": "ms"
        }
        r_view = self.local_http_client.post('/graph/',
            data=json.dumps(data),
            content_type='application/json'
        )
        assert_equals(r_view.status_code, 201)
        assert_greater(len(r_view.data), 0)
        
        json_response = json.loads(r_view.data)
        assert_in("graph-key", json_response)
        assert_equal(len(json_response["graph-key"]), 24)

        graph_key = json_response["graph-key"]

        random_pings = []
        for i in xrange(1,5):
            random_ping = "%s.%s" % (random.randint(0, 20), random.randint(0, 20))
            random_pings.append(
                float(random_ping)
            )

        print(graph_key)
        for ping in random_pings:
            points_data = {
                "value": ping,
            }
            r_view = self.local_http_client.post('/graph/%s/' % graph_key,
                data=json.dumps(points_data),
                content_type='application/json'
            )
            assert_equals(r_view.status_code, 201)
            json_response = json.loads(r_view.data)
            assert_in("point", json_response)
            assert_in("value", json_response["point"])
            assert_in(ping, json_response["point"]["value"])

    
    #####
    def test_graph_creation_invalid_content_type(self):
        data = {
            "name": "my test graph",
            "units": "ms"
        }
        r_view = self.local_http_client.post('/graph/',
            data=json.dumps(data),
            content_type='invalid/content-type'
        )
        assert_equals(r_view.status_code, 422)
        assert_greater(len(r_view.data), 0)
        json_response = json.loads(r_view.data)
        assert_in("error", json_response)
        assert_equals(json_response["error"], '`application/json` or `x-www-form-urlencoded` are supported')


    """
        Testing "application/json""
    """
    def test_graph_creation_json(self):
        data = {
            "name": "my test graph",
            "units": "ms"
        }
        r_view = self.local_http_client.post('/graph/',
            data=json.dumps(data),
            content_type='application/json'
        )
        assert_equals(r_view.status_code, 201)
        assert_greater(len(r_view.data), 0)
        
        json_response = json.loads(r_view.data)
        assert_in("graph-key", json_response)
        assert_equal(len(json_response["graph-key"]), 24)

    def test_graph_creation_incorrect_data_units_json(self):
        data = {
            "name": "my test graph",
        }
        r_view = self.local_http_client.post('/graph/',
            data=json.dumps(data),
            content_type='application/json'
        )
        assert_equals(r_view.status_code, 422)
        assert_greater(len(r_view.data), 0)
        json_response = json.loads(r_view.data)
        assert_in("error", json_response)
        assert_equals(json_response["error"], 'units required')

    def test_graph_creation_incorrect_data_name_json(self):
        data = {
            "units": "seconds",
        }
        r_view = self.local_http_client.post('/graph/',
            data=json.dumps(data),
            content_type='application/json'
        )
        assert_equals(r_view.status_code, 422)
        assert_greater(len(r_view.data), 0)
        json_response = json.loads(r_view.data)
        assert_in("error", json_response)
        assert_equals(json_response["error"], 'name required')
    
    def test_graph_point_push(self):
        data = {
            "name": "my test graph",
            "units": "ms"
        }
        r_view = self.local_http_client.post('/graph/',
            data=json.dumps(data),
            content_type='application/json'
        )
        assert_equals(r_view.status_code, 201)
        assert_greater(len(r_view.data), 0)
        
        json_response = json.loads(r_view.data)
        assert_in("graph-key", json_response)
        assert_equal(len(json_response["graph-key"]), 24)

        graph_key = json_response["graph-key"]
        points_data = {
            "value": 7
        }
        r_view = self.local_http_client.post('/graph/%s/' % graph_key,
            data=json.dumps(points_data),
            content_type='application/json'
        )
        assert_equals(r_view.status_code, 201)
        json_response = json.loads(r_view.data)
        assert_in("point", json_response)
        assert_in("value", json_response["point"])
        assert_in(7, json_response["point"]["value"])

    def test_graph_point_push_json(self):
        data = {
            "name": "my test graph",
            "units": "ms"
        }
        r_view = self.local_http_client.post('/graph/',
            data=json.dumps(data),
            content_type='application/json'
        )
        assert_equals(r_view.status_code, 201)
        assert_greater(len(r_view.data), 0)
        
        json_response = json.loads(r_view.data)
        assert_in("graph-key", json_response)
        assert_equal(len(json_response["graph-key"]), 24)

        graph_key = json_response["graph-key"]
        points_data = {
            "value": 7,
            "date": "%s" % datetime.datetime.now()
        }
        r_view = self.local_http_client.post('/graph/%s/' % graph_key,
            data=json.dumps(points_data),
            content_type='application/json'
        )
        assert_equals(r_view.status_code, 201)
        json_response = json.loads(r_view.data)
        assert_in("point", json_response)
        assert_in("value", json_response["point"])
        assert_in(7, json_response["point"]["value"])

    """
        Testing "x-www-form-urlencoded"
    """
    def test_graph_creation_x_www(self):
        data = {
            "name": "my test graph",
            "units": "ms"
        }
        r_view = self.local_http_client.post('/graph/',
            data=data,
            content_type='application/x-www-form-urlencoded'
        )
        assert_equals(r_view.status_code, 201)
        assert_greater(len(r_view.data), 0)
        
        json_response = json.loads(r_view.data)
        assert_in("graph-key", json_response)
        assert_equal(len(json_response["graph-key"]), 24)

    def test_graph_creation_incorrect_data_units_x_www(self):
        data = {
            "name": "my test graph"
        }
        r_view = self.local_http_client.post('/graph/',
            data=data,
            content_type='application/x-www-form-urlencoded'
        )
        assert_equals(r_view.status_code, 422)
        assert_greater(len(r_view.data), 0)
        json_response = json.loads(r_view.data)
        assert_in("error", json_response)
        assert_equals(json_response["error"], 'units required')        
    
    def test_graph_creation_incorrect_data_name_x_www(self):
        data = {
            "units": "ms"
        }
        r_view = self.local_http_client.post('/graph/',
            data=data,
            content_type='application/x-www-form-urlencoded'
        )
        assert_equals(r_view.status_code, 422)
        assert_greater(len(r_view.data), 0)
        json_response = json.loads(r_view.data)
        assert_in("error", json_response)
        assert_equals(json_response["error"], 'name required')   
    
    def test_graph_point_push(self):
        data = {
            "name": "my test graph",
            "units": "ms"
        }
        r_view = self.local_http_client.post('/graph/',
            data=data,
            content_type='application/x-www-form-urlencoded'
        )
        assert_equals(r_view.status_code, 201)
        assert_greater(len(r_view.data), 0)
        
        json_response = json.loads(r_view.data)
        assert_in("graph-key", json_response)
        assert_equal(len(json_response["graph-key"]), 24)

        graph_key = json_response["graph-key"]
        points_data = {
            "value": 7
        }
        r_view = self.local_http_client.post('/graph/%s/' % graph_key,
            data=points_data,
            content_type='application/x-www-form-urlencoded'
        )
        assert_equals(r_view.status_code, 201)
        json_response = json.loads(r_view.data)
        assert_in("point", json_response)
        assert_in("value", json_response["point"])
        assert_in(7, json_response["point"]["value"])
        

    def test_graph_point_push_x_www(self):
        data = {
            "name": "my test graph",
            "units": "ms"
        }
        r_view = self.local_http_client.post('/graph/',
            data=data,
            content_type='application/x-www-form-urlencoded'
        )
        assert_equals(r_view.status_code, 201)
        assert_greater(len(r_view.data), 0)
        
        json_response = json.loads(r_view.data)
        assert_in("graph-key", json_response)
        assert_equal(len(json_response["graph-key"]), 24)

        graph_key = json_response["graph-key"]
        points_data = {
            "value": 7,
            "date": "%s" % datetime.datetime.now()
        }
        r_view = self.local_http_client.post('/graph/%s/' % graph_key,
            data=points_data,
            content_type='application/x-www-form-urlencodedjson'
        )
        assert_equals(r_view.status_code, 201)
        json_response = json.loads(r_view.data)
        assert_in("point", json_response)
        assert_in("value", json_response["point"])
        assert_in(7, json_response["point"]["value"])



    # def tearDown(self):
    #     pass

if __name__ == '__main__':
    unittest.main()