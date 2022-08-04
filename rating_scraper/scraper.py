import requests
from bs4 import BeautifulSoup as bs
import json, re, concurrent.futures
    
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

def scrap_imdb(title, date, expr):
    url = 'https://www.imdb.com/find?q=' + title + ' ' + date
    page = requests.get(url, headers)
    if page.status_code == 200:
        soup = bs(page.text, 'html')
        table = soup.find("table", {"class": "findList"})
        for row in table.findAll("tr"):
            cell = row.findAll("td")[1]
            # print(cell.contents)
            link_n_title = cell.contents[1]
            desc = cell.contents[2].text
            match_res = re.fullmatch(expr, desc)
            if link_n_title.string == title and match_res:
                return fetch_imdb_rating(link_n_title['href']) 
        return "?.?"
    else:
        print("ERROR: scrap_imdb status code: " + str(page.status_code))
        return "?.?"

def scrap_rating(content):
    date, expr = scrap_date(content['id'])
    date = "" if date is None else (" " + date)
    if expr:
        rating = scrap_imdb(content['title'], date, expr)
    print(rating)
    rating = rating if rating != "?.?" else fetch_rating_google(content['title'] + date)
    rating = rating if len(rating) == 3 else (rating+".0")
    # print(rating)
    return rating
  
#https://www.netflix.com/title/70143836
#type="application/ld+json". 

def scrap_date(id):
    url = 'https://www.netflix.com/title/' + id
    page = requests.get(url, headers)
    if page.status_code == 200:
        soup = bs(page.text, 'html')
        res = soup.find("div", {"class": "title-info-metadata-wrapper"})
        date = res.find("span", {"data-uia": "item-year"}).string
        genre = json.loads(soup.find("script", {"type": "application/ld+json"}).text)["@type"]
        if genre == "TVSeries":
            expr = " (\([I]+\) )?\("+date+"\) \(TV Series\) "
        else:
            expr = " (\([I]+\) )?\("+date+"\) "
        return date, expr
    else:
        print("ERROR: sscrap_date status code: " + str(page.status_code))
        return None, None  

def fetch_imdb_rating(title_id):
    url = 'https://www.imdb.com' + title_id
    page = requests.get(url, headers)
    if page.status_code == 200:
        soup = bs(page.text, 'html')
        res = soup.find("script", {"type": "application/ld+json"})
        data = json.loads(res.text)
        return str(data["aggregateRating"]["ratingValue"])
    else:
        print("ERROR: fetch_imdb_rating status code: " + str(page.status_code))
        return "?.?" 

def fetch_rating_google(search):
    url = "https://www.google.com/search?q=" + search
    page = requests.get(url, headers)
    if page.status_code == 200:
        soup = bs(page.text, "html")
        res = soup.find(text=re.compile("([0-9]{1})(\.[0-9]{1})?(\/10)"))
        res = "?.?/?" if res is None else res.text
        rating = res.split('/')[0]
        return rating
    else:
        print("ERROR: fetch_rating_google status code: " + page.status_code)
        return "?.?"


content = {}
content["title"] = "Business Proposal"
content["id"] = "81509440"
print(scrap_rating(content))