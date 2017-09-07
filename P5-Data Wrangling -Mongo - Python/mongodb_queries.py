from pymongo import MongoClient
import pprint as pp

## Getting the database ##
def get_db(db_name):
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db

## Query output
def mongo_query(db, query):
    return [doc for doc in db.kolkata.aggregate(query)]

query_01 = [{'$group': {'_id': '$created.user','count': {'$sum': 1}}}, {'$sort': {'count': -1}}, {'$limit': 5}]
query_02 = [{'$group': {'_id': '$created.user','count': {'$sum': 1}}}, {'$group': {'_id': '$count','num_users': {'$sum': 1}}}, {'$sort': {'_id': 1}}, {'$limit': 1}]


if __name__ == '__main__':
	db = get_db('cities')
	print "Top 5 users, according to order of contribution... \n"
	pp.pprint(mongo_query(db, query_01))
	print "\nNumber of users, who contributed least... \n"
	pp.pprint(mongo_query(db, query_02))