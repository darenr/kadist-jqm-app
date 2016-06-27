#!/usr/bin/env python
# -*- coding: utf-8 -*--

__author__ = 'daren race'

from flask import Flask, render_template, request, Response, jsonify, redirect, abort, current_app
from functools import wraps
from flask.ext.compress import Compress
import codecs
import json
import sys
import collections
from flask.ext.cors import CORS

project_name = 'Kadist Mobile'

app = Flask(__name__)
Compress(app)
CORS(app)

# approot = "http://polar-island-6673.herokuapp.com"
approot = "http://0.0.0.0:5000"

site = json.loads('''
{
	"pages": [{
		"title": "home",
		"img": "/static/images/logo.gif",
		"id": "home",
		"sections": [{
			"title": "Kadist Locations:",
      "icon": "pin",
			"list": [{
				"img": "/static/images/kadist-sf.jpg",
				"title": "San Francisco",
				"html": "<p>3295 20th Street, (415) 738-8668</p>",
				"link": "#kadist-sf"
			}, {
				"img": "/static/images/kadist-paris.jpg",
				"title": "Paris",
				"html": "<p>19bis/21 rue des Trois Frères, +33 1 42 51 83 49</p>",
				"link": "#kadist-paris"
			}, {
				"img": "/static/images/kadist-colombia.jpg",
				"title": "Colombia",
				"link": "#kadist-columnbia"
			}]
		}]
	}, {
		"title": "Kadist San Francisco",
		"img": "/static/images/kadist-sf.jpg",
		"id": "kadist-sf",
		"sections": [{
			"title": "SF Events:",
      "icon": "calendar",
			"list": [{
				"img": "/static/images/event-1.jpg",
				"title": "ANTHONY DISCENZA: THE REPOSITORY OF THE FUTURE",
				"html": "SAN FRANCISCO 6.25.2016",
				"link": "http://kadist.org/en/programs/all/2473"
			}, {
				"img": "/static/images/event-2.jpg",
				"title": "MALIK GAINES ON SYLVESTER",
				"html": "SAN FRANCISCO 6.15.2016",
				"link": "http://kadist.org/en/programs/all/2472"
			}, {
				"img": "/static/images/event-3.png",
				"title": "CARLOS AMORALES: CYCLOPE",
				"html": "SAN FRANCISCO 4.30.2016",
				"link": "http://kadist.org/en/programs/all/2462"
			}]
		}, {
			"title": "SF Exhibitions:",
      "icon": "calendar",
			"list": [{
				"img": "/static/images/exhib-1.jpg",
				"title": "SHOOSHIE SULAIMAN",
				"html": "Opening reception: Friday, June 10 from 6 to 9pm<br>Exhibition from June 11 to July 31, 2016",
				"link": "http://kadist.org/en/programs/all/2464"
			}, {
				"img": "/static/images/exhib-2.jpg",
				"title": "YIN-JU CHEN: EXTRASTELLAR EVALUATIONS",
				"html": "Wednesday, May 11, 6-9pm",
				"link": "http://kadist.org/en/programs/all/2466"
			}]
		}, {
			"title": "SF About:",
     "list": [{
     				"img": "/static/images/k.jpg",
            "title": "About Kadist Foundation",
            "link": "#about"
     }]
		}]
	}]
}
''')


@app.route('/', methods=['GET', 'OPTIONS'])
def homepage():
    return render_template("index.html",
                           title=project_name,
                           approot=approot,
                           project_name=project_name,
                           pages=site['pages'])


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', threaded=True,
            processes=1, port=5000, passthrough_errors=True)
