# -*- coding: utf-8 -*-
import base64,os,requests
import argparse
import json

email = 'xx'
key = 'xx'
full = 'false' #搜索结果是否包含一年前的，fofa的默认搜索结果为一年内数据

def getFofa(page,search,output):

    global result
    
    search = base64.b64encode(search.encode('utf-8')).decode('utf-8')
    url = "https://fofa.so/api/v1/search/all?email={}&key={}&qbase64={}&size={}&full={}".format(email,key,search,page,full)
    response = requests.get(url)
    
    res = json.loads((response.content).decode('utf-8'))

    with open('{}'.format(output),'a+') as w:
        for i in range(len(res["results"])):
            url = res["results"][i][0]
            if 'http' not in url:
                url = 'http://{}'.format(url)
            w.write('{}\n'.format(url))

    print("File save as  {}/{}".format(os.getcwd(),output))


if __name__ == '__main__':

    parser =argparse.ArgumentParser(description="python3 fofa.py -q 'app = xxx' -p 3 -o 某系统.txt" )
    parser.add_argument('-q', '--query', default='', help="xxx系统")
    parser.add_argument('-p', '--page', default='', help="100")
    parser.add_argument('-o', '--output', default='result.txt', help="xxx.txt")
    args = parser.parse_args()
    query = ''
    page = ''
    output = ''
    if args.query:
        query = args.query
    if args.page:
        page = args.page
    if args.output:
        output = args.output
    getFofa(page,query,output)
