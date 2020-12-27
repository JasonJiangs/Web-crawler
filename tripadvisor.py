#-*- coding=utf-8 -*-
#@time : 2020/12/9 下午3:29
#@Author : WuErShan
#@File : comment_spider.py
#@Software : PyCharm

import time
import csv
import requests
import json
import bs4
import re
import os
import pandas as pd
import random
from concurrent.futures import ThreadPoolExecutor


def get_pri_info(page):

    # 解析页面
    soup=bs4.BeautifulSoup(page,'html.parser')
    items=soup.find_all('div',class_="prw_rup prw_meta_hsx_responsive_listing ui_section listItem")

    # data_ls用来一会保存数据
    data_ls=[]


    # 遍历所有条目，获得酒店名，酒店链接后缀
    for item in items:
        data=[]
        link=item.find('div',class_="listing_title").find('a')['href']
        name = item.find('div',class_="listing_title").find('a').get_text()



        # 保存数据
        data.append(str(name))
        data.append(str(link))

        data_ls.append(data)

    return data_ls


# 获取ip池
def get_ips():
    with open('tbip.txt', 'r', encoding='utf-8') as f:
        tbips = f.read()
        tbipsarray = tbips.split('\n')
        # 过滤空字符
        tbipsarray = list(filter(None, tbipsarray))
    return tbipsarray

# 随机获取一个ip
def randomip():
    # 获取最新ip池
    ips = get_ips()
    randomip = random.choice(ips)
    return randomip



