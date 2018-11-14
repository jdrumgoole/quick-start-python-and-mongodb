import pymongo
import pprint
import shutil

from pymongo import MongoClient

def print_cursor(cursor, pretty_print=False):
    (columns, lines) = shutil.get_terminal_size(fallback=(80, 24))
    try:
        line_count = 0
        for doc in cursor:
            if len(str(doc)) > columns or pretty_print:
                for line in pprint.pformat(doc).splitlines():
                    print(line)
                    line_count += 1
                    if line_count == lines - 5:
                        print("Hit Return to continue")
                        _ = input()
                        line_count = 0
            else:
                print(doc)
                line_count += 1
                if line_count == lines - 5:
                    print("Hit Return to continue")
                    _ = input()
                    line_count = 0

            (columns, lines) = shutil.get_terminal_size(fallback=(80, 24))

    except KeyboardInterrupt:
        return


def get_collection(host, db_name, collection_name):

    c: MongoClient = pymongo.MongoClient(host=host)
    db = c[db_name]
    collection = db[collection_name]
    return collection


client = pymongo.MongoClient()
database = client["demo"]
zipcodes = database["zipcodes"]
