#!/usr/bin/env python3
# Copyright (C) @ZauteKm
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import os
import asyncio
from urllib.parse import urlparse
from pyrogram.errors import UserNotParticipant, UserBannedInChannel
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from youtube_dl import YoutubeDL
from opencc import OpenCC
from config import Config
import wget

ZauteKm = Client(
   "Kayla Streamer",
   api_id=Config.APP_ID,
   api_hash=Config.API_HASH,
   bot_token=Config.TG_BOT_TOKEN,
)

YTDL_REGEX = (r"^((?:https?:)?\/\/)"
              r"?((?:www|m)\.)"
              r"?((?:youtube\.com|youtu\.be|xvideos\.com|pornhub\.com"
              r"|xhamster\.com|xnxx\.com))"
              r"(\/)([-a-zA-Z0-9()@:%_\+.~#?&//=]*)([\w\-]+)(\S+)?$")
s2tw = OpenCC('s2tw.json').convert


@ZauteKm.on_message(filters.command("start"))
async def start(client, message):
   if message.chat.type == 'private':
       await ZauteKm.send_message(
               chat_id=message.chat.id,
               text="""<b>Hey There, I'm Just A Gift To @theonlygirlyou \n\Made by @meerfreak

He programmed me to download videos and Audios for you from YouTube.

Hit the help button.. So i can guid you on how to use me✌️</b>""",   
                            reply_markup=InlineKeyboardMarkup(
                                [
                                [
                                        InlineKeyboardButton('🙆🏻‍♂️ Help', callback_data="help"),
                                        InlineKeyboardButton('Tell Me What you think 😇', url='https://telegram.me/meerfreak')
                                    ],[
                                        InlineKeyboardButton('🧑‍🔧 Owner', url='https://t.me/theonlygirlyou'),
                                        InlineKeyboardButton('Friend', url='https://t.me/meerfreak'),
                                        InlineKeyboardButton('Ameer Bestie 📢', url='tg://settings')
                                    ],[
                                        InlineKeyboardButton('🔻 Favourite Place🔻', url='https://youtube.com'),
                                    ]]
                            ),        
            disable_web_page_preview=True,        
            parse_mode="html")

@ZauteKm.on_message(filters.command("help"))
async def help(client, message):
    if message.chat.type == 'private':   
        await ZauteKm.send_message(
               chat_id=message.chat.id,
               text="""<b><u>Miss Khaila😚</u></b>

Just Send me a YouTube url to download it in video or audio format!

<b>▷ I pleadge to serve you My Lady😎</b>""",
        reply_markup=InlineKeyboardMarkup(
                                [[
                                        InlineKeyboardButton(
                                            "🔙 Back", callback_data="start"),
                                        InlineKeyboardButton(
                                            "About 🙄", callback_data="about"),
                                  ],[
                                        InlineKeyboardButton("🧑‍🔧 Owner", url="https://t.me/theonlygirlyou"),
                                        InlineKeyboardButton("🤖 Bot Coder", url="https://t.me/meerfreak"),
                                        InlineKeyboardButton('Chat 📢', url="https://t.me/meerfreak")
                                    ],[
                                        InlineKeyboardButton("❤️ Favorite site🔻", url="https://youtube.com"),
                                    ]]
                            ),        
            disable_web_page_preview=True,        
            parse_mode="html")

@ZauteKm.on_message(filters.command("about"))
async def about(client, message):
    if message.chat.type == 'private':   
        await ZauteKm.send_message(
               chat_id=message.chat.id,
               text="""<b><u>About Khaila Streamer </u></b>

<b>▷ 🧑‍🔧 About My Existance:</b> <a href="https://t.me/meerfreak">Ameer</a> Created me to so that i can become your servant. 

<b>▷ 📚 Library :</b> <a href="https://github.com/pyrogram/pyrogram">Pyrogram</a>

<b>▷ 📢 My Goal:</b> My goal is to serve you. I am delighted to be at your service 😁

<b>▷ 🌀 HOPE YOU LIKE. Also am just a bot. i might misbehave sometimes. Pls just report me quickly  to :</b> <a href="https://t.me/meerfreak">Ameer</a>""",
     reply_markup=InlineKeyboardMarkup(
                                [[
                                        InlineKeyboardButton(
                                            "🔙 Back", callback_data="help"),
                                        InlineKeyboardButton(
                                            "Credit ❤️", url="https://t.me/theonlygirlyou"),
                                  ],[
                                        InlineKeyboardButton("🧑‍🔧 Owner", url="https://t.me/theonlygirlyou"),
                                        InlineKeyboardButton("🤖 Bot Coder", url="https://t.me/meerfreak"),
                                        InlineKeyboardButton('Chat 📢', url="https://t.me/meerfreak")
                                    ],[
                                        InlineKeyboardButton("🔻 Favorite Site 🔻", url="https://youtube.com"),
                                    ]]
                            ),        
            disable_web_page_preview=True,        
            parse_mode="html")


