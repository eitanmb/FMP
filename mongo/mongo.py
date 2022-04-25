from pymongo import *
import json
import os
from modulos.file_basics import *

client = MongoClient()
db = client.dbfmp

def create_collection_from_json( folder, collection ):

    for base, dirs, files in os.walk(folder):

        for file in files:
            print(file)
            f = open(f'{folder}{file}',)

            try:
                doc = json.load(f)
                if len(doc) > 0:
                    print(collection.insert_one(doc))
            except Exception as e:
                print(e)


def encontrar_companias_duplicadas( collection ):
    companias = collection.distinct('longName')

    for compania in companias:
        symbol = collection.find_one({"longName":compania})['symbol']
        print(symbol)
        append_to_file( 'tickersNoDuplciados.csv', f"{symbol}\n" )


#Insertar documentos en la collection profile desde archivos json
create_collection_from_json('json/outlook/', db.outlook)

# encontrar_companias_duplicadas(db.profiles)
