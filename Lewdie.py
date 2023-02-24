import os

import discord
import regex

import e621

intents = discord.Intents.all()
client = discord.Client(intents=intents)
de = discord.Embed()

@client.event
async def on_ready():
    print('logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----')
    await client.change_presence(activity=discord.Game(name="UwU my OwO"))

@client.event
async def on_message(message):

    # ---Kill Switch---
    if message.content.startswith('!lewdieSTOP'):
        if "ghxc2" in format(message.author):
            await message.channel.send('Okey! Goodnight')
            exit()

    # ---Not From Lewdias herself---
    if message.author == client.user:
        return

    # ---Not from ANY bot---
    if message.author.bot == True:
        # print(message.author, 'that was a bot!')
        return 

    # ---Responses uwu---
    regexowo = "([o|u|O|U|0-9|\-|\.|\;|\^][w|u|v|W|V|o|O|_|\-|\^|A|\.|0-9][o|u|O|U|0-9|\-|\.|\;|\^])"
    if regex.match(regexowo, message.content):
        await message.channel.send(regex.findall(regexowo, message.content)[0])

    if ('good bot') in str.lower(message.content):
        await message.channel.send("OwO you're welcome!! >W<")
    # ---E6 Commands!---
    if message.content.startswith("!e6new"):
        await message.channel.send(e621.getImageNewest())

    if message.content.startswith("!e6tag"):
        tags = message.content.split(" ")

        tags = tags[1:]
        await message.channel.send('ohh~! coming up! Tags: ' + " ".join(tags))
        tagsStr = "+".join(tags)
        links = e621.getImagesByTags(tagsStr)
        if "latias" in message.content:
            await message.channel.send('Me~? >//w//<')
        await message.channel.send("Sauce: <" + links[1] + ">")
        if links[0] != "None":
            await message.channel.send(links[0])
        else:
            await message.channel.send("Uh ohh! no link?")

client.run(str(os.environ.get("TOKEN")))