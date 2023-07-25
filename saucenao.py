import os
import this
import time

import requests
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# Header info

api_key=config.get("Tokens", "SAUCENAOTOKEN")
EnableRename=False
minsim='90!'
url = 'http://saucenao.com/search.php?output_type=2&minsim='+minsim+'&api_key='+api_key
get = requests.get

def getSauce(img: str):
    try:
        global url
        url += '&url=' + img
        results = get(url).json()
        result = results['results'][0]
        # e621 priority
        # Might throw error unsure
        try:
            for resulturl in result['data']['ext_urls']:
                if "e621" in resulturl:
                    return resulturl
        except:
            x = 1

        try:
            return result['data']['source']
        except:
            return result['data']['ext_urls'][0]
    except:
        raise Exception("No results found")

