"""
training on Flask
"""
import json
from flask import Flask, request, render_template, flash, url_for, jsonify
import random
from flask_restful import reqparse, abort, Api, Resource, fields
from os import path
import datetime

app = Flask(__name__)
api = Api(app)
path = path.dirname(path.abspath(__file__))


class Collection(Resource):
    """
    initial emualtion of db
    """
    def __init__(self):
        self.poi_collection_list = self.openDB()
        
        self.poi_col_fields = {
        'col_id': fields.Integer,
        'name': fields.String,
        'date_created': fields.DateTime,
        'date_updated': fields.DateTime,
        'poi_ids': fields.Integer,
        }
    
    def openDB(self):
        output = []
        with open(path+'\\collections.txt',mode='r') as rfile:
            for f in rfile:
                output.append(json.loads(f))
        return output
		
    def deleteItem(self, name):
        output = []	
        with open(path+'\\collections.txt',mode='r') as rfile:
            for f in rfile:
                item = json.loads(f)
                if item['name'] != name['name']:                   
                   output.append(item)
                else:
                   print(item)
        f1 = open(path+'\\collections.txt',mode='w')
        f1.close()
        with open(path+'\\collections.txt',mode='a') as outfile:
            for o in output:
                json.dump(o, outfile)
                outfile.write('\n')
        self.poi_collection_list = self.openDB()

    def addItemtoDB(self, item):
        with open(path+'\\collections.txt',mode='a') as outfile:
            json.dump(item, outfile)
            outfile.write('\n')
        self.poi_collection_list = self.openDB()
	
    def createNewCollection(self, new_collection):
        next_id = int(self.poi_collection_list[-1]["col_id"]) + 1
        new_collection["col_id"] = next_id
        new_collection["poi_ids"] = []
        self.poi_collection_list.append(new_collection)
        return self.poi_collection_list[-1]

    def get(self, param):
        return self.poi_collection_list

    def randomPOIlist(self):
        the_collection = random.choice(self.poi_collection_list)        
        pois = POIs()
        return pois.getListOfPOIByID(the_collection['poi_ids'])

    def getNames(self):
        output = []
        for collection in self.poi_collection_list:
            if 'name' in collection.keys():
                output.append(collection['name'])
        return output

    def updateCollectioninDB(self, old_name, new_name, poi_ids):
        pass
		
    def delete_collection(self, name):
        for collection in self.poi_collection_list:
            if collection['name'] == name:
                print (jsonify(self.poi_collection_list[collection]))
                del self.poi_collection_list[collection]

    def saveCollectionToDB(self):
        with open(path+'\\collections.txt',mode='w') as outfile:
            for collection in self.poi_collection_list:
                json.dump(collection, outfile)
                outfile.write('\n')
				
    def put(self, param):
        updated_collection = ''
        action = request.form.get('action')        
        if action == "send":
            poi_id = int(request.form.get('poi_id'))
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
        if action == "rename":
            old_collection_name = request.form.get('old_name_collection')
            new_collection_name = request.form.get('new_name_collection')
            numbers = request.form.get('poi_ids')
            updated_colection = updateCollectioninDB(old_collection_name, new_collection_name, numbers)
        return updated_collection, 201

    def post(self, param):
        new_collection = {}
        for field in self.poi_col_fields:
            new_collection[field] = request.form.get(field)
        the_new_collection = self.createNewCollection(new_collection)
        self.addItemtoDB(the_new_collection)
        return the_new_collection, 201
 
    def delete(self, param):
        if param in self.getNames():
            for collection in self.poi_collection_list:
                if collection['name'] == param:
                    self.deleteItem(collection)
            return '', 204
        else:
            print('no such collection')


class POIs(Resource):
    """
    initial emualtion of db
    """
    def __init__(self):
        self.all_pois = self.openDB()
        self.poi_fields = {
        "poi_id": fields.Integer,
        "poi_name": fields.String,
        "date_created": fields.DateTime,
        "date_updated": fields.DateTime,
        "lat": fields.Float,
		"lng": fields.Float,
		"type": fields.String,
		"subtype": fields.String,
        }

    def openDB(self):
        output = []
        with open(path+'\\pois.txt',mode='r', encoding='utf-8') as rfile:
            for f in rfile:
                output.append(json.loads(f))
        return output
		
    def saveDB(self, poi_list):
        with open(path+'\\pois.txt',mode='w') as outfile:
            for poi in poi_list:
                json.dump(poi, outfile)
                outfile.write('\n')
        self.all_pois = self.openDB()			

    def addPOItoDB(self, item):
        with open(path+'\\pois.txt',mode='a') as outfile:
            json.dump(item, outfile)
            outfile.write('\n')
        self.all_pois = self.openDB()
		
    def deletePOIfromDB(self):
        pass	

    def updatePOIinDB(self):
        pass
		
    def getListOfPOIByID(self, id_list):
        output = []
        if len(id_list) > 0:
            for id in id_list:
                for poi in self.all_pois:
                    if poi['poi_id'] == id:
                        output.append(poi)
        return output

    def get(self, the_collection):
        if the_collection == 'all':            
            return self.all_pois
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

    def put(self,the_collection):
        updated_poi = {}
        if the_collection == 'update':
            for field in self.poi_fields:
                updated_poi[field] = request.form.get(field)
                print(str(field),": ",str(updated_poi[field]))
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

ctp = Collection()

# index page
@app.route('/')
def index():
    return render_template('index.html')

# stage01
@app.route('/stage01')
def stage01():
    poi_list = ctp.randomPOIlist()
    return render_template('stage01.html', name='stage01', poi_list=poi_list)


# stage02
@app.route('/stage02')
def stage02():    
    return render_template('stage02.html', name='stage02')

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

parser = reqparse.RequestParser()
post_parser = reqparse.RequestParser()
# parser.add_argument('the_collection')

api.add_resource(Collection, '/api/collections/<param>')
api.add_resource(POIs, '/api/pois/<the_collection>')


if __name__ == "__main__":
    app.run(debug=True)