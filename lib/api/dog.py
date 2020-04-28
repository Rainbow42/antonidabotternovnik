import requests
import main
import re
import json
from main import send_message

def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']

    return url
def get_image_url():
    allowed_extension = ['jpg','jpeg','png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url()
        file_extension = re.search("([^.]*)$",url).group(1).lower()
        """with open('updets.json', 'w')as f:
            json.dump(url, f)"""
    return url

def bots(chat_id):
    url = get_image_url()
    send_message(chat_id,url)
