import random
import subprocess
import sys
import discord
import regex
import e621
import configparser
import saucenao


intents = discord.Intents.all()
client = discord.Client(intents=intents)
de = discord.Embed()
blacklist = {"...", "0.0", "4.4", "7.7", "9.9"}
commands = "```!help\n" \
           "--- e621 Commands ---\n" \
           "!e6tag\n" \
           "!e6new\n" \
           "!e6fav\n" \
           "--- Misc Commmands ---\n" \
           "!sauce\n" \
           "!icon\n```" \
           "!version\n" \
           "--- ADMIN COMMANDS ---\n" \
           "!lewdieUPDATE\n" \
           "!lewdieSTOP\n"


# Start of functions
async def command_selector(message):
    which_command = message.content.split(" ")[0]
    if which_command == "!e6new":
        await e6new(message)
    elif which_command == "!e6tag":
        await e6tag(message)
    elif which_command == "!e6fav":
        await e6fav(message)
    elif which_command == "!lewdieSTOP":
        await stop(message)
    elif which_command == "!sauce":
        await sauce(message)
    elif which_command == "!icon":
        await icon(message)
    elif which_command == "!help":
        await help_command(message)
    elif which_command == "!lewdieUPDATE":
        await update(message)
    elif which_command == "!version":
        await version(message)


# ---e6 Commands--- #
def get_e6_tags(message):
    tags = message.content.split(" ")
    tags = tags[1:]
    tags_str = "+".join(tags)
    return tags_str


async def e6new(message):
    response_list = ["The hottest sauce of the press! ;3"]
    if message.content == "!e6new":
        links = e621.get_image_newest()
        response_list.append("Sauce: <" + links[1] + ">")
        response_list.append("" + links[0])
    else:
        tags = message.content.split(" ")
        tags = tags[1:]
        links = e621.get_newest_image_by_tags("+".join(tags))
        response_list.append("Jus what you wan: " + " ".join(tags))
        response_list.append("Sauce: <" + links[1] + ">")
        response_list.append("" + links[0])

    await message.channel.send("\n".join(response_list))


async def e6tag(message):
    tags_str = get_e6_tags(message)
    response_list = ['ohh~! coming up! Tags: ' + tags_str.replace("+", " ")]
    try:
        links = e621.get_images_by_tags(tags_str)
        if "latias" in message.content:
            response_list.append('Me~? >//w//<')
        response_list.append("Sauce: <" + links[1] + ">")
        if links[0] != "None":
            response_list.append(links[0])
        else:
            response_list.append("Uh ohh! no link?")
    except:
        response_list.append("None cri sowy ;-;")
    await message.channel.send("\n".join(response_list))


async def e6fav(message):
    tags_str = get_e6_tags(message)
    response_list = ["ohh~! You wan best? You get best~ Tags : "]
    try:
        links = e621.get_best_post(tags_str)
        if "latias" in message.content:
            response_list.append('Me at my best~? >///<')
        response_list.append("Sauce: <" + links[1] + ">")
        if links[0] != "None":
            response_list.append(links[0])
        else:
            response_list.append("Uh ohh! no link?")
    except:
        response_list.append("None cri sowy ;-;")
    await message.channel.send("\n".join(response_list))


# ---Sauce--- #
async def sauce(message):
    response_list = ["Saucey comin up!"]
    try:
        response_list.append("Sauce: " + saucenao.get_sauce(message.content[7:]))
    except:
        response_list.append("Couldn find it, sowwy >>")
    await message.channel.send("\n".join(response_list))


# -- Icons! -- #
async def icon(message):
    if message.content == "!icon":
        await message.channel.send(message.author.avatar.url)
    else:
        await message.channel.send(message.mentions[0].avatar.url)


# --- ADMIN COMMANDS --- #
async def stop(message):
    if is_admin(message):
        await message.channel.send('Okey! Goodnight')
        exit()


async def update(message):
    if is_admin(message):
        await message.channel.send("Updating!")
        subprocess.run(["./update.sh"])


# --- Help Command --- #
async def help_command(message):
    await message.channel.send(commands)


# --- Bot Checker --- #
def is_bot(message):
    return message.author.bot


def is_lewdie(message):
    return message.author == client.user


def is_user(message):
    return not (is_lewdie(message) and is_bot(message))


# --- ADMIN CHECKER --- #
def is_admin(message):
    if "ghxc2" in format(message.author):
        return True
    else:
        return False


# --- Message Responder --- #
async def message_responder(message):
    await owo_checker(message)
    await bot_compliment_checker(message)


async def generic_responder(message):
    await boo_sender(message)

# --- owo checker --- #
async def owo_checker(message):
    try:
        msg = message.content
        owo_regex = "((?<!\<)([o|u|O|U|0-9|\-|\.|\;|\^][w|u|v|W|V|o|O|_|\-|\^|A|\.|0-9][o|u|O|U|0-9|\-|\.|\;|\^])(?![\w\s]*[\>]))"
        url_found = regex.findall("http[^\s]*", msg)
        if url_found:
            msg = str(msg).replace(url_found[0], "")
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


# --- MISC --- #
async def version(message):
    v = sys.version_info
    await message.channel.send("Python: v" + str(v[0]) + "." + str(v[1]) + "." + str(v[2]))


async def boo_sender(message):
    rand = random.randrange(1, 100)
    if rand == 1:
        await message.channel.send("Boo~ òwó")


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


    # Generic responses
    await generic_responder(message)

print("Loaded successfully")
# client.run(str(os.environ.get('TOKEN')))
config = configparser.ConfigParser()
config.read('config.ini')
TOKEN = config.get("Tokens", "TOKEN")

client.run(TOKEN)
