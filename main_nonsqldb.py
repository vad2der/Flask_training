"""
training on Flask
"""
import json
from flask import Flask, request, render_template, flash, url_for, jsonify
import random
from flask_restful import reqparse, Api, Resource, fields
from os import path
import pymongo
from bson import ObjectId

app = Flask(__name__)
api = Api(app)
path = path.dirname(path.abspath(__file__))
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client.naviguide_database
poi_col = db.collections
pois = db.pois


def getApiKeys():
    output = []
    with open(path+'\\API_KEYS.txt',mode='r') as rfile:
        for f in rfile:
            output.append(json.loads(f))
    return output

try:
    GOOGLEMAPS_KEY = getApiKeys()[0]['Google']
except IOError as e:
    print('\nno file for keys found\n', e)
finally:
    GOOGLEMAPS_KEY = ''


def toJson(data):
    if "_id" in data.keys():
        del data["_id"]
    output = str(data)
    output = output.replace("'", '"')
    output = output.replace("None", "")
    output = json.loads(output)
    return output


class Collection(Resource):
    """
    initial emualtion of db
    """
    def __init__(self):
        self.poi_col_fields = {
        "col_id": fields.Integer,
        "name": fields.String,
        "poi_ids": fields.Integer,
        }

    def get(self, param):
        output = []
        if param == 'all':
            try:
                all_collections = poi_col.find()
                for a in all_collections:
                    the_line = {}
                    for f in self.poi_col_fields:
                        the_line[f] = a[f]
                        if a[f] is None:
                            the_line[f] = []
                    output.append(toJson(the_line))
            except ValueError as e:
                print('\nerror:', e)
            return output

    def put(self, param):
        updated_collection = ''
        action = request.form.get('action')
        if action == "send":
            poi_id = int(request.form.get('poi_id'))
            current_poi_ids = db.collections.find_one({"name": param})["poi_ids"]
            db.collections.update_one({"name": param,
                                       "$set": {"poi_ids": current_poi_ids.append(poi_id)}})
            for collection in self.poi_collection_list:
                if ((collection["name"] == param) and (poi_id not in collection["poi_ids"])):
                    collection["poi_ids"].append(poi_id)
                    updated_collection = collection
            self.saveCollectionToDB()
        if action == "remove":
            poi_id = int(request.form.get('poi_id'))
            for collection in self.poi_collection_list:
                if (collection["name"] == param):
                    collection["poi_ids"].remove(poi_id)
                    updated_collection = collection
            self.saveCollectionToDB()
        if action == "collection update":
            new_collection_name = request.form.get('name')
            numbers = request.form.get('poi_ids')
            id = request.form.get('col_id')
            description = request.form.get('collection_description')
            self.delete_collection(param)
            new_col = {"name": new_collection_name, "poi_ids": numbers, "col_id": id, "collection_description": description}
            self.addItemtoDB(new_col)
            return new_col, 201

    def post(self, param):
        new_collection = {}
        for field in self.poi_col_fields:
            new_collection[field] = request.form.get(field)
        poi_col.insert(new_collection)
        return toJson(new_collection), 201

    def delete(self, param):
        poi_col.remove({"name": param})
        return '', 204


class POIs(Resource):
    """
    initial emualtion of db
    """
    def __init__(self):
        self.poi_fields = {
        "poi_id": fields.Integer,
        "poi_name": fields.String,
        "poi_lat": fields.Float,
		"poi_lng": fields.Float,
		"poi_type": fields.String,
		"poi_subtype": fields.String,
        }

    def get(self, the_collection):
        output = []
        if the_collection == 'all':
            try:
                all_pois = pois.find()
                for a in all_pois:
                    the_line = {}
                    for f in self.poi_fields:
                        the_line[f] = a[f]
                        if a[f] is None:
                            the_line[f] = []
                    output.append(toJson(the_line))
            except ValueError as e:
                print('\nerror:', e)
            return output
        collection_pois = poi_col.find_one({"name": the_collection})
        collection_pois = collection_pois["poi_ids"]
        if type(collection_pois) is not list:
            collection_pois = []
        for collection_poi in collection_pois:
            output.append(pois.find({"poi_id": collection_poi}))
        return output

    def put(self,the_collection):
        updated_poi = {}
        if the_collection == 'update':
            for field in self.poi_fields:
                updated_poi[field] = request.form.get(field)
        updated_poi['poi_id'] = int(updated_poi['poi_id'])
        for poi in self.all_pois:
            if poi['poi_id'] == updated_poi['poi_id']:
                self.all_pois.remove(poi)
                self.all_pois.append(updated_poi)
        self.saveDB(self.all_pois)
        return updated_poi, 201

    def post(self, the_collection):
        new_poi = {}
        for field in self.poi_fields:
            new_poi[field] = request.form.get(field)
        new_poi["poi_id"] = int(self.all_pois[-1]["poi_id"]) + 1
        self.addPOItoDB(new_poi)
        return new_poi, 201

    def delete(self, the_collection):
        output = []
        point_id = int(request.form.get("poi_id"))
        for poi in self.all_pois:
            if int(poi["poi_id"]) != point_id:
                output.append(poi)
        self.saveDB(output)
        return '', 204

# index page
@app.route('/')
def index():
    return render_template('index.html')

# stage01
@app.route('/stage01')
def stage01():
    return render_template('stage01.html', name='stage01', poi_list=[])

# stage02
@app.route('/stage02')
def stage02():
    return render_template('stage02.html', name='stage02', GOOGLEMAPS_KEY=GOOGLEMAPS_KEY)

# map page
@app.route('/<name>', methods=['GET', 'POST'])
def map(name):
    if name == 'todo':
        return render_template('todo.html', name=name)

parser = reqparse.RequestParser()
post_parser = reqparse.RequestParser()
# parser.add_argument('the_collection')

api.add_resource(Collection, '/api/collections/<param>')
api.add_resource(POIs, '/api/pois/<the_collection>')


if __name__ == "__main__":
    app.run(debug=True)