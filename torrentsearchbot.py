import requests
from telegraph import Telegraph
from telethon import TelegramClient, events
from telethon import custom, events, Button
import re
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from Configs import Config
from loggers import logging
bot = TelegramClient("bot", api_id=Config.API_ID, api_hash=Config.API_HASH)
torrentbot = bot.start(bot_token=Config.BOT_TOKEN)

help_txt = (
    "<b>How To Use Me?</b> \n\n"
    "<code>/search <KeyWord> - Searches The Key Word Given For Torrent Magnets. \n"
    "/help - No One is Gonna Help You. \n"
)

@torrentbot.on(events.NewMessage(pattern="^/search (.*)"))
async def search(event):
    starkpro = event.pattern_match.group(1)
    apifinal = "https://api.sumanjay.cf/torrent/?query=" + starkpro
    hmmyeah = event.sender_id
    replied_user = await event.client(GetFullUserRequest(event.sender_id))
    firstname = replied_user.user.first_name
    try:
        sed = requests.get(url=apifinal, timeout=10).json()
    except requests.exceptions.Timeout as err: 
        await event.reply("Cound't Fetch Anything?, Check Spelling Maybe?")
        return
    if len(sed) == 0:
        await event.reply("Cound't Fetch Anything?, Check Spelling Maybe?")
        return
    glass = await event.reply("Searching For Results 🔎")
    hmm = f"Search Results \nQuery : {starkpro} \nFetched For : {firstname} \n\n"
    for okpro in sed:
        seds = okpro["age"]
        okpros = okpro["leecher"]
        sadstark = okpro["magnet"]
        okiknow = okpro["name"]
        starksize = okpro["size"]
        starky = okpro["type"]
        seeders = okpro["seeder"]
        sites = okpro["site"]
        hmm += (
            f"Name : {okiknow}\n"
            f"Size : {starksize}\n"
            f"Age : {seds}\n"
            f"Total Leechers : {okpros}\n"
            f"Type : {starky} \n"
            f"Seeder : {seeders} \n"
            f"Site : {sites} \n"
            f"Magnet : {sadstark}\n\n"
        )
    url = "https://del.dog/documents"
    r = requests.post(url, data=hmm.encode("UTF-8")).json()
    url = f"https://del.dog/{r['key']}"
    await glass.delete()
    await torrentbot.send_message(event.chat_id,
        message=f"**Results Fetched SucessFully**",
        buttons = [
              [Button.url("See Results", f"{url}")],
              ]
             )
    await torrentbot.send_message(Config.DUMB_CHAT, f"USER-ID : `{hmmyeah}` \nSearched For : `{starkpro}`")


@torrentbot.on(events.NewMessage(pattern="^/help$"))
async def search(event):
    await event.reply(help_txt, parse_mode="HTML")

@torrentbot.on(events.NewMessage(pattern="^/start$"))
async def search(event):
    starkbot = await torrentbot.get_me()
    bot_id = starkbot.first_name
    bot_username = starkbot.username
    replied_user = await event.client(GetFullUserRequest(event.sender_id))
    firstname = replied_user.user.first_name
    vent = event.chat_id
    sedtext = (f'**Hey, {firstname} !** \n`I am a Simple Torrent Search Bot.` \n'
    '`Send Me A Query And I will Give You Magnet Link Pasted In Dogbin.` \n'
    '__Thank You For Using Me.__ \n'
    '**(C) @STARKGANG**')
    await torrentbot.send_message(event.chat_id, message=sedtext, buttons = [
             [custom.Button.inline("Help ❓", data="mewant")],
             [custom.Button.inline("Close 🔐", data="close ")],
              ]
             )
    
@torrentbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"mewant")))
async def help(event):
    okbruh = ("**How To Use Me?**\n\n"
    "`/search <KeyWord>` - __Searches The Key Word Given For Torrent Magnets.__ \n"
    "`/help` - __No One is Gonna Help You.__ \n")
    await event.edit(
            okbruh,
            buttons=[
                [Button.url("Join Channel", "t.me/Telegram")],
            ],
        )
@torrentbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"close")))
async def help(event):
    await event.delete()
    
print("Bot Is Alive.")
def startbot():
    torrentbot.run_until_disconnected()


if __name__ == "__main__":
    startbot()
