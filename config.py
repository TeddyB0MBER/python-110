import pymongo
import certifi

con_str = "mongodb+srv://J0J0MA:Uncharted3@cluster0.ojnzevz.mongodb.net/?retryWrites=true&w=majority"
# the area where <password> is, you will replace with simple password
client = pymongo.MongoClient(con_str, tlsCAFile=certifi.where())

db = client.get_database("OrganikaCh32")  # Database name

me = {
    "first": "Tuong",
    "last": "Do",
    "age": 26,
    "hobbies": [],
    "address": {
        " street": 123,
        "area": "City heights",
        "city": "San Diego",
        "state": "CA"
    }
}
