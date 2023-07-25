import os
import requests
import random
import configparser
# URL
urlTemplate = "https://e621.net/posts.json?"
sauceTemplate = "https://e621.net/posts/"
config = configparser.ConfigParser()
config.read('config.ini')
# Headers
# Insures API user-agent
headers = {
    'login': 'ghxc2',
    'User-Agent': str(config.get("Tokens", "E6TOKEN"))
}

# Shorthand for future coding
get = requests.get


def getNewestImageByTags(tag: str):
    url = urlTemplate + "tags=" + tag + ";limit=1"
    results = get(url, headers=headers).json()
    post = getRandPost(results)
    return post['file']['url'], sauceBuilder(post["id"], tags=tag)


def getImageNewest():
    url = urlTemplate + ";limit=1"
    results = get(url, headers=headers).json()
    post = getRandPost(results)
    return post["file"]["url"], sauceBuilder(post["id"])


def getImagesByTags(tag: str):
    url = urlTemplate + "tags=" + tag + ";limit=100"
    results = get(url, headers=headers).json()
    post = getRandPost(results)
    return post['file']['url'], sauceBuilder(post["id"], tags=tag)

def sauceBuilder(id, tags=""):
    if tags == "":
        return sauceTemplate + str(id)
    else:
        return sauceTemplate + str(id) + "?q=" + tags

def getRandPost(posts):
    return random.choice(posts["posts"])

eval(compile())