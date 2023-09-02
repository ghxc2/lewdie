import discord
import regex
import e621
import configparser
import saucenao


intents = discord.Intents.all()
client = discord.Client(intents=intents)
de = discord.Embed()
blacklist = {"...", "0.0", "4.4", "7.7", "9.9"}
commands = "!help\n" \
           "--- e621 Commands ---\n" \
           "!e6tag\n" \
           "!e6new\n" \
           "!e6fav\n" \
           "--- Misc Commmands ---\n" \
           "!sauce\n" \
           "!icon\n"


# Start of functions
async def command_selector(message):
    which_command = message.content.split(" ")[0]
    match which_command:
        case "!e6new":
            await e6new(message)
        case "!e6tag":
            await e6tag(message)
        case "!e6fav":
            await e6fav(message)
        case "!lewdieSTOP":
            await stop(message)
        case "!sauce":
            await sauce(message)
        case "!icon":
            await icon(message)


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
        response_list.append("Sauce: " + saucenao.getSauce(message.content[7:]))
    except:
        response_list.append("Couldn find it, sowwy >>")
    await message.channel.send("\n".join(response_list))


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
