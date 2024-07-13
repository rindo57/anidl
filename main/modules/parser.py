import asyncio
from main.modules.utils import status_text
from main import status
from main.modules.db import get_animesdb, get_uploads, save_animedb
import feedparser
from main import queue
from main.inline import button1

def trim_title(title: str):
    title = title.rsplit(' ', 1)[0]
    title = title.replace("[Magnet] ", "")
    title = f"{title} [Erai-raws]"
    title = title.replace("- Ouji no Kikan", "S2")
    title = title.replace("Mahou Tsukai no Yome Season 2 Cour 2", "Mahou Tsukai no Yome Season 2 Part 2")
    title = title.replace("NieR:Automata Ver1.1a Part 2", "NieR Automata Ver1_1a Season 2")
    title = title.replace(" (CA)", "")
    title = title.replace(" (JA)", "")
    title = title.replace(" (Japanese Audio)", " (JA)")
    title = title.replace(" (Chinese Audio)", " (CA)")
    title = title.replace(" (Multi)", "")
    title = title.replace("Tian Guan Ci Fu Di Er Ji", "Heaven Official's Blessing S2")
    title = title.replace("(AAC 2.0) ", "")
    ext = ".mkv"
    title = title + ext
    return title

def trim_titlex(title: str):
    title = title.rsplit(' ', 1)[0]
    title = title.replace("[SubsPlease] ", "")
    title = title.replace(" (1080p) ", "")
    title = f"{title} [SubsPlease]"
    ext = ".mkv"
    title = title + ext
    return title
def multi_sub(title: str):
    subtitle = title.split()[-1] 
    return subtitle

def parse():
    a = feedparser.parse("https://www.siftrss.com/f/6XM5qNo7aq")
    ny = feedparser.parse("https://nyaa.si/?page=rss&q=%22[SubsPlease]%20Ore%20wa%20Subete%20wo%20Parry%20suru%22%20(1080p)%20-HEVC")
    b = a["entries"]
    c = ny["entries"]
    
    data = []    
    data.reverse()
    for i in b:
        item = {}
        item['title'] = trim_title(i['title'])
        item['subtitle'] = (i['erai_subtitles'])
        item['size'] = i['erai_size']   
        item['link'] = "magnet:?xt=urn:btih:" + i['erai_infohash']
        item['480p'] = '0'
        data.append(item)
    for i in ny:
        
        item['title'] = trim_titlex(i['title'])        
        item['subtitle'] = "us"
        item['size'] = i['nyaa_size']   
        item['link'] = "magnet:?xt=urn:btih:" + i['nyaa_infohash']
        item['480p'] = '0'
        data.append(item)
    return data

async def auto_parser():
    while True:
        try:
            await status.edit(await status_text("Parsing Rss, Fetching Magnet Links..."),reply_markup=button1)
        except:
            pass

        rss = parse()
        data = await get_animesdb()
        uploaded = await get_uploads()

        saved_anime = []
        for i in data:
            saved_anime.append(i["name"])

        uanimes = []
        for i in uploaded:
            uanimes.append(i["name"])
        
        for i in rss:
            if i["title"] not in uanimes and i["title"] not in saved_anime:
                if ".mkv" in i["title"] or ".mp4" in i["title"]:
                    title = i["title"]
                    await save_animedb(title,i)

        data = await get_animesdb()
        for i in data:
            if i["data"] not in queue:
                queue.append(i["data"])    
                print("Saved ", i["name"])   

        try:
            await status.edit(await status_text("Idle..."),reply_markup=button1)
        except:
            pass

        await asyncio.sleep(30)
