# -*- coding: utf-8 -*-
import base64,os,requests
import argparse
import json,datetime

email = ''
key = ''

full = 'false' #搜索结果是否包含一年前的，fofa的默认搜索结果为一年内数据

def getFofa(page,size,search,output,all):

    global result
    with open('{}'.format(output),'a+') as w:
        if int(all) != 1:
            search64 = base64.b64encode(search.encode('utf-8')).decode('utf-8')
            url = "https://fofa.info/api/v1/search/all?email={}&key={}&qbase64={}&page={}&size={}&full={}".format(email,key,search64,page,size,full)
            print(url)
            response = requests.get(url)
            res = json.loads((response.content).decode('utf-8'))
            for i in range(len(res["results"])):
                url = res["results"][i][0]
                if 'http' not in url:
                    url = 'http://{}'.format(url)
                w.write('{}\n'.format(url))

        if int(all) == 1:

            size = 10000
            search64 = base64.b64encode(search.encode('utf-8')).decode('utf-8')
            url = "https://fofa.info/api/v1/search/all?email={}&key={}&qbase64={}&page={}&size={}&full={}".format(email,key,search64,page,size,full)
            response = requests.get(url)
            res = json.loads((response.content).decode('utf-8'))

            if res["size"] > 10000:
                print("[+] 数据超过一万条,防止使用F币,调用日期语法分批获得近90天内的数据:")
                now_time = datetime.datetime.now()
                now_date = now_time.strftime('%Y-%m-%d')

                for i in range(1,92):
                    after_time = now_time + datetime.timedelta(days=-i)
                    after_time_nyr = after_time.strftime('%Y-%m-%d')

                    before_time = now_time + datetime.timedelta(days=-i+1)
                    before_time_nyr = before_time.strftime('%Y-%m-%d')

                    search64 = search + 'after="{after_time_nyr}" && before = "{before_time_nyr}"'
                    search64 = base64.b64encode(search64.encode('utf-8')).decode('utf-8')
                    url = "https://fofa.info/api/v1/search/all?email={}&key={}&qbase64={}&page={}&size={}&full={}".format(email,key,search64,page,size,full)
                    print("[+] {} -- {}".format(after_time_nyr,before_time_nyr))
                    print(url)
                    response = requests.get(url)
                    res = json.loads((response.content).decode('utf-8'))
                    for i in range(len(res["results"])):
                        url = res["results"][i][0]
                        if 'http' not in url:
                            url = 'http://{}'.format(url)
                        w.write('{}\n'.format(url))
            else:
                print(url)
                for i in range(len(res["results"])):
                    url = res["results"][i][0]
                    if 'http' not in url:
                        url = 'http://{}'.format(url)
                    w.write('{}\n'.format(url))

    print("File save as  {}/{}".format(os.getcwd(),output))

if __name__ == '__main__':

    parser =argparse.ArgumentParser(description="python3 fofa.py -q 'app = xxx' -p 3 -o 某系统.txt" )
    parser.add_argument('-q', '--query', default='', help="xxx系统")
    parser.add_argument('-p', '--page', default='1', help="100")
    parser.add_argument('-s', '--size', default='10000', help="100")
    parser.add_argument('-all', '--all', default='', help="100")
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
