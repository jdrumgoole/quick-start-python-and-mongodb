# PyMongo Create

MongoDB has exact analogies to most of the concepts we know from SQL land.

|  SQL           | MongoDB        |
|--------------- |----------------|
| Database       | Database       |
| Table          | [Collection](https://docs.mongodb.com/manual/core/databases-and-collections/#collections)     |
| Row            | [Document (JSON)](https://docs.mongodb.com/manual/core/document/)|
| Indexes        | [Indexes](https://docs.mongodb.com/manual/indexes/)   |
| Join           | [$lookup](https://docs.mongodb.com/manual/reference/operator/aggregation/lookup/)|
| ACID Transactions | [ACID Transactions](https://docs.mongodb.com/manual/core/write-operations-atomicity/#multi-document-transactions)|

In MongoDB collections represent a collection of JSON documents. There are no constraints on 
the structure of the JSON inserted and each document inserted can vary in the number of fields
and their sub-structure. 

Lets look at how we insert JSON documents into MongoDB. 

First lets start a local single instance of`mongod`
<pre>
$ <b>mkdir data</b>
$ <b>mongod --dbpath data</b>
2018-07-31T12:30:54.379+0100 I CONTROL  [main] Automatically disabling TLS 1.0, to force-enable TLS 1.0 specify --sslDisabledProtocols 'none'
2018-07-31T12:30:54.393+0100 I CONTROL  [initandlisten] MongoDB starting : pid=6421 port=27017 dbpath=data 64-bit host=Joes-MacBook-Air.local
2018-07-31T12:30:54.393+0100 I CONTROL  [initandlisten] db version v4.0.0-rc7
2018-07-31T12:30:54.393+0100 I CONTROL  [initandlisten] git version: 7230641bb09b1ceb04c3135cf83a5044c4838906
2018-07-31T12:30:54.393+0100 I CONTROL  [initandlisten] allocator: system
<b>etc ...</b>
</pre>

the `mongod` starts listen on port `27017` by default and as every MongoDB driver
defaults to connecting on `localhost:27017` we won't need to specify a [connection string](https://docs.mongodb.com/manual/reference/connection-string/)
explicitly in these early examples. 

Now we want to work with the Python driver. These examples are using Python 3.6.5 but everything
should work with versions as old as 2.7 without problems. 

Unlike SQL databases and collections in MongoDB spring to life automatically as we name then so lets
look at how create create a client proxy, a database and a collection.

<pre>
(venv) JD10Gen:ep002 jdrumgoole$ <b>python</b>
Python 3.6.5 (v3.6.5:f59c0932b4, Mar 28 2018, 03:03:55)
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>>
>>> <b>import pymongo</b>                                                           
>>> <b>client = pymongo.MongoClient()</b>                                         
>>> <b>database = client[ "ep002" ]</b>
>>> <b>people_collection = database[ "people_collection" ]</b>
>>> <b>result=database.people_collection.insert_one({"name" : "Joe Drumgoole"})</b>
>>> <b>database.people_collection.find_one()</b>
{'_id': ObjectId('5b62e6f8c3b498fbfdc1c20c'), 'name': 'Joe Drumgoole'}
>>> <b>result.inserted_id</b>
ObjectId('5b62e6f8c3b498fbfdc1c20c')
>>>
</pre>

First we import the `pymongo` library. (see [episode one](https://github.com/jdrumgoole/PyMongo-Monday/blob/master/ep001-SettingUpYourPyMongoEnvironment.md) for how to install the pymongo library)
Then we create the [local client proxy object](http://api.mongodb.com/python/current/api/pymongo/mongo_client.html),`client = pymongo.MongoClient()`. the client object manages a
connection pool to the server and can be used to set a number of operational parameters related to server connections.
We can leave the parameter list to the `MongoClient` call blank. The server by default listens on port `27017` and the
client by default attempts to connect to `localhost:27017`. 

Once we have a `client` object we can now create a database and a collection. These spring to life automatically when
they are referred to:
<pre>
>>> <b>database = client[ "ep002" ]</b>
>>> <b>people_collection = database[ "people_collection" ]</b>
</pre>

A database is effectively a container for collections. A collection provides a container for documents
 

ObjectId('5b60558293d635192ad586e0')

<pre>ObjectId( <font color="red">5b605582</font> 93d635**192a**d586e0')</pre>

| Timestamp   | Machine Identifier        | Process ID | Counter |
|-------------|---------------------------|------------|---------|
| 4 Bytes     | 3 Bytes                   | 2 Bytes    | 3 Bytes |
| 5b605582    | 93d635                    | 192a       | d586e0  |
