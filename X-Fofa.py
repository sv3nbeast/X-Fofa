#!/usr/bin/python3

import requests,time,random,os,re,sys,base64,urllib.parse
from pyquery import PyQuery as pq

banner = '''
 __   __           ______            __         
 \ \ / /          |  ____|          / _|        
  \ V /   ______  | |__      ___   | |_    __ _ 
   > <   |______| |  __|    / _ \  |  _|  / _` |
  / . \           | |      | (_) | | |   | (_| |
 /_/ \_\          |_|       \___/  |_|    \__,_|
                                                
                                by 斯文
'''

def usera():
    #user_agent 集合
    user_agent_list = [
     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
      'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
     'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
     'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
     'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
     'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
     'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
     'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
     'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
     'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
     'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    ]
    #随机选择一个
    user_agent = random.choice(user_agent_list)
    #传递给header
    headers = { 'User-Agent': user_agent }
    return headers
    
def getPage(cookie,search):

    url='https://classic.fofa.so/result?page=1&qbase64={}'.format(search)
    cookies = {'_fofapro_ars_session':cookie}
    req = requests.get(url=url,headers=usera(),cookies=cookies)
    pageHtml = pq(req.text)
    page = (pageHtml('div.list_jg')).text()
    # page = page.find('')
    
    pattern = re.compile(u'获得 (.*?) 条匹配结果')
    result  = re.findall(pattern,page)
    result  = result[0].replace(',','')

    if (int(result) % 10) >0:
        allPage = int(result) // 10 + 1
    else:
        allPage = int(result) // 10

    return allPage

def start(search,file,cookie):
    
    search=search.encode(encoding="utf-8")
    search=base64.b64encode(search).decode()
    search=urllib.parse.quote(search)
    # if os.path.exists("result.txt"): #删除存在的文件
        # os.remove("result.txt")
    # cookie = input("请输入Fofa的Cookie的_fofapro_ars_session值:")
    allPage = getPage(cookie,search)
    print(banner)
    startPage = input("[+ 搜索结果共有{}页，请输入从第几页开始收集地址(例:5):".format(allPage))
    page      = input("[+ 搜索结果共有{}页，请输入准备收集页数(例:20):".format(allPage))
    endPage   = int(startPage) + int(page)

    cookies={'_fofapro_ars_session':cookie}#这里是你的fofa账号登录后的cookie值
    url='https://fofa.so/result?qbase64={}'.format(search)
    # doc=pq(url)
    print("[+ 正在向{}.txt文件写入结果".format(file))
    with open('%s.txt'%file,'a+',encoding='utf-8') as f:
        for i in range(int(startPage),endPage):
            url='https://classic.fofa.so/result?page={}&qbase64={}'.format(i,search)
            req = requests.get(url=url,headers=usera(),cookies=cookies)
            if '游客使用高级语法' in req.text:
                print('[- Cookie已失效，请重新填写https://classic.fofa.so的Cookie,不是https://fofa.so的Cookie')
                break
            print("[+ 正在读取第{}页   状态码:{}".format(i,req.status_code))
            doc=pq(req.text)

            url=doc('div.results_content .list_mod_t').items()
            title=doc('div.list_mod_c ul').items()

            for u,t in zip(url,title):
                t.find('i').remove()
                relUrl   = u.find('a').eq(0).attr.href
                relTitle = t.find('li').eq(0).text()

                if 'result?qbase64=' in relUrl:
                    relDoc  = pq(u)
                    relIp   = relDoc('.ip-no-url').text()
                    relPort = (relDoc('.span')).find('a').eq(0).text()
                    relUrl  = 'http://{}:{}'.format(str(relIp),relPort)
                if relTitle == '':
                    relTitle = '空'
                print("Url: %s  Title: %s"%(relUrl, relTitle))
                f.write("%s\n"%(relUrl))
                f.flush()

            time.sleep(3)


if __name__ == '__main__':
    if len(sys.argv)==1:
        print(banner)
        print('''Usage:请输入参数\n例如:python X-Fofa.py 'app="Solr"' Solr  94bbbb177c4a564feddb8c7d413d5d61\n例如:python FofaCrawler.py 'app="Solr"'(Fofa搜索语法) Solr(搜索结果文件名)  94bbbb177c4a564feddb8c7d413d5d61(Fofa的Cookie的_fofapro_ars_session值)''')
        sys.exit(0)
        
    search=sys.argv[1]
    file=sys.argv[2]
    cookie = sys.argv[3]
    start(search,file,cookie)


