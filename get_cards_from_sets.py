#Modules
from pokemontcgsdk import Set
from pokemontcgsdk import Card
from pymongo import MongoClient
import json

#Get the sets from the pokemontcg api
sets = Set.all()


#Connect to Mongo
mongo_client = MongoClient("mongodb://pokemoncards.win:27017")

#Get the Database Object
test_database = mongo_client.test
sets_collection = test_database.sets
cards_collection = test_database.cards

#Get cards from the set
cards = Card.where(setCode=set.code).all()

#For each card, insert a document into mongo
for set in sets:
    cards = Card.where(setCode=set.code).all()
    for card in cards:
        cards_collection.insert_one({
            "_id": card.id,
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

