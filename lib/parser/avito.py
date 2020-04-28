import requests
import re
import csv
from bs4 import BeautifulSoup


#name='asus'
def get_html(url):
    r = requests.get(url)
    return r.text

def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('div', class_='pagination-pages')
    try:
        p = pages.find_all('a', 'pagination-page')[-1].get('href')
        print(re.findall('(\d+)', str(pages)))
        total_pages = p.sub(r'\D', '', p)
       # total_pages = (re.sub(r'\D', '', str(pages)))
        a = []
        a.append(total_pages)
        print(a)
    except:return False
    return a

def write_csv(data):
    with open('avito.csv','w') as f:
        writer = csv.writer(f)
        writer.writerow((data['title'],
                       data['price'],
                       data['street'],
                       data['url']))
        #print((data['title'], data['price'], data['street'], data['url']))


def get_page_data(html):
    soup = BeautifulSoup(html,'lxml')
    try:
        ads = soup.find('div',class_='catalog-list').find_all('div',class_="item_table")
        for ad in ads:
            try:
                title = ad.find('div',class_='description').find("h3").text.strip()
            except:
                title =''
            try:
                url = 'https://www.avito.ru ' + ad.find('div',class_='description').find("h3").find("a").get("href")
            except:
                url=''
            try:
                price = ad.find('div',class_="about").text.strip()
            except:
                price = ''
            try:
                street = ad.find('div',class_='data').find_all('p')[-1].text.strip()
            except:
                metro = " "
            data = {'title':title,
                  'price':price,
                  'street':street,
                   'url':url}
            #print(data)
            write_csv(data)
    except:
        with open('avito.csv', 'w') as f:
            f.write("Search error! This model may be missing, try entering a query later or select a different model.")



def avito(name):

    url = 'https://www.avito.ru/saransk/noutbuki?p=1&q=' + name
    base_url = 'https://www.avito.ru/saransk/noutbuki?'
    page_part = 'p='
    query_part = '&q='+name
    #total_pages  = get_total_pages(get_total_pages(get_html(url)))
    total_pages =2
    for x in range(1,total_pages):
         url_gen = base_url + page_part + str(x) + query_part
         html = get_html(url_gen)
         get_page_data(html)
