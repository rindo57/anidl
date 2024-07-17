
import asyncio
import time
import aiohttp
import requests
import aiofiles
import sys
from main.modules.compressor import compress_video, compress_video720p, compress_video1080p
from pymediainfo import MediaInfo
from main.modules.utils import episode_linker, get_duration, get_epnum, status_text, get_filesize, b64_to_str, str_to_b64, send_media_and_reply, get_durationx

from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from main.modules.uploader import upload_video, upload_video720p, upload_video1080p
from main.modules.thumbnail import generate_thumbnail

import os

from main.modules.db import del_anime, save_uploads, is_fid_in_db, is_tit_in_db, save_480p, save_720p, save_1080p

from main.modules.downloader import downloader

from main.modules.anilist import get_anilist_data, get_anime_img, get_anime_name

from config import INDEX_USERNAME, UPLOADS_USERNAME, UPLOADS_ID, INDEX_ID, PROGRESS_ID, LINK_ID

from main import app, queue, status

from pyrogram.errors import FloodWait

from pyrogram import filters, enums

from main.inline import button1

status: Message

async def tg_handler():

    while True:

        try:
            if len(queue) != 0:

                i = queue[0]  

                i = queue.pop(0)
                
                id, name, video = await start_uploading(i)
                print("Title: ", i["title"])
                await del_anime(i["title"])
                await save_uploads(i["title"])
                await asyncio.sleep(30)


            else:                

                if "Idle..." in status.text:

                    try:

                        await status.edit(await status_text("Idle..."))

                    except:

                        pass

                await asyncio.sleep(30)

                

        except FloodWait as e:

            flood_time = int(e.x) + 5

            try:

                await status.edit(await status_text(f"Floodwait... Sleeping For {flood_time} Seconds"),reply_markup=button1)

            except:

                pass

            await asyncio.sleep(flood_time)

        except:

            pass

def replace_text_with_mapping(subtitle, mapping):
    for original_text, replacement_text in mapping.items():
        subtitle = subtitle.replace(original_text, replacement_text)
    return subtitle


mapping = {
    "us": "ENG",
    "br": "POR-BR",
    "mx": "SPA-LA",
    "es": "SPA",
    "sa": "ARA",
    "fr": "FRE",
    "de": "GER",
    "it": "ITA",
    "ru": "RUS",
    "ja": "JPN",
    "pt": "POR",
    "pl": "POL",
    "nl": "DUT",
    "nb": "NOB",
    "fi": "FIN",
    "tr": "TUR",
    "sv": "SWE",
    "el": "GRE",
    "he": "HEB",
    "ro": "RUM",
    "id": "IND",
    "th": "THA",
    "ko": "KOR",
    "da": "DAN",
    "zh": "CHI",
    "bg": "BUL",
    "vn": "VIE",
    "hi": "HIN",
    "te": "TEL",
    "uk": "UKR",
    "hu": "HUN",
    "cs": "CES",
    "hr": "HRV",
    "my": "MAY",
    "sk": "SLK",
    "fil": "FIL",
    "cn": "CHI",
    "jp": "JAP",
    "no": "NOB",
    "se": "SWE",
    "gr": "GRE",
    "kr": "KOR",
    "dk": "DAN",
    "cz": "CES"
}

def get_audio_language(video_path):
    try:
        media_info = MediaInfo.parse(video_path)
        for track in media_info.tracks:
            if track.track_type == 'Audio':
                language = track.language
                language = language.replace("ja", "JP")
                return language
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
        

