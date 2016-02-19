"""
training on Flask
"""
import json
from flask import Flask, request, render_template, flash, url_for, jsonify
import random
from flask_restful import reqparse, abort, Api, Resource, fields, marshal_with
from os import path
import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:test123@localhost/pg_naviguide'
db = SQLAlchemy(app)

api = Api(app)
path = path.dirname(path.abspath(__file__))


def getApiKeys():
    output = []
    try:
        with open(path+'\\API_KEYS.txt',mode='r') as rfile:
            for f in rfile:
                output.append(json.loads(f))
    except Exception as e:
        print ("File not found")
        output.append({"Google": ""})
    return output

GOOGLEMAPS_KEY = getApiKeys()[0]['Google']

class POI_db(db.Model):    
    __tablename__ = 'poi'
    poi_id = db.Column(db.Integer, unique=True, primary_key=True)
    poi_name = db.Column(db.String(50))
    poi_lat = db.Column(db.Float)
    poi_lng = db.Column(db.Float)
    poi_type = db.Column(db.String(50))
    poi_subtype = db.Column(db.String(50))

    def __init__(self, poi_name, poi_lat, poi_lng, poi_type, poi_subtype):
        self.poi_name = poi_name
        self.poi_lat = float(poi_lat)
        self.poi_lng = float(poi_lng)
        self.poi_type = poi_type
        self.poi_subtype = poi_subtype
        self.poi_id = self.next_id()
		
    def __repr__(self):
        return [i.serialize for i in POI_db.query.all()]
		
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
           "poi_name": self.poi_name,
           "poi_lat" : self.poi_lat,
           "poi_lng" : self.poi_lng,
           "poi_type" : self.poi_type,
           "poi_subtype" : self.poi_subtype
           # This is an example how to deal with Many2Many relations
           #'many2many'  : self.serialize_many2many
        }
	   
    @property
    def serialize_many2many(self):
        """
        Return object's relations in easily serializeable format.
        NB! Calls many2many's serialize property.
        """
        return [ item.serialize for item in self.many2many]
	   
    def next_id(self):
        try:
            qry = (db.session.query(db.func.max(POI_db.poi_id)).scalar())
        except Exception as e:
            qry = 0
        if qry is None:
            qry = 0
        return qry + 1
   
	   
class POI_Collection_db(db.Model):
    __tablename__ = 'POI_Collection'
    poi_id = db.Column(db.Integer, primary_key=True, unique=False)
    collection_id = db.Column(db.Integer, primary_key=True, unique=False)

    def __init__(self, poi_id, collection_id):
        self.poi_id = poi_id
        self.collection_id = collection_id

    def __repr__(self):
        return {"collection_id": self.collection_id,
                "poi_id"       : self.poi_id}
    
    def __str__(self):
        return {"collection_id": self.collection_id,
                "poi_id"       : self.poi_id}

		
class Collection_db(db.Model):    
    __tablename__ = 'collection'
    collection_id = db.Column(db.Integer, unique=True, primary_key=True)
    collection_name = db.Column(db.String(50))
    collection_description = db.Column(db.String(250))

    def __init__(self, collection_name, collection_id=None, poi_ids=None, collection_description=None):
        self.collection_id = self.next_id()
        self.collection_name = collection_name		
        if poi_ids is None:
            self.poi_ids = []
        else:
            self.poi_ids = poi_ids
        if self.collection_description is None:
            self.collection_description = ""

    def __str__(self):
        return [i.serialize for i in Collection_db.query.all()]
			
    def __repr__(self):
        return [i.serialize for i in pois.query.filter(collection_id==self.collection_id)]
		
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {"collection_name"       : self.collection_name,
                "collection_id"         : self.collection_id,
		        "collection_description": self.collection_description,
                "poi_ids"               : self.serialize_many2many
        }
	   
    @property
    def serialize_many2many(self):
       """
       Return object's relations in easily serializeable format.
       NB! Calls many2many's serialize property.
       """
       return [ item.serialize for item in self.many2many]
	   
    def next_id(self):
        try:
            qry = (db.session.query(db.func.max(Collection_db.collection_id)).scalar())
        except Exception as e:
            qry = 0
        if qry is None:
            qry = 0
        return qry + 1

poi_col_fields = {
        "collection_id": fields.Integer,
        "collection_name": fields.String,
        "poi_ids": fields.List(fields.Nested(fields.Integer)),
		"collection_description": fields.String
        }

