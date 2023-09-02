import discord
import regex
import e621
import configparser
import saucenao


intents = discord.Intents.all()
client = discord.Client(intents=intents)
de = discord.Embed()
blacklist = {"...", "0.0", "4.4", "7.7", "9.9"}


# Start of functions
async def command_selector(message):
    which_command = message.content.split(" ")[0]
    match which_command:
        case "!e6new":
            await e6new(message)
        case "!e6tag":
            await e6tag(message)
        case "!lewdieSTOP":
            await stop(message)
        case "sauce":
            await sauce(message)
        case "icon":
            await icon(message)


# ---e6 Commands--- #
async def e6new(message):
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


async def e6tag(message):
    try:
        tags = message.content.split(" ")

        tags = tags[1:]
        await message.channel.send('ohh~! coming up! Tags: ' + " ".join(tags))
        tags_str = "+".join(tags)
        links = e621.getImagesByTags(tags_str)
        if "latias" in message.content:
            await message.channel.send('Me~? >//w//<')
        await message.channel.send("Sauce: <" + links[1] + ">")
        if links[0] != "None":
            await message.channel.send(links[0])
        else:
            await message.channel.send("Uh ohh! no link?")
    except:
        await message.channel.send("None cri sowy ;-;")


async def e6fav(message):
    return


async def e6score(message):
    return


# ---Sauce--- #
async def sauce(message):
    await message.channel.send("Saucey comin up!")
    try:
        await message.channel.send("Sauce: " + saucenao.getSauce(message.content[7:]))
    except:
        await message.channel.send("Couldn find it, sowwy >>")


# -- Icons! -- #
async def icon(message):
    if message.content == "!icon":
        await message.channel.send(message.author.avatar.url)
    else:
        await message.channel.send(message.mentions[0].avatar.url)


# ---Kill Switch--- #
async def stop(message):
    if message.content.startswith('!lewdieSTOP'):
        if "ghxc2" in format(message.author):
            await message.channel.send('Okey! Goodnight')
            exit()


# --- Bot Checker --- #
def is_bot(message):
    return message.author.bot


def is_lewdie(message):
    return message.author == client.user


def is_user(message):
    return not (is_lewdie(message) and is_bot(message))


# --- Message Responder --- #
async def message_responder(message):
    await owo_checker(message)
    await bot_compliment_checker(message)


# --- owo checker --- #
async def owo_checker(message):
    try:
        msg = message.content
        owo_regex = "((?<!\<)([o|u|O|U|0-9|\-|\.|\;|\^][w|u|v|W|V|o|O|_|\-|\^|A|\.|0-9][o|u|O|U|0-9|\-|\.|\;|\^])(?![\w\s]*[\>]))"
        url_found = regex.findall("http[^\s]*", msg)
        if url_found:
            msg = str(msg).replace(url_found[0], "")
        print(msg)
        match = regex.findall(owo_regex, msg)
        if match:
            match = match[0][0]
            if not match.isnumeric() and match not in blacklist and not bool(regex.search(r"\d\.\d", msg)):
                await message.channel.send(match)
    except:
        this = True


# --- Bot Compliments --- #
async def bot_compliment_checker(message):
    if 'good bot' in str.lower(message.content):
        await message.channel.send("OwO you're welcome!! >W<")
    if 'bad bot' in str.lower(message.content):
        await message.channel.send('Sowy ;^;')


# --- RUNTIME --- #
@client.event
async def on_ready():
    print('logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----')
    await client.change_presence(activity=discord.Game(name="UwU my OwO"))


@client.event
async def on_message(message):

    # Assure message is from user
    if not is_user(message):
        return

    # Determine command and respond
    # Stop if message is command
    if message.content.startswith("!"):
        await command_selector(message)
        return

    # Respond to message if contains coded responses
    await message_responder(message)


print("Loaded successfully")
# client.run(str(os.environ.get('TOKEN')))
config = configparser.ConfigParser()
config.read('config.ini')
TOKEN = config.get("Tokens", "TOKEN")

client.run(TOKEN)
