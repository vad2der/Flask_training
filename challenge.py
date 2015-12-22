import json
import io
import codecs
import sys

"""
some solid variables
"""
path = "C:\\Python34\\source_files\\"
products_file = "products.txt"
listing_file = "listings.txt"
#sys.stdout = codecs.getwriter("iso-8859-1")(sys.stdout, 'xmlcharrefreplace')
	
def openProducts(pathfile):
	"""
	function to open file containing products
	returns list of json objects (every consists of 4 dicts)
	"""
	rfile = io.open(pathfile, 'r', encoding = 'utf-8')
	l = []
	for f in rfile:
		l.append(json.loads(f))
	return l

def printProducts(products, start = None, finish = None):	
	"""
	represents list of products in defined scopes
	"""
	if start is None:
		start = 0	
	if finish is None:
		finish = len(listing)
	for ind in range(start, finish):
		print (ind, "--------------")
		for k, v in products[ind].items():
			print (k, ": ", v)

def openListing(pathfile):
	"""
	function to open file containing listing
	returns list of json objects (every consists of dicts)
	"""
	rfile = io.open(pathfile, 'r', encoding = 'utf-8')
	l = []
	for f in rfile:
		l.append(json.loads(f))
	return l

def printListing(listing, start = None, finish = None):
	"""
	represents list from listing in defined scopes
	TODO: deal with encoding	
	"""
	if start is None:
		start = 0	
	if finish is None:
		finish = len(listing)
	for ind in range(start, finish):		
		print (ind, "++++++++")
		for k, v in listing[ind].items():
			print (k, ": ", v)
	
products = openProducts(path+products_file)
printProducts(products, 0, 3)
listing = openListing(path+listing_file)
printListing(listing, 4210, 4220)