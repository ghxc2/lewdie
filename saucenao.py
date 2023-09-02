import requests
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# Header info

api_key = config.get("Tokens", "SAUCENAOTOKEN")
enable_rename = False
min_sim = '90!'
url = 'http://saucenao.com/search.php?output_type=2&minsim='+min_sim+'&api_key='+api_key
get = requests.get


def get_sauce(img: str):
    try:
        global url
        url += '&url=' + img
        results = get(url).json()
        result = results['results'][0]
        # e621 priority
        # Might throw error unsure
        try:
            for result_url in result['data']['ext_urls']:
                if "e621" in result_url:
                    return result_url
        except:
            x = 1

        try:
            return result['data']['source']
        except:
            return result['data']['ext_urls'][0]
    except:
        raise Exception("No results found")