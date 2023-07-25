import os

import discord
import regex
import e621
import configparser
import saucenao


intents = discord.Intents.all()
client = discord.Client(intents=intents)
de = discord.Embed()
blacklist = {"...", "0.0", "4.4", "7.7", "9.9"}

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
    try:
        msg = message.content
        regexowo = "((?<!\<)([o|u|O|U|0-9|\-|\.|\;|\^][w|u|v|W|V|o|O|_|\-|\^|A|\.|0-9][o|u|O|U|0-9|\-|\.|\;|\^])(?![\w\s]*[\>]))"
        urlFound = regex.findall("http[^\s]*", msg)
        if urlFound:
            msg = str(msg).replace(urlFound[0], "")
        print(msg)
        match = regex.findall(regexowo, msg)
        if match:
            match = match[0][0]
            if not match.isnumeric() and match not in blacklist and not bool(regex.search(r"\d\.\d", msg)):
                await message.channel.send(match)
    except:
        this = True

    if ('good bot') in str.lower(message.content):
        await message.channel.send("OwO you're welcome!! >W<")
    if ('bad bot') in str.lower(message.content):
        await message.channel.send('Sowy ;^;')
    # ---E6 Commands!---
    if message.content.startswith("!e6new"):
        if message.content == "!e6new":
            links = e621.getImageNewest()
            await message.channel.send("The hottest sauce of the press! ;3")
            await message.channel.send("Sauce: <" + links[1] + ">")
            await message.channel.send(links[0])
        else:
            tags = message.content.split(" ")
            tags = tags[1:]
            links = e621.getNewestImageByTags("+".join(tags))
            await message.channel.send("The hottest sauce of the press! ;3")
            await message.channel.send("Jus what you wan: " + " ".join(tags))
            await message.channel.send("Sauce: <" + links[1] + ">")
            await message.channel.send(links[0])

    if message.content.startswith("!e6tag"):
        try:
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
        except:
            await message.channel.send("None cri sowy ;-;")

    # -- Saucenao -- #

    if message.content.startswith("!sauce"):
        await message.channel.send("Saucey comin up!")
        try:
            await message.channel.send("Sauce: " + saucenao.getSauce(message.content[7:]))
        except:
            await message.channel.send("Couldn find it, sowwy >>")

    # -- Icons! -- #

    if message.content.startswith("!icon"):
        if message.content == "!icon":
           await message.channel.send(message.author.avatar.url)
        else:
            await message.channel.send(message.mentions[0].avatar.url)
print("Loaded successfully")
# client.run(str(os.environ.get('TOKEN')))
config = configparser.ConfigParser()
config.read('config.ini')
TOKEN = config.get("Tokens", "TOKEN")

client.run(TOKEN)