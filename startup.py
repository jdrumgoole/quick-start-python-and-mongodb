import pymongo

client = pymongo.MongoClient()
database = client["demo"]
zipcodes=database["zipcodes"]
