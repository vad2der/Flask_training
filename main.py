"""
training on Flask
"""

from flask import Flask, request, render_template

app = Flask(__name__)

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

@app.route('/map/mymap-01')
def map(name):
	return render_template('map_view.html', name=name)
	
if __name__ == "__main__":
	app.run(debug=True)