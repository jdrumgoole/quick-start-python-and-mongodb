Our final part of CRUD is the *D* for *Delete*. The delete
operator in the `PyMongo` driver is implemented in two functions:

* [`delete_one`](http://api.mongodb.com/python/current/api/pymongo/collection.html#pymongo.collection.Collection.delete_one)
* [`delete_many`](http://api.mongodb.com/python/current/api/pymongo/collection.html#pymongo.collection.Collection.delete_many)

Like their peers these are collection level operations that work 
with a filter argument to select the documents to be deleted. 

To see these operations at work we need to work on a local collection as the
Zipcode collection on Atlas is read-only. To dump this collection locally use
the [`mongodump`](https://docs.mongodb.com/manual/reference/program/mongodump/)
program. We point it at Atlas to download the data.

```bash
$ mongodump --host demodata-shard-0/demodata-shard-00-00-rgl39.mongodb.net:27017,demodata-shard-00-01-rgl39.mongodb.net:27017,demodata-shard-00-02-rgl39.mongodb.net:27017 --ssl --username readonly --password readonly --authenticationDatabase admin --db demo --collection zipcodes
```

This will dump all the data to a default directory called `dump` in the current
working directory.

Now we need to load this into a locally running instance of MongoDB. First we
start a local version of MongoDB (`mongod`). Once that is running we can run 
the following [`mongorestore`](https://docs.mongodb.com/manual/reference/program/mongorestore/) 
command.

```bash
$ mongorestore --drop
2019-01-13T21:01:46.921+0000	using default 'dump' directory
2019-01-13T21:01:46.921+0000	preparing collections to restore from
2019-01-13T21:01:46.990+0000	reading metadata for demo.zipcodes from dump/demo/zipcodes.metadata.json
2019-01-13T21:01:47.076+0000	restoring demo.zipcodes from dump/demo/zipcodes.bson
2019-01-13T21:01:47.393+0000	restoring indexes for collection demo.zipcodes from metadata
2019-01-13T21:01:47.629+0000	finished restoring demo.zipcodes (29353 documents)
2019-01-13T21:01:47.629+0000	done
```

The `mongorestore`command must be run from the same directory as we ran the 
`mongodump` command. It will create a new database called `demo` and within
that database will be a single collection called `zipcodes`. This collection
contains all the ZIP codes for the USA. This local collection is what we will
use to demonstrate the delete function. We can restore the full collection at
any time by runnning the `mongorestore --drop` command again. The `--drop` flag
ensures that we remove the database and collection before restoring so we
always end up with a single set of valid ZIP codes. 

Lets look at our collection using the Python interpreter.

```python
$ python
Python 3.6.5 (v3.6.5:f59c0932b4, Mar 28 2018, 03:03:55)
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import pymongo
>>> client=pymongo.MongoClient()
>>> db=client['demo']
>>> db.list_collection_names()
['zipcodes']
>>> zipcodes=db["zipcodes"]
>>> zipcodes.find_one()
{'_id': '01001', 'city': 'AGAWAM', 'loc': [-72.622739, 42.070206], 'pop': 15338, 'state': 'MA'}
```

Now, 

