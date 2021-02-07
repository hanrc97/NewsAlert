from bs4 import BeautifulSoup
import requests
import iMessage
from threading import Timer
from newspaper import Article
import time
import datetime


# 水环学院·通知公告
def getSWREgnews():
    while True:
        try:
            url = 'http://www.swre.cugb.edu.cn'
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:71.0) Gecko/20100101 Firefox/71.0"}

            response = requests.get(url=url, headers=headers).content
            soup = BeautifulSoup(response, 'html.parser')
            links = soup.findAll("div", {"class": "main_rt_lt_bg"})[1].findAll('a')
        except Exception as e:
            print(e) #打印异常信息至log
        else:
            return links


def JudgeNews():
    signal = 0
    links = getSWREgnews()  # 调用getSWREnews()函数获取信息
    for i in links:
        if i.get('title') not in NewsTitle:  # 对新调用函数后获得的links遍历，
            signal = 1  # 将signal标志为1，方便接下来情况并重新保存NewsTitle
            url = 'http://www.swre.cugb.edu.cn/' + i.get('href')
            content = Article(url, language='zh')
            content.download()
            content.parse()
            iMessage.send_Message(News=content.text + "\n" + url, sub='水环通告：' + i.get('title'))
            # 将不存在于NewsTitle中的新闻发送至指定邮箱
    if signal == 1:  # 根据前面遍历后的signal信号
        NewsTitle.clear()  # 若为1,则清空NewsTitle列表
        for i in links:
            NewsTitle.append(i.get('title'))  # 重新遍历links,将title保存至NewsTitle
    # print(NewsTitle) 测试专用，否则请注释
    t = Timer(300, JudgeNews)  # 每300秒执行一次该函数
    t.start()
    print(NewsTitle)


if __name__ == "__main__":
    NewsTitle = []  # 程序首次运行，创建一个新闻标题空列表
    links = getSWREgnews()
    for i in links:
        NewsTitle.append(i.get('title'))  # 将新闻标题信息全部保存于NewsTitle列表中
    print("程序监测启动时间: " + str(datetime.datetime.now()))
    print("【日志模式：异常】")
    print(NewsTitle)
    time.sleep(3)  # 主线程暂停60秒后再执行
    JudgeNews()  # 调用JudgeNews()函数判断是否为最新新闻

    # iMessage.send_Message(News=news, sub='地大研院今日要闻' + date)
    # linux系统下程序后台运行并logging命令：
    # nohup python3 -u SWRENewsAlert.py > SWREout.log 2>&1 &
