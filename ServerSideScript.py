#handle both getting information from POST and retrieval of info from _grab

#needs to be run in one instance of cmd, then run TestScript in another window to conduct tests.

from flask import Flask, request
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

ServerSideScript = Flask(__name__)

@ServerSideScript.route('/')
def default():
    return 'Up and running!'

#@ServerSideScript.route('/handleRequest', methods = ['POST', 'GET'])
#just returns the json of whatever was sent through request
@ServerSideScript.route('/handlePOSTRequest', methods = ['POST'])
def handlePOSTRequest():
    request_data = request.get_json()
    return (request_data)

@ServerSideScript.route('/handleGETRequest', methods = ['GET'])
def handleGETRequest():
    data = {'foo': 'bar', 'running': True}
    return (json.dumps(data))


if __name__ == '__main__':
    ServerSideScript.run(debug = True, host = '0.0.0.0')

