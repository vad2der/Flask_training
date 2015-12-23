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
	# if start point is not set
	if start is None:
		start = 0
	# if finish point is not set
	if finish is None:
		finish = len(products)
	# if finish point further than the range of the passed list
	if ((finish != 0) and (len(products) < finish)):
		finish = len(products)
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
	foreign_key1 = []
	foreign_key2 = []
	for k1 in template.keys():
		for k2 in source.keys():
			if k1.lower() == k2.lower():
				foreign_key1.append(k1)
				foreign_key2.append(k2)
	if len(foreign_key1) == 0:
		print ('\nNo perfect match in keys. Try to get partly match...')
		for k1 in template.keys():
			for k2 in source.keys():
				if (k1.lower() in k2.lower()) or (k2.lower() in k1.lower()):
					foreign_key1.append(k1)
					foreign_key2.append(k2)
	if len(foreign_key1) == 0:
		print ('\nNo matches found. Key reference has to be manually handeled')
	else:
		print ('\ntemplate key(s): {}\nsource key(s): {}\nfound as matching'.format(foreign_key1[0], foreign_key2[0]))
	return (foreign_key1[0], foreign_key2[0])
	
			
def findMatches(template, source, foreign_key1 = None, foreign_key2 = None):
	"""
	function takes
		template (JSON object)
		source (list of JSON objects)
	looks for matches of template in source
	returns a list
	"""	
	# getting step 1 criteria
	if ((foreign_key1 is None) and (foreign_key2 is None)):
		foreign_key1, foreign_key2 = findForKeys(template, source[0])
	# if smthng goes wrong
	if ((foreign_key1 is None) and (foreign_key2 is not None)) or ((foreign_key1 is not None) and (foreign_key2 is None)):
		print ('\nBoth foreign keys should be assigned.')
	# match by foreign key - step 1
	result1 = []
	for s in source:		
		if (template[foreign_key1].lower() in s[foreign_key2].lower()):
			result1.append(s)
	# match by having other records in - step 2
	result2 = []	
	for r in result1:
		for k2, v2 in template.items():
			if ((k2.lower() == foreign_key1) or ('price' in k2.lower()) or ('currency' in k2.lower())):
				continue
			for k1, v1 in r.items():
				if (v2 in v1):
					result2.append(r)		
	return result2
	

products = openObjects(path+products_file)
printObjects(products, 0, 1)
listing = openObjects(path+listing_file)
#printObjects(listing, 4210, 4211)
matches = findMatches(products[0], listing)
printObjects(matches, 0, 5)