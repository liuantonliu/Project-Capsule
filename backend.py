import firebase_admin
import firebase
from firebase_admin import credentials
from firebase_admin import firestore
from flask_cors import CORS
from flask import Flask, jsonify, request, make_response

import json
import requests

app = Flask(__name__)
CORS(app)

#this is the wardrobe object, tracks the number of items in the closet in order to assign primarykey
class wardrobe:
    def __init__(self):
        self.index = 0
    def add_item(self):
        self.index += 1
    def del_item(self):
        self.index -= 1

#connect to database
def connection():
    cred = credentials.Certificate("C:/projectcapsule/projectcapsule-a0abd-firebase-adminsdk-vcr5b-8a2bff8f5f.json")
    firebase_admin.initialize_app(cred)

    db = firestore.client()
    return db

#declare global objects
mywardrobe = wardrobe()
db = connection()

@app.route("/search", methods=["POST"])
def fullsearch():
    userinput = request.get_json(force=True)['searchstr']
    related_tags = get_related_tags_json(userinput)
    knownwords = knownkeywords(db)
    queryparam = query(related_tags, knownwords)
    output = search(queryparam)
    return jsonify(output), 200

#generate dictionary of tags that exist in the wardrobe
def knownkeywords(db):
    users_ref = db.collection(u'closet-items')
    docs = users_ref.stream()
    description = []
    colour = []
    type = []

    for doc in docs:
        docdict = doc.to_dict()
        description_temp = docdict['description'].split(',')
        for entry in description_temp:
            if entry not in description:
                description.append(entry)
        colour_temp = docdict['colour'].split(',')
        for entry in colour_temp:
            if entry not in colour:
                colour.append(entry)
        type_temp = docdict['type'].split(',')
        for entry in type_temp:
            if entry not in type:
                type.append(entry)
    
    keywords = {'type' : type, 'colour': colour, 'description': description}
    return keywords

def get_related_tags_json(userInput):
    tags = requests.get("https://api.datamuse.com/words",params={"ml":userInput})
    related_tags = tags.json()
    return related_tags

#Use to find common strings.
#Inputs required: API and wardrobe dictionaries.
#Returns dictionary only containing common values.
def query(API, wardrobe):
    searchWord = []
    for words in API:
        searchWord += [words['word']]
    keys = wardrobe.keys()
    #Breaks down dictionary into lists containing wardrobe values for each key.
    wardrobeKey1 = wardrobe.get('type')
    wardrobeKey2 = wardrobe.get('colour')
    wardrobeKey3 = wardrobe.get('description')

    #lists containing wardrobe and API common strings.
    list1 = []
    list2 = []
    list3 = []

    for x in wardrobeKey1:
        if (x in searchWord):
            list1 = list1 + [x]

    for y in wardrobeKey2:
        if (y in searchWord):
            list2 = list2 + [y]

    for z in wardrobeKey3:
        if (z in searchWord):
            list3 = list3 + [z]

    finalAnswer ={'type': 0, 
                'colour': 0, 
                'description': 0}

    finalAnswer['type'] = list1
    finalAnswer['colour'] = list2
    finalAnswer['description'] = list3

    return finalAnswer #Dictionary containing only values in common with API search word.

def search(dict):
    try:
        type_search = dict['type']
    except KeyError:
        pass
    try:
        colour_search = dict['colour']
    except:
        pass
    try:
        description_search = dict['description']
    except:
        pass
    type_ref = db.collection(u'closet-items').where('type', u'in', type_search).stream()
    colour_ref = db.collection(u'closet-items').where('colour', u'in', colour_search).stream()
    description_ref = db.collection(u'closet-items').where('description', u'in', description_search).stream()
    output = {}
    for article in type_ref:
        output[article.id] = article.to_dict()
    for article in colour_ref:
        output[article.id] = article.to_dict()
    for article in description_ref:
        output[article.id] = article.to_dict()
    return output

@app.route("/upload", methods=["POST"])
#upload article
def article_upload():
    dict = request.get_json(force = True)
    mywardrobe.add_item()
    docname = str(mywardrobe.index)
    doc_ref = db.collection(u'closet-items').document(str(mywardrobe.index))
    doc_ref.set({
        u'type': dict['type'],
        u'colour': dict['colour'],
        u'timesworn': dict['timesworn'],
        u'donation': dict['donation'],
        u'description': dict['description']

    })
    response = {"message": "got it!"}
    return jsonify(response), 200

@app.route("/edit", methods=["POST"])
def update():
    dict = request.get_json(force = True)
    target = db.collection(u'closet-items').document(str(dict['id']))
    target.update({
        dict['field']: dict['change']
    })
    response = {"message": "got it!"}
    return jsonify(response), 200

'''
def cool():
    test = request.get_json(force = True)
    print(test)
    response = {"message": "got it!"}
    return jsonify(response), 200


def search():
    test = request.get_json(force = True)
    print(test)
    db = connection()
    count = init_wardrobe_count(db)
    print(count)
    
    article_upload(db, 'top', 'green', '0', 'False', 'casual')
    article_upload(db, 'pants', 'white', '0', 'False', 'denim,high waist')
    article_upload(db, 'scarf', 'blue', '0', 'False', 'wool,plaid')
    print(count)
    search(db, {'type': ['top', 'pants']})
    knownkeywords(db)
    return None

#runs initially to determine how many items are in the closet
def init_wardrobe_count(db):
    users_ref = db.collection(u'closet-items')
    docs = users_ref.stream()
    count = 0

    for doc in docs:
        count += 1
    
    mywardrobe.index = count

    return count

#generate dictionary of tags that exist in the wardrobe
def knownkeywords(db):
    users_ref = db.collection(u'closet-items')
    docs = users_ref.stream()
    description = []
    colour = []
    type = []

    for doc in docs:
        docdict = doc.to_dict()
        description_temp = docdict['description'].split(',')
        for entry in description_temp:
            if entry not in description:
                description.append(entry)
        colour_temp = docdict['colour'].split(',')
        for entry in colour_temp:
            if entry not in colour:
                colour.append(entry)
        type_temp = docdict['type'].split(',')
        for entry in type_temp:
            if entry not in type:
                type.append(entry)
    
    keywords = {'type' : type, 'colour': colour, 'description': description}
    print(keywords)
    return keywords
'''
if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=2145, type=int,
                        help='port to listen on')
    args = parser.parse_args()
    port = args.port
    app.run(host='0.0.0.0', port=port)