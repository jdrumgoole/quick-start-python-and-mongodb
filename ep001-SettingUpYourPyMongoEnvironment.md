# Setting Up Your PyMongo Environment
Welcome to PyMongo Monday. This is the first in a series of regular blog posts that will introduce developers to 
programming MongoDB using the Python programming language. It’s called PyMongo Monday because 
[PyMongo](https://api.mongodb.com/python/current/) is 
the name of the client library (in MongoDB speak we refer to it as a "driver") we use to interact 
with the MongoDB Server. Monday because we aim to release each new episode on Monday.

To get started we need to install the toolchain used by a typical MongoDB Python developer.

## Installing m
First up is [**m**](https://github.com/aheckmann/m). Hard to find online unless your search for "MongoDB m", **m** is 
a tool to manage and use multiple installations of the MongoDB Server in parallel. It is an invaluable tool 
if you want to try out the latest and greatest beta version but still continue mainline development 
on our current stable release.

The easiest way to install **m** is with [npm](https://nodejs.org/en/) the Node.js package manager 
(which it turns out is not just for Node.js). 
<pre>
$ <b>sudo npm install -g m</b>
Password:******
/usr/local/bin/m -> /usr/local/lib/node_modules/m/bin/m
+ m@1.4.1
updated 1 package in 2.361s
$
</pre>
If you can’t or don’t want to use npm you can download and install directly from the github 
[repo](https://github.com/aheckmann/m). See the [README](https://github.com/aheckmann/m/blob/master/README.md) 
there for details.

For today we will use **m** to install the current stable production version 
([4.0.2](https://docs.mongodb.com/manual/release-notes/4.0/) at the time of writing).  
We run the **stable** command to achieve this.

<pre>
$ <b>m stable</b>
MongoDB version 4.0.2 is not installed.
Installation may take a while. Would you like to proceed? [y/n] <b>y</b>
... installing binary

######################################################################## 100.0%
/Users/jdrumgoole
... removing source
... installation complete
$
</pre>

If you need to use the path directly in another program you can get that with **m bin.**

<pre>
$ <b>m bin 4.0.0</b>
/usr/local/m/versions/4.0.1/bin
$
</pre>

To run the corresponding binary do **m use stable**

<pre>
$ <b>m use stable</b>
2018-08-28T11:41:48.157+0100 I CONTROL  [main] Automatically disabling TLS 1.0, to force-enable TLS 1.0 specify --sslDisabledProtocols 'none'
2018-08-28T11:41:48.171+0100 I CONTROL  [initandlisten] MongoDB starting : pid=38524 port=27017 dbpath=/data/db 64-bit host=JD10Gen.local
2018-08-28T11:41:48.171+0100 I CONTROL  [initandlisten] db version v4.0.2
2018-08-28T11:41:48.171+0100 I CONTROL  [initandlisten] git version: fc1573ba18aee42f97a3bb13b67af7d837826b47
<b><i>&lt other server output &gt</i></b>
<b>...</b>
2018-06-13T15:52:43.648+0100 I NETWORK  [initandlisten] waiting for connections on port 27017
</pre>

Now that we have a server running we can confirm that it works by connecting via the 
[mongo shell](https://docs.mongodb.com/manual/mongo/).

<pre>
$ <b>mongo</b>
MongoDB shell version v4.0.0
connecting to: mongodb://127.0.0.1:27017
MongoDB server version: 4.0.0
Server has startup warnings:
2018-07-06T10:56:50.973+0100 I CONTROL  [initandlisten]
2018-07-06T10:56:50.973+0100 I CONTROL  [initandlisten] ** WARNING: Access control is not enabled for the database.
2018-07-06T10:56:50.973+0100 I CONTROL  [initandlisten] **          Read and write access to data and configuration is unrestricted.
2018-07-06T10:56:50.973+0100 I CONTROL  [initandlisten] ** WARNING: You are running this process as the root user, which is not recommended.
2018-07-06T10:56:50.973+0100 I CONTROL  [initandlisten]
2018-07-06T10:56:50.973+0100 I CONTROL  [initandlisten] ** WARNING: This server is bound to localhost.
2018-07-06T10:56:50.973+0100 I CONTROL  [initandlisten] **          Remote systems will be unable to connect to this server.
2018-07-06T10:56:50.973+0100 I CONTROL  [initandlisten] **          Start the server with --bind_ip &lt address&gt to specify which IP
2018-07-06T10:56:50.973+0100 I CONTROL  [initandlisten] **          addresses it should serve responses from, or with --bind_ip_all to
2018-07-06T10:56:50.973+0100 I CONTROL  [initandlisten] **          bind to all interfaces. If this behavior is desired, start the
2018-07-06T10:56:50.973+0100 I CONTROL  [initandlisten] **          server with --bind_ip 127.0.0.1 to disable this warning.
2018-07-06T10:56:50.973+0100 I CONTROL  [initandlisten]

&mdash&mdash&mdash
Enable MongoDB's free cloud-based monitoring service to collect and display
metrics about your deployment (disk utilization, CPU, operation statistics,
etc).

The monitoring data will be available on a MongoDB website with a unique
URL created for you. Anyone you share the URL with will also be able to
view this page. MongoDB may use this information to make product
improvements and to suggest MongoDB products and deployment options to you.

To enable free monitoring, run the following command:
db.enableFreeMonitoring()
---

>
</pre>

These warnings are standard. They flag that this database has no access controls setup by default and, 
that it is only listening to connections coming from the machine it is running on (*localhost*). 
We will learn how to setup access control and listen on a broader range of ports in later episodes.

## Installing the PyMongo Driver

But this series is not about the MongoDB Shell, which uses JavaScript as its coin of the realm, 
it’s about Python. How do we connect to the database with Python?

First we need to install the MongoDB Python Driver, [PyMongo](https://docs.mongodb.com/ecosystem/drivers/). 
In MongoDB parlance a driver is a language-specific client library that allows developers to 
interact with the server in the idiom of their own programming language.

For Python that means installing the driver with `pip`. In node.js the driver is 
installed using `npm` and in Java you can use `maven`.

<pre>
$ <b>pip3 install pymongo</b>
Collecting pymongo
  Downloading https://files.pythonhosted.org/packages/a1/e0/51df08036e04c1ddc985a2dceb008f2f21fc1d6de711bb6cee85785c1d78/pymongo-3.7.1-cp27-cp27m-macosx_10_13_intel.whl (333kB)
    100% |████████████████████████████████| 337kB 4.1MB/s
Installing collected packages: pymongo
Successfully installed pymongo-3.7.1
$
</pre>

We recommend you use a [virtual environment](https://docs.python.org/3/library/venv.html) to isolate your 
PyMongo Monday code. This is not required but is very convenient for isolating different development streams.

Now we can connect to the database:

<pre>
$ <b>python</b>
Python 3.6.5 (v3.6.5:f59c0932b4, Mar 28 2018, 03:03:55)
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> <b>import pymongo</b>                                                  <i>(1)</i>
>>> <b>client = pymongo.MongoClient(host="mongodb://localhost:8000")</b>   <i>(2)</i>
>>> <b>result = client.admin.command("isMaster")</b>                       <i>(3)</i>
>>> <b>import pprint</b>
>>> <b>pprint.pprint(result)</b>
{'ismaster': True,
 'localTime': datetime.datetime(2018, 6, 13, 21, 55, 2, 272000),
 'logicalSessionTimeoutMinutes': 30,
 'maxBsonObjectSize': 16777216,
 'maxMessageSizeBytes': 48000000,
 'maxWireVersion': 6,
 'maxWriteBatchSize': 100000,
 'minWireVersion': 0,
 'ok': 1.0,
 'readOnly': False}
>>>
</pre>

First we import the PyMongo library *(1)*. Then we create a local `client` object *(2)* that holds the connection 
pool and other status for this server. We generally don’t want more than one `MongoClient` object 
per program as it provides its own connection pool. 

Now we are ready to issue a command to the server. 
In this case its the standard MongoDB server information command which is called rather 
anachronistically `isMaster` *(3)*. This is a hangover from the very early versions of MongoDB. 
It appears in pre 1.0 versions of MongoDB  ()which is over ten years old at this stage). 
The `isMaster` command returns a `dict` which details a bunch of server information. In order to 
format this in a more readable way we import the `pprint` library.

# Conclusion
That’s the end of episode one. We have installed MongoDB, installed the Python client library (aka driver),
started a `mongod` server and established a connection between the client and server.

Next week we will introduce CRUD operations on MongoDB, starting with **Create**.

For direct feedback please pose your questions on [twitter/jdrumgoole](https://twitter.com/jdrumgoole). 
That way everyone can see the answers. 

The best way to try out MongoDB is via [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
 our fully managed Database as a Service available on AWS, Google Cloud Platform (CGP) and Azure. 
 
 
