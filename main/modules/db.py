import asyncio
import pymongo
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from config import MONGO_DB_URI
print("[INFO]: STARTING MONGO DB CLIENT")
mongo_client = MongoClient(MONGO_DB_URI)
db = mongo_client.autoanime480p
dbx = mongo_client["anidl"]
filesdb = dbx["files"]
dbz = mongo_client["progress"]
animedb = db.animes
uploadsdb = db.uploads
user_data = db['users']
progressdb=dbz["info"]
async def present_user(user_id : int):
    found = user_data.find_one({'_id': user_id})
    return bool(found)

async def add_user(user_id: int):
    user_data.insert_one({'_id': user_id})
    return

async def get_animesdb(): 
    anime_list = []
    async for name in animedb.find():
        anime_list.append(name)
    return anime_list

async def save_animedb(name,data): 
    data = await animedb.insert_one({"name": name, "data": data})
    return
  
async def del_anime(name): 
    try:
        animesdb = db.animes
        result = await animesdb.delete_one({"name": name})
        if result.deleted_count > 0:
            print(f"Successfully deleted anime: {name}")
        else:
            print(f"No anime found with the name: {name}")
    except pymongo.errors.PyMongoError as e:
        print(f"Error deleting anime: {e}")

async def get_uploads(): 
    anime_list = []
    async for name in uploadsdb.find():
        anime_list.append(name)
    return anime_list

async def save_uploads(name):
    uploadb = db.uploads
    print("save_uploads: ", name)
    data = await uploadb.insert_one({"name": name})
    return

def is_fid_in_db(fid):
    data = filesdb.find_one({"fid": fid})
    if data:
        return data
    else:
        return None

def save_postid(name, postid):
    animexdb = db.animes
    animexdb.update_one(
        {
            "name": name
        },
        {"$set": {"data.postid": postid}},
        upsert=True,
    )
    return
def save_480p(name):
    animexdb = db.animes
    animexdb.update_one(
        {
            "name": name
        },
        {"$set": {"data.uploaded": '480p'}},
        upsert=True,
    )
    return

def pending_720p(name):
    animexdb = db.animes
    animexdb.update_one(
        {
            "name": name
        },
        {"$set": {"data.pending": '720p + 1080p'}},
        upsert=True,
    )
    return

def pending_1080p(name):
    animexdb = db.animes
    animexdb.update_one(
        {
            "name": name
        },
        {"$set": {"data.pending": '1080p'}},
        upsert=True,
    )
    return

def no_pending(name):
    animexdb = db.animes
    animexdb.update_one(
        {
            "name": name
        },
        {"$set": {"data.pending": '0'}},
        upsert=True,
    )
    return
def save_720p(name):
    animexdb = db.animes
    animexdb.update_one(
        {
            "name": name
        },
        {"$set": {"data.uploaded": '480p + 720p'}},
        upsert=True,
    )
    return
def save_1080p(name):
    animexdb = db.animes
    animexdb.update_one(
        {
            "name": name
        },
        {"$set": {"data.save_1080p": '480p + 720p + 1080p'}},
        upsert=True,
    )
    return

def save_file_in_db(filed, hash, subtitle, img, audio_info, tit, alink, size, upid=None):
    filesdb.update_one(
        {
            "hash": hash,
            "fid": str(upid),
        },
        {"$set": {"filename": filed, "filenamex": filed, "code": hash, "msg_id": upid, "subtitle": subtitle, "audio": audio_info, "etitle": tit, "size": size}},
        upsert=True,
    )
    return
    
def is_tit_in_db(bit):
    uploadeb = db.uploads
    data = uploadeb.find_one({"name": bit})
    if data:
        return True
    else:
        return False

async def get_postid(name):
    andb = db['animes']
    result = await andb.find_one({ "name": name }, {"data.postid": 1 })
    if result:
        xy = result["data"]["postid"]
        return xy
    else:
        return None

async def get_link480p(filename):    
    andb = db['animes']
    result = await andb.find_one({ "name": filename }, {"data.slink480p": 1 })
    if result:
        xo = result["data"]["slink480p"]
        return xo
    else:
        return None
        
async def get_link720p(filename):    
    andb = db['animes']
    result = await andb.find_one({ "name": filename }, {"data.slink720p": 1 })
    if result:
        yo = result["data"]["slink720p"]
        return yo
    else:
        return None

async def get_size480p(filename):    
    andb = db['animes']
    result = await andb.find_one({ "name": filename }, {"data.size480p": 1 })
    if result:
        xo = result["data"]["size480p"]
        return xo
    else:
        return None

async def get_size720p(filename):    
    andb = db['animes']
    result = await andb.find_one({ "name": filename }, {"data.size720p": 1 })
    if result:
        xo = result["data"]["size720p"]
        return xo
    else:
        return None
        
def save_link480p(name, link):
    animexdb = db['animes']
    animexdb.update_one(
        {
            "name": name
        },
        {"$set": {"data.slink480p": link}},
        upsert=True,
    )
    return

    
def save_link720p(name, link):
    animexdb = db['animes']
    animexdb.update_one(
        {
            "name": name
        },
        {"$set": {"data.slink720p": link}},
        upsert=True,
    )
    return

def save_link1080p(name, link):
    animexdb = db.animes
    animexdb.update_one(
        {
            "name": name
        },
        {"$set": {"data.slink1080p": link}},
        upsert=True,
    )
    return

def save_size480p(title, size480p):
    animexdb = db['animes']
    animexdb.update_one(
        {
            "name": title
        },
        {"$set": {"data.size480p": size480p}},
        upsert=True,
    )
    return

def save_size720p(title, size480p):
    animexdb = db['animes']
    animexdb.update_one(
        {
            "name": title
        },
        {"$set": {"data.size720p": size480p}},
        upsert=True,
    )
    return

def save_size1080p(title, size1080p):
    animexdb = db['animes']
    animexdb.update_one(
        {
            "name": title
        },
        {"$set": {"data.size1080p": size1080p}},
        upsert=True,
    )
    return

def save_progress(title,status,engine,percent, speed, ETA,res):
    progressdb.update_one(
        {
            "name": title,
        },
        {"$set": {"status": f"{status} ⚡", "Engine": engine, "Precentage": f"{percent}%", "speed": speed, "ETA": ETA, "res": res}},
        upsert=True,
    )
    return

async def del_progress(title):
    try:
        result = await progressdb.delete_one({"name": title})
        if result.deleted_count > 0:
            print(f"Successfully deleted progress: {title}")
        else:
            print(f"No anime found with the progress: {title}")
    except pymongo.errors.PyMongoError as e:
        print(f"Error deleting progress: {e}")
    return
