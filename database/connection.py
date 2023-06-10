
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps
from bson.json_util import loads
import json
import datetime
import time
import os
import sys
sys.path.append('./')
from loader import conf
config = conf.config

from tkinter import *
requirement_collections = [
    'account',
    'logs',
    'proxy',
    'tds_account'
]

db = None

def getCol():
    global db
    url = config.get('database', 'mongodb_uri')
    database = config.get('database', 'mongodb_database')
    # get all collections
    client = MongoClient(url)
    if database not in client.list_database_names():
        client[database] # create database
    db = client[database]
    for col in requirement_collections:
        if col not in db.list_collection_names():
            db.create_collection(col)
            db[col].insert_one({'ahex': 'hextool'})
            db[col].delete_one({'ahex': 'hextool'})
            
    return db

def getCountAccountFB ():
    return db['account'].count_documents({})

def insertAccountFB (acc: dict) -> int:
    db['account'].insert_one(acc)
    return getCountAccountFB()


def getAccountFB (uid: str) -> dict:
    return db['account'].find_one({'uid': uid})

def getAllAccountFB () -> list:
    return list(db['account'].find({}))


def updateProfilePath (uid: str, path: str) -> int:
    db['account'].update_one({'uid': uid}, {'$set': {'profile_path': path}})
    return getCountAccountFB()

def updateStatusAccountFB (uid: str, status: str) -> int:
    db['account'].update_one({'uid': uid}, {'$set': {'status': status}})
    return getCountAccountFB()

def updateProxyAccountFB (uid: str, proxy: str) -> int:
    db["account"].update_one({'uid': uid}, {'$set': {'proxy': proxy}})
    return getCountAccountFB()

def updateInfoFacebook (uid: str, info: dict) -> int:
    db['account'].update_one({'uid': uid}, {'$set': {'info': info}})
    return getCountAccountFB()
def getCountAccountFBNoProxy () -> int:
    return db['account'].count_documents({'proxy': None or ''})


def reUpdateAccountFB (uid: str, entrs: list) -> int:

    for entr in entrs:
        name = entr.tag
        if name != '_id':
            value = entr.get()
            type = entr.type
            if type == int:
                value = int(value)
            elif type == float:
                value = float(value)
            elif type == bool:
                value = bool(value)
            elif type == list:
                value = value.split(',')
            elif type == dict:
                value = eval(value)
            elif type == str:
                value = str(value)
            db['account'].update_one({'uid': uid}, {'$set': {name: value}})


def getAccountFBNoProxy() -> list:
    noProxyAccount = []
    allAccount = getAllAccountFB()
    for acc in allAccount:
        if 'proxy' not in acc or acc['proxy'] == None or acc['proxy'] == '':
            noProxyAccount.append(acc)
    return noProxyAccount
    
def getCountAccountFBLive () -> int:
    return db['account'].count_documents({'status': True})
def removeAccountFB (uid: str) -> int:
    db['account'].delete_one({'uid': uid})
    return getCountAccountFB()


def addAccTDS (user, pasw, uid, proxy):
    db['tds_account'].insert_one({'user': user, 'pass': pasw, 'uid': uid, 'proxy': proxy})

def getALLAccTDS ():
    return list(db['tds_account'].find({}))

def getTDSAccount (user):
    # find account by user
    return  db['tds_account'].find_one({'user': user})

def removeTDSAccount (user: str) -> None:
    db["tds_account"].delete_one({'user': user})

def clearAllAccount ():
    db['account'].delete_many({})