from bs4 import BeautifulSoup
import requests
from datetime import datetime

from classes.competition import Competition

def readSlocomps(pages = 1):
    """Skrap data from SloComps.

    Returns:
        list: List of competitions.
    """
    url = 'https://comps.sffa.org'
    
    # Find page range.
    page_response = requests.get(url)
    page = BeautifulSoup(page_response.content, "html.parser")
    page_range = int(page.find_all(class_ = 'pager-current')[0].text.strip().split(' of ')[1])
    
    # read from following urls
    urls = [url if (i == 0) else url + "/?page=%d" % i for i in range(0, page_range + 1)]
    
    competitions = []
    for url in urls:
        page_response = requests.get(url)
        page = BeautifulSoup(page_response.content, "html.parser")
        data = page.find_all(class_ = "view-nc-calendar")
        
        for comps in data:
            temp = comps.find_all(class_ = "nc-postcard-left-wrap")
    
            for comp in temp:
                C = Competition()
                
                comp_name = comp.find("h4").string
                C.SetName(comp_name)
                
                comp_url = url + comp.find("h4").find("a").get("href")
                C.SetUrl(comp_url)
                
                comp_location = comp.find_all(class_ = "subi")[2].string.replace(" ", "")
                C.SetLocation(comp_location)
                
                date = comp.find_all(class_ = "date-display-single")[0].string.split(".")
                comp_start = datetime.strptime(date[0] + "-" + date[1] + "-" + date[2], '%d-%m-%Y')
                C.SetStartDate(comp_start)
                
                date = comp.find_all(class_ = "date-display-single")[1].string.split(".")
                comp_end = datetime.strptime(date[0] + "-" + date[1] + "-" + date[2], '%d-%m-%Y')
                C.SetEndDate(comp_end)
                
                C.SetSport(0)
    
                competitions.append(C)

    return competitions