async def start_uploading(data):

    try:
        if data["480p"]=='0':
            title = data["title"]
            dbtit = data["title"]
            link = data["link"]
            size = data["size"]
            size = size.replace("GB", " GiB")
            nyaasize = size
            subtitl = data["subtitle"]
            subtitle = replace_text_with_mapping(subtitl, mapping)
            name, ext = title.split(".")

            name += f" [AniDL]." + ext

            KAYO_ID =  -1001895203720
            uj_id = 1159872623
            DATABASE_ID = -1001895203720
            bin_id = -1002062055380
            name = name.replace(f" [AniDL].","").replace(ext,"").strip()
            zumba = title.replace("S2", "Season 2")
            id, img, tit = await get_anime_img(get_anime_name(zumba))
            msg = await app.send_photo(bin_id,photo=img,caption=title)

            print("Downloading --> ",name)
            img, alink = await get_anilist_data(zumba)
            await asyncio.sleep(5)
            await status.edit(await status_text(f"Downloading {name}"),reply_markup=button1)
            file = await downloader(msg,link,size,title)

            await msg.edit(f"Download Complete : {name}")
            print("Encoding --> ",name)

            duration = get_duration(file)
            durationx = get_durationx(file)
            #filed = os.path.basename(file)
            filed = title
            
            #filed = filed.replace("[1080p][Multiple Subtitle]", "[1080p Web-DL]")
            filed = filed.replace("[1080p]", "[1080p Web-DL]")
            filed = filed.replace("2nd Season", "S2")
            filed = filed.replace("Season 2", "S2")
            filed = filed.replace("Season 3", "S3")
            filed = filed.replace("Season 4", "S4")
            filed = filed.replace("3rd Season", "S3")
            filed = filed.replace("4th Season", "S4")
            filed = filed.replace("5th Season", "S5")
            filed = filed.replace("6th Season", "S6")
            filed = filed.replace("7th Season", "S7")
            
            fpath = "downloads/" + filed
            
            
            subtitle = subtitle.replace("][", ", ")
            subtitle = subtitle.replace("[", "")
            subtitle = subtitle.replace("]", "")     
            print(subtitle)
            os.rename(file,"video.mkv")
            titlx = filed.replace('[Erai-raws]', '[Web][480p x265 10Bit][Opus][Erai-raws]')
            titlx = titlx.replace('[SubsPlease]', '[Web][480p x265 10Bit][Opus][SubsPlease]')
            titm = f"**[AniDL] {titlx}**"
            tito = f"[AniDL] {titlx}"
            
            main = await app.send_photo(KAYO_ID,photo=img, caption=titm)
            video_path="video.mkv"
        
            audio_language = get_audio_language(video_path)
            if audio_language:
                print("Audio Track Language:", audio_language)
            else:
                print("Failed to get audio language.")
            compressed = await compress_video(duration,main,tito)
    

            if compressed == "None" or compressed == None:

                print("Encoding Failed Uploading The Original File")

                os.rename("video.mkv",fpath)

            else:

                os.rename("out.mkv",fpath)
  
            print("Uploading --> ",name)
            video = await upload_video(msg,title,tito,img,fpath,id,tit,name,size,main,subtitle,nyaasize,audio_language, alink)
            print("480title: ", data["title"])
            save_480p(data["title"])
   
            print(data["title"])
            titlev2 = data["title"]
            id, img, tit = await get_anime_img(get_anime_name(titlev2))
            msg2 = await app.send_photo(bin_id,photo=img,caption=titlev2)
            titlev2 = titlev2.replace("[1080p]", "[1080p Web-DL]")
            titlev2 = titlev2.replace("2nd Season", "S2")
            titlev2 = titlev2.replace("Season 2", "S2")
            titlev2 = titlev2.replace("Season 3", "S3")
            titlev2 = titlev2.replace("Season 4", "S4")
            titlev2 = titlev2.replace("3rd Season", "S3")
            titlev2 = titlev2.replace("4th Season", "S4")
            titlev2 = titlev2.replace("5th Season", "S5")
            titlev2 = titlev2.replace("6th Season", "S6")
            titlev2 = titlev2.replace("7th Season", "S7")
            
            titlx2 = titlev2.replace('[Erai-raws]', '[Web][720p x265 10Bit][Opus][Erai-raws]')
            titlx2 = titlx2.replace('[SubsPlease]', '[Web][720p x265 10Bit][Opus][SubsPlease]')
            titm2 = f"**[AniDL] {titlx2}**"
            tito2 = f"[AniDL] {titlx2}"
            main2 = await app.send_photo(KAYO_ID,photo=img, caption=titm2)
            compressed2 = await compress_video720p(duration,main2,tito2)
    

            if compressed2 == "None" or compressed2 == None:

                print("Encoding Failed Uploading The Original File")

                os.rename("video.mkv",fpath)

            else:

                os.rename("out.mkv",fpath)
  
            print("Uploading --> ",name)
            video = await upload_video720p(msg2,title,tito2,img,fpath,id,tit,name,size,main2,subtitle,nyaasize,audio_language, alink)
            save_720p(data["title"])
            await asyncio.sleep(5)
