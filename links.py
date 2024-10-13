"""if i give a page title, I want the 5 most clicked links from that page"""
"""I want a chronological order of all links which are of dates in a dict form of {"date":["title","url"]}"""
import wikipediaapi
import requests
from datetime import datetime, timedelta
import random
wiki_wiki=wikipediaapi.Wikipedia('content (unnatisaraswat007@gmail.com)','en')
#first thing is there is a list of items in the notion page

def links_list(page):
    l=[]
    links=page.links
    for title in sorted(links.keys()):
        page=wiki_wiki.page(title)
        l.append(f"{title}")
    return l


def get_pageviews(page_title, start_date, end_date):
    headers = {
    "User-Agent": "content (unnatisaraswat007@gmail.com)",
}

    url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia.org/all-access/all-agents/{page_title}/daily/{start_date}/{end_date}"
    response=requests.get(url,headers=headers)
    if response.status_code==200:
        data=response.json()
        #print(data)
        views=sum(item['views'] for item in data['items'])
        return views
    else:
        print(f"Error fetching data for {page_title}: {response.status_code}")
def ordered_titles(title_main_page,first_few,func=1):
    l=links_list(wiki_wiki.page(title_main_page))
    random.shuffle(l)
    #print(l[:first_few])
    end_date = datetime.now()
    start_date = end_date - timedelta(days=5 * 365)
    start_date_str = start_date.strftime("%Y%m%d")  
    end_date_str = end_date.strftime("%Y%m%d")  
    dict={}
    for i in l[:first_few]:
        dict[i]=get_pageviews(i,start_date_str,end_date_str)
    sorted_views=sorted(dict.items(),key=lambda x: x[1],reverse=True)
    if func==1:
        return sorted_views[:5]
    else:
        return sorted_views[-5:]
if __name__ == "__main__":
    title_main_page=input("enter the title ")
    func=int(input("enter function(1 or 2)"))
    first_few=int(input("enter first_few"))
    print(ordered_titles(title_main_page,first_few,func))

    

    