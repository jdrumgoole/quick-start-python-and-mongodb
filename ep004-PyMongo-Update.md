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
 
 * `replace` : find_one_and_replace, replace_one
 * `update`: updateOne, updateMany
 
 The `replace` functions are designed to take a whole document as a match and 
 replace that matching document with a brand new document. the `update`
 style functions are more flexible as they can take a range of 
 `update operators` that only update using specific fields.
 
 There is no `replace_many` as replacing many copies of a document with
 a single document doesn't make a lot of sense.
 
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

```bash
$ mongo
MongoDB shell version v4.0.1
connecting to: mongodb://127.0.0.1:27017
MongoDB server version: 4.0.1

> show databases
admin   0.000GB
config  0.000GB
demo    0.000GB
local   0.000GB
> use demo
switched to db demo
> show collections
zipcodes
>
``` 

