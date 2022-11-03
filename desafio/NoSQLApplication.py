import datetime
import pprint

import pymongo as pyM

client = pyM.MongoClient("mongodb+srv://pymongo:mofio200@cluster0.s2cgewe.mongodb.net/?retryWrites=true&w=majority")

db = client.text
collection = db.text_collection
print(db.text_collection)

new_posts = [{
            "author": "Virna",
            "address": "rua alguma coisa",
            "cpf": "12546525478",
            "conta": 12546,
            "agencia": 52285,
            "type": "CC",
            "saldo": 0,
            "date": datetime.datetime(2009, 11, 10, 10, 45)
}]

posts = db.posts
result = posts.insert_many(new_posts)

print("\n Documentos na coleção post")
for post in posts.find():
    pprint.pprint(post)

print(posts.count_documents({}))
print(posts.count_documents({"author": "Virna"}))
