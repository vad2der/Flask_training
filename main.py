"""
training on Flask
"""

from flask import Flask, request, render_template, jsonify
import json
app = Flask(__name__)

poi_list = [
{'poi_name': 'Kamennie palatki', 'lat': 56.842912, 'lng': 60.678538, 'type': 'Natural', 'subtype': 'Rock'},
{'poi_name': 'Shartash ozero', 'lat': 56.847335, 'lng': 60.692927, 'type': 'Natural', 'subtype': 'Waterbody'},
{'poi_name': 'One more point', 'lat': 56.855640, 'lng': 60.759548,  'type': 'Natural', 'subtype': 'Rock'},
{'poi_name': 'Local Beach', 'lat': 56.859641, 'lng': 60.726486, 'type': 'Natural', 'subtype': 'Beach'}]

	
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

# map page
@app.route('/map/<name>')
def map(name):
	if name == 'todo':
		return render_template('todo.html', name=name)
	else:
		return render_template('map_view.html', name=name, poi_list=poi_list)



if __name__ == "__main__":
	app.run(debug=True)