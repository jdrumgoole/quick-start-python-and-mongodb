import pymongo
import pprint
import shutil

from pymongo import MongoClient


def client(mongodb_uri="mongodb://localhost:27017"):
    return pymongo.MongoClient(mongodb_uri)


def db(name, mongodb_uri="mongodb://localhost:27017"):
    return pymongo.MongoClient(mongodb_uri).get_database(name)


def collection(db_name, collection_name, mongodb_uri="mongodb://localhost:27017"):
    return pymongo.MongoClient(mongodb_uri).get_database(db_name).get_collection(collection_name)


def show_databases(mongodb_uri="mongodb://localhost:27017"):
    for i in pymongo.MongoClient(mongodb_uri).list_database_names():
        print(i)


def pager(lines, overlap=0):
    try:
        _, terminal_lines = shutil.get_terminal_size(fallback=(80, 24))
        line_count = 0
        for i, l in enumerate(lines, 1):
            print(l)
            line_count += 1
            if line_count == terminal_lines - overlap - 1:
                line_count = 0
                print("Hit Return to continue (q or quit to exit)", end="")
                user_input = input()
                if user_input.lower().strip() in ["q", "quit", "exit"]:
                    break

            _, terminal_lines = shutil.get_terminal_size(fallback=(80, 24))
    except KeyboardInterrupt:
        pass


def cursor_to_lines(cursor):
    for doc in cursor:
        for l in pprint.pformat(doc).splitlines():
            yield l


def print_cursor(cursor, overlap=3):
    return pager(cursor_to_lines(cursor), overlap)

# def print_cursor(cursor):
#
#     terminal_columns, terminal_lines = shutil.get_terminal_size(fallback=(80, 24))
#     try:
#         pager(cursor_to_lines(cursor))
#         line_count = 0
#         for doc in cursor_to_lines(cursor) :
#             if len(str(doc)) > terminal_columns or pretty_print:
#                 pager(pprint.pformat(doc).splitlines())
#             else:
#                 print(doc)
#                 line_count += 1
#                 if line_count == terminal_lines - 5:
#                     print("Hit Return to continue")
#                     _ = input()
#                     line_count = 0
#
#             terminal_columns, terminal_lines = shutil.get_terminal_size(fallback=(80, 24))
#
#     except KeyboardInterrupt:
#         return


def get_collection(host, db_name, collection_name):

    c: MongoClient = pymongo.MongoClient(host=host)
    db = c[db_name]
    collection = db[collection_name]
    return collection


client = pymongo.MongoClient()
database = client["demo"]
zipcodes = database["zipcodes"]
