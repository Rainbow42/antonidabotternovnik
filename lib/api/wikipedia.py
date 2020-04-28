import requests
import re
import json
import requests

session = requests.Session()

URL = "https://en.wikipedia.org/w/api.php"


def params_search(SEARCHPAGE):
     params = {
        'action':"query",
        'list':"search",
        'srsearch': searchpapage,
        'format':"json"
     }
     return  params

def get_updates(PARAMS):
    url = session.get(url=URL, params=params)
    data = url.json()
    return data

def html_remove(html):
    # html = DATA['query']['search'][0]['snippet']
    p = re.compile(r'<.*?>')
    return str(p.sub('', html))


def main_wikipedia(searchpapage:str):
    params =params_search(searchpapage)
    data = get_updates(params)
    with open('updets.json','w')as f:
        json.dump(DATA,f)
    try:
        if searchpapage in data['query']['search'][0]['title']:
            #print(html_remove(DATA) )
            html = data['query']['search'][0]['snippet']
            title = data['query']['search'][1]['title']
            html1 = data['query']['search'][1]['snippet']
            return str("Ваша страница поиска' {} ' существует в английской Википедии.\n  {}.\n  {} - {}.".format(searchpapage,
                                                                                                html_remove(html),
                                                                                                title,html_remove(html1)))
        else:
            return str("Ваш запрос отсутвует в Википедии.")
    except:
        return str ("Ошибка поиска, запрос неверный.")