# https://docs.pyrogram.org/start/examples/bot_keyboards
# Reply with inline keyboard
@ZauteKm.on_message(filters.private
                   & filters.text
                   & ~filters.edited
                   & filters.regex(YTDL_REGEX))
async def ytdl_with_button(c: Client, message: Message):
    if Config.UPDATES_CHANNEL is not None:
        try:
            user = await c.get_chat_member(Config.UPDATES_CHANNEL, message.chat.id)
            if user.status == "kicked":
                await c.send_message(
                    chat_id=message.chat.id,
                    text="Sorry, You are Banned to use me. Contact my [master](https://t.me/meerfreak).",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await c.send_message(
                chat_id=message.chat.id,
                text="**Please Tell my master what you think of me**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("my master", url=f"https://t.me/{Config.UPDATES_CHANNEL}")
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await c.send_message(
                chat_id=message.chat.id,
                text="Something went Wrong. Contact my [master](https://t.me/meerfreak).",
                parse_mode="markdown",
                disable_web_page_preview=True)
            return
    await message.reply_text(
        "**Choose Download type👇**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🎵 Audio",
                        callback_data="ytdl_audio"
                    ),
                    InlineKeyboardButton(
                        "Video 🎬",
                        callback_data="ytdl_video"
                    )
                ]
            ]
        ),
        quote=True
    )


@ZauteKm.on_callback_query(filters.regex("^ytdl_audio$"))
async def callback_query_ytdl_audio(_, callback_query):
    try:
        url = callback_query.message.reply_to_message.text
        ydl_opts = {
            'format': 'bestaudio',
            'outtmpl': '%(title)s - %(extractor)s-%(id)s.%(ext)s',
            'writethumbnail': True
        }
        with YoutubeDL(ydl_opts) as ydl:
            message = callback_query.message
            await message.reply_chat_action("typing")
            info_dict = ydl.extract_info(url, download=False)
            # download
            await callback_query.edit_message_text("**Downloading audio...**")
            ydl.process_info(info_dict)
            # upload
            audio_file = ydl.prepare_filename(info_dict)
            task = asyncio.create_task(send_audio(message, info_dict,
                                                  audio_file))
            while not task.done():
                await asyncio.sleep(3)
                await message.reply_chat_action("upload_document")
            await message.reply_chat_action("cancel")
            await message.delete()
    except Exception as e:
        await message.reply_text(e)
    await callback_query.message.reply_to_message.delete()
    await callback_query.message.delete()


if Config.AUDIO_THUMBNAIL == "No":
   async def send_audio(message: Message, info_dict, audio_file):
       basename = audio_file.rsplit(".", 1)[-2]
       # .webm -> .weba
       if info_dict['ext'] == 'webm':
           audio_file_weba = basename + ".weba"
           os.rename(audio_file, audio_file_weba)
           audio_file = audio_file_weba
       # thumbnail
       thumbnail_url = info_dict['thumbnail']
       thumbnail_file = basename + "." + \
           get_file_extension_from_url(thumbnail_url)
       # info (s2tw)
       webpage_url = info_dict['webpage_url']
       title = s2tw(info_dict['title'])
       caption = f"<b><a href=\"{webpage_url}\">{title}</a></b>"
       duration = int(float(info_dict['duration']))
       performer = s2tw(info_dict['uploader'])
       await message.reply_audio(audio_file, caption=caption, duration=duration,
                              performer=performer, title=title,
                              parse_mode='HTML', thumb=thumbnail_file)
       os.remove(audio_file)
       os.remove(thumbnail_file)

