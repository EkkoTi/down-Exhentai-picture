# import urllib
import re
import sys
import io
# import urllib.request, urllib.parse, urllib.error
# import http.cookiejar
from bs4 import BeautifulSoup
import requests
import os
import itchat
from itchat.content import *

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, errors = 'replace', line_buffering = True) # print（打印中文）
values = {'ipb_member_id':'1912783', 'ipb_pass_hash':'64071826da4baa6d6b2cd210119186a9', 'yay': 'louder', 'igneous': '9a915a161', 'lv': '1486572840-1486575927', 'uconfig': 'dm_t'}


'''---------------创建文件夹名字-----------------'''
def creatfile(filename):
    file_chars=['/','|','*','?','<','>',':']#检查文件夹字符串
    for file_char in file_chars:
        filename=filename.replace(file_char,'-')

    path = "C:/Users/Administrator/Desktop/微信公众号/ex/ex/%s" % (filename)
    if  os.path.isfile(path)==False:
        os.mkdir(path)





# cookie_filename = 'cookie.txt'
# cookie = http.cookiejar.MozillaCookieJar(cookie_filename)
# handler = urllib.request.HTTPCookieProcessor(cookie)
# opener = urllib.request.build_opener(handler)
#
# postdata = urllib.parse.urlencode(values).encode()
http_ip = '103.215.211.74:8080'
proxies = {'https':http_ip,'http':http_ip}
user_agent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729)'
headers = { 'User-Agent' : user_agent }


'''输入提取地址,返回一个bs对象'''
def bsObj(myUrl):
    print('准备获取源码')
    i = 0
    for i in range(5):
        try:
            req = requests.get(myUrl, cookies=values, headers=headers)
            if req.status_code == 200:
                break
        except Exception as ex:
            print('提交地址失败.....第%d次'%(i+1))

    print('获取成功')

    return BeautifulSoup(req.text.encode('utf-8'),features='html.parser')
    # print(bsObj)

# req = urllib.request.Request(myUrl,headers=headers)
# urlweb=urllib.request.urlopen(req).read().decode("utf-8")
# bsObj=BeautifulSoup(urlweb,features= "html.parser")
# myItems = bsObj.find_all("div", class_="id1")
# print(myItems)

# fp = open('mm.txt','r+',encoding='utf-8')#用来将主页上的个人信息存储
# i=0
# for item in myItems:
#     # item 中第一个是div的标题，也就是时间
#     # item 中第二个是div的内容，也就是内容
#     print(item.text)
#
#     i += 1
#     fp.write(item.text)

'''---------------提取主页文件夹名字-----------------'''
def first_sheet(bsObj):
    Div_id2_all = bsObj.find_all('div',attrs={'class':'id2'})
    for div_id2 in Div_id2_all:
        print(div_id2.a['href'])
        print(div_id2.get_text())
        '''创建文件夹'''
        creatfile(div_id2.get_text())




'''提取第二页源码'''
def picturesheet_url(chilesheet_url):
    page = litte_Pic_Num(bsObj(chilesheet_url))
    i=1

    print('有%s页'%(str(page)))
    for i in range(page):
        i+=1
        picture_url(bsObj(chilesheet_url+'?p=%s'%(i-1)),(i-1)*40)
    # req = requests.get(chilesheet_url,cookies=values,headers=headers)
    # return BeautifulSoup(req.text.encode('utf-8'),features='html.parser')

'''取大图地址'''
def picture_url(picture_bsobj,pic_Num):
    Div_all = picture_bsobj.find_all('div', attrs={'class': 'gdtm'})
    # print(Div_all)

    for div in Div_all:
        print(div.a['href'])
        print('---------------------------------------------------------------下载第%s图片----------------------------------------------'%(pic_Num+1))
        pic_Num += 1
        j = 0
        # print('初始化失败次数等于0')
        for j in range(10):
            if j <= 4:
                if down_pic(div.a['href'],pic_Num):
                    break
                if j >= 4 :
                    print('#########################################################第%s大图下载失败#########################'
                          '#####################'%(pic_Num+1))
            else:
                print('###############################切换代理下载')
                if down_pic(div.a['href'],pic_Num,True):
                    break
            if j>=9:
                print('#########################################################第%s大图下载失败#######################'
                  '#######################' % (pic_Num + 1))

            print('下载图片失败%s次,等待重新下载大图'%(j+1))

        print('----------------------------------------------------------------下载结束---------------------------------------------')
        print('正在下载下一张大图')







