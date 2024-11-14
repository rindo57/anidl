import asyncio
from main.modules.utils import status_text
from main import status
from main.modules.db import get_animesdb, get_uploads, save_animedb
import feedparser
from main import queue
from main.inline import button1
import re
def trim_title(title: str):
    match = re.match(r'(.*?)\s*(?:\|\s*(.*?))?\s*-\s*(\d+)(?=\s*\[)', title)
    if match:
        main_title = match.group(1)
        episode_number = match.group(3)
        cleaned_title = f"{main_title} - {episode_number}"
        titlef = cleaned_title.replace("[Magnet] ", "")
        print(titlef)
        titlef = f"{titlef} [Erai-raws]"
        ext = ".mkv"
        title = titlef + ext
    # Extract optional title part after '|'
        extracted_part = match.group(2)
    
        print("Cleaned Title:", cleaned_title)
        if extracted_part:
            print("Eng Title:", extracted_part)
            return title, extracted_part
        else:
            return title
    #title = title.rsplit(' ', 1)[0]
    
   
    
    '''#title = title.replace(": Ouji no Kikan", " S2")
   # title = title.replace("Saikyou no Shienshoku -Wajutsushi- de Aru Ore wa Sekai Saikyou Clan wo Shitagaeru", "Saikyou no Shien-shoku [Wajutsushi] de Aru Ore wa Sekai Saikyou Clan wo Shitagaeru")
    #title = title.replace("Fairy Tail - 100 Years Quest - S01", "Fairy Tail - 100 Years Quest - Special 01")
    #title = title.replace("Dungeon ni Deai wo Motomeru no wa Machigatteiru Darou ka: Familia Myth V", "Dungeon ni Deai wo Motomeru no wa Machigatteiru Darou ka V: Houjou no Megami-hen")
    title = title.replace("NieR:Automata Ver1.1a Part 2", "NieR Automata Ver1_1a Season 2")
    title = title.replace(" (CA)", "")
    title = title.replace(" (JA)", "")
    title = title.replace(" (Japanese Audio)", " (JA)")
    title = title.replace(" (Chinese Audio)", " (CA)")
    title = title.replace(" (Multi)", "")
    #title = title.replace("Tian Guan Ci Fu Di Er Ji", "Heaven Official's Blessing S2")
    title = title.replace("(AAC 2.0) ", "")'''
    
   

def trim_titlez(title: str):
    title = title.rsplit(' ', 1)[0]
    title = title.replace("[SubsPlease] ", "")
    title = title.replace(" (1080p)", "")
    title = f"{title} [SubsPlease]"
    ext = ".mkv"
    title = title + ext
    return title


def trim_titlex(title: str):
    ep = title.rsplit(' ', 5)[-1].replace("S02E", "S2 - ")
    title = title.rsplit(' ', 14)[0]
    title = title.replace("[Passerby-ApocalypticSubs] ", "")
    ext = ".mkv"
    title = title + " " + ep + " " + "[Passerby-ApocalypticSubs]" + ext
    print(title)
    return title
    
def multi_sub(title: str):
    subtitle = title.split()[-1] 
    return subtitle

def parse():
    a = feedparser.parse("https://siftrss.com/f/M6qVKl8MZl7")
    ny = feedparser.parse("https://www.siftrss.com/f/xg5xjGXvlP")
    b = a["entries"]
    
    c = ny["entries"]

    data = []    
    
    for i in b:
        if "(ITA)" not in i['title']:
            item = {}
            title, entitle = trim_title(i.get('title', '')), i.get('entitle', '')

# Update item accordingly
            item['title'] = title
            item['entitle'] = entitle
            item['subtitle'] = (i['erai_subtitles'])
            item['size'] = i['erai_size']   
            item['link'] = "magnet:?xt=urn:btih:" + i['erai_infohash']
            item['480p'] = '0'
            data.append(item)
            data.reverse()
    for i in c:
        item = {}
        item['title'] = trim_titlex(i['title'])  
        item['entitle'] = "The Seven Deadly Sins: Four Knights of the Apocalypse"
        item['subtitle'] = "us"
        item['size'] = i['nyaa_size']   
        item['link'] = "magnet:?xt=urn:btih:" + i['nyaa_infohash']
        item['480p'] = '0'
        data.append(item)
        data.reverse()
    return data

async def auto_parser():
    while True:
        try:
            await status.edit(await status_text("Parsing Rss, Fetching Magnet Links..."))
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
            await status.edit(await status_text("Idle..."))
        except:
            pass

        await asyncio.sleep(60)
