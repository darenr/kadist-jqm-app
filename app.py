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

project_name = 'Kadist'
project_version = '05'

app = Flask(__name__)
Compress(app)
CORS(app)

# approot = "http://polar-island-6673.herokuapp.com"
approot = "http://0.0.0.0:5000"

site = json.loads('''
{
	"pages": [{
		"title": "home",
		"img": "/static/images/kadist-logo.jpg",
		"id": "home",
		"sections": [{
			"title": "Kadist Locations:",
      "icon": "pin",
			"list": [{
				"img": "/static/images/united-states-of-america-flag-square-icon-256.png",
				"title": "San Francisco",
				"html": "<p>3295 20th Street<br>(415) 738-8668</p>",
				"link": "#kadist-sf"
			}, {
				"img": "/static/images/france-flag-square-icon-256.png",
				"title": "Paris",
				"html": "<p>19bis/21 rue des Trois Frères<br>+33 1 42 51 83 49</p>",
				"link": "#kadist-paris"
			}, {
				"img": "/static/images/colombia-flag-square-icon-256.png",
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
				"link": "#work2473"
			}, {
				"img": "/static/images/event-2.jpg",
				"title": "MALIK GAINES ON SYLVESTER",
				"html": "SAN FRANCISCO 6.15.2016",
				"link": "#work2472"
			}, {
				"img": "/static/images/event-3.png",
				"title": "CARLOS AMORALES: CYCLOPE",
				"html": "SAN FRANCISCO 4.30.2016",
				"link": "#work2462"
			}]
		}, {
			"title": "SF Exhibitions:",
      "icon": "calendar",
			"list": [{
				"img": "/static/images/exhib-1.jpg",
				"title": "SHOOSHIE SULAIMAN",
				"html": "Opening reception: Friday, June 10 from 6 to 9pm<br>Exhibition from June 11 to July 31, 2016",
				"link": "#work2464"
			}, {
				"img": "/static/images/exhib-2.jpg",
				"title": "YIN-JU CHEN: EXTRASTELLAR EVALUATIONS",
				"html": "Wednesday, May 11, 6-9pm",
				"link": "#work2466"
			}]
		}, {
			"title": "SF About:",
      "icon": "info",
      "list": [{
     				"img": "/static/images/k.jpg",
            "title": "About Kadist Foundation",
						"html": "maps, info, staff",
            "link": "#about"
     }]
		}
	 ]
	}]
}
''')

