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
    """

    :param collection: a collection we want to insert to
    :param values: values to be inserted
    :return: return approval that the document inserted.
    """
    connection = DB[collection]
    return connection.insert_one(values).inserted_id


def insert_many(collection:str, list_of_dicts:list):
    """
    :param collection:
    :param list_of_dicts: should be a list containing dictionaries.
    should look like this: [{},{},{}] -> the dictionaries should not be empty.
    :return: approval that the documents inserted.
    """
    connection = DB[collection]
    return connection.insert_many(list_of_dicts).inserted_ids


def delete_one(collection: str, query: dict):
    """

    :param collection:
    :param query:
    :return: approval that the document was deleted
    """
    connection = DB[collection]
    return connection.delete_one(query).deleted_count


def delete_many(collection: str, query: dict =None):
    """

    :param collection:
    :param query:
    :return: approval that the documents deleted.
    """
    connection = DB[collection]
    if query:
        return connection.delete_many(query).deleted_count
    # for developing using
    return connection.delete_many({}).deleted_count


def update_one(collection:str, query: dict, newValues: dict):
    """
    :param collection:
    :param query: the query that will help us select the needed document
    :param newValues: updated values
    :return: approval that the document was updated
    """
    connection = DB[collection]
    valid_new_values = {"$set": newValues}

    return connection.update_one(query, valid_new_values).modified_count


def update_one_and_return(collection: str, query: dict, newValues: dict):
    # this function is same as update_one.
    # the only differ is that the function returns the updated document.
    connection = DB[collection]
    return connection.find_one_and_update(query, newValues)


def update_many(collection:str, query: dict, newValues: dict):
    connection = DB[collection]
    return connection.update_many(query, newValues).modified_count


def find_one(collection: str, query: dict = {}):
    """
    :param collection:  the collection we want to find form
    :param query: if we don't want any query, the default value is none.
    :return: one document that follows the given query if given.
    """

    connection = DB[collection]
    # print(connection.find_one(query)['_id'])
    return connection.find_one(query)


def find_all(collection: str, query: dict = {}):
    """

    :param collection:  the collection we want to find form
    :param query: if we don't want any query, the default value is none.
    :return: iterable object containing all matching documents.
    """
    connection = DB[collection]
    return connection.find(query)


if __name__ == '__main__':
    delete_many('kids', {"class": "NY morning"})
    # con = DB["managers"].find()
    # print(find_one('kids',{"_id":"205634967"}))
    # for doc in con:
    #     print(doc)
