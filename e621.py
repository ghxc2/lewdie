import os

import requests
import random
# URL
urlTemplate = "https://e621.net/posts.json?"
sauceTemplate = "https://e621.net/posts/"
# Headers
# Insures API user-agent
headers = {
    'login': 'ghxc2',
    'User-Agent': str(os.environ.get('E6TOKEN'))
}

# Shorthand for future coding
get = requests.get

print()

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
