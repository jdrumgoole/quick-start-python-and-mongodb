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

In MongoDB however databases and collections spring to life by being named.

First lets start a local single instance `mongod`
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

ObjectId('5b60558293d635192ad586e0')

<pre>ObjectId( <font color="red">5b605582</font> 93d635**192a**d586e0')</pre>

| Timestamp   | Machine Identifier        | Process ID | Counter |
|-------------|---------------------------|------------|---------|
| 4 Bytes     | 3 Bytes                   | 2 Bytes    | 3 Bytes |
| 5b605582    | 93d635                    | 192a       | d586e0  |
