from django.http import HttpResponse, HttpRequest
import json
import logging
logger = logging.getLogger('django')
import datetime

def HttpResponseJson(payload):
    jsonData = json.dumps(payload, cls=JSONEncoder)
    response = HttpResponse(
            jsonData,
            content_type="application/json",
    )
    response["Access-Control-Allow-Origin"] = "*"
    return response

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self,obj)
        
def ResponseData(data, code=200, **kwargs):
    payload = {
        "code": code,
        "msg": "success",
        "data": data,
    }
    return HttpResponseJson(payload)

def ResponseError(msg, code=500, **kwargs):
    payload = {
        "code": code,
        "msg": msg,
    }
    payload.update(kwargs)
    return HttpResponseJson(payload)