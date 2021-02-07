from bs4 import BeautifulSoup
import requests
import iMessage
from threading import Timer
import time

#研究生院·招生
def getCUGBznews():
    url = 'https://www1.cugb.edu.cn/graduate.action'
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:71.0) Gecko/20100101 Firefox/71.0"}

    requests.packages.urllib3.disable_warnings()
    response = requests.get(url=url,headers=headers,verify=False).content
    soup = BeautifulSoup(response, 'html.parser')
    links = soup.findAll("ul", {"class": "record-list"})[0].findAll('a')
    return SortNews(links, 1)

#研究生院·培养-学籍
def getCUGBgnews():
    url = 'https://www1.cugb.edu.cn/graduate.action'
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:71.0) Gecko/20100101 Firefox/71.0"}

    requests.packages.urllib3.disable_warnings()
    response = requests.get(url=url,headers=headers,verify=False).content
    soup = BeautifulSoup(response, 'html.parser')
    links = soup.findAll("ul", {"class": "record-list"})[1].findAll('a')
    return SortNews(links, 2)

#研究生院·学位-学科
def getCUGBdnews():
    url = 'https://www1.cugb.edu.cn/graduate.action'
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:71.0) Gecko/20100101 Firefox/71.0"}

    requests.packages.urllib3.disable_warnings()
    response = requests.get(url=url,headers=headers,verify=False).content
    soup = BeautifulSoup(response, 'html.parser')
    links = soup.findAll("ul", {"class": "record-list"})[2].findAll('a')
    return SortNews(links, 3)

#研究生院·通知公告
def getCUGBnotice():
    url = 'https://www1.cugb.edu.cn/graduate.action'
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:71.0) Gecko/20100101 Firefox/71.0"}

    requests.packages.urllib3.disable_warnings()
    response = requests.get(url=url,headers=headers,verify=False).content
    soup = BeautifulSoup(response, 'html.parser')
    links = soup.findAll("ul", {"class": "box"})[0].findAll('a')
    return SortNews(links, 4)

#水环通知
def getSWREnotice():
    url = 'http://www.swre.cugb.edu.cn'
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:71.0) Gecko/20100101 Firefox/71.0"}

    response = requests.get(url=url,headers=headers).content
    soup = BeautifulSoup(response, 'html.parser')
    links = soup.findAll("div", {"class": "main_rt_lt_bg"})[1].findAll('a')
    return SortNews(links, 5)


#新闻整理合并
def SortNews(links, index):
    No = 0
    news = ""
    if index == 1:
        news = "\n【研院通知·招生】" + "\n"
        for i in links:
            No = No + 1
            news =  news + "\n" + str(No) + "、" + i.get('title') + \
                    "  ☛" + "https://www1.cugb.edu.cn/" + i.get('href')
    elif index == 2:
        news = "\n\n【研院通知·培养与学籍】" + "\n"
        for i in links:
            No = No + 1
            news =  news + "\n" + str(No) + "、" + i.get('title') + \
                    "  ☛" + "https://www1.cugb.edu.cn/" + i.get('href')
    elif index == 3:
        news = "\n\n【研院通知·学位与学科】" + "\n"
        for i in links:
            No = No + 1
            news =  news + "\n" + str(No) + "、" + i.get('title') + \
                    "  ☛" + "https://www1.cugb.edu.cn/" + i.get('href')
    elif index == 4:
        news = "\n\n【研院通知·通知公告】" + "\n"
        for i in links:
            No = No + 1
            news =  news + "\n" + str(No) + "、" + i.get('title') + \
                    "  ☛" + "https://www1.cugb.edu.cn/" + i.get('href')
    elif index == 5:
        news = "\n\n【水环通知】" + "\n"
        for i in links:
            No = No + 1
            news =  news + "\n" + str(No) + "、" + i.get('title') + \
                    "  ☛" + "http://www.swre.cugb.edu.cn/" + i.get('href')
    return news

if __name__ == "__main__":
    CUGBznews = getCUGBznews()
    CUGBgnews = getCUGBgnews()
    CUGBdnews = getCUGBdnews()
    CUGBnotice = getCUGBnotice()
    SWREnotice = getSWREnotice()
    news = CUGBznews + CUGBgnews + CUGBdnews + CUGBnotice + SWREnotice
    date = time.strftime("(%Y%m%d)", time.localtime(time.time()))
    iMessage.send_Message(News=news, sub='地大研院今日要闻' + date)