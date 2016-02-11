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
db.create_all()
api = Api(app)
path = path.dirname(path.abspath(__file__))


def getApiKeys():
    output = []
    with open(path+'\\API_KEYS.txt',mode='r') as rfile:
        for f in rfile:
            output.append(json.loads(f))        
    return output

GOOGLEMAPS_KEY = getApiKeys()[0]['Google']

class POI_db(db.Model):    
    __tablename__ = 'poi'
    poi_id = db.Column(db.Integer, unique=True, primary_key=True)
    poi_name = db.Column(db.String(50))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    poi_type = db.Column(db.String(50))
    poi_subtype = db.Column(db.String(50))

    def __init__(self, poi_name=None, lat=None, lng=None, poi_type=None, poi_subtype=None):
        self.poi_name = poi_name
        self.lat = float(lat)
        self.lng = float(lng)
        self.poi_type = poi_type
        self.poi_subtype = poi_subtype
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
		
    def __repr__(self):
        return jsonify(self.as_dict)

class POIID_db(db.Model):
    __tablename__ = 'poi_ids'
    id = db.Column(db.Integer, unique=True, primary_key=True)

    def as_dict(self):
        return {str(c.name): str(getattr(self, c.name)) for c in self.__table__.columns}

    def __init__(self, id=None):
        self.id = id

    def __repr__(self):
        return jsonify(id=str(self.id))

		
class Collection_db(db.Model):    
    __tablename__ = 'collection'
    col_id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(50))

    poi_ids = db.Column(db.Integer, db.ForeignKey('poi_ids.id'))
    poi=db.relationship('POIID_db')
    
    def as_dict(self):
        return {str(c.name): str(getattr(self, c.name)) for c in self.__table__.columns}

    def __init__(self, name, col_id=None, poi_ids=None):
        self.col_id = col_id
        self.name = name
        self.poi_ids = poi_ids

    def __repr__(self):
        return jsonify(col_id=str(self.col_id), name=self.name, poi_ids=str(self.poi_ids))

poi_col_fields = {
        'col_id': fields.Integer,
        'name': fields.String,
        'poi_ids': fields.List(fields.Nested(fields.Integer))
        }
		
class Collection_api(Resource):
    def __init__(self):      
        pass
    
    @marshal_with(poi_col_fields)
    def get(self, param):
        if param == 'all':
            all_col = Collection_db.query.all()			
            return all_col, 200
        else:
            collection = Collection_db.query.filter_by(name=param)
            print(len(collection))
            return collection, 200
				
    def put(self, param):
        updated_collection = ''
        return updated_collection, 201

    @marshal_with(poi_col_fields)
    def post(self, param):                
        new_collection = Collection_db(name=request.form.get('name'))
        #ff = dir(new_collection)
        #for f in ff:
            #print (getattr(new_collection, f))
        db.session.add(new_collection)
        db.session.commit()
        return new_collection, 201
 
    def delete(self, param):
        return '', 204

poi_fields = {
        "poi_id": fields.Integer,
        "poi_name": fields.String,
        "lat": fields.Float,
		"lng": fields.Float,
		"poi_type": fields.String,
		"subtype": fields.String,
        }

class POI_api(Resource):
    def __init__(self):
        pass

    @marshal_with(poi_fields)
    def get(self, the_collection):
        if the_collection == 'all':            
            return POI_db.query.all()
        poi_ids = db.session.query(Collection_db.poi_ids).filter(Collection_db.name==the_collection).first()
        output = []
        for p in poi_ids:
            poi = POI_db.query.filter_by(poi_id=p)
            output.append(poi)
        return output

    def put(self,the_collection):
        updated_poi = {}
        return updated_poi, 201

    @marshal_with(poi_fields)
    def post(self, the_collection):
        new_poi = POI_db(poi_name = request.form.get('poi_name'), lat = request.form.get('lat'), lng = request.form.get('lng'),
                         poi_type = request.form.get('poi_type'), poi_subtype = request.form.get('subtype'))
        #print (new_poi)
        db.session.add(new_poi)
        db.session.commit()
        return new_poi, 201
		
    def delete(self, the_collection):
        return '', 204

		
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