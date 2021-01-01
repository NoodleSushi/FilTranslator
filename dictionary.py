import requests
import html
import urllib
import json

DICT_LINK = "https://www.tagaloglessons.com/ajax/reference_guide_search_results.php?keyword="


def translate(word: str = "") -> list:
    JSONstr = requests.get(DICT_LINK+urllib.parse.quote(word)).text
    if JSONstr == "[]":
        return []
    JSONstr = html.unescape(JSONstr)
    JSONstr = JSONstr.replace("***", "")
    JSONstr = JSONstr.replace("^^^", "")
    return json.loads(JSONstr)