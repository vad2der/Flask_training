"""
training on Flask
"""

from flask import Flask, request, render_template, flash, url_for
import json
import random

# internal app import
import collectionToPoi

app = Flask(__name__)

class CTP:
    """
    initial emualtion of db
    """
    def __init__(self):
        self.poi_list_1 = [
        {'poi_name': 'Kamennie palatki', 'lat': 56.842912, 'lng': 60.678538, 'type': 'Natural', 'subtype': 'Rock'},
        {'poi_name': 'Shartash ozero', 'lat': 56.847335, 'lng': 60.692927, 'type': 'Natural', 'subtype': 'Waterbody'},
        {'poi_name': 'One more point', 'lat': 56.855640, 'lng': 60.759548,  'type': 'Natural', 'subtype': 'Rock'},
        {'poi_name': 'Local Beach', 'lat': 56.859641, 'lng': 60.726486, 'type': 'Natural', 'subtype': 'Beach'}]

        self.poi_list_2 = [
        {'poi_name': 'Prince`s Island', 'lat': 51.055520, 'lng': -114.070241, 'type': 'Natural', 'subtype': 'Park'},
        {'poi_name': 'Nose Hill', 'lat': 51.105876, 'lng': -114.111217, 'type': 'Natural', 'subtype': 'Park'},
        {'poi_name': 'Baker Park', 'lat': 51.100791, 'lng': -114.219045, 'type': 'Natural', 'subtype': 'Park'},
        {'poi_name': 'Canada Olimpic Park', 'lat': 51.082950, 'lng': -114.215201, 'type': 'Recreation', 'subtype': 'Winter Sport Activity Park'}]

        self.poi_list_3 = [
        {'poi_name': 'Roses City Beach', 'lat': 42.262312,'lng': 3.174488, 'type': 'Natural', 'subtype': 'Beach'},
        {'poi_name': 'Roses Citadel', 'lat': 42.265580, 'lng': 3.170584, 'type': 'Historical', 'subtype': 'Museum'},
        {'poi_name': 'Trinity Castle', 'lat': 42.246668, 'lng': 3.182242, 'type': 'Historical', 'subtype': 'Museum'},
        {'poi_name': 'Dolmen Path (Start)', 'lat': 42.256068, 'lng': 3.197926, 'type': 'Historical', 'subtype': 'Dolmen'}]

        self.poi_collection_list = ['collection 1', 'collection 2', 'collection 3']

    def getPOIlist(self, collection_name):
        if collection_name not in poi_collection_list:
            return ['No such POI collection found']
        if collection_name == 'collection 1':
            return self.poi_list_1
        if collection_name == 'collection 2':
            return self.poi_list_2
        if collection_name == 'collection 3':
            return self.poi_list_3

    def randomPOIlist(self):
        collection_list = [self.poi_list_1, self.poi_list_2, self.poi_list_3, 'current_location']
        return random.choice(collection_list)

ctp = CTP()

# index page
@app.route('/')
def index():
	return render_template('index.html')

# if datatype = 'str'
@app.route('/out/<service>')
def out(service, methods=['GET', 'POST']):
	return '<p>You have requested {}</p><p>Request method is {}</p>'. format(service, request.method)

# if datatype = 'int' - explicitly cast it
@app.route('/number/<int:num>')
def number(num):
	return 'You have entered number{}'. format(str(num))

def getPoiList():
    attempt_poi_collection = request.form.post['poi_collection_choise']
    return ctp.getPOIlist(poi_collection)	

# map page
@app.route('/map/<name>', methods=['GET', 'POST'])
def map(name):
    if name == 'todo':
        return render_template('todo.html', name=name)
    try:
        poi_list = getPOIlist()		
        return render_template('map_view.html', name=name, poi_collection_list=ctp.poi_collection_list, poi_list=poi_list)
    except Exception as e:
        return render_template('map_view.html', name=name, poi_collection_list=ctp.poi_collection_list)
		
# stage01
@app.route('/stage01')
def stage01():
    poi_list = ctp.randomPOIlist()
    return render_template('map_view.html', name='stage01', poi_list=poi_list)
		
if __name__ == "__main__":
	app.run(debug=True)	