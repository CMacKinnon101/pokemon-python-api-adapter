#Modules
from pokemontcgsdk import Set
from pymongo import MongoClient
import json

#Get the sets from the pokemontcg api
sets = Set.all()


#Connect to Mongo
mongo_client = MongoClient("mongodb://pokemoncards.win:27017")

#Get the Database Object
test_database = mongo_client.test
sets_collection = test_database.sets

#Insert Sets from API Into sets_collection
for set in sets:
    sets_collection.insert_one({
        "_id": set.code,
        "code": set.code,
        "name": set.name,
        "series": set.series,
        "total_cards": set.total_cards,
        "standard_legal": set.standard_legal,
        "expanded_legal": set.expanded_legal,
        "release_date": set.release_date
    })