'''下载图片'''
def down_pic(pic_url,pic_name,p_TorF = False):

    bs_pic = bsObj(pic_url)

    a = bs_pic.find('img',attrs={'id':"img"})
    Bpic_url = a['src']

    '''nl参数'''
    matchObj = re.search("(\d{1,7})-(\d{1,7})",a['onerror'])
    nl = matchObj.group()


    print(Bpic_url)
    path = "C:/Users/Administrator/Desktop/微信公众号/ex/ex/"
    try:
        print('获取大图地址中')
        if p_TorF :
            ir = requests.get(Bpic_url,cookies=values,headers=headers,proxies=proxies)
        else:
            ir = requests.get(Bpic_url, cookies=values, headers=headers)

        print('成功获取大图地址')
        if ir.status_code == 200:
            open(path+str(pic_name)+'.jpg', 'wb').write(ir.content)
            print('下载大图成功')
            return True

    except Exception as e:
        print('大图下载失败尝试nl大图')
        print('获取大图地址nl参数')


        bs_pic = bsObj(pic_url+'?nl='+nl)
        print('成功获取nl')

        a = bs_pic.find('img', attrs={'id': "img"})

        Bpic_url = a['src']


        try:
            if p_TorF:
                ir = requests.get(Bpic_url, cookies=values, headers=headers, proxies=proxies)
            else:
                ir = requests.get(Bpic_url, cookies=values, headers=headers)
            if ir.status_code == 200:
                open(path + str(pic_name) + '.jpg', 'wb').write(ir.content)
                print('下载nl参数大图成功')
                return True
        except Exception as e:
            return False

'''扫描ip是否可用'''
def Seachip(dr):
    # [118.197.9.242]
    dr.encoding='gb2312'
    ipbs = BeautifulSoup(dr.text,features='html.parser')
    print(ipbs.find('center').text)

'''获取小图页数'''
def litte_Pic_Num(urlbs):
    ptb = urlbs.find('table', attrs={'class': "ptb"})
    td = ptb.find_all('td', attrs={'onclick': "document.location=this.firstChild.href"})
    return len(td)


key = 'e2e9880722d34b9f953c785b27b048e2'
api = 'http://www.tuling123.com/openapi/api?key=' + key + '&info='

def output_info(msg):
    print('[INFO] %s' % msg)

@itchat.msg_register(TEXT, isGroupChat = True)
def groupchat_reply(msg):
    print(msg)
    if msg['isAt']:

        print(msg['Content'].find(' '))

        info = msg['Content'][msg['Content'].find('\u2005')+1:]

        print(info)
        url = requests.get(api + info)

        bs = BeautifulSoup(url.text.encode('utf-8'), features='html.parser')

        # itchat.send(u'@%s\u2005I received: %s' % (msg['ActualNickName'], msg['Content']), msg['FromUserName'])
        itchat.send(u'@%s\u2005: %s' % (msg['ActualNickName'],bs), msg['FromUserName'])

        print(bs.find('pre'))

itchat.auto_login()

itchat.run()




'''主函数调用'''
if __name__ == '__main__':
    # myUrl = "https://exhentai.org/?page=1"
    # first_sheet(bsObj(myUrl))
    myurl = 'https://exhentai.org/g/992052/9415f6f4c0/'
    # picturesheet_url(myurl)

    # picture_url(picturesheet_url(myurl))
    '''138查询代理ip是否可以用'''
    # k = 0
    # for k in range(5):
    #     try:
    #         dr = requests.get('http://1212.ip138.com/ic.asp', proxies=proxies)
    #         Seachip(dr)
    #         if dr.status_code == 200:
    #             print(k)
    #             break
    #     except Exception as e:
    #         print('检测ip失败,第%d次'%(k+1))
    # print(dr)
    # picture_url(bsObj(myurl))
    # down_pic('https://exhentai.org/s/e9a3601626/1028384-18', 3)
    # print(dr.status_code)

    # ir = requests.get('http://95.211.214.34/',cookies=values, headers=headers,proxies=proxies)
    # print(ir.status_code)
    # waitForConfirm = False
    # while 1:
    #     status = itchat.check_login(uuid)
    #     if status == '200':
    #         break
    #     elif status == '201':
    #         if waitForConfirm:
    #             output_info('Please press confirm')
    #             waitForConfirm = True
    #     elif status == '408':
    #         output_info('Reloading QR Code')
    #         uuid = open_QR()
    #         waitForConfirm = False
    #
    # userInfo = itchat.web_init()
    # itchat.show_mobile_login()
    # itchat.get_contact()
    # # print(userInfo['User'])
    # output_info('Login successfully as %s' %userInfo['User']['NickName'])
    #
    # itchat.start_receiving()
    # itchat.run()

    print(u'------------------------------结束-----------------------------------------')