# 1080p 

            msg3 = await app.send_photo(bin_id,photo=img,caption=title)
            
            titlx3 = titlev2.replace('[Erai-raws]', '[Web][1080p x265 10Bit][AAC][Erai-raws]')
            titlx3 = titlx3.replace('[SubsPlease]', '[Web][1080p x265 10Bit][AAC][SubsPlease]')
            titm3 = f"**[AniDL] {titlx3}**"
            tito3 = f"[AniDL] {titlx3}"
            main3 = await app.send_photo(KAYO_ID,photo=img, caption=titm3)
            
            compressed3 = await compress_video1080p(duration,main3,tito3)
    

            if compressed3 == "None" or compressed3 == None:

                print("Encoding Failed Uploading The Original File")

                os.rename("video.mkv",fpath)

            else:

                os.rename("out.mkv",fpath)
  
            print("Uploading --> ",name)
            video = await upload_video1080p(msg3,title,tito3,img,fpath,id,tit,name,size,main3,subtitle,nyaasize,audio_language, alink)
            save_1080p(data["title"])
            try:
                os.remove("video.mkv")
                os.remove("out.mkv")
                os.remove(file)
                os.remove(fpath)
            except:
                pass  

        
        elif data["480p"]=='01':
            title = data["title"]
            dbtit = data["title"]
            link = data["link"]
            size = data["size"]
            size = size.replace("GB", " GiB")
            nyaasize = size
            
            subtitl = data["subtitle"]
            subtitle = replace_text_with_mapping(subtitl, mapping)
            name, ext = title.split(".")

            name += f" [AniDL]." + ext

            KAYO_ID =  -1001895203720
            uj_id = 1159872623
            DATABASE_ID = -1001895203720
            bin_id = -1002062055380
            name = name.replace(f" [AniDL].","").replace(ext,"").strip()
            id, img, tit = await get_anime_img(get_anime_name(title))
            msg = await app.send_photo(bin_id,photo=img,caption=title)

            print("Downloading --> ",name)
            img, alink = await get_anilist_data(title)
            await asyncio.sleep(5)
            await status.edit(await status_text(f"Downloading {name}"),reply_markup=button1)
            file = await downloader(msg,link,size,title)

            await msg.edit(f"Download Complete : {name}")
            print("Encoding --> ",name)

            duration = get_duration(file)
            durationx = get_durationx(file)
            #filed = os.path.basename(file)
            filed = title
            
            filed = filed.replace("[1080p]", "[1080p Web-DL]")
            filed = filed.replace("2nd Season", "S2")
            filed = filed.replace("Season 2", "S2")
            filed = filed.replace("Season 3", "S3")
            filed = filed.replace("Season 4", "S4")
            filed = filed.replace("3rd Season", "S3")
            filed = filed.replace("4th Season", "S4")
            filed = filed.replace("5th Season", "S5")
            filed = filed.replace("6th Season", "S6")
            filed = filed.replace("7th Season", "S7")
            razo = filed.replace("[1080p Web-DL]", "[720p x265] @animxt")
            fpath = "downloads/" + filed
            ghostname = name
            ghostname = ghostname.replace("[1080p][Multiple Subtitle]", "")
            ghostname = ghostname.replace("[1080p]", "")
            ghostname = ghostname.replace("2nd Season", "S2")
            ghostname = ghostname.replace("3rd Season", "S3")
            subtitle = subtitle.replace("][", ", ")
            subtitle = subtitle.replace("[", "")
            subtitle = subtitle.replace("]", "")     
    
            os.rename(file,"video.mkv")
            titlx = title.replace('[Erai-raws]', '[Web][720p x265 10Bit][Opus][Erai-raws]')
            titlx = titlx.replace('[SubsPlease]', '[Web][720p x265 10Bit][Opus][SubsPlease]')
            titm = f"**[AniDL] {titlx}**"
            tito = f"[AniDL] {titlx}"
            main = await app.send_photo(KAYO_ID,photo=img, caption=titm)
            video_path="video.mkv"
        
            audio_language = get_audio_language(video_path)
            if audio_language:
                print("Audio Track Language:", audio_language)
            else:
                print("Failed to get audio language.")
            compressed = await compress_video720p(duration,main,tito)
    

            if compressed == "None" or compressed == None:

                print("Encoding Failed Uploading The Original File")

                os.rename("video.mkv",fpath)

            else:

                os.rename("out.mkv",fpath)
  
            print("Uploading --> ",name)
            video = await upload_video720p(msg,title,tito,img,fpath,id,tit,name,size,main,subtitle,nyaasize,audio_language, alink)
            save_720p(data["title"])
