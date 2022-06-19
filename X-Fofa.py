# -*- coding: utf-8 -*-
from array import array
import base64,os,requests
import argparse,sys
import json,datetime

email = ''
key = ''

full = 'false' #搜索结果是否包含一年前的，fofa的默认搜索结果为一年内数据

def remove_duplicates(output):
    print("[+] 正在去重...")
    f_read=open('log.log','r',encoding='utf-8')     #将需要去除重复值的txt文本重命名text.txt
    f_write=open(output,'w',encoding='utf-8')  #去除重复值之后，生成新的txt文本 --“去除重复值后的文本.txt”
    data=set()
    for a in [a.strip('\n') for a in list(f_read)]:
        if a not in data:
            f_write.write(a+'\n')
            data.add(a)
    f_read.close()
    f_write.close()
    os.remove('log.log')
    print("[+] 已去重")

def getFofa(page,size,search,output,all):

    global result
    with open('{}'.format('log.log'),'a+') as w:
        if '1' not in all:
            search64 = base64.b64encode(search.encode('utf-8')).decode('utf-8')
            url = "https://fofa.info/api/v1/search/all?email={}&key={}&qbase64={}&page={}&size={}&full={}".format(email,key,search64,page,size,full)
            print("[+] 关键字: {}".format(search))
            print(url)
            response = requests.get(url)
            res = json.loads((response.content).decode('utf-8'))

            for i in range(len(res["results"])):
                url = res["results"][i][0]
                if 'http' not in url:
                    url = 'http://{}'.format(url)
                w.write('{}\n'.format(url))

        if '1' in all:
            size = 10000
            search64 = base64.b64encode(search.encode('utf-8')).decode('utf-8')
            url = "https://fofa.info/api/v1/search/all?email={}&key={}&qbase64={}&page={}&size={}&full={}".format(email,key,search64,page,size,full)
            response = requests.get(url)
            res = json.loads((response.content).decode('utf-8'))

            if res["size"] > 10000:
                if "after=" in search or 'before' in search:
                    print("[+ 设置选项为all,经过查询后发现当前数据超过一万条,请不要在语法中定义时间日期关键词after/before")
                    sys.exit()
                print("[+] 数据超过一万条,防止使用F币,调用日期语法分批获得近90天内的数据:")

                now_time = datetime.datetime.now()
                now_date = now_time.strftime('%Y-%m-%d')

                for i in range(1,92):

                    before_time = now_time + datetime.timedelta(days=-i+2)
                    before_time_nyr = before_time.strftime('%Y-%m-%d')

                    searchTime = search + '&& before = "{}"'.format(before_time_nyr)
                    search64 = base64.b64encode(searchTime.encode('utf-8')).decode('utf-8')
                    url = "https://fofa.info/api/v1/search/all?email={}&key={}&qbase64={}&page={}&size={}&full={}".format(email,key,search64,page,size,full)
                    print("[+] before: {}".format(before_time_nyr))
                    print("[+] 关键字: {}".format(searchTime))
                    print(url)
                    response = requests.get(url)
                    res = json.loads((response.content).decode('utf-8'))
                    for i in range(len(res["results"])):
                        url = res["results"][i][0]
                        if 'http' not in url:
                            url = 'http://{}'.format(url)
                        w.write('{}\n'.format(url))
            else:
                print("[+] 关键字: {}".format(search))
                print(url)
                for i in range(len(res["results"])):
                    url = res["results"][i][0]
                    if 'http' not in url:
                        url = 'http://{}'.format(url)
                    w.write('{}\n'.format(url))
    
    remove_duplicates(output)

    print("File save as  {}/{}".format(os.getcwd(),output))

if __name__ == '__main__':

    parser =argparse.ArgumentParser(description="python3 fofa.py -q 'app = xxx' -p 3 -o 某系统.txt" )
    parser.add_argument('-q', '--query', default='', help="xxx系统")
    parser.add_argument('-p', '--page', default='1', help="100")
    parser.add_argument('-s', '--size', default='10000', help="100")
    parser.add_argument('-all', '--all', default='False', help="100")
    parser.add_argument('-o', '--output', default='result.txt', help="xxx.txt")
    args = parser.parse_args()
    query = ''
    page = ''
    output = ''
    if args.query:
        query = args.query
    if args.page:
        page = args.page
    if args.size:
        size = args.size
    if args.all:
        all = args.all
    if args.output:
        output = args.output
    getFofa(page,size,query,output,all)
