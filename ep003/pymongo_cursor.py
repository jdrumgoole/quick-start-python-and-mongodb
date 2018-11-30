"""
Class for printing out a MongoDB Cursor

joe.drumgoole@mongodb.com

"""

class MongoDB_Cursor(object):

    def __init__(self, cursor, plain_print=True, buffer_size=20):
        self._cursor = cursor
        self._plain_print = plain_print
        self._buffer_size = buffer_size

    def __call__(self):
        try:
            buffer_count = 0
            for doc in cursor:
                if len(str(doc)) < 80 or plain_print:
                    print(doc)
                    buffer_count += 1
                    if buffer_count == self._buffer_size:
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
