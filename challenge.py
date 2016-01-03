"""
Challenge task from Sortable
by Vadim Deryabin
Language used: Python 3
Approach: scoring matches
"""

import json
import os
import codecs
from multiprocessing.pool import ThreadPool


"""
some solid variables
"""
path = os.path.dirname(os.path.abspath(__file__))
source_path = path + '\\source_files\\'
products_file = "products.txt"
listing_file = "listings.txt"
selection_file = "result.txt"


def openObjects(pathfile):
    """
    function to open file containing products
    returns list of json objects (every consists of 4 dicts)
    """
    l = []
    with codecs.open(pathfile, mode='r', encoding='utf-8') as rfile:
        for f in rfile:
            l.append(json.loads(f))
        print ('\nApprehanded {} objects'.format(len(l)))
    return l


def printObjects(products, start = None, finish=None):
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
    if len(products) < 1:
        return
    print ('See output for objects from {} to {} (not including):'.format(start, finish))
    print ('\n')
    for ind in range(start, finish):
        print (ind, "--------------")
        for k, v in products[ind].items():
            k = (k.encode('cp1251', errors='ignore')).decode('utf-8', errors='ignore')
            v = (v.encode('cp1251', errors='ignore')).decode('utf-8', errors='ignore')
            print ('{} {} {}'.format(k, ": ", v))


def saveObjects(selection, name):
    with open(name, 'w') as outfile:
        for s in selection:
            json.dump(s, outfile, ensure_ascii=False)
            outfile.write('\n')

def findForKeys(template, source):
    """
    block for finding equal keys in dicts for forming 1 stage list
    return tuple with respective foreign keys
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
        print ('\ntemplate key(s): {}\nsource key(s): {}\nfound as matching and set as foreign key'
               .format(foreign_key1[0], foreign_key2[0]))
    foreign_key = foreign_key1
    return (foreign_key1[0], foreign_key2[0])


def findMatchesKnownFields(template, source, field, foreign_key1=None, foreign_key2=None):
    """
    function takes
        template (JSON object)
        source (list of JSON objects)
        field (str or list of srtings) = crucial field or list of fields
    function takes (optional):
        foreign_key1 (str) = foreign key to join template
        foreign_key2 (str) = foreign key to join source

    looks for matches of template in source

    returns a list
    """
    if type(field) is not list:
        print (type(field))
        field = [field]
        print ('Converting field param to list')
    # getting step 1 criteria
    if (foreign_key1 is None) and (foreign_key2 is None):
        foreign_key1, foreign_key2 = findForKeys(template, source[0])
    result1 = []
    # if smthng goes wrong
    if ((foreign_key1 is None) and (foreign_key2 is not None))\
            or ((foreign_key1 is not None) and (foreign_key2 is None)):
        print ('\nBoth foreign keys should be assigned.')
        result1 = source
    # match by foreign key - step 1
    else:
        refined_template1 = template[field[0]].lower().replace('_', ' ')
        if len(field) > 1:
            # designed for max 3 crucial fields. Can be unified by helper function, which may be recursive.
            refined_template2 = template[field[1]].lower().replace('_', ' ')
        else:
            refined_template2 = refined_template1
        if len(field) > 2:
            refined_template3 = template[field[2]].lower().replace('_', ' ')
        else:
            refined_template3 = refined_template1
        for s in source:
            # matching by 1)foreign key, 2)not picked before, 3) in top matching field, 4) in one of rest fields
            if template[foreign_key1].lower() in s[foreign_key2].lower() and \
                            s not in result1 and \
                            refined_template1 in str(s.values()).lower() and \
                            refined_template2 in str(s.values()).lower() or \
                            refined_template3 in str(s.values()).lower():
                result1.append(s)
    return result1


def getRelevantFields(template, source):
    """
    :param template - example for the search
    :param source - list of JSON objects to search in
    :return - list of dict field names where matches occure with number of matches
    """
    proper_fields = {}
    foreign_key1, foreign_key2 = findForKeys(template, source[0])
    for s in source:
        found = 0
        for v in s.values():
            for criteria in template.values():
                c_lower = criteria.lower().replace('_', ' ')
                if c_lower in v.lower():
                    if list(template.keys())[list(template.values()).index(criteria)] in template.keys()\
                            and str(list(template.keys())[list(template.values()).index(criteria)]) != foreign_key1:
                        found += 1
                        proper_fields[list(template.keys())[list(template.values()).index(criteria)]] = found
    print ('\nFields with matches are: {}'.format(proper_fields))
    return proper_fields


def sortDictTopResults(d):
    """
    input:
        dictionary
    output(return):
        list of dictionary keys referring to max value(s)
    """
    result = []
    max_score_value = [f for f in sorted(d, key=d.get, reverse=True)]
    max_score = d[max_score_value[0]]
    for k, v in d.items():
        if v >= max_score:
            result.append(k)
    return result


def searchUnknownFields(template, source):
    """
    input:
        template - example to search
        source - list of JSON objects to search in them
    output(return):
        list of selected objects
    """
    relevant_fileds_pool = ThreadPool(processes=1).apply_async(getRelevantFields, [template, source])
    proper_fields = relevant_fileds_pool.get()
    # get list of matching fields sorted by values (number of matches)
    list_proper_fields = [f for f in sorted(proper_fields, key=proper_fields.get, reverse=True)]
    print ('Proper fields are: ' + str(list_proper_fields))
    result = findMatchesKnownFields(template, source, list_proper_fields)
    return result

if __name__ == '__main__':

    pool_1 = ThreadPool(processes=1)

    products_pool = pool_1.apply_async(openObjects, [source_path+products_file])
    # get the list of products
    products = products_pool.get()
    printObjects(products, 0, 1)

    listing_pool = pool_1.apply_async(openObjects, [source_path+listing_file])
    # get the list from listing
    listing = listing_pool.get()
    #printObjects(listing, 0, 100)

    # selecting the template - search example
    template = products[2]

    """
    # manual example
    matches_pool = pool_1.apply_async(findMatchesKnownFields, [template, listing, 'model'])
    # find matches if we know the name of crucial fields
    matchesKnownFields = matches_pool.get()
    printObjects(matchesKnownFields, 0, 5)
    """

    unknown_fields_matches_pool = pool_1.apply_async(searchUnknownFields, [template, listing])
    uf_matches = unknown_fields_matches_pool.get()
    saveObjects(uf_matches, selection_file)
    printObjects(uf_matches, 0, 5)