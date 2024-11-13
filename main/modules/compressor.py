import asyncio
import aiofiles
import aiohttp
from pathlib import Path
from pyrogram import Client, idle, filters, enums
from main.modules.utils import get_progress_text 

import os

import re

import math

import subprocess

async def gg():
          cmd = f'''ffmpeg -hide_banner -loglevel quiet -progress "progressaa.txt" -i "video.mkv" -metadata title="AniDL Encodes" -pix_fmt yuv420p10le -r 24000/1001 -s 852x480 -preset medium -c:v libx265 -crf 23 -x265-params deblock=1,1:limit-sao:psy-rd=1.30:psy-rdoq=2:aq-mode=3:aq-strength=0.90:frame-threads=4:bframes=6:numa-pools=+:no-info=1 -metadata:s:v:0 title="[AniDL] ~ 480p x265 10Bit"  -map 0:v -c:a libopus -b:a 96k -map 0:a  -c:s copy -map 0:s? "out.mkv" -y''',
          subprocess.Popen(cmd,shell=True)

async def gg2():
          cmd = f'''ffmpeg -hide_banner -loglevel quiet -progress "progressaa.txt" -i "video.mkv" -metadata title="AniDL Encodes" -pix_fmt yuv420p10le -r 24000/1001 -s 1280x720 -preset medium -c:v libx265 -crf 22 -x265-params deblock=1,1:limit-sao:psy-rd=1.30:psy-rdoq=2:aq-mode=3:aq-strength=0.90:frame-threads=4:bframes=6:numa-pools=+:no-info=1 -metadata:s:v:0 title="[AniDL] ~ 720p x265 10Bit"  -map 0:v -c:a libopus -b:a 96k -map 0:a  -c:s copy -map 0:s? "out.mkv" -y''',
          subprocess.Popen(cmd,shell=True)

async def gg3():
          cmd = f'''ffmpeg -hide_banner -loglevel quiet -progress "progressaa.txt" -i "video.mkv" -metadata title="AniDL Encodes" -pix_fmt yuv420p10le -r 24000/1001 -s 1920x1080 -preset medium -c:v libx265 -crf 22 -x265-params deblock=1,1:limit-sao:psy-rd=1.30:psy-rdoq=2:aq-mode=3:aq-strength=0.90:frame-threads=4:bframes=6:numa-pools=+:no-info=1 -metadata:s:v:0 title="[AniDL] ~ 1080p x265 10Bit"  -map 0:v -c:a copy -map 0:a  -c:s copy -map 0:s? "out.mkv" -y''',
          subprocess.Popen(cmd,shell=True)
          
async def compress_video(total_time,main,name):

  try:

    video = "video.mkv"

    out = "out.mkv" 

    prog = "progressaa.txt"

    with open(prog, 'w') as f:

      pass

    

    asyncio.create_task(gg())

   

    while True:

      with open(prog, 'r+') as file:

        text = file.read()

        frame = re.findall("frame=(\d+)", text)

        time_in_us=re.findall("out_time_ms=(\d+)", text)

        progress=re.findall("progress=(\w+)", text)

        speed=re.findall("speed=(\d+\.?\d*)", text)

        if len(frame):

          frame = int(frame[-1])

        else:

          frame = 1

        if len(speed):

          speed = speed[-1]

        else:

          speed = 1

        if len(time_in_us):

          time_in_us = time_in_us[-1]

        else:

          time_in_us = 1

        if len(progress):

          if progress[-1] == "end":

            break

        

        time_done = math.floor(int(time_in_us)/1000000)

        

        progress_str = get_progress_text(name,"Encoding",time_done,str(speed),total_time,enco=True)

        try:

          await main.edit_message_text(progress_str, parse_mode=enums.ParseMode.HTML)

        except:

            pass

      await asyncio.sleep(15)

    if os.path.lexists(out):

        return out

    else:

        return "None"

  except Exception as e:

    print("Encoder Error",e)

#720p

async def compress_video720p(total_time,main,name):

  try:

    video = "video.mkv"

    out = "out.mkv" 

    prog = "progressaa.txt"

    with open(prog, 'w') as f:

      pass

    

    asyncio.create_task(gg2())

   

    while True:

      with open(prog, 'r+') as file:

        text = file.read()

        frame = re.findall("frame=(\d+)", text)

        time_in_us=re.findall("out_time_ms=(\d+)", text)

        progress=re.findall("progress=(\w+)", text)

        speed=re.findall("speed=(\d+\.?\d*)", text)

        if len(frame):

          frame = int(frame[-1])

        else:

          frame = 1

        if len(speed):

          speed = speed[-1]

        else:

          speed = 1

        if len(time_in_us):

          time_in_us = time_in_us[-1]

        else:

          time_in_us = 1

        if len(progress):

          if progress[-1] == "end":

            break

        

        time_done = math.floor(int(time_in_us)/1000000)

        

        progress_str = get_progress_text(name,"Encoding",time_done,str(speed),total_time,enco=True)

        try:

          await main.edit_message_tex(progress_str, parse_mode=enums.ParseMode.HTML)

        except:

            pass

      await asyncio.sleep(15)

    if os.path.lexists(out):

        return out

    else:

        return "None"

  except Exception as e:

    print("Encoder Error",e)


async def compress_video1080p(total_time,main,name):

  try:

    video = "video.mkv"

    out = "out.mkv" 

    prog = "progressaa.txt"

    with open(prog, 'w') as f:

      pass

    

    asyncio.create_task(gg3())

   

    while True:

      with open(prog, 'r+') as file:

        text = file.read()

        frame = re.findall("frame=(\d+)", text)

        time_in_us=re.findall("out_time_ms=(\d+)", text)

        progress=re.findall("progress=(\w+)", text)

        speed=re.findall("speed=(\d+\.?\d*)", text)

        if len(frame):

          frame = int(frame[-1])

        else:

          frame = 1

        if len(speed):

          speed = speed[-1]

        else:

          speed = 1

        if len(time_in_us):

          time_in_us = time_in_us[-1]

        else:

          time_in_us = 1

        if len(progress):

          if progress[-1] == "end":

            break

        

        time_done = math.floor(int(time_in_us)/1000000)

        

        progress_str = get_progress_text(name,"Encoding",time_done,str(speed),total_time,enco=True)

        try:

          await main.edit_message_text(progress_str, parse_mode=enums.ParseMode.HTML)

        except:

            pass

      await asyncio.sleep(10)

    if os.path.lexists(out):

        return out

    else:

        return "None"

  except Exception as e:

    print("Encoder Error",e)
