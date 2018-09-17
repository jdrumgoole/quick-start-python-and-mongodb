# PyMongo Monday Episode 2 : Create

(You should set up your environment as described in [Episode 1]()) 

In the next four episodes we will take you through the standard 
[CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete) operators that every database
is expected to support. In this episode we will focus on the **Create** in CRUD.

##Create
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

The `mongod` starts listening on port `27017` by default. As every MongoDB driver
defaults to connecting on `localhost:27017` we won't need to specify a 
[connection string](https://docs.mongodb.com/manual/reference/connection-string/) explicitly in these early examples. 

Now, we want to work with the Python driver. These examples are using Python 
3.6.5 but everything should work with versions as old as Python 2.7 without 
problems. 

Unlike SQL databases, databases and collections in MongoDB only have to be named 
to be created. As we will
see later this is a *lazy* creation process, and the database and corresponding 
collection are actually only created when a document is inserted. 

<pre>
$ <b>python</b>
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

First we import the `pymongo` library <i>(1)</i>, (see [episode one](https://github.com/jdrumgoole/PyMongo-Monday/blob/master/ep001-SettingUpYourPyMongoEnvironment.md) for how to install the pymongo library).
Then we create the [local client proxy object](http://api.mongodb.com/python/current/api/pymongo/mongo_client.html),
`client = pymongo.MongoClient()` <i>(2)</i> . The client object manages a 
connection pool to the server and can be used to set many operational 
parameters related to server connections.We can leave the parameter 
list to the `MongoClient` call blank. Remember, the server by default listens on 
port `27017` and the client by default attempts to connect to `localhost:27017`. 

Once we have a `client` object, we can now create a database, `ep002` *(3)* 
and a collection, `people_collection` <i>(4)</i>. Note that we do not need an
explicit DDL statement. 

##Using Compass to examine the database server
A database is effectively a container for collections. A collection provides a 
container for documents.Neither the database nor the collection will be 
created on the server until you actually insert a document. If you check the 
server by connecting [MongoDB Compass](https://www.mongodb.com/products/compass)
you will see that there are no databases or collections on this server 
before the `insert_one` call. 

![screen shot of compass at start](https://s3-eu-west-1.amazonaws.com/developer-advocacy-public/pymongo-monday/ep002-compass-at-start.png)

These commands are lazily evaluated. So, until we actually insert a document into the collection, nothing 
happens on the server.

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

We will see that the database, the collection, and the document are created.

![screen shot of compass with collection](https://s3-eu-west-1.amazonaws.com/developer-advocacy-public/pymongo-monday/ep002-compass-with-collection.png)

And we can see the document in the database.

![screen shot of compass with document](https://s3-eu-west-1.amazonaws.com/developer-advocacy-public/pymongo-monday/ep002-compass-with-doc.png)

##_id Field

Every object that is inserted into a MongoDB database gets an automatically 
generated `_id` field. This fieldis guaranteed to be unique for every document 
inserted into the collection. This unique property is enforced as the _id field 
is [automatically indexed](https://docs.mongodb.com/manual/indexes/#default-id-index) 
and the [index is unique](https://docs.mongodb.com/manual/core/index-unique/). 

The value of the `_id` field is defined as follows:

![ObjectID](https://github.com/jdrumgoole/PyMongo-Monday/raw/master/images/ep002-objectid.png)


The `_id` field is generated on the client and you can see the PyMongo generation code in the 
[objectid.py](https://github.com/mongodb/mongo-python-driver/blob/master/bson/objectid.py) file. Just search
for the `def _generate` string. All MongoDB drivers generate `_id` fields on the client side. The `_id` field
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

##Wrap Up
That is *create* in MongoDB. We started a `mongod` instance, created a `MongoClient` proxy, created
a database and a collection and finally made then spring to life by inserting a document.

Next up we will talk more abou *Read* part of CRUD. In MongoDB this is the `find` query which we saw a 
little bit of earlier on in this episode.

---

For direct feedback please pose your questions on [twitter/jdrumgoole](https://www.twitter.com/jdrumgoole) that way everyone can see the answers.

The best way to try out MongoDB is via [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) our Database as a Service.
It’s free to get started with MongoDB Atlas so give it a try today.

