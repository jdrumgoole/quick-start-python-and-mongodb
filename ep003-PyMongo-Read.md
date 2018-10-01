# PyMongo Monday - Episode 3 - Read

Previously we covered:
 * Episode 1 : [Setting Up Your MongoDB Environment](https://github.com/jdrumgoole/PyMongo-Monday/blob/master/ep001-SettingUpYourPyMongoEnvironment.md)
 * Episode 2 : [CRUD - Create](https://github.com/jdrumgoole/PyMongo-Monday/blob/master/ep002-PyMongo-Create.md)
 
In this episode (episode 3) we are are going to cover
the Read part of CRUD. MongoDB provides a query interface
through the [find](http://api.mongodb.com/python/current/api/pymongo/collection.html#pymongo.collection.Collection.find) 
function.

We are going to demonstrate `Read` by doing find queries on a collection
hosted in [MongoDB Atlas](https://www.mongodb.com/cloud/atlas). The MongoDB 
connection string is:

`mongodb+srv://demo:demo@demodata-rgl39.mongodb.net/test?retryWrites=true`

This is a cluster running a database called *demo* with a single collection 
called *zipcodes*. Every ZIP code in the US is in this database.

To connect to this cluster we are going to use the Python shell.

```python
$ cd ep003
$ pipenv shell
Launching subshell in virtual environment…
JD10Gen:ep003 jdrumgoole$  . /Users/jdrumgoole/.local/share/virtualenvs/ep003-blzuFbED/bin/activate
(ep003-blzuFbED) JD10Gen:ep003 jdrumgoole$ python
Python 3.6.5 (v3.6.5:f59c0932b4, Mar 28 2018, 03:03:55)
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>>
>>> from pymongo import MongoClient
>>> client = MongoClient(host="mongodb+srv://demo:demo@demodata-rgl39.mongodb.net/test?retryWrites=true")
>>> db = client["demo"]
>>> zipcodes=db["zipcodes"]
>>> zipcodes.find_one()
{'_id': '01069', 'city': 'PALMER', 'loc': [-72.328785, 42.176233], 'pop': 9778, 'state': 'MA'}
>>>
```

The `find_one` query will get the first record in the collection. You can see 
the structure of the fields in the returned document. The `_id` is the zipcode. 
The `city` is the city name. The `loc` is the GPS coordindates of each zipcode. T
he `pop` is the population size and the `state` is the two letter state code. 
We are connecting with the default user `demo` with the password `demo`. This
user only has read-only access to this database and collection.

So what if we want to select all the ZIP codes for a particular city?

Querying in MongoDB consists of constructing a partial
JSON document that matches the fields you want to select on. So to get
all the zipcodes in the city of PALMER we use the following query

```Python
>>> zipcodes.find({'city': 'PALMER'})
<pymongo.cursor.Cursor object at 0x104c155c0>
>>>
```

Note we are using `find()` rather than `find_one()` as we want to return
all the matching documents. In this case `find()` will return a 
[cursor](http://api.mongodb.com/python/current/api/pymongo/cursor.html). 

To print the cursor contents just keep calling `.next()` on the cursor 
as follows:

```python
>>> cursor=zipcodes.find({'city': 'PALMER'})
>>> cursor.next()
{'_id': '01069', 'city': 'PALMER', 'loc': [-72.328785, 42.176233], 'pop': 9778, 'state': 'MA'}
>>> cursor.next()
{'_id': '37365', 'city': 'PALMER', 'loc': [-85.564272, 35.374062], 'pop': 1685, 'state': 'TN'}
>>> cursor.next()
{'_id': '50571', 'city': 'PALMER', 'loc': [-94.543155, 42.641871], 'pop': 1119, 'state': 'IA'}
>>> cursor.next()
{'_id': '66962', 'city': 'PALMER', 'loc': [-97.112214, 39.619165], 'pop': 276, 'state': 'KS'}
>>> cursor.next()
{'_id': '68864', 'city': 'PALMER', 'loc': [-98.241146, 41.178757], 'pop': 1142, 'state': 'NE'}
>>> cursor.next()
{'_id': '75152', 'city': 'PALMER', 'loc': [-96.679429, 32.438714], 'pop': 2605, 'state': 'TX'}
>>> cursor.next()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/jdrumgoole/.local/share/virtualenvs/ep003-blzuFbED/lib/python3.6/site-packages/pymongo/cursor.py", line 1197, in next
    raise StopIteration
StopIteration
```

As you can see cursors follow the Python [iterator protocol](https://wiki.python.org/moin/Iterator) 
and will raise a `StopIteration` exception when the cursor is exhausted. 

However, calling `.next()` continously is a bit of a drag. Instead you can 
import the [`pymongo_shell`](https://github.com/jdrumgoole/PyMongo-Monday/blob/master/ep003/pymongo_shell.py) 
package and call the `print_cursor()` function. It will print out twenty 
records at a time.

```python
>>> from pymongo_shell import print_cursor
>>> print_cursor(zipcodes.find({'city': 'PALMER'}))
{'_id': '01069', 'city': 'PALMER', 'loc': [-72.328785, 42.176233], 'pop': 9778, 'state': 'MA'}
{'_id': '37365', 'city': 'PALMER', 'loc': [-85.564272, 35.374062], 'pop': 1685, 'state': 'TN'}
{'_id': '50571', 'city': 'PALMER', 'loc': [-94.543155, 42.641871], 'pop': 1119, 'state': 'IA'}
{'_id': '66962', 'city': 'PALMER', 'loc': [-97.112214, 39.619165], 'pop': 276, 'state': 'KS'}
{'_id': '68864', 'city': 'PALMER', 'loc': [-98.241146, 41.178757], 'pop': 1142, 'state': 'NE'}
{'_id': '75152', 'city': 'PALMER', 'loc': [-96.679429, 32.438714], 'pop': 2605, 'state': 'TX'}
>>>
```
If we don't need all the fields in the doc we can use 
[projection](https://docs.mongodb.com/v3.2/tutorial/project-fields-from-query-results/) 
to remove some fields. This is a second doc argument to the `find()` function. 
This doc can specify the fields to return explicitly.

```python
>>> print_cursor(zipcodes.find({'city': 'PALMER'}, {'city':1,'pop':1}))
{'_id': '01069', 'city': 'PALMER', 'pop': 9778}
{'_id': '37365', 'city': 'PALMER', 'pop': 1685}
{'_id': '50571', 'city': 'PALMER', 'pop': 1119}
{'_id': '66962', 'city': 'PALMER', 'pop': 276}
{'_id': '68864', 'city': 'PALMER', 'pop': 1142}
{'_id': '75152', 'city': 'PALMER', 'pop': 2605}
```

To include multiple fields in a query just add them to query doc. Each field is
treated as a boolean `and` to select the documents that will be returned. 


```python
>>> print_cursor(zipcodes.find({'city': 'PALMER', 'state': 'MA'}, {'city':1,'pop':1}))
{'_id': '01069', 'city': 'PALMER', 'pop': 9778}
>>>
```

To pick documents with one field `or` the other we can use the `$or` operator.

```python
>>> print_cursor(zipcodes.find({ '$or' : [ {'city': 'PALMER' }, {'state': 'MA'}]}))
{'_id': '01069', 'city': 'PALMER', 'loc': [-72.328785, 42.176233], 'pop': 9778, 'state': 'MA'}
{'_id': '01002', 'city': 'CUSHMAN', 'loc': [-72.51565, 42.377017], 'pop': 36963, 'state': 'MA'}
{'_id': '01012', 'city': 'CHESTERFIELD', 'loc': [-72.833309, 42.38167], 'pop': 177, 'state': 'MA'}
{'_id': '01073', 'city': 'SOUTHAMPTON', 'loc': [-72.719381, 42.224697], 'pop': 4478, 'state': 'MA'}
{'_id': '01096', 'city': 'WILLIAMSBURG', 'loc': [-72.777989, 42.408522], 'pop': 2295, 'state': 'MA'}
{'_id': '01262', 'city': 'STOCKBRIDGE', 'loc': [-73.322263, 42.30104], 'pop': 2200, 'state': 'MA'}
{'_id': '01240', 'city': 'LENOX', 'loc': [-73.271322, 42.364241], 'pop': 5001, 'state': 'MA'}
{'_id': '01370', 'city': 'SHELBURNE FALLS', 'loc': [-72.739059, 42.602203], 'pop': 4525, 'state': 'MA'}
{'_id': '01340', 'city': 'COLRAIN', 'loc': [-72.726508, 42.67905], 'pop': 2050, 'state': 'MA'}
{'_id': '01462', 'city': 'LUNENBURG', 'loc': [-71.726642, 42.58843], 'pop': 9117, 'state': 'MA'}
{'_id': '01473', 'city': 'WESTMINSTER', 'loc': [-71.909599, 42.548319], 'pop': 6191, 'state': 'MA'}
{'_id': '01510', 'city': 'CLINTON', 'loc': [-71.682847, 42.418147], 'pop': 13269, 'state': 'MA'}
{'_id': '01569', 'city': 'UXBRIDGE', 'loc': [-71.632869, 42.074426], 'pop': 10364, 'state': 'MA'}
{'_id': '01775', 'city': 'STOW', 'loc': [-71.515019, 42.430785], 'pop': 5328, 'state': 'MA'}
{'_id': '01835', 'city': 'BRADFORD', 'loc': [-71.08549, 42.758597], 'pop': 12078, 'state': 'MA'}
{'_id': '01845', 'city': 'NORTH ANDOVER', 'loc': [-71.109004, 42.682583], 'pop': 22792, 'state': 'MA'}
{'_id': '01851', 'city': 'LOWELL', 'loc': [-71.332882, 42.631548], 'pop': 28154, 'state': 'MA'}
{'_id': '01867', 'city': 'READING', 'loc': [-71.109021, 42.527986], 'pop': 22539, 'state': 'MA'}
{'_id': '01906', 'city': 'SAUGUS', 'loc': [-71.011093, 42.463344], 'pop': 25487, 'state': 'MA'}
{'_id': '01929', 'city': 'ESSEX', 'loc': [-70.782794, 42.628629], 'pop': 3260, 'state': 'MA'}
Hit Return to continue
```
We can do range selections by using the [`$lt`](https://docs.mongodb.com/manual/reference/operator/query/lt/#op._S_lt)
and [`$gt`](https://docs.mongodb.com/manual/reference/operator/query/gt/)
operators.

```python
>>> print_cursor(zipcodes.find({'pop' : { '$lt':8, '$gt':5}}))
{'_id': '05901', 'city': 'AVERILL', 'loc': [-71.700268, 44.992304], 'pop': 7, 'state': 'VT'}
{'_id': '12874', 'city': 'SILVER BAY', 'loc': [-73.507062, 43.697804], 'pop': 7, 'state': 'NY'}
{'_id': '32830', 'city': 'LAKE BUENA VISTA', 'loc': [-81.519034, 28.369378], 'pop': 6, 'state': 'FL'}
{'_id': '59058', 'city': 'MOSBY', 'loc': [-107.789149, 46.900453], 'pop': 7, 'state': 'MT'}
{'_id': '59242', 'city': 'HOMESTEAD', 'loc': [-104.591805, 48.429616], 'pop': 7, 'state': 'MT'}
{'_id': '71630', 'city': 'ARKANSAS CITY', 'loc': [-91.232529, 33.614328], 'pop': 7, 'state': 'AR'}
{'_id': '82224', 'city': 'LOST SPRINGS', 'loc': [-104.920901, 42.729835], 'pop': 6, 'state': 'WY'}
{'_id': '88412', 'city': 'BUEYEROS', 'loc': [-103.666894, 36.013541], 'pop': 7, 'state': 'NM'}
{'_id': '95552', 'city': 'MAD RIVER', 'loc': [-123.413994, 40.352352], 'pop': 6, 'state': 'CA'}
{'_id': '99653', 'city': 'PORT ALSWORTH', 'loc': [-154.433803, 60.636416], 'pop': 7, 'state': 'AK'}
>>>
```

Again sets of `$lt` and `$gt` are combined as a boolean `and`. if you
need different logic you can use the [boolean operators](https://docs.mongodb.com/manual/reference/operator/query-logical/).

# Conclusion

Today we have seen how to query documents using a query template, how to reduce
the output using projections and how to create more complex queries using 
boolean and `$lt` and `$gt` operators.

Next time we will talk about the Update portion of CRUD.

MongoDB has a very rich and full featured query language including support 
for querying using full-text, geo-spatial coordinates and nested queries. 
Give the query language a spin with the Python shell using the tools we 
outlined above. The complete zip codes data set is publicly available for read 
queries at the MongoDB URI:

**mongodb+srv://demo:demo@demodata-rgl39.mongodb.net/test?retryWrites=true"**

Try [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) via the free-tier 
today. A free MongoDB cluster for your own personal use forever!
 

