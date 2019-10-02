from mimesis import Generic, randints
from mimesis.enums import Gender
import pymongo
import argparse
import random
import pprint
from datetime import timedelta,datetime
import sys


class User:

    def __init__(self, locale:str="en", seed:int = None):

        self._locale = locale
        self._seed = seed
        if self._seed:
            self._generic = Generic(self._locale, self._seed)
        else:
            self._generic = Generic(self._locale)

        self._user_id = 1000

    def make_user(self):

        person = self._generoc.person
        address = self._generic.address
        business = self._generic.business
        internet = self._generic.internet
        datetime = self._generic.datetime

        user = {}
        interests = ["Soccer", "Golf", "Football", "Stamp Collecting", "skydiving",
                     "Board gaming", "Darts", "Swimmming", "Triathlon", "Running",
                     "Reading", "politics"]

        gender = random.choice(list(Gender))
        gender_string = str(gender).split(".")[1]
        user["first_name"] = person.name(gender)
        user["last_name"] = person.surname(gender)
        user["gender"] = gender_string
        user["company"] = business.company()
        email_domain = "".join(user['company'].lower().split(" "))
        user["email"] = f"{user['first_name']}.{user['last_name']}@{email_domain}{internet.top_level_domain()}"
        year = random.randint(2000, 2018)
        user["registered"] = datetime.datetime(start=year)
        user["user_id"] = self._user_id
        self._user_id = self._user_id + 1
        user["country"]= address.country()
        user["city"] = address.city()
        user["phone"] = person.telephone()
        user["location"] = { "type": "Point", "coordinates" : [address.longitude(), address.latitude()]}
        user["language"] = person.language()
        sample_size = random.randint(0,5)
        user["interests"] = random.sample(interests, sample_size)
        user["last_login"] = user["registered"] + timedelta(minutes=random.randint(5, 600000))
        return user

    def make_sessions(self, user):


        start_session = { "user" : user["user_id"],
                          "login" : user["registered"]}
        end_session = {"user": user["user_id"],
                       "logout" : start_session["login"] + timedelta(minutes=random.randint(0, 180),
                                                                     seconds=random.randint(1, 59),
                                                                     milliseconds=random.randint( ))}
        sessions = random.randint(1, 300)

        for i in range(1, sessions):
            start_session = { "user" : user["user_id"],
                              "login" : }


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--mongodb", default="mongodb://localhost:27017", help="MongoDB host: [default: %(default)s]")
    parser.add_argument("--database", default="USERS",help="MongoDB database name: [default: %(default)s]")
    parser.add_argument("--collection", default="profiles", help="Default collection for random data:[default: %(default)s]")
    parser.add_argument("--count", default=10, type=int, help="How many docs to create: [default: %(default)s]")
    parser.add_argument("--batchsize", default=1000, type=int, help="How many docs to insert per batch: [default: %(default)s]")
    parser.add_argument("-locale", default="en", help="Locale to use for data: [default: %(default)s]")
    parser.add_argument("--seed", type=int, help="Use this seed value to ensure you always get the same data")
    parser.add_argument("--drop", default=False, action="store_true", help="Drop data before creating a new set [default: %(default)s]")
    parser.add_argument("--report", default=False, action="store_true", help="send all generated JSON to the screen [default: %(default)s]" )
    args = parser.parse_args()

    client = pymongo.MongoClient(args.mongodb)

    db = client[args.database]
    collection =db[args.collection]

    batch = []

    if args.drop:
        print(f"Dropping collection: {collection.name}")
        db.drop_collection(args.collection)
    


    print("")
    try:
        start=datetime.utcnow()
        for i in range(args.count):
            user = make_user(generic)
            #print(f"{i+1}. {user['_id']}")
            if args.report:
                pprint.pprint(user)
            batch.append(user)
            if len(batch) % args.batchsize == 0:
                collection.insert_many(batch)
                batch = []

        if len(batch) > 0:
            collection.insert_many(batch)
            batch = []

        finish = datetime.utcnow()
    except pymongo.errors.BulkWriteError as e:
        print(e.details)
        print(f"Processed {i} docs")
        sys.exit(1)

    elapsed = finish - start
    print("")
    print(f"Inserted {i+1} docs into {db.name}.{collection.name}")
    print(f"Elapsed time: {elapsed}")
    elapsed_time = float(elapsed.seconds) + float(elapsed.microseconds)/1000000
    print(f"Elapsed seconds: {elapsed_time}")

    docs_per_second = float(i+1)/elapsed_time
    print(f"Inserted {round(docs_per_second, 0)} docs per second")

    
        

