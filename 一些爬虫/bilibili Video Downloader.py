import urllib.request as ur
import os
import json
av = input('av号：')
res = ur.urlopen('https://api.bilibili.com/x/web-interface/view?aid='+str(av))
html = res.read().decode('utf-8')
html = json.loads(html)
print('若视频只有一P则填入1')
p = input('p：')
try:cid = html['data']['pages'][int(p)-1]['cid']
except IndexError:
    print('没有这一P！')
    os.system('pause')
except KeyError:
    print('av号错了！')
    os.system('pause')
else:
    title = html['data']['title']
    res = ur.urlopen('https://api.bilibili.com/x/player/playurl?avid='+str(av)+'&cid='+str(cid)+'&otype=json')
    html = res.read()
    html = json.loads(html)
    url = html['data']['durl'][0]['url']
    header = {}
    header['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36i/537.36'
    header['Referer'] = 'https://www.bilibili.com/video/$avStr'
    res = ur.Request(url,headers=header)
    res = ur.urlopen(res)
    print('视频为：'+title+',是否下载？')
    download = input('输入1下载，否则退出程序')
    if download=='1':
        name = input('请输入文件名（不需要拓展名）')
        print('正在下载中...')
        html = res.read()
        print('正在写入文件...')
        with open(str(name)+'.flv','wb') as f:
            f.write(html)
        print('下载成功！\n文件位置与本程序位置相同')
    os.system('pause')
