Last time we showed you how to setup up your <a href="https://blog.joedrumgoole.com/2018/09/10/pymongo-monday-episode-1-setting-up-your-pymongo-environment/">environment</a>.

In the next few episodes we will take you through the standard <a href="https://en.wikipedia.org/wiki/Create,_read,_update_and_delete">CRUD</a> operators that every database is expected to support. In this episode we will focus on the <strong>Create</strong> in CRUD.

## Create

Lets look at how we insert JSON documents into MongoDB.

First lets start a local single instance of <code>mongod</code> using <a href="https://github.com/aheckmann/m">m</a>.

```bash
$ m use stable
2018-08-28T14:58:06.674+0100 I CONTROL [main] Automatically disabling TLS 1.0, to force-enable TLS 1.0 specify --sslDisabledProtocols 'none'
2018-08-28T14:58:06.689+0100 I CONTROL [initandlisten] MongoDB starting : pid=43658 port=27017 dbpath=/data/db 64-bit host=JD10Gen.local
2018-08-28T14:58:06.689+0100 I CONTROL [initandlisten] db version v4.0.2
2018-08-28T14:58:06.689+0100 I CONTROL [initandlisten] git version: fc1573ba18aee42f97a3bb13b67af7d837826b47
2018-08-28T14:58:06.689+0100 I CONTROL [initandlisten] allocator: syste

etc...
```

The <code>mongod</code> starts listening on port <code>27017</code> by default. As every MongoDB driver
defaults to connecting on <code>localhost:27017</code> we won't need to specify a <a href="https://docs.mongodb.com/manual/reference/connection-string/">connection string</a> explicitly in these early examples.

Now, we want to work with the Python driver. These examples are using Python
3.6.5 but everything should work with versions as old as Python 2.7 without problems.

Unlike SQL databases, databases and collections in MongoDB only have to be named to be created. As we will see later this is a <em>lazy</em> creation process, and the database and corresponding collection are actually only created when a document is inserted.

```python
$ python
Python 3.6.5 (v3.6.5:f59c0932b4, Mar 28 2018, 03:03:55)
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>>
>>> import pymongo
>>> client = pymongo.MongoClient()
>>> database = client[ "ep002" ]
>>> people_collection = database[ "people_collection" ]
>>> result=people_collection.insert_one({"name" : "Joe Drumgoole"})
>>> result.inserted_id
ObjectId('5b7d297cc718bc133212aa94')
>>> result.acknowledged
True
>>> people_collection.find_one()
{'_id': ObjectId('5b62e6f8c3b498fbfdc1c20c'), 'name': 'Joe Drumgoole'}
True
>>>
```

First we import the <code>pymongo</code> library <i>(line 6)</i>. Then we create the <a href="http://api.mongodb.com/python/current/api/pymongo/mongo_client.html">local client proxy object</a>,
<code>client = pymongo.MongoClient()</code> <em>(line 7)</em> . The client object manages a connection pool to the server and can be used to set many operational parameters related to server connections.

We can leave the parameter list to the <code>MongoClient</code> call blank. Remember, the server by default listens on port <code>27017</code> and the client by default attempts to connect to <code>localhost:27017</code>.

Once we have a <code>client</code> object, we can now create a database, <code>ep002</code> <em>(line 8)</em>
and a collection, <code>people_collection</code> <em>(line 9)</em>. Note that we do not need an explicit DDL statement.

## Using Compass to examine the database server

A database is effectively a container for collections. A collection provides a container for documents. Neither the database nor the collection will be created on the server until you actually insert a document. If you check the server by connecting <a href="https://www.mongodb.com/products/compass">MongoDB Compass</a> you will see that there are no databases or collections on this server before the <code>insert_one</code> call.

<img src="https://raw.githubusercontent.com/jdrumgoole/PyMongo-Monday/master/images/ep002-compass-at-start.png" alt="screen shot of compass at start" />

These commands are lazily evaluated. So, until we actually insert a document into the collection, nothing happens on the server.

Once we insert a document:

```python
>>>> result=database.people_collection.insert_one({"name" : "Joe Drumgoole"})
>>> result.inserted_id
ObjectId('5b7d297cc718bc133212aa94')
>>> result.acknowledged
True
>>> people_collection.find_one()
{'_id': ObjectId('5b62e6f8c3b498fbfdc1c20c'), 'name': 'Joe Drumgoole'}
True
>>>
```

We will see that the database, the collection, and the document are created.

<img src="https://raw.githubusercontent.com/jdrumgoole/PyMongo-Monday/master/images/ep002-compass-with-collection.png" alt="screen shot of compass with collection" />

And we can see the document in the database.

<img src="https://raw.githubusercontent.com/jdrumgoole/PyMongo-Monday/master/images/ep002-compass-with-doc.png" alt="screen shot of compass with document" />

## _id Field

Every object that is inserted into a MongoDB database gets an automatically
generated <code>_id</code> field. This field is guaranteed to be unique for every document
inserted into the collection. This unique property is enforced as the _id field
is <a href="https://docs.mongodb.com/manual/indexes/#default-id-index">automatically indexed</a>
and the <a href="https://docs.mongodb.com/manual/core/index-unique/">index is unique</a>.

The value of the <code>_id</code> field is defined as follows:

<img src="https://raw.githubusercontent.com/jdrumgoole/PyMongo-Monday/master/images/ep002-objectid.png" alt="ObjectID" />

The <code>_id</code> field is generated on the client and you can see the PyMongo generation code in the <a href="https://github.com/mongodb/mongo-python-driver/blob/master/bson/objectid.py">objectid.py</a> file. Just search for the <code>def _generate</code> string. All MongoDB drivers generate <code>_id</code> fields on the client side. The <code>_id</code> field allows us to insert the same JSON object many times and allow each one to be uniquely identified. The <code>_id</code> field even gives a temporal ordering and you can get this from an ObjectID via the <a href="https://api.mongodb.com/python/2.7.1/api/bson/objectid.html">generation_time</a> method.

```Python
>>> from bson import ObjectId
>>> x=ObjectId('5b7d297cc718bc133212aa94')
>>> x.generation_time
datetime.datetime(2018, 8, 22, 9, 14, 36, tzinfo=)
>>> <b>print(x.generation_time)</b>
2018-08-22 09:14:36+00:00
>>>
```

<h2>Wrap Up</h2>

That is <em>create</em> in MongoDB. We started a <code>mongod</code> instance, created a <code>MongoClient</code> proxy, created a database and a collection and finally made then spring to life by inserting a document.

Next up we will talk more abou <em>Read</em> part of CRUD. In MongoDB this is the <code>find</code> query which we saw a little bit of earlier on in this episode.

<hr />

For direct feedback please pose your questions on <a href="https://www.twitter.com/jdrumgoole">twitter/jdrumgoole</a> that way everyone can see the answers.

The best way to try out MongoDB is via <a href="https://www.mongodb.com/cloud/atlas">MongoDB Atlas</a> our Database as a Service.
It’s free to get started with MongoDB Atlas so give it a try today.
