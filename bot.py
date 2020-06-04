import discord
import asyncio
import datetime
import json
import os
import commands

client = discord.Client()
cfg = open("config.json", "r")
tmpconfig = cfg.read()
cfg.close()
config = json.loads(tmpconfig)
token = os.environ['token']
guild_id = config["server-id"]
logs_channel = config["logs-channel-id"]


invites = {}
last = ""

async def fetch():
 global last
 global invites
 await client.wait_until_ready()
 gld = client.get_guild(int(guild_id))
 logs = client.get_channel(int(logs_channel))
 while True:
  invs = await gld.invites()
  tmp = []
  for i in invs:
   for s in invites:
    if s[0] == i.code:
     if int(i.uses) > s[1]:
      usr = gld.get_member(int(last))
      testh = f"{usr.name} **joined**; Invited by **{i.inviter.name}** (**{str(i.uses)}** invites)"
      await logs.send(testh)
   tmp.append(tuple((i.code, i.uses)))
  invites = tmp
  await asyncio.sleep(4)


@client.event
async def on_ready():
 print("ready!")
 await client.change_presence(activity = discord.Activity(name = "joins", type = 2))


@client.event
async def on_member_join(meme):
 global last
 last = str(meme.id)




client.loop.create_task(fetch())
client.run(os.environ['token'])