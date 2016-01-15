"""
training on Flask
"""

from flask import Flask, request, render_template, flash, url_for
import json

# internal app import
import collectionToPoi

app = Flask(__name__)

class CTP():
    """
    initial emualtion of db
    """
    poi_collection_list = ['collection 1', 'collection 2', 'collection 3']

    poi_list_1 = [
    {'poi_name': 'Kamennie palatki', 'lat': 56.842912, 'lng': 60.678538, 'type': 'Natural', 'subtype': 'Rock'},
    {'poi_name': 'Shartash ozero', 'lat': 56.847335, 'lng': 60.692927, 'type': 'Natural', 'subtype': 'Waterbody'},
    {'poi_name': 'One more point', 'lat': 56.855640, 'lng': 60.759548,  'type': 'Natural', 'subtype': 'Rock'},
    {'poi_name': 'Local Beach', 'lat': 56.859641, 'lng': 60.726486, 'type': 'Natural', 'subtype': 'Beach'}]

    poi_list_2 = [
    {'poi_name': 'Kamennie palatki', 'lat': 56.842912, 'lng': 60.678538, 'type': 'Natural', 'subtype': 'Rock'},
    {'poi_name': 'Shartash ozero', 'lat': 56.847335, 'lng': 60.692927, 'type': 'Natural', 'subtype': 'Waterbody'},
    {'poi_name': 'One more point', 'lat': 56.855640, 'lng': 60.759548,  'type': 'Natural', 'subtype': 'Rock'},
    {'poi_name': 'Local Beach', 'lat': 56.859641, 'lng': 60.726486, 'type': 'Natural', 'subtype': 'Beach'}]

    poi_list_3 = [
    {'poi_name': 'Kamennie palatki', 'lat': 56.842912, 'lng': 60.678538, 'type': 'Natural', 'subtype': 'Rock'},
    {'poi_name': 'Shartash ozero', 'lat': 56.847335, 'lng': 60.692927, 'type': 'Natural', 'subtype': 'Waterbody'},
    {'poi_name': 'One more point', 'lat': 56.855640, 'lng': 60.759548,  'type': 'Natural', 'subtype': 'Rock'},
    {'poi_name': 'Local Beach', 'lat': 56.859641, 'lng': 60.726486, 'type': 'Natural', 'subtype': 'Beach'}]

    def getPOIlist(collection_name):
        if collection_name not in poi_collection_list:
            return ['No such POI collection found']
        if collection_name == 'collection 1':
            return poi_list_1
        if collection_name == 'collection 2':
            return poi_list_2
        if collection_name == 'collection 3':
            return poi_list_3		
ctp = CTP()
# index page
@app.route('/')
def index():
	return '<h2>This is the home page</h2>'

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
    try:        
        poi_list = getPOIlist()		
        return render_template('map_view.html', name=name, poi_collection_list=ctp.poi_collection_list, poi_list=poi_list)
    except Exception as e:
        return render_template('map_view.html', name=name, poi_collection_list=ctp.poi_collection_list)
		
    if name == 'todo':
        return render_template('todo.html', name=name)


		
if __name__ == "__main__":
	app.run(debug=True)	