def spider(link):

    find_script=re.compile('(?<=</div><script>)(.*?)(?=</script>)')
    find_reviewlist=re.compile('(?<="reviewListPage":)(.*?)(?=,"reviewAggregations":)')
    data_ls=[]

    url='https://www.tripadvisor.com{}'.format(link)

    head = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'referer': 'https://cn.tripadvisor.com/Tourism-g297472-Wenzhou_Zhejiang-Vacations.html',
        'cookie': 'TAUnique=%1%enc%3A4w9P9TsHCujD3V%2FPbQf89X3iVuvpJdhKwN%2BE3itCaRPiJ6g91gwMNg%3D%3D; ServerPool=B; TART=%1%enc%3Aw91fz20H%2FPUQCvvGrNGPfQGoYNx%2BouA53Dl8YhSz9dwMFE3PymCTvsKuF0aM5ESWhI5mOGAqLoI%3D; TADCID=CVHT8tvx30oV8um1ABQCjnFE8vTET66GHuEzPi7KfWHKk99xtyJ7QT38aagpI_Xhg9Sp9yeWYt2mOjQQ-bkZVmtJp2zYUP4nfNg; TASSK=enc%3AAH98OTFpBbzUhJmcVnBRhkHv77CsUkhb8%2BEMNlzWxuVmautKAkN24MqY9w5AyoBImCTRbjmv%2FPIbSh%2Bz4AjJCnrDWdn3PUFJ86pXo36KNFRwceUiJdrQqCnJr7%2F8%2BgqqWQ%3D%3D; PMC=V2*MS.33*MD.20201128*LD.20201128; TATrkConsent=eyJvdXQiOiIiLCJpbiI6IkFMTCJ9; __gads=ID=d7c83e60e13cb583:T=1606545026:S=ALNI_Mbz5sGtcZFWHv_En8IrRNG4ccs3_g; TAPD=tripadvisor.cn; BEPIN=%1%1760da5235d%3Bweb271a.a.tripadvisor.com%3A30023%3B; TATravelInfo=V2*AY.2021*AM.5*AD.21*DY.2021*DM.5*DD.22*A.2*MG.-1*HP.2*FL.3*DSM.1606546816485*AZ.1*RS.1; CM=%1%mds%2C1606546816449%2C1606633216%7C; PAC=AJI6paGpdLP7GvLKFKc0X35EZB7bE7SyO87iA1mBTpbaltrf6KR6sYJsZ0FsIZJeVevDQPh9quacVlmUstAKQuqhlLH3nFR3obFwnNiaCkXSvXeOpwHDfRH6kbtcJKLC5A%3D%3D; SRT=%1%enc%3Aw91fz20H%2FPUQCvvGrNGPfQGoYNx%2BouA53Dl8YhSz9dwMFE3PymCTvsKuF0aM5ESWhI5mOGAqLoI%3D; TAReturnTo=%1%%2FHotel_Review-g297472-d504804-Reviews-Overseas_Chinese_Hotel_Wenzhou-Wenzhou_Zhejiang.html; roybatty=TNI1625!AHDebL91gi1wiXqtKsAkLd7CE4uTnPxbfOgrt9yQNAb1o447r85d49SJUYUXFSVvQfe5Tn7p5Uf9Hk4TTTfcYPWQP8gGkhbCdSg4vZ7YDFB%2FeYwsvgFpTcGghrY7ozPTbz%2BqoOrQllizImY9Y9V4jUNw2pUnCY3LgkRRl9Q4Dw2x%2C1; __vt=0PvcTTLtk5lcxbq6ABQCq4R_VSrMTACwWFvfTfL3vxGozPRWLUQzCu5H6hoHd80593zPRIL4zIbCtEmWeo8FkUMUoRxLLTOg4x4hfU2BtclN0ZTJTrhuG6Vgz7Iaqm-PmBUDIyWGarr5zPShT4dHMER5vJc; TASession=V2ID.1A4B00779FC928D82F621ABD2A3EFA61*SQ.140*LS.DemandLoadAjax*GR.89*TCPAR.42*TBR.84*EXEX.19*ABTR.21*PHTB.82*FS.87*CPU.50*HS.recommended*ES.popularity*DS.5*SAS.popularity*FPS.oldFirst*FA.1*DF.0*TRA.true*LD.504804*EAU._; TAUD=LA-1606545021352-1*RDD-1-2020_11_28*HDD-1791304-2021_05_21.2021_05_22.1*HD-1795104-2021_05_21.2021_05_22.297472*G-1795105-2.1.297472.*ARDD-1795106-2021_05_21.2021_05_22*LD-9444473-2021.5.21.2021.5.22*LG-9444476-2.1.T.'}
    proxies={'http': "http://"+randomip()}
    print(proxies)
    response = requests.get(url=url, headers=head,proxies=proxies)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    # 定位页面数
    pages=soup.find('div',class_="pageNumbers").find_all('a',class_="pageNum")
    try:
        page=pages[-1].get_text()
    except:
        page=1

    # 定位script
    script = re.findall(find_script, str(soup))[0]




    # 定位评论
    reviewlist=re.findall(find_reviewlist,script)[0]
    reviews=json.loads(reviewlist)["reviews"]


    for revi in reviews:
        ls=[]
        try:
            user_id = revi['userProfile']['userId']
        except:
            user_id=''
        try:
            user_name=revi['userProfile']['displayName']
        except:
            user_name=''
        try:
            contribution=revi['userProfile']['contributionCounts']['sumAllUgc']
        except:
            contribution=''
        try:
            review_score=revi["rating"]
        except:
            review_score=''
        try:
            review_date=revi["createdDate"]
        except:
            review_date=''
        try:
            text = revi['text']
        except:
            text=''
        try:
            title=revi['title']
        except:
            title=''
        try:
            helpful_votes=revi["helpfulVotes"]
        except:
            helpful_votes=''
        try:
            location=revi['userProfile']['hometown']['location']['additionalNames']['long']
        except:
            location=''
        try:
            stay_date=revi['tripInfo']['stayDate']
        except:
            stay_date=''
        try:
            helpful=revi['userProfile']['contributionCounts']['helpfulVote']
        except:
            helpful=''
        try:
            resp_content=revi['mgmtResponse']['text']
            resp=1
        except:
            resp_content =''
            resp = 0


        ls.append(user_id)
        ls.append(user_name)
        ls.append(review_date)
        ls.append(location)
        ls.append(contribution)
        ls.append(review_score)
        ls.append(title)
        ls.append(text)
        ls.append(helpful_votes)
        ls.append(stay_date)
        ls.append(helpful)
        ls.append(resp)
        ls.append(resp_content)
        data_ls.append(ls)


    if int(page)>1:

        # 建立线程池
        pool=ThreadPoolExecutor(10)

        for i in range(1,int(page)):
        # for i in range(2,5):
            # 把任务加在池中
            pool.submit(spider_page,i,url,find_script,find_reviewlist,data_ls)

        pool.shutdown(wait=True)

    return data_ls

