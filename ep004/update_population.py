"""
@Author: Joe.Drumgoole@mongodb.com
"""

import pymongo
import argparse
from dateutil.parser import parse
from datetime import datetime
import pprint
import sys


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="mongodb://localhost:27017", help="default host for MongoDB")
    parser.add_argument("--pop", type=int,  help="New population value")
    parser.add_argument("--date", default=datetime.utcnow(), type=parse, help="Timestamp for new population")
    parser.add_argument("--zipcode", type=str, help="zipcode to update")
    parser.add_argument("--drop", default=False, action="store_true",  help="Drop the zipcodes_pop db")

    args = parser.parse_args()

    client = pymongo.MongoClient(host=args.host)
    database = client["demo"]
    zipcodes = database["zipcodes"]
    zipcodes_new = database["zipcodes_new"]

    if args.drop:
        print("Dropping 'zipcodes_new' database")
        zipcodes_new.drop()

    if args.zipcode:
        zip_doc = zipcodes.find_one({"_id" : args.zipcode})
        if zip_doc:
            print("Original zipcode data:")
            pprint.pprint(zip_doc)
        else:
            print(f"No such zipcode:{args.zipcode}")
            sys.exit(1)

    if args.pop and args.zipcode:
        zip_doc = zipcodes.find_one({"_id": args.zipcode})
        zip_doc["pop"] = {"pop": args.pop, "timestamp": args.date}
        zipcodes_new.update({"_id":args.zipcode}, zip_doc, upsert=True)
        print("New zipcode data: " + zip_doc["_id"])
        pprint.pprint(zip_doc)

