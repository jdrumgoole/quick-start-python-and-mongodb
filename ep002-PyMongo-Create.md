# PyMongo Create

(You should set up your environment as described in [Episode 1]()) 

In the next four episodes we will take you through the standard 
[CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete) operators that every database
is expected to support. In this episode we will focus on **Create**.

##Create
MongoDB has exact analogies to most of the concepts we know from SQL land.

|  SQL           | MongoDB        |
|--------------- |----------------|
| Database       | [Database](https://docs.mongodb.com/manual/core/databases-and-collections/)       |
| Table          | [Collection](https://docs.mongodb.com/manual/core/databases-and-collections/#collections)     |
| Row            | [Document (JSON)](https://docs.mongodb.com/manual/core/document/)|
| Indexes        | [Indexes](https://docs.mongodb.com/manual/indexes/)   |
| Join           | [$lookup](https://docs.mongodb.com/manual/reference/operator/aggregation/lookup/)|
| ACID Transactions | [ACID Transactions](https://docs.mongodb.com/manual/core/write-operations-atomicity/#multi-document-transactions)|

The main difference is that in MongoDB collections represent a collection of [JSON](https://www.json.org/) 
documents. There are no constraints on the structure of the JSON inserted. Each new document inserted 
can vary in the number of fields and their sub-structure compared to their predecessors. 

Lets look at how we insert JSON documents into MongoDB. 

First lets start a local single instance of `mongod` using [m](https://github.com/aheckmann/m).
<pre>
$ <b>m use stable</b>
2018-08-28T14:58:06.674+0100 I CONTROL  [main] Automatically disabling TLS 1.0, to force-enable TLS 1.0 specify --sslDisabledProtocols 'none'
2018-08-28T14:58:06.689+0100 I CONTROL  [initandlisten] MongoDB starting : pid=43658 port=27017 dbpath=/data/db 64-bit host=JD10Gen.local
2018-08-28T14:58:06.689+0100 I CONTROL  [initandlisten] db version v4.0.2
2018-08-28T14:58:06.689+0100 I CONTROL  [initandlisten] git version: fc1573ba18aee42f97a3bb13b67af7d837826b47
2018-08-28T14:58:06.689+0100 I CONTROL  [initandlisten] allocator: system

<b><i>etc...</i></b>
</pre>

the `mongod` starts listening on port `27017` by default. As every MongoDB driver
defaults to connecting on `localhost:27017` we won't need to specify a 
[connection string](https://docs.mongodb.com/manual/reference/connection-string/)
explicitly in these early examples. 

Now we want to work with the Python driver. These examples are using Python 3.6.5 but everything
should work with versions as old as Python 2.7 without problems. 

Unlike SQL databases, collections in MongoDB spring to life automatically as we name them. Let's
look at how create create a client proxy, a database and a collection.

<pre>
(venv) JD10Gen:ep002 jdrumgoole$ <b>python</b>
Python 3.6.5 (v3.6.5:f59c0932b4, Mar 28 2018, 03:03:55)
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>>
>>> <b>import pymongo</b>                                                     <i>(1)</i>                                                       
>>> <b>client = pymongo.MongoClient()</b>                                     <i>(2)</i>                                         
>>> <b>database = client[ "ep002" ]</b>                                       <i>(3)</i> 
>>> <b>people_collection = database[ "people_collection" ]</b>                <i>(4)</i> 
>>> <b>result=people_collection.insert_one({"name" : "Joe Drumgoole"})</b>    <i>(5)</i>
>>> <b>result.inserted_id</b>                                                 <i>(6)</i>
ObjectId('5b7d297cc718bc133212aa94')
>>> <b>result.acknowledged</b>
True
>>> <b>people_collection.find_one()</b>
{'_id': ObjectId('5b62e6f8c3b498fbfdc1c20c'), 'name': 'Joe Drumgoole'}
True
>>>
</pre>

First we import the `pymongo` library <i>(1)</i>. (see [episode one](https://github.com/jdrumgoole/PyMongo-Monday/blob/master/ep001-SettingUpYourPyMongoEnvironment.md) for how to install the pymongo library)
Then we create the [local client proxy object](http://api.mongodb.com/python/current/api/pymongo/mongo_client.html),
`client = pymongo.MongoClient()` <i>(2)</i> . The client object manages a connection pool to the server and can be 
used to set a number of operational parameters related to server connections.
We can leave the parameter list to the `MongoClient` call blank. The server by default listens on port `27017` and the
client by default attempts to connect to `localhost:27017`. 

Once we have a `client` object we can now create a database, `ep002` *(3)* and a collection, 
`people_collection` <i>(4)</i>. We do not need an explicit DDL. We just name these objects and the driver 
and server will ensure that they spring to life when a document  is inserted.

A database is effectively a container for collections. A collection provides a container for documents.
Neither the database nor the collection will be created on the server until you actually
insert a document. If you check the server by connecting [MongoDB Compass](https://www.mongodb.com/products/compass)
you will see that their are no databases or collection on this cluster before the `insert_one` call. 

![screen shot of compass at start](https://s3-eu-west-1.amazonaws.com/developer-advocacy-public/pymongo-monday/ep002-compass-at-start.png)

These commmands are lazily evaluated so until we actually insert a document into the collection nothing is
happening on the server.

Once we insert a document:

<pre>
>>> <b>result=database.people_collection.insert_one({"name" : "Joe Drumgoole"})</b>
>>> <b>result.inserted_id</b>
ObjectId('5b7d297cc718bc133212aa94')
>>> <b>result.acknowledged</b>
True
>>> <b>people_collection.find_one()</b>
{'_id': ObjectId('5b62e6f8c3b498fbfdc1c20c'), 'name': 'Joe Drumgoole'}
True
>>>
</pre>

Every object that is inserted into a MongoDB database gets and automatically generated `_id` field. This field
is guaranteed to be unique for every document inserted into the collection and this unique property is enforced
as the `_id` field is an [automatically indexed](https://docs.mongodb.com/manual/indexes/#default-id-index) 
and the [index is unique](https://docs.mongodb.com/manual/core/index-unique/). 
The value of the `_id` field is defined as follows:

![ObjectID](https://s3-eu-west-1.amazonaws.com/developer-advocacy-public/pymongo-monday/ep002-ObjectID.png)

The `_id` field is generated on the client and for PyMongo you can see the generation code in the 
[objectid.py](https://github.com/mongodb/mongo-python-driver/blob/master/bson/objectid.py) file. Just search
for the ` def _generate` string. All MongoDB drivers generate `_id` fields on the client side. the `_id` field
allows us to insert the same JSON object many times and allow each one to be uniquely identified. The `_id` 
field even gives a temporal ordering and you can get this from an ObjectID via the 
[generation_time](https://api.mongodb.com/python/2.7.1/api/bson/objectid.html) method.
<pre>
>>> <b>from bson import ObjectId</b>
>>> x=ObjectId('5b7d297cc718bc133212aa94')
>>> <b>x.generation_time</b>
datetime.datetime(2018, 8, 22, 9, 14, 36, tzinfo=<bson.tz_util.FixedOffset object at 0x1049efa20>)
>>> <b>print(x.generation_time)</b>
2018-08-22 09:14:36+00:00
>>>
</pre>

We will see that the database, the collection and the document spring to life once the document 
is inserted.
![screen shot of compass with collection](https://s3-eu-west-1.amazonaws.com/developer-advocacy-public/pymongo-monday/ep002-compass-with-collection.png)
And we can see the document in the database.
![screen shot of compass with document](https://s3-eu-west-1.amazonaws.com/developer-advocacy-public/pymongo-monday/ep002-compass-with-doc.png)
That is *create* in MongoDB. We started a `mongod` instance, created a `MongoClient` proxy, created
a database and a collection and finally made then spring to life by inserting a document. 

Next up we will talk more abou *Read* part of CRUD. In MongoDB this is the `find` query which we saw a 
little bit of earlier on in this episode.