def spider_page(i,url,find_script,find_reviewlist,data_ls):

    head = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'referer': 'https://cn.tripadvisor.com/Tourism-g297472-Wenzhou_Zhejiang-Vacations.html'}
    proxies = {'http': "http://" + randomip()}
    print(proxies)
    review_url = url[:url.find('Reviews-') + 8] + 'or' + str(i * 5) + url[url.find('Reviews-') + 7:]
    print(review_url)
    response = requests.get(url=review_url, headers=head)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    # 定位script
    script = re.findall(find_script, str(soup))[0]

    # 定位评论
    reviewlist = re.findall(find_reviewlist, script)[0]
    reviews = json.loads(reviewlist)["reviews"]


    for revi in reviews:
        ls = []
        try:
            user_id = revi['userProfile']['userId']
        except:
            user_id = ''
        try:
            user_name = revi['userProfile']['displayName']
        except:
            user_name = ''
        try:
            contribution = revi['userProfile']['contributionCounts']['sumAllUgc']
        except:
            contribution = ''
        try:
            review_score = revi["rating"]
        except:
            review_score = ''
        try:
            review_date = revi["createdDate"]
        except:
            review_date = ''
        try:
            text = revi['text']
        except:
            text = ''
        try:
            helpful_votes=revi["helpfulVotes"]
        except:
            helpful_votes=''
        try:
            title = revi['title']
        except:
            title = ''
        try:
            location = revi['userProfile']['hometown']['location']['additionalNames']['long']
        except:
            location = ''
        try:
            stay_date = revi['tripInfo']['stayDate']
        except:
            stay_date = ''
        try:
            helpful = revi['userProfile']['contributionCounts']['helpfulVote']
        except:
            helpful = ''
        try:
            resp_content = revi['mgmtResponse']['text']
            resp = 1
        except:
            resp_content = ''
            resp = 0
        try:
            photos=revi["photos"]
            photos_number=len(photos)
            if photos_number==0:
                photos_binary=0
            else:
                photos_binary=1
        except:
            photos_number=0
            photos_binary=0


        ls.append(user_id)
        ls.append(user_name)
        ls.append(review_date)
        ls.append(location)
        ls.append(contribution)
        ls.append(review_score)
        ls.append(title)
        ls.append(text)
        ls.append(helpful_votes)
        ls.append(stay_date)
        ls.append(helpful)
        ls.append(resp)
        ls.append(resp_content)
        ls.append(photos_binary)
        ls.append(photos_number)
        data_ls.append(ls)
        print(ls)
        time.sleep(0.5)
    return data_ls




if __name__ == '__main__':

    id_data=pd.read_excel('./new_hotel.xlsx')
    id_data['hotel_name']=id_data['hotel_name'].str.strip()
    id_data.index = id_data['hotel_name']

    id_dict=id_data['Hotel_ID'].to_dict()
    print(id_dict)

    try:
        os.mkdir('./comment')
    except:
        print('已创建文件夹')
    with open('./comment/12-21.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(
            ['Hotel_ID', 'Reviewer_ID', 'Reviewer', 'Day of posting', 'Location', 'contributions',
             'Rating','Title','Content',"helpfulVotes",'Date of stay','Helpful','Response','Response_comment','Photos_binary','Photos_number'])

    data_ls=[]
    for i in range(29):
        print('爬到第{}页'.format(str(i+1)))
        with open('{}.txt'.format(str(i + 1))) as f:
            page = f.read()

        data_ls.extend(get_pri_info(page))

    temp_list = []  # 定义一个临时空列表，用于保存临时数据。
    for i in data_ls:  # 遍历原列表，判断如果元素不在临时列表，就追加进去，如果在，就不加。
        if i not in temp_list:
            temp_list.append(i)

    print(len(temp_list))
    j=0
    for data in temp_list:
        j += 1
        print('完成第{}家酒店评论爬取'.format(str(j)))
        if j>=0:
            tab = []
            name = data[0]
            try:
                hotel_id=id_dict[name.strip()]
            except:
                hotel_id=''

            link = data[1]
            print(link)

            try:
                data_list = spider(link)
            except:
                data_list=[]

            for i in range(len(data_list)):
                try:
                    user_id=data_list[i][0]
                except:
                    user_id=''
                try:
                    review_name=data_list[i][1]
                except:
                    review_name=''
                try:
                    post_date=data_list[i][2]
                except:
                    post_date=''
                try:
                    location=data_list[i][3]
                except:
                    location=''

                try:
                    contribution=data_list[i][4]
                except:
                    contribution=''
                try:
                    rating=data_list[i][5]
                except:
                    rating=''
                try:
                    title=data_list[i][6]
                except:
                    title=''
                try:
                    content=data_list[i][7]
                except:
                    content=''
                try:
                    helpful_vote=data_list[i][8]
                except:
                    helpful_vote=''
                try:
                    stay_date=data_list[i][9]
                except:
                    stay_date=''
                try:
                    helpful=data_list[i][10]
                except:
                    helpful=''
                try:
                    resp=data_list[i][11]
                except:
                    resp=''
                try:
                    resp_content=data_list[i][12]
                except:
                    resp_content=''
                try:
                    photos_binary=data_list[i][13]
                except:
                    photos_binary=0
                try:
                    photos_number=data_list[i][14]
                except:
                    photos_number=0

                with open('./comment/12-21.csv', 'a') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow([hotel_id,user_id,review_name,post_date,location,
                                     contribution,rating,title,content,helpful_vote,stay_date,helpful,resp,resp_content,photos_binary,photos_number])


