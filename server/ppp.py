import requests
import re
from bs4 import BeautifulSoup
import lxml
import time

def get_all_page_links(search_word):
    all_urls = []
    def get_page_links(search_word,pagenum):
        urls = []
        url = 'https://zhidao.baidu.com/search?word=' + search_word + '&ie=gbk&site=-1&sites=0&date=0&pn=' + str(pagenum) + '0'
        usr_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
        headers = {'User-Agent': usr_agent, 'Connection':'close'}
        while True:
            try:
                res = requests.get(url, headers = headers)
            except:
                print("sleep 5 sec")
                time.sleep(5)
                continue
            break
        html = res.text
        soup = BeautifulSoup(html,'lxml')
        result = soup.select('dt[class="dt mb-4 line"] a[class = "ti"]')
        for item in result:
            urls.append((item.get("href")))
        return urls
    for i in range(70):
        print("success"+ " " + str(i) + "\n")
        temp = get_page_links(search_word,i)
        all_urls.extend(temp)
    return all_urls

def get_info_zhidao(zhidao_url):
    url = zhidao_url
    usr_agent = 'Mozilla/5.0 (X11; Linux X86 64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    headers = {'User-Agent': usr_agent, 'Connection':'close'}
    while True:
        try:
            res = requests.get(url, headers = headers)
        except:
            print("sleep 5 sec")
            time.sleep(5)
            continue
        break
    res.encoding = 'GBK'
    html = res.text
    soup = BeautifulSoup(html,'lxml')

    try:
        quest = soup.find('span',class_ = re.compile('con-')).text.strip()
    except:
        print("quest error")
        quest =""
    if (quest == ""):
        try:
            quest = soup.find('span',class_ = 'ask-title').text.strip()
        except:
            return "", ""

    try:
        content = soup.find('div', class_ = re.compile("-text mb-10"))
    except:
        content = None
        print("content error")
    if (content == None):
        return quest, "" 
    content = content.text.strip()
    temp = content.split()
    lenth = len(temp)
    ansr = ""
    for i in range(1,lenth):
        ansr += temp[i]
    req_ans = (quest, ansr)
    return quest, ansr

def produce_urls(search_word):
    all_urls = get_all_page_links(search_word)
    #f = open("./server/data/urls.txt","w") 
    f = open("urls.txt","w") 
    for url in all_urls:
        f.writelines(url+"\n")
        print(url)
    f.close()
    print("links ready!")

def produce_dbdata(search_word):
    produce_urls(search_word)
    result =[]
    f1 = open("./server/data/problems.txt", "w")
    #f1 = open("problems.txt","w")
    f2 = open("./server/data/ansr.txt", "w")
    #f2 = open("ansr.txt","w")
    f3 = open("./server/data/prob_ans.txt", "w")
    #f3 = open("prob_ans.txt","w")
    f4 = open("./server/data/urls.txt", "r")
    #f4 = open("urls.txt","r")
    all_urls = [line.strip() for line in f4.readlines()]
    cnt = 0
    for url in all_urls:
        if (url.find("zhidao") != -1):
            print(cnt, "\t", url)
            quest, ansr = get_info_zhidao(url)
            if not(quest == "" and ansr == ""):
                result.append((url, quest, ansr))
                f1.writelines(quest.encode("gbk", "ignore").decode(
                    "gbk", "ignore") + "\n")
                f2.writelines(ansr.encode("gbk", "ignore").decode(
                    "gbk", "ignore") + "\n")
                f3.writelines((quest + " " + ansr).encode("gbk",
                                                          "ignore").decode("gbk", "ignore") + "\n")

                cnt += 1
    f1.close()
    f2.close()
    f3.close()
    print("complete!")
    return result


if __name__ == "__main__":
    produce_dbdata("新型冠状肺炎")
