#Modules
import configparser
from pokemontcgsdk import Set
from pokemontcgsdk import Card
from pymongo import MongoClient

#Config
Config = configparser.ConfigParser()
Config.read("settings.ini")
host = Config.get("db", "host")
port = Config.get("db", "port")
user = Config.get("db", "user")
password = Config.get("db", "password")

pass_colon_str = ""
at_str = ""

if user:
    pass_colon_str = ":"
    at_str = "@"

#Build Connection String
connection_string = "mongodb://{0}{1}{2}{3}{4}:{5}".format(user, pass_colon_str, password, at_str, host, port)

#Get the sets from the pokemontcg api
print("Getting sets from pokemontcgsdk")
pokemontcgapi_sets = Set.all()
print("  Found sets:")
for pokemontcgapi_set in pokemontcgapi_sets:
    print("  -- {0}".format(pokemontcgapi_set.name))

#Connect to Mongo
print("Connecting to {0}".format(connection_string))
mongo_client = MongoClient(connection_string)

#Get the Database Object
card_data_database = mongo_client.card_data
sets_collection = card_data_database.sets
cards_collection = card_data_database.cards

#Get all the sets that we already have cards for
print("\nGetting sets from {0}".format(host))
mongo_sets_cursor = sets_collection.find()

#For each card, insert a document into mongo
print("\nInserting Cards into mongo")

for pokemontcgapi_set in pokemontcgapi_sets:
    already_have_set = False
    print("Checking for {0}({1})".format(pokemontcgapi_set.name, pokemontcgapi_set.code))
    for mongo_set in mongo_sets_cursor:
        if mongo_set.get('code') == pokemontcgapi_set.code:
            already_have_set = True
            print("Skipping {0}({1})".format(mongo_set.get('name'), mongo_set.get('code')))
            break


    if not already_have_set:
        print("\nInserting {0}:".format(pokemontcgapi_set.name))
        print("***********************************")
        #Get the cards from the set
        cards = Card.where(setCode=pokemontcgapi_set.code).all()
        #Insert each card document into mongo
        for card in cards:
            print("-- {0}({1})".format(card.name, card.id))
            cards_collection.insert_one({
                "pokemontcgapi_id": card.id,
                "name": card.name,
                "national_pokedex_number": card.national_pokedex_number,
                "image_url": card.image_url,
                "subtype": card.subtype,
                "supertype": card.supertype,
                "ability": card.ability,
                "ancient_trait": card.ancient_trait,
                "hp": card.hp,
                "number": card.number,
                "artist": card.artist,
                "rarity": card.rarity,
                "series": card.series,
                "set": card.set,
                "set_code": card.set_code,
                "retreat_cost": card.retreat_cost,
                "text": card.text,
                "types": card.types,
                "attacks": card.attacks,
                "weaknesses": card.weaknesses,
                "resistances": card.resistances
            })
        sets_collection.insert_one({
            "code": pokemontcgapi_set.code,
            "name": pokemontcgapi_set.name,
            "series": pokemontcgapi_set.series,
            "total_cards": pokemontcgapi_set.total_cards,
            "standard_legal": pokemontcgapi_set.standard_legal,
            "expanded_legal": pokemontcgapi_set.expanded_legal,
            "release_date": pokemontcgapi_set.release_date
        })
        print("Finished inserting {0}({1})\n\n".format(pokemontcgapi_set.name, pokemontcgapi_set.code))
print("\nClosing connection to {0}".format(host))
mongo_client.close()