import urllib.request
import urllib.parse
import json

while 1:
    contest=str(input('请输入翻译内容,输入-1退出\n'))

    if contest=='-1':
        break
    
    url='http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'

    head={}
    head['User_Agent']='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    
    data={}
    data['i']=contest
    data['from']= 'AUTO'
    data['to']= 'AUTO'
    data['smartresult']='dict'
    data['client']='fanyideskweb'
    data['salt']='15656811332752'
    data['sign']='51763d2d84d4ce9e2c32e3af6fcda1c0'
    data['ts']='1565681133275'
    data['bv']='48b19e5b92693b3779082041b5e5429b'
    data['doctype']='json'
    data['version']='2.1'
    data['keyfrom']='fanyi.web'
    data['action']='FY_BY_CLICKBUTTION'
    data=urllib.parse.urlencode(data).encode('utf-8')

    response = urllib.request.Request(url,data,head)
    #response.add_header('User_Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36')
    response = urllib.request.urlopen(response)
    html=response.read().decode('utf-8')

    print(json.loads(html)['translateResult'][0][0]['tgt'])
    print('')
