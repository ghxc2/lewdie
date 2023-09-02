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


def get_newest_image_by_tags(tag: str):
    url = urlTemplate + "tags=" + tag + ";limit=1"
    results = get(url, headers=headers).json()
    post = get_rand_post(results)
    return post['file']['url'], sauce_builder(post["id"], tags=tag)


def get_image_newest():
    url = urlTemplate + ";limit=1"
    results = get(url, headers=headers).json()
    post = get_rand_post(results)
    return post["file"]["url"], sauce_builder(post["id"])


def get_images_by_tags(tag: str):
    url = urlTemplate + "tags=" + tag + ";limit=100"
    results = get(url, headers=headers).json()
    post = get_rand_post(results)
    return post['file']['url'], sauce_builder(post["id"], tags=tag)


def sauce_builder(id_str, tags=""):
    if tags == "":
        return sauceTemplate + str(id_str)
    else:
        return sauceTemplate + str(id_str) + "?q=" + tags


def get_rand_post(posts):
    return random.choice(posts["posts"])


def get_best_post(tag: str):
    return get_newest_image_by_tags(tag + "+order:favcount")
