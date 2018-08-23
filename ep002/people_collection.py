#
# Author: Joe.Drumgoole@mongodb.com
#


import pymongo
if __name__ == "__main__":
    client = pymongo.MongoClient()
    client.drop_database("ep002")
    database = client["ep002"]
    people_collection = database["people_collection"]

