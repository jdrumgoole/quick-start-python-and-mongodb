Our final part of CRUD is the *D* for *Delete*. The delete
operator in the `PyMongo` driver is implemented in two functions:

* `[delete_one](http://api.mongodb.com/python/current/api/pymongo/collection.html#pymongo.collection.Collection.delete_one)`
* `[delete_many](http://api.mongodb.com/python/current/api/pymongo/collection.html#pymongo.collection.Collection.delete_many)`

like their peers these are collection level operations that work 
with a filter argument to select the documents to be deleted. 
