import urllib.request as ur
cmd = '2'
while cmd!='1':
    print('注意：不支持只能试听片段的曲目')
    wid = input('id:')
    print('')
    url = 'https://api.fczbl.vip/163/?type=url&id='+ str(wid)
    
    response = ur.Request(url)
    response = ur.urlopen(response)
    html = response.read()
    name = input('文件名：')
    print('')
    with open(str(name)+'.mp3','wb')as f:
        f.write(html)
    cmd = input('输入1退出')