else:
    async def send_audio(message: Message, info_dict, audio_file):
       basename = audio_file.rsplit(".", 1)[-2]
       # .webm -> .weba
       if info_dict['ext'] == 'webm':
           audio_file_weba = basename + ".weba"
           os.rename(audio_file, audio_file_weba)
           audio_file = audio_file_weba
       # thumbnail
       lol = Config.AUDIO_THUMBNAIL
       thumbnail_file = wget.download(lol)
       # info (s2tw)
       webpage_url = info_dict['webpage_url']
       title = s2tw(info_dict['title'])
       caption = f"<b><a href=\"{webpage_url}\">{title}</a></b>"
       duration = int(float(info_dict['duration']))
       performer = s2tw(info_dict['uploader'])
       await message.reply_audio(audio_file, caption=caption, duration=duration,
                              performer=performer, title=title,
                              parse_mode='HTML', thumb=thumbnail_file)
       os.remove(audio_file)
       os.remove(thumbnail_file)

@ZauteKm.on_callback_query(filters.regex("^ytdl_video$"))
async def callback_query_ytdl_video(_, callback_query):
    try:
        # url = callback_query.message.text
        url = callback_query.message.reply_to_message.text
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'outtmpl': '%(title)s - %(extractor)s-%(id)s.%(ext)s',
            'writethumbnail': True
        }
        with YoutubeDL(ydl_opts) as ydl:
            message = callback_query.message
            await message.reply_chat_action("typing")
            info_dict = ydl.extract_info(url, download=False)
            # download
            await callback_query.edit_message_text("**Downloading video...**")
            ydl.process_info(info_dict)
            # upload
            video_file = ydl.prepare_filename(info_dict)
            task = asyncio.create_task(send_video(message, info_dict,
                                                  video_file))
            while not task.done():
                await asyncio.sleep(3)
                await message.reply_chat_action("upload_document")
            await message.reply_chat_action("cancel")
            await message.delete()
    except Exception as e:
        await message.reply_text(e)
    await callback_query.message.reply_to_message.delete()
    await callback_query.message.delete()

if Config.VIDEO_THUMBNAIL == "No":
   async def send_video(message: Message, info_dict, video_file):
      basename = video_file.rsplit(".", 1)[-2]
      # thumbnail
      thumbnail_url = info_dict['thumbnail']
      thumbnail_file = basename + "." + \
          get_file_extension_from_url(thumbnail_url)
      # info (s2tw)
      webpage_url = info_dict['webpage_url']
      title = s2tw(info_dict['title'])
      caption = f"<b><a href=\"{webpage_url}\">{title}</a></b>"
      duration = int(float(info_dict['duration']))
      width, height = get_resolution(info_dict)
      await message.reply_video(
          video_file, caption=caption, duration=duration,
          width=width, height=height, parse_mode='HTML',
          thumb=thumbnail_file)

      os.remove(video_file)
      os.remove(thumbnail_file)

else:
   async def send_video(message: Message, info_dict, video_file):
      basename = video_file.rsplit(".", 1)[-2]
      # thumbnail
      lel = Config.VIDEO_THUMBNAIL
      thumbnail_file = wget.download(lel)
      # info (s2tw)
      webpage_url = info_dict['webpage_url']
      title = s2tw(info_dict['title'])
      caption = f"<b><a href=\"{webpage_url}\">{title}</a></b>"
      duration = int(float(info_dict['duration']))
      width, height = get_resolution(info_dict)
      await message.reply_video(
          video_file, caption=caption, duration=duration,
          width=width, height=height, parse_mode='HTML',
          thumb=thumbnail_file)

      os.remove(video_file)
      os.remove(thumbnail_file)

def get_file_extension_from_url(url):
    url_path = urlparse(url).path
    basename = os.path.basename(url_path)
    return basename.split(".")[-1]


def get_resolution(info_dict):
    if {"width", "height"} <= info_dict.keys():
        width = int(info_dict['width'])
        height = int(info_dict['height'])
    # https://support.google.com/youtube/answer/6375112
    elif info_dict['height'] == 1080:
        width = 1920
        height = 1080
    elif info_dict['height'] == 720:
        width = 1280
        height = 720
    elif info_dict['height'] == 480:
        width = 854
        height = 480
    elif info_dict['height'] == 360:
        width = 640
        height = 360
    elif info_dict['height'] == 240:
        width = 426
        height = 240
    return (width, height)


@ZauteKm.on_callback_query()
async def button(bot, update):
      cb_data = update.data
      if "help" in cb_data:
        await update.message.delete()
        await help(bot, update.message)
      elif "about" in cb_data:
        await update.message.delete()
        await about(bot, update.message)
      elif "start" in cb_data:
        await update.message.delete()
        await start(bot, update.message)

print(
    """
Bot Started!
Join @JosProjects
"""
)

ZauteKm.run()