"""
REST classes
"""		
class Collection_api(Resource):
    def __init__(self):      
        pass
    
    @marshal_with(poi_col_fields)
    def get(self, param):
        if param == 'all':	
            return Collection_db.query.all(), 200
        elif param in [collection_name for collection_name, in db.session.query(Collection_db.collection_name).all()]:
            collection = db.session.query(Collection_db).filter(Collection_db.collection_name==param).first()
            the_collection_id, = db.session.query(Collection_db.collection_id).filter(Collection_db.collection_name==param).first()
            print ("collection id: ", the_collection_id)
            poi_ids = [id for id, in db.session.query(POI_Collection_db.poi_id).filter(POI_Collection_db.collection_id==the_collection_id)]
            #print (poi_ids)
            output = {"collection_id": collection.collection_id,
                      "collection_name": collection.collection_name,
                      "collection_description": collection.collection_description,
                      "poi_ids": poi_ids}
            print (output)
            return output, 200

    @marshal_with(poi_col_fields)
    def put(self, param):
        the_collection_id = db.session.query(Collection_db.collection_id).filter(Collection_db.collection_name==param).scalar()
        the_collection = db.session.query(Collection_db).filter(Collection_db.collection_name==param)
        updated_collection = the_collection
        if request.form.get("action") == 'send':
            poi_collection = POI_Collection_db(collection_id=the_collection_id, poi_id=int(request.form.get("poi_id")))
            db.session.add(poi_collection)
            db.session.commit()
        elif request.form.get("action") == 'collection update':
            the_collection_details = {"collection_name": request.form.get('collection_name'),
                                      "collection_description": request.form.get('collection_description')}            
            updated_collection = db.session.query(Collection_db).filter(Collection_db.collection_id==request.form.get('collection_id'))\
                                                                .update(the_collection_details)
            db.session.commit()
        return updated_collection, 201

    @marshal_with(poi_col_fields)
    def post(self, param):
        new_collection = Collection_db(collection_name=request.form.get("collection_name"))
        db.session.add(new_collection)
        db.session.commit()
        return new_collection, 201
 
    def delete(self, param):
        db.session.query(Collection_db).filter(Collection_db.collection_name==param).delete()
        db.session.commit()
        return '', 204

poi_fields = {
        "poi_id": fields.Integer,
        "poi_name": fields.String,
        "poi_lat": fields.Float,
		"poi_lng": fields.Float,
		"poi_type": fields.String,
		"poi_subtype": fields.String,
        }

class POI_api(Resource):
    def __init__(self):
        pass

    @marshal_with(poi_fields)
    def get(self, the_collection):
        if the_collection == 'all':            
            return POI_db.query.all()        
        elif the_collection in [collection_name for collection_name, in db.session.query(Collection_db.collection_name).all()]:
            print (the_collection)
            print ([collection_name for collection_name, in db.session.query(Collection_db.collection_name).all()])
            the_collection_id = db.session.query(Collection_db.collection_id).filter(Collection_db.collection_name==the_collection).scalar()
            poi_ids = [id for id, in db.session.query(POI_Collection_db.poi_id).filter(POI_Collection_db.collection_id==the_collection_id)]
            print ('ids in the collecction ', poi_ids)
            pois = [poi.__dict__ for poi in db.session.query(POI_db).filter(POI_db.poi_id.in_(poi_ids)).all()]
            if len(pois) == 0:
                return [], 200
            output = []
            for poi in pois:
                d = {}
                for pf in poi_fields:
                    d[pf] = poi[pf]
                output.append(d)
            print (output)
            return output, 200
        else:
            return [], 200

    def put(self,the_collection):
        the_poi_details = {"poi_name": request.form.get('poi_name'),
                           "poi_lat": request.form.get('poi_lat'),
                           "poi_lng": request.form.get('poi_lng'),
                           "poi_type": request.form.get('poi_type'),
                           "poi_subtype": request.form.get('poi_subtype')}
        the_poi = db.session.query(POI_db).filter(POI_db.poi_id==request.form.get('poi_id')).update(the_poi_details)
        db.session.commit()
        return the_poi, 201

    @marshal_with(poi_fields)
    def post(self, the_collection):
        new_poi = POI_db(poi_name = request.form.get('poi_name'),
                         poi_lat = request.form.get('poi_lat'),
                         poi_lng = request.form.get('poi_lng'),
                         poi_type = request.form.get('poi_type'),
                         poi_subtype = request.form.get('poi_subtype'))
        #print (new_poi)
        db.session.add(new_poi)
        db.session.commit()
        return new_poi, 201
		
    def delete(self, the_collection):
        db.session.query(POI_db).filter(POI_db.poi_id==request.form.get('poi_id')).delete()
        db.session.commit()
        return '', 204

db.create_all()
		
# index page
@app.route('/')
def index():
    return render_template('index.html')

# stage01 - OBSOLETE!!!
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
    if name == "create_all":
        db.create_all()
    try:
        poi_list = getPOIlist()		
        return render_template('map_view.html', name=name, poi_collection_list=[], poi_list=[])
    except Exception as e:
        return render_template('map_view.html', name=name, poi_collection_list=[])

api.add_resource(Collection_api, '/api/collections/<param>')
api.add_resource(POI_api, '/api/pois/<the_collection>')


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)