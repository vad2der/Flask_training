"""
Flask project using non sql DB.
in progress...
"""
import json
from flask import Flask, request, render_template, flash, url_for, jsonify
from flask_restful import reqparse, Api, Resource, fields
from os import path
import pymongo

# common variables
app = Flask(__name__)
api = Api(app)
path = path.dirname(path.abspath(__file__))
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client.naviguide_database
poi_col = db.collections
pois = db.pois


def getApiKeys():
    """
    method to get an API key from a text file (not included in repo)
    """
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


def toValidJson(data):
    """
    :param: an object to convert to the valid JSON
    :return: JSON object to be understand and evaluated by front end and readable by db
    """
    if "_id" in data.keys():
        del data["_id"]
    # TODO: turn BSON object to string to use it as actual id
    output = str(data)
    output = output.replace("None", "")
    #output = ast.literal_eval(output) # AST does not understand empty values???
    output = output.replace("'", '"')
    output = json.dumps(output)
    return output


class Collection(Resource):
    """
    CRUD methods for db on Collections
    """
    def __init__(self):
        self.poi_col_fields = {
        "collection_id": fields.Integer,
        "collection_name": fields.String,
        "collection_description": fields.String,
        "poi_ids": fields.Integer,
        }
        self.projection = {"_id": 0}

    def get(self, param):
        """
        Returns all collections or a perticular collection from db
        :param: name of collection or 'all'
        :return: collection or list of collecitons
        """
        output = []
        if param == 'all':
            try:
                all_collections = poi_col.find()
                for a in all_collections:
                    output.append(toValidJson(a))
            except ValueError as e:
                print('\nerror:', e)
            return output
        else:
            try:
                the_collection = poi_col.find_one({"collection_name": param})
            except ValueError as e:
                print('\nerror:', e)
            return the_collection

    def put(self, param):
        updated_collection = ''
        action = request.form.get('action')
        if action == "send":
            poi_id = int(request.form.get('poi_id'))
            current_poi_ids = db.collections.find_one({"collection_name": param})["poi_ids"]
            db.collections.update_one({"collection_name": param,
                                       "$set": {"poi_ids": current_poi_ids.append(poi_id)}})
        if action == "remove":
            poi_id = int(request.form.get('poi_id'))
            db.collections.update_one({"collection_name": param,
                                       "$set": {"poi_ids": current_poi_ids.remove(poi_id)}})
        if action == "collection update":
            new_collection_name = request.form.get('collection_name')
            numbers = request.form.get('poi_ids')
            id = request.form.get('collection_id')
            description = request.form.get('collection_description')
            updated_collection = poi_col.update_one({'collectio_id': id},
                                                    {'$set': {"collection_name": new_collection_name,
                                                              "collection_description": description,
                                                              "poi_ids": numbers}})
        return updated_collection, 201

    def post(self, param):
        new_collection = {}
        for field in self.poi_col_fields:
            new_collection[field] = request.form.get(field)
        try:
            poi_col.insert_one(new_collection)
        except Exception as e:
            print('Unexpected error inserting into the MongoDB: ', type(e), e)
        return toValidJson(new_collection), 201

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
        "poi_subtype": fields.String,}

    def get(self, the_collection, method='GET'):
        output = []
        if the_collection == 'all':
            try:
                all_pois = pois.find()
                for a in all_pois:
                    output.append(toValidJson(a))
            except ValueError as e:
                print('\nerror:', e)
            return output
        collection_pois = poi_col.find_one({"collection_name": the_collection})
        collection_pois = collection_pois["poi_ids"]
        if type(collection_pois) is not list:
            collection_pois = []
        for collection_poi in collection_pois:
            output.append(pois.find({"poi_id": collection_poi}))
        return output

    def put(self, the_collection, methode='PUT'):
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

    def post(self, method='POST'):
        new_poi = {}
        for field in self.poi_fields:
            new_poi[field] = request.form.get(field)
        new_poi["poi_id"] = pois.find().sort({"poi_id": -1}).limit(1)+1
        print (new_poi["poi_id"])
        pois.insert_one(new_poi)
        return new_poi, 201

    def delete(self, the_collection, method='DELETE'):
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

api.add_resource(Collection, '/api/collections/<param>')
api.add_resource(POIs, '/api/pois/<the_collection>')


if __name__ == "__main__":
    app.run(debug=True)