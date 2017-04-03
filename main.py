#Modules
from pokemontcgsdk import Set
#from pymongo import MongoClient

#Get sets from API

sets = Set.all()
print(sets)
#
# #Connect to Mongo
#
# mongo_client = MongoClient("mongodb://pokemoncards.win:27017")
#
# #Get the Database Object
#
# test_database = mongo_client.test
# sets_collection = test_database.sets
#
# #Insert Sets from API Into sets_collection
#
# sets_collection.insert_many(sets)
