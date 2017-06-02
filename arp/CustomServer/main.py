#!/usr/bin/env python
# coding=utf-8
from flask import *
import sys


app = Flask(__name__)

@app.route("/", methods=['GET'])
def hack():
	return send_from_directory(directory=current_app.root_path, filename='test.apk')
#	return "Hack by cc"

@app.route("/getStatus", methods=['GET'])
def index():
	data = {
		'is_has_new': 1,
		'url': 'http://www.umisen.com:8080/404_new.apk'
	}

	return json.dumps(data)


@app.route("/404_new.apk")
def fuck():
	return send_from_directory(directory=current_app.root_path, filename='test.apk')


@app.route("/hello", methods=['GET'])
def haasdas():
	return "hellasdasdo"


@app.errorhandler(404)
def test(e):
	return send_from_directory(directory=current_app.root_path, filename='test.apk')



app.debug = True
app.run(host='0.0.0.0', port=int(sys.argv[1]), threaded=True)
