"""
training on Flask
"""

from flask import Flask, request, render_template, flash, url_for, jsonify
import random
from flask_restful import reqparse, abort, Api, Resource, fields

app = Flask(__name__)
api = Api(app)

api_out = {}


class Collection(Resource):
    """
    initial emualtion of db
    """
    def __init__(self):
        self.poi_list_1 = {"col_id": 111, "name": "Collection 1", "poi_ids": [9101, 9102, 9103, 9104]}
        self.poi_list_2 = {"col_id": 222, "name": "Collection 2", "poi_ids": [9201, 9202, 9203, 9204]}
        self.poi_list_3 = {"col_id": 333, "name": "Collection 3", "poi_ids": [9301, 9302, 9303, 9304]}
        self.poi_list_4 = {"col_id": 444, "name": "Collection 4", "poi_ids": []}
        self.poi_collection_list = [self.poi_list_1, self.poi_list_2, self.poi_list_3, self.poi_list_4]

        self.poi_col_fields = {
        'col_id': fields.Integer,
        'name': fields.String,
        'date_created': fields.DateTime,
        'date_updated': fields.DateTime,
        'poi_ids': fields.Integer,
        }

    def createNewCollection(self, new_collection):
        next_id = int(self.poi_collection_list[-1]["col_id"]) + 1
        new_collection["col_id"] = next_id
        new_collection["poi_ids"] = []
        self.poi_collection_list.append(new_collection)
        return self.poi_collection_list[-1]

    def get(self):
        return self.poi_collection_list

    def randomPOIlist(self):
        the_collection = random.choice(self.poi_collection_list)        
        pois = POIs()
        return pois.getListOfPOIByID(the_collection['poi_ids'])

    def put(self):
        pass

    def post(self):
        new_collection = {}
        for field in self.poi_col_fields:
            new_collection[field] = request.form.get(field)
        the_new_collection = self.createNewCollection(new_collection)
        return the_new_collection, 201
 
    def delete(self):
        pass


class POIs(Resource):
    """
    initial emualtion of db
    """
    def __init__(self):
        self.all_pois = [
        {'poi_id': 9101, 'poi_name': 'Kamennie palatki', 'lat': 56.842912, 'lng': 60.678538, 'type': 'Natural', 'subtype': 'Rock'},
        {'poi_id': 9102, 'poi_name': 'Shartash ozero', 'lat': 56.847335, 'lng': 60.692927, 'type': 'Natural', 'subtype': 'Waterbody'},
        {'poi_id': 9103, 'poi_name': 'One more point', 'lat': 56.855640, 'lng': 60.759548,  'type': 'Natural', 'subtype': 'Rock'},
        {'poi_id': 9104, 'poi_name': 'Local Beach', 'lat': 56.859641, 'lng': 60.726486, 'type': 'Natural', 'subtype': 'Beach'},
        {'poi_id': 9201, 'poi_name': 'Prince`s Island', 'lat': 51.055520, 'lng': -114.070241, 'type': 'Natural', 'subtype': 'Park'},
        {'poi_id': 9202, 'poi_name': 'Nose Hill', 'lat': 51.105876, 'lng': -114.111217, 'type': 'Natural', 'subtype': 'Park'},
        {'poi_id': 9203, 'poi_name': 'Baker Park', 'lat': 51.100791, 'lng': -114.219045, 'type': 'Natural', 'subtype': 'Park'},
        {'poi_id': 9204, 'poi_name': 'Canada Olimpic Park', 'lat': 51.082950, 'lng': -114.215201, 'type': 'Recreation', 'subtype': 'Winter Sport Activity Park'},
        {'poi_id': 9301, 'poi_name': 'Roses City Beach', 'lat': 42.262312,'lng': 3.174488, 'type': 'Natural', 'subtype': 'Beach'},
        {'poi_id': 9302, 'poi_name': 'Roses Citadel', 'lat': 42.265580, 'lng': 3.170584, 'type': 'Historical', 'subtype': 'Museum'},
        {'poi_id': 9303, 'poi_name': 'Trinity Castle', 'lat': 42.246668, 'lng': 3.182242, 'type': 'Historical', 'subtype': 'Museum'},
        {'poi_id': 9304, 'poi_name': 'Dolmen Path (Start)', 'lat': 42.256068, 'lng': 3.197926, 'type': 'Historical', 'subtype': 'Dolmen'}]

    def getListOfPOIByID(self, id_list):
        output = []
        if len(id_list) > 0:
            for id in id_list:
                for poi in self.all_pois:
                    if poi['poi_id'] == id:
                        output.append(poi)
        return output

    def get(self, the_collection):
        col = Collection()
        the_col = ''
        found = False
        for c in col.poi_collection_list:
            if c['name'].lower() == the_collection.lower():
                the_col = c
                found = True
        output = []
        if (found == False):
            return
        for i in the_col['poi_ids']:
            for ap in self.all_pois:
                if (ap['poi_id'] == i):
                    output.append(ap)
        return output

    def put(self):
        pass

    def post(self):
        pass
 
    def delete(self):
        pass


ctp = Collection()


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
    return 'You have entered number {}'. format(str(num))


def getPoiList():
    attempt_poi_collection = request.form.post['poi_collection_choise']
    return ctp.getPOIlist(poi_collection)	


# stage01
@app.route('/stage01')
def stage01():
    poi_list = ctp.randomPOIlist()
    return render_template('stage01.html', name='stage01', poi_list=poi_list)


# stage02
@app.route('/stage02')
def stage02():
    poi_list = ctp.randomPOIlist()
    return render_template('stage02.html', name='stage02')

#test custom rest api
@app.route('/test')
def test():
    return jsonify(name="Olga", nickname="Hare", attribute1='sweet', attributr2='sexy')

# map page
@app.route('/<name>', methods=['GET', 'POST'])
def map(name):
    if name == 'todo':
        return render_template('todo.html', name=name)
    try:
        poi_list = getPOIlist()		
        return render_template('map_view.html', name=name, poi_collection_list=ctp.poi_collection_list, poi_list=poi_list)
    except Exception as e:
        return render_template('map_view.html', name=name, poi_collection_list=ctp.poi_collection_list)


def abort_if_todo_doesnt_exist(collection_name):
    if collection_name not in ctp.collection_list:
        abort(404, message="POI list {} doesn't exist".format(collection_name))

parser = reqparse.RequestParser()
post_parser = reqparse.RequestParser()
# parser.add_argument('the_collection')

api.add_resource(Collection, '/api/collections/')
api.add_resource(POIs, '/api/pois/<the_collection>')


if __name__ == "__main__":
    app.run(debug=True)