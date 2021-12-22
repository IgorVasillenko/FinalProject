import pymongo
'''
In this file, we will have all our necessary atomic DB functions:
inert, find , update and delete.
our global variables are:
 1. client -> our connection to mongoDB
 2. DB -> our connection to face-recognition-db DB
'''
# client is the connection
client = pymongo.MongoClient(
    "mongodb+srv://admin:igoramit0987@cluster0.c2drp.mongodb.net/face-recognition-db?retryWrites=true&w=majority")

DB = client['face-recognition-db']


def insert_one(collection:str, values:dict):
    connection = DB[collection]
    insert = connection.insert_one(values)


def insert_many(collection:str, list_of_dicts:list):
    """
    :param collection:
    :param list_of_dicts: should be a list containing dictonaries.
    should look like this: [{},{},{}] -> the dictonaries should not be empty.
    :return:
    """
    connection = DB[collection]
    insert_many = connection.insert_many(list_of_dicts)
    print(insert_many)


def delete_one(collection:str, query:dict):
    connection = DB[collection]
    connection.delete_one(query)


def delete_many(collection:str, query:dict):
    connection = DB[collection]
    connection.delete_many(query)


def update_one(collection:str, query:dict, newValues:dict):
    """
    :param collection:
    :param query:
    :param newValues: new values should be in this format: {"$set": { "address": "Canyon 123" } }
    :return:
    """
    connection = DB[collection]
    return connection.update_one(query, newValues)


def update_one_and_return(collection:str, query:dict, newValues:dict):
    # this function is same as updade_one.
    # the only differ is that the function returns the updated document.
    connection = DB[collection]
    return connection.find_one_and_update(query, newValues)


def update_many(collection:str, query:dict, newValues:dict):
    connection = DB[collection]
    connection.update_many(query, newValues)


def find_one(collection:str, query:dict=None):
    """
    :param collection:  the collection we want to find form
    :param query: if we don't want any query, the default value is none.
    :return: one document that follows the given query if given.
    """

    connection = DB[collection]
    return connection.find_one(query)


if __name__ == '__main__':
    # delete_one('kids', {"name": "amit"})
    # insert_many('kids',[{"name":"amit", "age":"20"},{"name":"amit", "age":"20"},{"name":"amit", "age":"20"}])
    # delete_many('kids',{"name":"amit", "age":"20"})
    # print(update_one('kids', {"name":"amit"}, {"$set":{"update":"works"}}))
    # insert_one('managers', {'username': 'AAA', 'password':'AAA'})
    print ('file DB functions is working')