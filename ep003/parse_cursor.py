import pprint


def parsex(cursor):
    for doc in cursor:
        for i,line in enumerate(pprint.pformat(doc).splitlines(), 1):
            print(i, line)
            if 20 == int(i):
                print("Hit Return to continue")
                x=input()
