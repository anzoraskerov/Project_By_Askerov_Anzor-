from pymongo import MongoClient

client = MongoClient("mongodb://mongodb-container:27017")

db = client.orders_db
products_collection = db.get_collection("products")
busket_collection = db.get_collection("busket")