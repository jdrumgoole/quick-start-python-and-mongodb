"""
Convenience functions for MongoDB in the Python shell

@Author: Joe.Drumgoole@mongodb.com

"""
import pprint
import pymongo


def get_collection(host, db_name, collection_name ):

    client = pymongo.MongoClient(host=host)
    db = client[db_name]
    collection = db[collection_name]
    return collection


def print_cursor(cursor, plain_print=True, buffer_size=20):
    try:
        buffer_count = 0
        for doc in cursor:
            if len(str(doc)) < 80 or plain_print:
                print(doc)
                buffer_count += 1
                if buffer_count == buffer_size:
                    print("Hit Return to continue")
                    _ = input()
                    buffer_count = 0
            else:
                for line in pprint.pformat(doc).splitlines():
                    print(line)
                    buffer_count += 1
                if buffer_count == buffer_size:
                    print("Hit Return to continue")
                    _ = input()
                    buffer_count = 0
    except KeyboardInterrupt:
        return
