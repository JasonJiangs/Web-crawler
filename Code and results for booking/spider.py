#-*- coding=utf-8 -*-
#@time : 2021/1/6 下午9:32
#@Author : WuErShan
#@File : spider.py
#@Software : PyCharm

import requests
import bs4
import json
import csv
import re




# 1.请求页面，拿到数据
def get_url(page):
    try:
        # 搜索页面的基础链接
        url='https://www.booking.com/searchresults.html'
        # 搜索链接的参数，用offset参数来改变页面数
        para={
            'aid': 304142,
            'label': 'gen173nr - 1FCAEoggI46AdIM1gEaKQCiAEBmAExuAEXyAEM2AEB6AEB - AECiAIBqAIEuAL809H_BcACAdICJDFiMDA5MzZmLTdlZDEtNDQ2NS05MzAxLTEzOTQ3NDk1ZWE5ZdgCBeACAQ',
                'sid': '812a8027f50ad0dcda4b038f582497a8',
        'tmpl': 'searchresults',
        'class_interval': '1',
        'dest_id': '20088325',
        'dest_type': 'city',
        'dtdisc': '0',
        'from_sf': '1',
        'group_adults': '2',
        'group_children': '0',
        'inac': '0',
        'index_postcard': '0',
        'label_click': 'undef',
        'no_rooms': '1',
        'postcard': '0',
        'raw_dest_type': 'city',
        'room1': 'A, A',
        'sb_price_type': 'total',
        'search_selected': 1,
        'shw_aparth': 1,
        'slp_r_match': 0,
        'src': 'index',
        'src_elem': 'sb',
        'srpvid': '1a526031bd3f01f6',
        'ss': 'New York, United States of America',
        'ss_all': 0,
        'ssb': 'empty',
        'sshis': 0,
        'top_ufis': 1,
        'rows': 25,
        'offset': (page-1)*25 # （页数-1）*25
        }

        # 请求头，防止被认出是爬虫
        head={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
        # 返回response对象
        response=requests.get(url=url,headers=head,params=para,timeout=(3,7))
        return response.text
    except:
        get_url(page)
# 2.解析数据
def parse_url(text):

    # 用Beautifulsoup解析页面
    soup=bs4.BeautifulSoup(text,'html.parser')
    # 提取所有有class="bui-link"的标签，该标签内有酒店页面的链接
    links=soup.find_all('a',class_="bui-link")
    link_ls=[]
    # 遍历link_ls，提取酒店页面链接
    for l in links:
        # 提取标签内的'href'属性
        link=l['href']
        # 判定是否是酒店页面
        if 'hotel' in link[:7]:
            link_ls.append('https://www.booking.com'+link.replace('\n',''))
    print(link_ls)
    return link_ls

# 爬取酒店页面内信息
def spider(l,url):
    data=[]
    print(url)
    head={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

    response=requests.get(url=url,headers=head)
    soup=bs4.BeautifulSoup(response.text,'html.parser')
    # 提取script,内有大部分酒店相关数据
    script=soup.find('script',type="application/ld+json")
    script=str(script)[len('<script type="application/ld+json">')+1:-(len('</script>'))]
    script=json.loads(script)

    # hotle_id
    hotel_id=str(l+1)
    data.append(hotel_id)

    # name
    try:
        name=script["name"]
    except:
        name=''
    data.append(name)

    # streetAddress
    try:
        streetAddress=script["address"]["streetAddress"]
    except:
        streetAddress=''
    data.append(streetAddress)

    # priceRange
    try:
        priceRange=script["priceRange"]
    except:
        priceRange=''
    data.append(priceRange)

    # ratingValue
    try:
        ratingValue=script["aggregateRating"]["ratingValue"]
    except:
        ratingValue=''
    data.append(ratingValue)

    # reviewCount
    try:
        reviewCount=script["aggregateRating"]["reviewCount"]
    except:
        reviewCount=''
    data.append(reviewCount)

    # Popular Mentions
    # mentions_ls=soup.find_all('span',class_="bui-input-checkbutton__item")
    # mentions=[]
    # for mention in mentions_ls:
    #     mention=mention.get_text()
    #     mentions.append(mention)

    # mentions_link
    try:
        find_link=re.compile("(?<=var exportedVars = JSON.parse\(')(.*?)(?='\);)")
        json_content=re.findall(find_link,response.text)[0].replace('\\','').replace("' || '{}",'')

        json_content=json.loads(json_content)
        mention_ls=json_content["fe_hotel_review_topics"]
        data_ls=[]
        for m in mention_ls:
            da=[]
            popular_mention=m["category_name"]
            da.append(popular_mention)
            # mention_id=m["category_id"]
            # data.append(mention_id)
            mention_total=str(m["total"])
            da.append(mention_total)

            data_ls.append(':'.join(da))
        data.append(';'.join(data_ls))
    except:
        data.append('')

    # reasons
    try:
        reasons=soup.find_all('p',class_="usp_heading")
        ls=[]
        for reason in reasons:
            reason=reason.get_text()
            ls.append(reason)
        reasons='\n'.join(ls)
    except:
        reasons=''
    data.append(reasons)

    return data

    # hotel_name
    # hotel_name=soup.find('meta',itemprop="name")



def save_data(data):
    with open('data.csv','a') as f:
        writer=csv.writer(f)
        writer.writerow(data)








if __name__ == '__main__':

    # 爬取搜索页面，抓取酒店页面链接。
    for page in range(25):
        print(page)
        text=get_url(page)
        link_ls=parse_url(text)
        # 3.保存数据
        with open('links.txt','a')as f:
            f.write('\n'.join(link_ls)+'\n')

    # 写入表头
    with open('data.csv','a') as csv_file:
        writer=csv.writer(csv_file)
        writer.writerow(["Hotel Id","Hotel Name","streetAddress","priceRange","ratingValue","reviewCount","Popular Mentions","Reasons"])
    #
    # 打开links.txt,提取酒店页面链接。
    with open('links.txt','r') as f:
        link_ls=f.readlines()
        ls=[]
    for link in link_ls:
        if link not in ls:
            ls.append(link)

    print(len(ls))

    # i=0
    # 遍历酒店链接列表，抓取酒店页面信息。
    for l in range(len(link_ls)):
        link=link_ls[l].replace('\n','')
        data=spider(l,link)
        save_data(data)
        print(l)





