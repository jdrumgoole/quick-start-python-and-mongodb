# PyMongo Monday - EP03 - Update

This is part 4 of PyMongo Monday. Previously we have covered:

 * EP1 - [Setting up your MongoDB Environment](https://www.mongodb.com/blog/post/pymongo-monday-setting-up-your-pymongo-environment)
 * EP2 - [Create - the C in CRUD](https://www.mongodb.com/blog/post/pymongo-monday-pymongo-create)
 * EP2 - [Read - the R in CRUD](https://www.mongodb.com/blog/post/pymongo-monday-episode-3-read)

 
We are now into *Update*, the *U* in CRUD. The key aspect of update is the 
ability to change a document in place. In order for this to happen we must
have some way to select the document and change parts of that document. In
the `pymongo` driver this is achieved with two functions:
 
 * `[update_one]`(http://api.mongodb.com/python/current/api/pymongo/operations.html#pymongo.operations.UpdateOne), 
 * `[update_many]`(http://api.mongodb.com/python/current/api/pymongo/operations.html#pymongo.operations.UpdateMany)
 
Each update operation can take a range of `update operators` that
define how we can mutate a document during update. 

Lets get a copy of the zipcode database hosted on [MongoDB Atlas](https://www.mongodb.com/cloud).
As our copy hosted in Atlas is not writable we can't test `update` directly on
it.
 
However, we can create a local copy with this simple script:
 
 ```bash
 $ mongodump --host demodata-shard-0/demodata-shard-00-00-rgl39.mongodb.net:27017,demodata-shard-00-01-rgl39.mongodb.net:27017,demodata-shard-00-02-rgl39.mongodb.net:27017 --ssl --username readonly --password readonly --authenticationDatabase admin --db demo
2018-10-22T01:18:35.330+0100	writing demo.zipcodes to
2018-10-22T01:18:36.097+0100	done dumping demo.zipcodes (29353 documents)
```

This will create a backup of the data in a `dump` directory in the current
working directory.

to restore the data to a local `mongod` make sure you are running `mongod` 
locally and just run `mongorestore` in the same directory as you ran
`mongodump`.

```bash
$ mongorestore
2018-10-22T01:19:19.064+0100	using default 'dump' directory
2018-10-22T01:19:19.064+0100	preparing collections to restore from
2018-10-22T01:19:19.066+0100	reading metadata for demo.zipcodes from dump/demo/zipcodes.metadata.json
2018-10-22T01:19:19.211+0100	restoring demo.zipcodes from dump/demo/zipcodes.bson
2018-10-22T01:19:19.943+0100	restoring indexes for collection demo.zipcodes from metadata
2018-10-22T01:19:20.364+0100	finished restoring demo.zipcodes (29353 documents)
2018-10-22T01:19:20.364+0100	done
```

You will now have a `demo` database on your local `mongod` with single
collection called `zipcodes`.

```python
$ python
Python 3.6.5 (v3.6.5:f59c0932b4, Mar 28 2018, 03:03:55)
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import pymongo
>>> client = pymongo.MongoClient()
>>> database=client['demo']
>>> zipcodes=database["zipcodes"]
>>> zipcodes.find_one()
{'_id': '01001', 'city': 'AGAWAM', 'loc': [-72.622739, 42.070206], 'pop': 15338, 'state': 'MA'}
>>>
>
```

Each document in this database has the same format:

```python
{
 '_id': '01001',                  # ZIP code
 'city': 'AGAWAM',                # City name
 'loc': [-72.622739, 42.070206],  # Geo Spatial Coordinates
 'pop': 15338,                    # Population of within zip code        
 'state': 'MA',                   # Two letter state code (MA = Massachusetts)
}
```

Let's say we want to change the population to reflect the most [current value](https://www.unitedstateszipcodes.org/01001/#stats).
Today the population of 01001 is approximately 16769. to change the value we
would execute the following update.

```python
>>> zipcodes.update( {"_id" : "01001"}, {"$set" : { "pop" : 16769}})
{'n': 1, 'nModified': 1, 'ok': 1.0, 'updatedExisting': True}
>>> zipcodes.find_one({"_id" : "01001"})
{'_id': '01001', 'city': 'AGAWAM', 'loc': [-72.622739, 42.070206], 'pop': 16769, 'state': 'MA'}
>>>
```

Here we see the [`$set`](https://docs.mongodb.com/manual/reference/operator/update/set/#up._S_set)
operator in action. The `$set` operator will set a field to a new value or
create that field if it  doesn't exist in the document. So we could add 
a new field by doing:

```python
>>> zipcodes.update_one( {"_id" : "01001"}, {"$set" : { "population_record" : []}})
<pymongo.results.UpdateResult object at 0x1042dc488>
>>> zipcodes.find_one({"_id" : "01001"})
{'_id': '01001', 'city': 'AGAWAM', 'loc': [-72.622739, 42.070206], 'pop': 16769, 'state': 'MA', 'population_record': []}
>>>
```

Here we are adding a new field called `population_record`. This field is 
an array field and has been set to the empty array for now. Now we can 
update the array with a history of the population for the zip code area.

```python
>>> zipcodes.update_one({"_id" : "01001"}, { "$push" : { "population_record" : { "pop" : 15338, "timestamp": None }}})
<pymongo.results.UpdateResult object at 0x106c210c8>
>>> zipcodes.find_one({"_id" : "01001"})
{'_id': '01001', 'city': 'AGAWAM', 'loc': [-72.622739, 42.070206], 'pop': 16769, 'state': 'MA', 'population_record': [{'pop': 15338, 'timestamp': None}]}
>>> from datetime import datetime
>>> zipcodes.update_one({"_id" : "01001"}, { "$push" : { "population_record" : { "pop" : 16769, "timestamp": datetime.utcnow() }}})
<pymongo.results.UpdateResult object at 0x106c21908>
>>> zipcodes.find_one({"_id" : "01001"})                                                                 
{'_id': '01001', 'city': 'AGAWAM', 'loc': [-72.622739, 42.070206], 'pop': 16769, 'state': 'MA', 'population_record': [{'pop': 15338, 'timestamp': None}, {'pop': 16769, 'timestamp': datetime.datetime(2018, 10, 22, 11, 37, 5, 60000)}]}
>>> x=zipcodes.find_one({"_id" : "01001"})
>>> x
{'_id': '01001', 'city': 'AGAWAM', 'loc': [-72.622739, 42.070206], 'pop': 16769, 'state': 'MA', 'population_record': [{'pop': 15338, 'timestamp': None}, {'pop': 16769, 'timestamp': datetime.datetime(2018, 10, 22, 11, 37, 5, 60000)}]}
>>> import pprint
>>> pprint.pprint(x)
{'_id': '01001',
 'city': 'AGAWAM',
 'loc': [-72.622739, 42.070206],
 'pop': 16769,
 'population_record': [{'pop': 15338, 'timestamp': None},
                       {'pop': 16769,
                        'timestamp': datetime.datetime(2018, 10, 22, 11, 37, 5, 60000)}],
 'state': 'MA'}
>>>
```

Here we have appended two documents to the array so that we have a history
of the changes in population. The original value of 15338 was captured at 
an unknown time in the past so we set that timestamp to `None`. We updated the
other value today so we can set that timestamp to the current time. In both
cases we use the [`$push`](https://docs.mongodb.com/manual/reference/operator/update/push/#up._S_push)
operator to push new elements onto the end of the array `population_record`.

You can see how we use `pprint` to produce the output in a slightly more
readable format. 

If we want to apply updates to more than one record we use the 
[`update_many`](http://api.mongodb.com/python/current/api/pymongo/collection.html#pymongo.collection.Collection.update_many) 
to apply changes to more than one document. Now if the filter applies to more
than one document the changes will be applied to each document. So imagine
we wanted to add the city sales tax to each city. First, we want to add the 
city sales tax to all the zipcode regions in New York.

```python
>>> zipcodes.update_many( {'city': "NEW YORK"}, { "$set" : { "sales tax" : 4.5 }})
<pymongo.results.UpdateResult object at 0x1042dcd88>
>>> zipcodes.find( {"city": "NEW YORK"})
<pymongo.cursor.Cursor object at 0x101e09410>
>>> cursor=zipcodes.find( {"city": "NEW YORK"})
>>> cursor.next()
{u'city': u'NEW YORK', u'loc': [-73.996705, 40.74838], u'sales tax': 4.5, u'state': u'NY', u'pop': 18913, u'_id': u'10001'}
>>> cursor.next()
{u'city': u'NEW YORK', u'loc': [-73.987681, 40.715231], u'sales tax': 4.5, u'state': u'NY', u'pop': 84143, u'_id': u'10002'}
>>> cursor.next()
{u'city': u'NEW YORK', u'loc': [-73.989223, 40.731253], u'sales tax': 4.5, u'state': u'NY', u'pop': 51224, u'_id': u'10003'}
>>>
```

The final kind of `update` operation we want to talk about is `upsert`. We can 
add the `upsert` flag to any update operation to do an insert of the target
document even when it doesn't match. When is this useful?

Imagine we have a read-only collection of zipcode data and we want to create a 
new collection (call it `zipcodes_new`) that contains updates to the zipcodes
that contain changes in population.

As we collect new population stats zipcode by zipcode we want to update 
the `zipcodes_new` collection with new documents containing the updated zipcode 
data. In order to simplify this process we can do the updates as an `upsert`.

Below is a fragment of code from [update_population.py](https://github.com/jdrumgoole/PyMongo-Monday/blob/master/ep004/update_population.py)
```python
zip_doc = zipcodes.find_one({"_id": args.zipcode})
zip_doc["pop"] = {"pop": args.pop, "timestamp": args.date}
zipcodes_new.update({"_id":args.zipcode}, zip_doc, upsert=True)
print("New zipcode data: " + zip_doc["_id"])
pprint.pprint(zip_doc)
```
The `upsert=True` flag ensures that if we don't match the initial clause 
`{"_id":args.zipcode}` we will still insert the `zip_doc` doc. This is a common
pattern for `upsert` usage: Initially we insert based on a unique key. As the
the number of inserts grows the likelihood that we will be updating an
existing key as opposed to inserting a new key grows. the `upsert=True` flag 
allows us to handle both situations in a single `update` statement.

There is a lot more to [update](https://docs.mongodb.com/manual/reference/method/db.collection.update/)
and will return to `update` later in the series. For now just remember that
`update` is generally used for mutating existing documents using a range 
of [update operators](https://docs.mongodb.com/manual/reference/operator/update/#id1).

Next time we will complete our first pass over CRUD operations with the 
final function [delete](https://docs.mongodb.com/manual/tutorial/remove-documents/)


 







