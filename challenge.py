import json
import io
import codecs


"""
some solid variables
"""
path = "C:\\Python34\\source_files\\"
products_file = "products.txt"
listing_file = "listings.txt"
#sys.stdout = codecs.getwriter("iso-8859-1")(sys.stdout, 'xmlcharrefreplace')
	
def openObjects(pathfile):
	"""
	function to open file containing products
	returns list of json objects (every consists of 4 dicts)
	"""
	rfile = codecs.open(pathfile, mode = 'r', encoding = 'utf-8')
	l = []
	for f in rfile:
		l.append(json.loads(f))
	return l

def printObjects(products, start = None, finish = None):	
	"""
	represents list of products in defined scopes
	"""
	if start is None:
		start = 0	
	if finish is None:
		finish = len(listing)
	print ('\n')
	print ('{} objects in list'.format(len(products)))
	print ('See output for objects from {} to {} (not including):'.format(start, finish))
	print ('\n')
	for ind in range(start, finish):
		print (ind, "--------------")
		for k, v in products[ind].items():
			k = (k.encode('cp1251', errors = 'ignore')).decode('utf-8', errors = 'ignore')
			v = (v.encode('cp1251', errors = 'ignore')).decode('utf-8', errors = 'ignore')
			print ('{} {} {}'.format(k, ": ", v))

def findForKeys(template, source):
	"""
	block for finding equal keys in dicts for forming 1 stage list
	return tuple with respectiv foreign keys
	"""
	foreign_key1 = None
	foreign_key2 = None
	for k1 in template.keys():
		for k2 in source.keys():
			if k1.lower() == k2.lower():
				foreign_key1 = k1
				foreign_key2 = k2
	if foreign_key1 is None:
		print ('No perfect match in keys. Try to get partly match...')
		for k1 in template.keys():
			for k2 in source.keys():
				if (k1.lower() in k2.lower()) or (k2.lower() in k1.lower()):
					foreign_key1 = k1
					foreign_key2 = k2
	if foreign_key1 is None:
		print ('No matches found. Key reference has to be manually handeled')
	return (foreign_key1, foreign_key2)
	
			
def findMatches(template, source):
	"""
	function takes
		template (JSON object)
		source (list of JSON objects)
	looks for matches of template in source
	returns a list
	"""
	result = []
	foreign_key1, foreign_key2 = findForKeys(template, source[0])

	# simple iterative search
	for s in source:
		if template[foreign_key1] in s[foreign_key2]:
			result.append(s)	
	return result
	

products = openObjects(path+products_file)
#printObjects(products, 0, 1)
listing = openObjects(path+listing_file)
#printObjects(listing, 4210, 4211)
matches = findMatches(products[0], listing)
printObjects(matches, 0, 5)