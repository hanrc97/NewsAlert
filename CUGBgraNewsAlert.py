from bs4 import BeautifulSoup
import requests
import iMessage
from threading import Timer
from newspaper import Article
import time
import datetime


# 研究生院·最新消息
def getCUGBgranews():
    while True:
        try:
            url = 'https://www1.cugb.edu.cn/graduate.action'
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:71.0) Gecko/20100101 Firefox/71.0"}

            requests.adapters.DEFAULT_RETRIES = 15
            requests.packages.urllib3.disable_warnings()
            s = requests.session()
            s.keep_alive = False
            
            response = requests.get(url=url, headers=headers, verify=False).content
            soup = BeautifulSoup(response, 'html.parser')
            links1 = soup.findAll("ul", {"class": "record-list"})[1].findAll('a') #培养与学籍
            links2 = soup.findAll("ul", {"class": "record-list"})[2].findAll('a') #学位与学科
            links3 = soup.findAll("ul", {"class": "box"})[0].findAll('a') #通知与通告
        except Exception as e:
            print("异常发生时间：" + str(datetime.datetime.now()))
            print("异常具体信息：") #打印异常信息至log
            print(e)
        else:
            return links1, links2, links3

def JudgeNews():
    signal = 0
    links1, links2, links3 = getCUGBgranews()  # 调用getCUGBgranews()函数获取信息
    # print(links1) #测试专用，否则请注释
    # print(links2) #测试专用，否则请注释
    # print(links3) #测试专用，否则请注释
    for i, j, k in zip(links1, links2, links3):
        if i.get('title') not in NewsTitle:  # 对新调用函数后获得的links1遍历，
            signal = 1  # 将signal标志为1，方便接下来情况并重新保存NewsTitle
            url = 'https://www1.cugb.edu.cn/' + i.get('href')
            content = Article(url, language='zh')
            content.download()
            content.parse()
            iMessage.send_Message(News=content.text + "\n" + url, sub='📌研院·培养与学籍：📢 ' + i.get('title'))
            # 将不存在于NewsTitle中的新闻发送至指定邮箱
        if j.get('title') not in NewsTitle:
            signal = 1  # 将signal标志为1，方便接下来情况并重新保存NewsTitle
            url = 'https://www1.cugb.edu.cn/' + j.get('href')
            content = Article(url, language='zh')
            content.download()
            content.parse()
            iMessage.send_Message(News=content.text + "\n" + url, sub='📌研院·学科与学位：📢 ' + j.get('title'))
        if k.get('title') not in NewsTitle:
            signal = 1  # 将signal标志为1，方便接下来情况并重新保存NewsTitle
            url = 'https://www1.cugb.edu.cn/' + k.get('href')
            content = Article(url, language='zh')
            content.download()
            content.parse()
            iMessage.send_Message(News=content.text + "\n" + url, sub='📌研院·通知公告：📢 ' + k.get('title'))
            # 将不存在于NewsTitle中的新闻发送至指定邮箱
    if signal == 1:  # 根据前面遍历后的signal信号
        NewsTitle.clear()  # 若为1,则清空NewsTitle列表
        for i, j, k in zip(links1, links2, links3):
            NewsTitle.append(i.get('title'))  # 重新遍历links,将title保存至NewsTitle
            NewsTitle.append(j.get('title'))  # 重新遍历links,将title保存至NewsTitle
            NewsTitle.append(k.get('title'))  # 重新遍历links,将title保存至NewsTitle
    # print(NewsTitle) #测试专用，否则请注释
    t = Timer(300, JudgeNews)  # 每300秒执行一次该函数
    t.start()


if __name__ == "__main__":
    NewsTitle = []  # 程序首次运行，创建一个新闻标题空列表
    links1, links2, links3 = getCUGBgranews() # 调用getCUGBgranews()函数获取信息
    for i, j, k in zip(links1, links2, links3):
        NewsTitle.append(i.get('title'))  # 将新闻标题信息全部保存于NewsTitle列表中
        NewsTitle.append(j.get('title'))  # 将新闻标题信息全部保存于NewsTitle列表中
        NewsTitle.append(k.get('title'))  # 将新闻标题信息全部保存于NewsTitle列表中
    print("程序监测启动时间: " + str(datetime.datetime.now()))
    print("【日志模式：异常】")
    print(NewsTitle) #测试专用，否则请注释
    time.sleep(60)  # 主线程暂停60秒后再执行
    JudgeNews()  # 调用JudgeNews()函数判断是否为最新新闻

    # iMessage.send_Message(News=news, sub='地大研院今日要闻' + date)
    # linux系统下程序后台运行并logging命令：
    # nohup python3 -u CUGBgraNewsAlert.py > CUGBgraout.log 2>&1 &