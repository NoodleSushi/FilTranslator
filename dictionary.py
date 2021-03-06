import requests
import html
import urllib.parse
import json


class Dictionary:
    DICT_LINK = "https://www.tagaloglessons.com/ajax/reference_guide_search_results.php?keyword="
    
    @staticmethod
    def translate(word: str = "") -> list:
        json_str: str = requests.get(Dictionary.DICT_LINK+urllib.parse.quote(word)).text
        json_str = html.unescape(json_str).replace("***", "").replace("^^^", "")
        return json.loads(json_str)
