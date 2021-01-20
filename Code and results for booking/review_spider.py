#-*- coding=utf-8 -*-
#@time : 2021/1/7 下午11:00
#@Author : WuErShan
#@File : review_spider.py
#@Software : PyCharm

import requests
import re
import bs4
import pandas as pd
import numpy as np
import csv
import random
from concurrent.futures import ThreadPoolExecutor
import sys
import json


class Reviews():
    def __init__(self):
        # 打开links.txt,提取酒店页面链接。
        with open('links.txt', 'r') as f:
            self.link_ls = f.readlines()
        self.head={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
        self.baseurl='https://www.booking.com/reviewlist.en-gb.html'

        df = pd.read_csv('./data.csv')
        df = df.drop('Hotel_id', axis=1)
        df = df.drop_duplicates(keep='first')
        df.index = np.arange(1, len(df) + 1)
        id = pd.Series(np.arange(0, len(df) + 1)).astype(str)
        df.insert(0, 'Hotel_id', id)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 1000)
        # df["Hotel Name"]=df["Hotel Name"].apply(lambda x:x.lower().replace(' ','-'))
        df.set_index(df["Hotel Name"], inplace=True)
        self.items = df['Hotel_id']
        print(self.items)
        self.data_ls=[]
        self.over=[]


    def main(self):
        for l in range(len(self.link_ls)):
            if l>=524:
                link = self.link_ls[l].replace('\n', '')
                print(link)
                page,base_url=self.ask_first(link)
                if page != '':
                    self.spiders(page,base_url)
                    self.save_data(self.data_ls)
                print('第{}家酒店爬取完毕'.format(str(l+1)))





    def ask_first(self,link):
        try:
            find_aid = re.compile('(?<=aid=)(.*?)(?=&amp;)')
            self.aid = re.findall(find_aid, link)[0]
            find_label = re.compile('(?<=label=)(.*?)(?=&amp;)')
            self.label = re.findall(find_label, link)[0]
            find_pagename = re.compile('(?<=https://www.booking.com/hotel/us/)(.*?)(?=\.)')
            self.pagename = re.findall(find_pagename, link)[0]
            find_srpvid = re.compile('(?<=srpvid=)(.*?)(?=&amp;)')
            self.srpvid = re.findall(find_srpvid, link)[0]
            name=self.get_name(link)
            print(name)


            self.id=self.items[name]
            para = {'aid': self.aid,
                    ';cc1': 'us',
                    'pagename': self.pagename,
                    'r_lang': '',
                    'review_topic_category_id': '',
                    'type': 'total',
                    'score':'',
                    'sort': 'f_recent_desc',
                    'dist': 1,
                    'offset': 0,
                    'rows': 10,
                    'rurl': '',
                    'text': '',
                    'translate': '',
                    'time_of_year': '',
                    '_': 1610033970510}
            proxies = {'http': 'http://' + self.randomip()}

            response = requests.get(url=self.baseurl, headers=self.head, params=para,timeout=(3,7),proxies=proxies)
            print(1)
            text=response.text.encode("utf-8")
            print(2)
            soup = bs4.BeautifulSoup(text, 'html.parser')
            print(3)
            review_list = soup.find_all('li',class_="review_list_new_item_block")
            self.data_ls=[]

            for review in review_list:
                data = []
                data.append(self.id)
                # Reviewer
                try:
                    reviewer = review.find('span', class_="bui-avatar-block__title").get_text().replace('\n', '')
                except:
                    reviewer=''
                data.append(reviewer)
                # Date of Posting
                try:
                    post_date = review.find_all('span', class_="c-review-block__date")[1].get_text().replace('\n', '').replace('Reviewed: ','')
                except:
                    post_date=''
                data.append(post_date)
                # Location
                try:
                    location = review.find('span', class_="bui-avatar-block__subtitle").get_text().replace('\n', '')
                except:
                    location=''
                data.append(location)
                # Rating
                try:
                    rating = review.find('div', class_="bui-review-score__badge").get_text().replace('\n', '')
                except:
                    rating=''
                data.append(rating)
                # Title
                try:
                    title = review.find('div', class_="bui-grid__column-10").get_text().replace('\n', '')
                    title=str(' '.join(title.split()))
                except:
                    title=''
                data.append(title)
                # Smile Content
                try:
                    smile_content = review.find('div', class_="c-review__row").get_text().replace('\n', '')
                    smile_content =str(' '.join(smile_content.split()).replace(' · ',' '))
                except:
                    smile_content = ''
                data.append(smile_content)
                # Cry Content
                try:
                    cry_content = review.find('div', class_="c-review__row lalala").get_text().replace('\n', '')
                    cry_content =str(' '.join(cry_content.split()).replace(' · ',' '))
                except:
                    cry_content = ''
                data.append(cry_content)
                # Room Type
                try:
                    room_type = review.find('li',class_="bui-list__item review-block__room-info--disabled").get_text().replace('\n', '')
                except:
                    room_type=''
                    # Stay Period
                try:
                    stay = review.find('ul',class_="bui-list bui-list--text bui-list--icon bui_font_caption c-review-block__row c-review-block__stay-date").get_text().replace('\n', '').split('·')
                    stay_period = stay[0]
                    # Check in Date
                    check_date = stay[1]
                    check_date=str(''.join(check_date.split()))
                except:
                    stay_period=''
                    check_date=''
                try:
                    travel_type=review.find('ul',class_="bui-list bui-list--text bui-list--icon bui_font_caption review-panel-wide__traveller_type c-review-block__row").get_text().replace('\n','')
                except:
                    travel_type=''
                data.append(room_type)
                data.append(stay_period)
                data.append(check_date)
                data.append(travel_type)

                # Helpful
                try:
                    helpful = review.find_all('div', class_="review-helpful__container").find('strong').get_text()
                except:
                    helpful = ''
                data.append(helpful)

                # Response Response Comment
                try:
                    response_content = review.find_all('span', class_="c-review-block__response__body bui-u-hidden")[
                        0].get_text()
                    response_binary = 1
                except:
                    response_content = ''
                    response_binary = 0
                data.append(response_binary)
                data.append(response_content)

                # Photos Binary Photo Number
                try:
                    photos = review.find_all('li', class_="c-review-block__photos__item")
                    photos_number = len(photos)
                    if photos_number != 0:
                        photos_binary = 1
                    else:
                        photos_binary = 0
                except:
                    photos_number = 0
                    photos_binary = 0
                data.append(photos_binary)
                data.append(photos_number)

                print(data)
                self.data_ls.append(data)
            try:
                pages = soup.find_all('div', class_="bui-pagination__item")
                page = pages[-2].find('span').get_text()
                base_url='https://www.booking.com'+str(pages[-2].find('a')['href'])

            except:
                page = ''
                base_url=''

            print(page)
            print(base_url)
            return page,base_url
        except:
            page,base_url=self.ask_first(link)
            return page, base_url

    def get_name(self, url):

        try:
            head = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

            response = requests.get(url=url, headers=head,timeout=(3,7))
            soup = bs4.BeautifulSoup(response.text, 'html.parser')
            # 提取script,内有大部分酒店相关数据
            script = soup.find('script', type="application/ld+json")
            script = str(script)[len('<script type="application/ld+json">') + 1:-(len('</script>'))]
            script = json.loads(script)

            # name
            try:
                name = script["name"]
            except:
                name = ''

            return name
        except:
            self.get_name(url)






    def spiders(self,page,link):
        baseurl=link[:link.find('&offset')]
        print(baseurl)
        pool=ThreadPoolExecutor(10)
        for i in range(2,int(page)):
            pool.submit(self.spider,baseurl,i)
        pool.shutdown(wait=True)


    def spider(self,baseurl,i):
        try:
            url = baseurl + "&offset={}".format(str((i - 1) * 10))
            print(url)
            proxies = {'http': 'http://' + self.randomip()}

            response = requests.get(url=url, headers=self.head,timeout=(3,7),proxies=proxies)
            soup = bs4.BeautifulSoup(response.text.encode('utf-8'), 'html.parser')
            review_list = soup.find_all('li',class_="review_list_new_item_block")
            print(len(review_list))

            for review in review_list:

                data = []
                data.append(self.id)


                # Reviewer
                try:
                    reviewer = review.find('span', class_="bui-avatar-block__title").get_text().replace('\n', '')
                except:
                    reviewer = ''
                data.append(reviewer)
                # Date of Posting
                try:
                    post_date = review.find_all('span', class_="c-review-block__date")[1].get_text().replace('\n', '').replace('Reviewed: ','')
                except:
                    post_date = ''
                data.append(post_date)
                # Location
                try:
                    location = review.find('span', class_="bui-avatar-block__subtitle").get_text().replace('\n', '')
                except:
                    location = ''
                data.append(location)
                # Rating
                try:
                    rating = review.find('div', class_="bui-review-score__badge").get_text().replace('\n', '')
                except:
                    rating = ''
                data.append(rating)
                # Title
                try:
                    title = review.find('div', class_="bui-grid__column-10").get_text().replace('\n', '')
                    title=str(' '.join(title.split()))
                except:
                    title = ''
                data.append(title)
                # Smile Content
                try:
                    smile_content = review.find('div', class_="c-review__row").get_text().replace('\n', '')
                    smile_content=str(' '.join(smile_content.split()).replace(' · ',' '))
                except:
                    smile_content = ''
                data.append(smile_content)
                # Cry Content
                try:
                    cry_content = review.find('div', class_="c-review__row lalala").get_text().replace('\n', '')
                    cry_content=str(' '.join(cry_content.split()).replace(' · ',' '))
                except:
                    cry_content = ''
                data.append(cry_content)
                # Room Type
                try:
                    room_type = review.find('li',
                                            class_="bui-list__item review-block__room-info--disabled").get_text().replace(
                        '\n', '')
                except:
                    room_type = ''
                    # Stay Period
                try:
                    stay = review.find('ul',
                                       class_="bui-list bui-list--text bui-list--icon bui_font_caption c-review-block__row c-review-block__stay-date").get_text().replace(
                        '\n', '').split('·')
                    stay_period = stay[0]
                    # Check in Date
                    check_date = stay[1]
                    check_date=str(' '.join(check_date.split()))
                except:
                    stay_period = ''
                    check_date = ''
                try:
                    travel_type = review.find('ul',
                                              class_="bui-list bui-list--text bui-list--icon bui_font_caption review-panel-wide__traveller_type c-review-block__row").get_text().replace(
                        '\n', '')
                except:
                    travel_type = ''
                data.append(room_type)
                data.append(stay_period)
                data.append(check_date)
                data.append(travel_type)
                # Helpful
                try:
                    helpful=review.find_all('div',class_="review-helpful__container").find('strong').get_text()
                except:
                    helpful=''
                data.append(helpful)

                # Response Response Comment
                try:
                    response_content=review.find_all('span',class_="c-review-block__response__body bui-u-hidden")[0].get_text()
                    response_binary=1
                except:
                    response_content=''
                    response_binary=0
                data.append(response_binary)
                data.append(response_content)


                # Photos Binary Photo Number
                try:
                    photos=review.find_all('li',class_="c-review-block__photos__item")
                    photos_number=len(photos)
                    if photos_number!=0:
                        photos_binary=1
                    else:
                        photos_binary=0
                except:
                    photos_number=0
                    photos_binary=0
                data.append(photos_binary)
                data.append(photos_number)

                print(data)
                self.data_ls.append(data)
            print('第{}页爬取完毕'.format(str(i)))
        except:
            print('重新发起请求')
            self.spider(baseurl,i)

    # 获取ip池
    def get_ips(self):
        with open('tbip.txt', 'r', encoding='utf-8') as f:
            tbips = f.read()
            tbipsarray = tbips.split('\n')
            # 过滤空字符
            tbipsarray = list(filter(None, tbipsarray))
        return tbipsarray

    # 随机获取一个ip
    def randomip(self):
        # 获取最新ip池
        ips = self.get_ips()
        randomip =random.choice(ips)
        return randomip

    def save_data(self, data_ls):
        with open('./all_reviews.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerows(data_ls)








if __name__ == '__main__':
    # with open('./all_reviews.csv','w') as f:
    #     writer=csv.writer(f)
    #     writer.writerow(["Hotel_id","Reviewer","Date of Posting","Location","Rating","Title",
    #                      "Smile Content","Cry Content","Room Type","Stay Period","Check in Date","Travel Type","Helpful","Response Binary","Response Comment","Photos Binary","Photos Number"])
    r=Reviews()
    r.main()
