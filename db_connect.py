import os
import configparser
from pymongo import MongoClient

config = configparser.ConfigParser(interpolation=None)
config.read("credentials.ini")
environment = os.getenv("APP_ENV","dev")

username = config[environment]["username"]
password = config[environment]["password"]
endpoint = config[environment]["endpoint"]
database_name = config[environment]["database"]

uri = "mongodb://" + username + ":" + password + "@" + endpoint + "/" + database_name + "?authSource=admin"

client = MongoClient(uri, serverSelectionTimeoutMS=5000)
database = client.get_database(database_name)

database.command("ping")
print("connected to MongoDB:", database.name)
print("server:", client.adress)

result = list(database.environment_info.aggregate([{"$limit": 1}]))

if result:
    print("Environment:", result[0]["name"])
else:
    print("Environment: Data not found")

client.close()

