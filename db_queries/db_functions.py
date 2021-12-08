import pymongo

# client is the connection
client = pymongo.MongoClient("mongodb+srv://admin:igoramit0987@cluster0.c2drp.mongodb.net/face-recognition-db?retryWrites=true&w=majority")
# db = client.testdb = client.test
# client.list_database_names() show all dbs in our connection
print(client.list_database_names())
#
# # get the DB
# our_db = client['admin']
#
# # to show collections in a database use mydb.list_collection_names()
# print(our_db.list_collection_names())