works = json.loads('''
{
	"pages": {
		"work2473": {
			"title": "ANTHONY DISCENZA: THE REPOSITORY OF THE FUTURE",
			"img": ["/static/images/works/2473.jpg"],
			"html": ["The Repository is a proposed speculative research entity intended to track and analyze new developments in the future as they unfold. By identifying the future as a site of active construction, The Repository hopes to identify emergent narratives of the present which may not be otherwise apprehensible. On Saturday June 25th, Kadist hosts the first working session of The Repository to collectively review a selection of past, obsolete or present constructions of the future while introducing The Repository’s proposed strategies for implementation and development to come."]
		},
		"work2472": {
			"title": "MALIK GAINES ON SYLVESTER",
			"img": ["/static/images/works/2472.jpg"],
			"html": [
				"Malik Gaines discusses Sylvester, who was a member of San Francisco's Cockettes troupe before becoming a disco star of the 1970s. Sylvester combined a queer performance of gender with signs and sounds of musical virtuosity, making a unique contribution to his era. Gaines considers Sylvester among other radical performers in his forthcoming book ",
				"Excesses of the Sixties: Black Performance on the Outskirts of the Left.",
				"Malik Gaines is an artist and writer based in New York. He is a member of the performance group My Barbarian and assistant professor of Performance Studies at NYU's Tisch School of the Arts.",
				"This program is made possible in part by Headlands Center for the Arts, where Gaines is currently artist in residence."
			]
		},
		"work2462": {
			"title": "CARLOS AMORALES: CYCLOPE",
			"img": [
				"/static/images/works/2462.png"
			],
			"html": [
				"For the last two years, Mexico-City based artist Carlos Amorales has been developing a series of works in relation to what he calls 'Cubismo ideológico'. Three films and a manifesto arose from this investigaton and Cyclope at Kadist marks the US premier of the first performance in this 'Cubismo ideológico' series. Philippe Eustachon, Enrique Arriaga, and special guest Elsa-Louise Manceaux join the artist in this percussive and spoken word concert."
			]
		},
		"work2464": {
			"title": "SHOOSHIE SULAIMAN",
			"img": [
				"/static/images/works/2464a.jpg",
				"/static/images/works/2464b.jpg",
				"/static/images/works/2464c.jpg",
				"/static/images/works/2464d.jpg",
				"/static/images/works/2464e.jpg",
				"/static/images/works/2464f.jpg",
				"/static/images/works/2464g.jpg",
				"/static/images/works/2464h.jpg"
			],
			"html": ["Spring artist in residency, Shooshie Sulaiman is part of the Kadist collection. Her first solo exhibition in Europe, will open at Kadist Paris on June 10, 2016.",
				"The work of Malaysian artist Shooshie Sulaiman develops in various forms, from site-specific installations and outdoor performances, to a daily practice of writing and drawing. She started her artistic practice during the 1990’s, when Malaysia opened to the free market and became more international, not without psychological impact on its society. Thus, her work can be perceived as a precious testimony of what the country went through, an emotional landscape of what happened politically and socially during that time.",
				"Shooshie Sulaiman commits to two complementary practices, her personal work and her collective projects, which aim for a solidary artistic community. Challenging the demarcations between the private and public spheres, the commercial and non-commercial, she created a gallery in 2006, named 12. When she considered that the model was inappropiate, she started a platform for artists, MAIX (Malaysia Artists’ Intention Experiment), in 2014. These initiatives reflect her main concerns of sharing spaces and experiences to develop a deeper collective awareness, challenging the institution by trying to shape one able to face every type of artistic experiment such as ephemeral art.",
				"Next to writing and drawing, Shooshie Sulaiman practices gardening on a daily basis in Kuala Lumpur.  In France, the tradition of gardening has turned it into a codified art, characterized by historical movements, which mirror the spirit of the times. How can an activity that she considered as natural as drinking water be celebrated as an art? Is an artist a gardener, or is a gardener an artist? Wondering if a scientific experiment could be aesthetic, she started by creating a new rose, grafting two botanic species: a rose coming from the bush growing on her mother’s grave in Johor State, the other one from a farm nearby Paris. Given that earth is just earth, and biosciences can create and clone exotica, why would a Malay Mawar (“rose” in Malay) marrying a French Rose not be singularly original and successful?",
				"n Kadist’s outdoor spaces, where the “marriage” took place, she has created not only a fusion, a bridge between two cultures, but a living exhibition which asks for care. In parallel, Shooshie Sulaiman involved participants in the dissemination of her drawings around Parisian gardens, a protocol that she calls « Planting Drawings ». This research on gardening extends the framework of the exhibition itself, it nourishes a long-term project that the artist is developing with her community through the acquisition of a plot of land in the forest two and a half hours away from Kuala Lumpur- a vision of an ecosystem in which gardening could provide a living. Can an aesthetic experiment in the long run define a model of sustainability?"
			],
			"videos": [
				 "<iframe width=\\"100%\\" height=\\"315\\" src=\\"https://www.youtube.com/embed/N61kCnu-UyM\\" frameborder=\\"0\\" allowfullscreen></iframe>"
			]
		},
		"work2466": {
			"title": "YIN-JU CHEN: EXTRASTELLAR EVALUATIONS",
			"img": ["/static/images/works/2466.jpg"],
			"html": [
				"I Adama",
				"Greetings humans.",
				"I High Priest of survivor civilization.",
				"Lemuria alive beneath Mount Shasta California.",
				"Mother land observe.",
				"Geometry language.",
				"Past learn, present see, future review.",
				"Come",
				"Adama"
			]
		}
	}
}
''')

@app.route('/', methods=['GET', 'OPTIONS'])
def homepage():
    return render_template("index.html",
                           title=project_name,
                           approot=approot,
                           project_name=project_name,
													 version=project_version,
                           pages=site['pages'],
													 works=works['pages'])


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', threaded=True,
            processes=1, port=5000, passthrough_errors=True)
