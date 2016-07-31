import datetime
import dateutil
from dateutil.parser import *
from dateutil.tz import *

import settings


def parseDate(string_date):
    parsed_date = dateutil.parser.parse(string_date, ignoretz=False)
    return parsed_date

def convertToUTC(datetime_instance):
    datetime_instance.astimezone(tzutc())
    return datetime_instance

def parseHTTPRequest(request, keys):
    """
       Parse an HTTP request
    """
    data = {
        "date": datetime.datetime.utcnow()
    }

    proceed = False
    for content_type in settings.AVAILABLE_CONTENT_TYPES:
        if content_type in request.headers.get("Content-Type"):
            proceed = True
    
    if proceed == False:
        return None, "`application/json` or `x-www-form-urlencoded` are supported"

    if "application/json" in request.headers.get("Content-Type"):
        json_request = request.get_json()
        if "name" in json_request:
            data["name"] = json_request["name"]
        else:
            if "name" in keys:
                return None, "name required"
        
        if "units" in json_request:
            data["units"] = json_request["units"]
        else:
            if "units" in keys:
                return None, "units required"
        
        if "date" in json_request:
            # Step 1 - parse a datetime
            parsed_date = parseDate(json_request["date"])
            # Step 2 - convert to UTC
            data["date"] = convertToUTC(parsed_date)
        else:
            if "date" in keys:
                return None, "date required"

        if "unixtimestamp" in json_request:
            date = datetime.datetime.fromtimestamp(json_request['unixtimestamp'])
            data["date"] = date
        else:
            if "unixtimestamp" in keys:
                return None, "unixtimestamp required"
        
        if "value" in json_request:
            data["value"] = json_request["value"]
        else:
            if "value" in keys:
                return None, "value required"
    
    if "x-www-form-urlencoded" in request.headers.get("Content-Type"):
        if "name" in request.form:
            data["name"] = request.form["name"]
        else:
            if "name" in keys:
                return None, "name required"
        
        if "units" in request.form:
            data["units"] = request.form["units"]
        else:
            if "units" in keys:
                return None, "units required"
        
        if "date" in request.form:
            # Step 1 - parse a datetime
            parsed_date = parseDate(request.form["date"])
            # Step 2 - convert to UTC
            data["date"] = convertToUTC(parsed_date)
        else:
            if "date" in keys:
                return None, "date required"

        if "unixtimestamp" in request.form:
            date = datetime.datetime.fromtimestamp(request.form['unixtimestamp'])
            data["date"] = date
        else:
            if "unixtimestamp" in keys:
                return None, "unixtimestamp required"            
        
        if "value" in request.form:
            data["value"] = float(request.form["value"])
        else:
            if "value" in keys:
                return None, "value required"
    
    return data, None