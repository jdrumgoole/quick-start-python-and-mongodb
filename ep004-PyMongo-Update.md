# PyMongo Monday - EP03 - Update

This is part 4 of PyMongo Monday. Previously we have
covered:

 * EP1 - Setting up your MongoDB Environment
 * EP2 - Create - the C in CRUD
 * EP2 - Read - the R in CRUD

 
We are now into *Update*, the *U* in CRUD. The key aspect of update is the 
ability to change a document in place. In order for this to happen we must
have some way to select and document and change parts of that document.In
the `pymongo` driver this is achieved with two types of functions:
 
 * `update`: [updateOne](http://api.mongodb.com/python/current/api/pymongo/operations.html#pymongo.operations.UpdateOne), 
 [updateMany](http://api.mongodb.com/python/current/api/pymongo/operations.html#pymongo.operations.UpdateMany)
 
Each update operation can take a range of `update operators` that
define how we can mutate a document during update. 

 
Lets get a copy of the ZIPs database as our copy hosted in Atlas is not
writable so we can't test `update`.
 
We can take a copy with this simple script:
 
 ```bash
 $ mongodump --host demodata-shard-0/demodata-shard-00-00-rgl39.mongodb.net:27017,demodata-shard-00-01-rgl39.mongodb.net:27017,demodata-shard-00-02-rgl39.mongodb.net:27017 --ssl --username readonly --password readonly --authenticationDatabase admin --db demo
2018-10-22T01:18:35.330+0100	writing demo.zipcodes to
2018-10-22T01:18:36.097+0100	done dumping demo.zipcodes (29353 documents)
```

This will create a backup of the data in a `dump` directory in the current
working directory.

to restore the data to a local `mongod` make sure you are running `mongod` 
locally and just run `mongorestore` 

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
 'pop': 15338,                    # Population of zip code        
 'state': 'MA',                   # State
}
```

Lets say we want to change the population to reflect the most [current value](https://www.unitedstateszipcodes.org/01001/#stats).
Today the population if 01001 is approximately 16769. to change the value we
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
>>> zipcodes.update( {"_id" : "01001"}, {"$set" : { "population_record" : []}})
{'n': 1, 'nModified': 1, 'ok': 1.0, 'updatedExisting': True}
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

You can see how we use `pprint` to produce the output in slightly more
readable format. 



