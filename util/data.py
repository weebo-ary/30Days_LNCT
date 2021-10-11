import csv
from pymongo import MongoClient
from copy import deepcopy

client = MongoClient('<mongodb connection string>')


def loadNewData():
    db = client.gecr
    studata = db.studata
    studata.drop()

    db = client.gecr
    studata = db.studata
    with open("util/data.csv", newline='') as csvFile:
        reader = csv.DictReader(csvFile)
        dataToInsert = []
        for row in reader:
            dataToInsert.append({
                "email":row["Student Email"],
                "name": row["Student Name"],
                "track1": int(row["# of Skill Badges Completed in Track 1"]),
                "track2": int(row["# of Skill Badges Completed in Track 2"]),
                "totalQuest" : (int(row["# of Skill Badges Completed in Track 1"]) + int(row["# of Skill Badges Completed in Track 2"]))
            })
        resp =deepcopy(dataToInsert)
        studata.insert_many(dataToInsert)
        sortList = sorted(resp, key = lambda i: i['totalQuest'],reverse=True)
        studata.insert_one({"dataName":"sortedData","data":sortList})
        print(resp)
    return resp


def getAllData():
    db = client.gecr
    studata = db.studata
    leadboard =  studata.find_one({ "dataName": "sortedData" })
    leadboard.pop("_id")
    return leadboard

def findData(email):
    db = client.gecr
    studata = db.studata
    stuemail =  studata.find_one({ "email": email })
    if(not stuemail):
        return None
    stuemail.pop("_id")
    return stuemail


