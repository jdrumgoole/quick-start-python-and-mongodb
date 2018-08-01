"""
Print a mongodb cursor using the Python shell

@Author: Joe.Drumgoole@mongodb.com

"""
import pprint


def cursor_print(cursor):
    for i in cursor:
        pprint.pprint(i)