#1080p 

            msg3 = await app.send_photo(bin_id,photo=img,caption=title)
            titlx3 = title.replace('[Erai-raws]', '[Web][1080p x265 10Bit][AAC][Erai-raws]')
            titlx3 = titlx3.replace('[SubsPlease]', '[Web][1080p x265 10Bit][AAC][SubsPlease]')
            
            titm3 = f"**[AniDL] {titlx3}**"
            tito3 = f"[AniDL] {titlx3}"
            main3 = await app.send_photo(KAYO_ID,photo=img, caption=titm3)
            
            compressed = await compress_video1080p(duration,main3,tito3)
    

            if compressed == "None" or compressed == None:

                print("Encoding Failed Uploading The Original File")

                os.rename("video.mkv",fpath)

            else:

                os.rename("out.mkv",fpath)
  
            print("Uploading --> ",name)
            video = await upload_video1080p(msg3,title,tito3,img,fpath,id,tit,name,size,main3,subtitle,nyaasize,audio_language, alink)
            save_1080p(data["title"])
            try:
                os.remove("video.mkv")
                os.remove("out.mkv")
                os.remove(file)
                os.remove(fpath)
            except:
                pass 
        #1080p
        elif data["480p"]=='012':
            title = data["title"]
            dbtit = data["title"]
            link = data["link"]
            size = data["size"]
            size = size.replace("GB", " GiB")
            nyaasize = size
            subtitl = data["subtitle"]
            subtitle = replace_text_with_mapping(subtitl, mapping)
            name, ext = title.split(".")

            name += f" [AniDL]." + ext

            KAYO_ID =  -1001895203720
            uj_id = 1159872623
            DATABASE_ID = -1001895203720
            bin_id = -1002062055380
            name = name.replace(f" [AniDL].","").replace(ext,"").strip()
            id, img, tit = await get_anime_img(get_anime_name(title))
            msg = await app.send_photo(bin_id,photo=img,caption=title)

            print("Downloading --> ",name)
            img, alink = await get_anilist_data(title)
            await asyncio.sleep(5)
            await status.edit(await status_text(f"Downloading {name}"),reply_markup=button1)
            file = await downloader(msg,link,size,title)

            await msg.edit(f"Download Complete : {name}")
            print("Encoding --> ",name)

            duration = get_duration(file)
            durationx = get_durationx(file)
            #filed = os.path.basename(file)
            filed = title
            
            #filed = filed.replace("[1080p][Multiple Subtitle]", "[1080p Web-DL]")
            #filed = filed.replace("[1080p]", "[1080p Web-DL]")
            filed = filed.replace("2nd Season", "S2")
            filed = filed.replace("Season 2", "S2")
            filed = filed.replace("Season 3", "S2")
            filed = files.replace("Season 4", "S2")
            filed = filed.replace("3rd Season", "S3")
            filed = filed.replace("4th Season", "S4")
            filed = filed.replace("5th Season", "S5")
            filed = filed.replace("6th Season", "S6")
            filed = filed.replace("7th Season", "S7")
            razo = filed.replace("[1080p Web-DL]", "[720p x265] @animxt")
            fpath = "downloads/" + filed
            ghostname = name
            ghostname = ghostname.replace("[1080p][Multiple Subtitle]", "")
            ghostname = ghostname.replace("[1080p]", "")
            ghostname = ghostname.replace("2nd Season", "S2")
            ghostname = ghostname.replace("3rd Season", "S3")
            subtitle = subtitle.replace("][", ", ")
            subtitle = subtitle.replace("[", "")
            subtitle = subtitle.replace("]", "")     
    
            os.rename(file,"video.mkv")
            titlx = title.replace('[Erai-raws]', '[Web][1080p x265 10Bit][AAC][Erai-raws]')
            titlx = titlx.replace('[SubsPlease]', '[Web][1080p x265 10Bit][AAC][SubsPlease]')
            titm = f"**[AniDL] {titlx}**"
            tito = f"[AniDL] {titlx}"
            main = await app.send_photo(KAYO_ID,photo=img, caption=titm)
            video_path="video.mkv"
        
            audio_language = get_audio_language(video_path)
            if audio_language:
                print("Audio Track Language:", audio_language)
            else:
                print("Failed to get audio language.")
            compressed = await compress_video1080p(duration,main,tito)
    

            if compressed == "None" or compressed == None:

                print("Encoding Failed Uploading The Original File")

                os.rename("video.mkv",fpath)

            else:

                os.rename("out.mkv",fpath)
  
            print("Uploading --> ",name)
            video = await upload_video1080p(msg,title,tito,img,fpath,id,tit,name,size,main,subtitle,nyaasize,audio_language, alink)
            save_1080p(data["title"])
            try:
                os.remove("video.mkv")
                os.remove("out.mkv")
                os.remove(file)
                os.remove(fpath)
            except:

                pass  
        else:
            print("All format uploaded.")
            id = None
            name = None
            video = None

   
    except FloodWait as e:

        flood_time = int(e.x) + 5

        try:

            await status.edit(await status_text(f"Floodwait... Sleeping For {flood_time} Seconds"),reply_markup=button1)

        except:

            pass

        await asyncio.sleep(flood_time)
        
    return id, name, video

    
