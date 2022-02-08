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

def update_one(collection:str, query:dict, newValues:dict):
    """
    :param collection:
    :param query: the query that will help us select the needed document
    :param newValues: new values should be in this format: {"$set": { "address": "Canyon 123" } }
    :return: approval that the document was updated
    """
    connection = DB[collection]
    return connection.update_one(query, newValues).modified_count


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
    # print(delete_one('kids', {"name": "amit"}))
    # print(insert_many('kids',[{"_id":12,"first_name":"amit", "last_name":"margalittt","class":"NY morning"},{"_id":122,"first_name":"amit", "last_name":"margalittt", "class":"NY morning"},{"_id":1232, "first_name":"amit", "last_name":"margalittt", "class":"NY morning"}]))
    # print(delete_many('kids',()))
    # print(bool(update_one('kids', {"name":"amit"}, {"$set":{"update":"works"}})))
    # print(insert_one('managers', {'_id': 'AAA', 'password':'AAA', "first_name":"Amit", "last_name": "meow", "class":"NY morning"}))
    # print ('file DB functions is working')
    x = find_one('kids',{"_id":"205634967"})
    _bytes = x["picture1"]
    # f = open("assets/images/image1.png", "wb")
    # f.write(_bytes)
    # f.close()
    # print(update_many('kids', {"name":"amit"},{"$set":{"class":"NY morning"}}))
    # con = DB["managers"].find()
    # print(find_one('kids',{"_id":"205634967"}))
    # for doc in con:
    #     print(doc)
