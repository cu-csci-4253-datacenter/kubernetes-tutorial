from app import app
from app.forms import BlogForm
import redis
import json

from flask import render_template, flash, redirect, request, make_response, Response

def allMsgs(r):
    data = [ x.decode('utf-8') for x in r.lrange("data", 0, -1) ]
    return Response(json.dumps(data), mimetype="application/json");

@app.route('/')
def root():
        return app.send_static_file('index.html')

@app.route('/message/set/<string:value>', methods=['GET'])
def set(value):
    r = redis.Redis(host=app.config['REDIS_MASTER_SERVICE_HOST'],
                    port=app.config['REDIS_MASTER_SERVICE_PORT'])
    r.rpush("data", value)
    return allMsgs(r)

@app.route('/message/all', methods=['GET'])
def all():
    r = redis.Redis(host=app.config['REDIS_SLAVE_SERVICE_HOST'],
                    port=app.config['REDIS_SLAVE_SERVICE_PORT'])
    return allMsgs(r)

@app.route('/message/erase', methods=['GET'])
def erase():
    r = redis.Redis(host=app.config['REDIS_SLAVE_SERVICE_HOST'],
                    port=app.config['REDIS_SLAVE_SERVICE_PORT'])
    r.delete("data")
    return allMsgs(r)

