import argparse
from bson.objectid import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri="mongodb+srv://useralina:12345@project1.wut54bm.mongodb.net/?appName=project1"
client=MongoClient(uri, server_api=ServerApi("1"))
db=client.alina

parser=argparse.ArgumentParser(description="Server Cats")
parser.add_argument("--action", help="read_all, read_name, update_age, update_features, " \
"delete_cat, delete")
parser.add_argument("--id")
parser.add_argument("--name")
parser.add_argument("--age")
parser.add_argument("--features", nargs="+")

arg=vars(parser.parse_args())

action=arg.get('action')
id=arg.get('id')
name=arg.get('name')
age=arg.get('age')
features=arg.get('features')


def find():
    return db.cats.find()

def find_by_name(name):
    return db.cats.find({"name":name})


def update_age(pk,age):
    r=db.cats.update_one({"_id":ObjectId(pk)},{
        "$set":{
         'age':age   
        }
    })
    return r

def update_features(name, features):
    r = db.cats.update_one(
        {"name": name},
        {"$addToSet": {"features": {"$each": features}}}
    )
    return r


def update_features(name,features):
    r=db.cats.update_one({"name":name},{
        "$addToSet":{
         'features':features   
        }
    })
    return r

def delete_by_name(name):
    return db.cats.delete_one({"name":name})


def delete_all():
    return db.cats.delete_many({})

def main():
    pk=id
    match action:
        case 'read_all':
            r=find()
            print([e for e in r])
        case 'read_name':
            r=find_by_name(name)
            print([e for e in r])
        case 'update_age':
            r=update_age(pk,age)
            print(r)
        case 'update_features':
            r=update_features(name,features)
            print(r)
        case 'delete_cat':
            r=delete_by_name(name)
            print(r)
        case 'delete':
            r=delete_all()
            print(r)
        case _:
            print('Oops! Invalid command. Try again!')
if __name__=='__main__':
    main()