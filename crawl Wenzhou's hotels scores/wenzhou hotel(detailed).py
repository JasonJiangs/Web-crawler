# -*- coding=utf-8 -*-


import requests
import bs4
import json
import re
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv

'''
由于网站信息缺失比较严重，且网页是动态加载的，
选择selsenium与requests并用的爬取方式
'''


# 获取星级标签内的酒店信息，返回字典
def star(driver):
    s = {}
    find_pre_page = re.compile('(?<=家企业中有 )(.*?)(?= 家)')

    # 等待加载
    time.sleep(5)

    # 定位星级分类标签量
    stars = driver.find_elements_by_xpath('//*[@id="component_6"]/div/div[2]/div[8]/div[2]/div')

    time.sleep(5)

    # 迭代循环，访问所有标签
    for j in range(len(stars)):
        star = driver.find_element_by_xpath(
            '//*[@id="component_6"]/div/div[2]/div[8]/div[2]/div[{}]'.format(str(j + 1)))

        # 符合的企业量
        number = str(star.text).split('\n')[1]

        # 星级名
        star_name = str(star.text).split('\n')[0]
        print(number)

        # 如果企业量不为零，获取页面数和源代码
        if number != '0':
            star.click()
            time.sleep(5)
            pre_page = driver.find_element_by_xpath(
                '//*[@id="taplc_dh_sort_filter_entry_0"]/div[1]/div[1]/div[1]/span').text
            print(pre_page)
            pre_page = re.findall(find_pre_page, pre_page)[0]
            print(pre_page)
            page = int(pre_page) // 30
            print(page)

            html = driver.page_source

            # 解析源代码，获取标签内企业名
            soup = bs4.BeautifulSoup(html, 'html.parser')
            items = soup.find('div', id="taplc_hsx_hotel_list_lite_dusty_hotels_combined_sponsored_0",
                              class_="ppr_rup ppr_priv_hsx_hotel_list_lite").find_all('div',
                                                                                      class_="prw_rup prw_meta_hsx_responsive_listing ui_section listItem")

            for item in items:
                name = item.find('div', class_="listing_title").find('a').get_text()
                s[name] = star_name
                print(name)

            # 遍历该标签内的所有页面
            for i in range(page):

                if i == 0:
                    driver.find_element_by_xpath(
                        '//*[@id="taplc_main_pagination_bar_dusty_hotels_resp_0"]/div/div/div/a').click()
                elif i == page + 1:
                    pass
                else:
                    driver.find_element_by_xpath(
                        '//*[@id="taplc_main_pagination_bar_dusty_hotels_resp_0"]/div/div/div/a[2]').click()
                time.sleep(5)

            # 释放该标签
            star.click()
            time.sleep(5)
    return s


# 获取区级标签内的酒店信息，返回字典
# 基本思路同上，修改变量、参数即可
def area(driver):
    a = {}
    find_pre_page = re.compile('(?<=家企业中有 )(.*?)(?= 家)')
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="component_6"]/div/div[2]/div[6]/div[2]/div[5]').click()
    areas = driver.find_elements_by_xpath('//*[@id="component_6"]/div/div[2]/div[6]/div[2]/div')
    time.sleep(5)
    for j in range(len(areas) - 1):
        area = driver.find_element_by_xpath(
            '//*[@id="component_6"]/div/div[2]/div[6]/div[2]/div[{}]'.format(str(j + 1)))
        area_name = str(area.text).split('\n')[0]
        number = str(area.text).split('\n')[1]
        print(number)
        if number != '0':
            area.click()
            time.sleep(5)
            pre_page = driver.find_element_by_xpath(
                '//*[@id="taplc_dh_sort_filter_entry_0"]/div[1]/div[1]/div[1]/span').text
            print(pre_page)
            pre_page = re.findall(find_pre_page, pre_page)[0]
            print(pre_page)
            page = int(pre_page) // 30
            print(page)

            html = driver.page_source

            soup = bs4.BeautifulSoup(html, 'html.parser')
            items = soup.find('div', id="taplc_hsx_hotel_list_lite_dusty_hotels_combined_sponsored_0",
                              class_="ppr_rup ppr_priv_hsx_hotel_list_lite").find_all('div',
                                                                                      class_="prw_rup prw_meta_hsx_responsive_listing ui_section listItem")

            for item in items:
                name = item.find('div', class_="listing_title").find('a').get_text()
                a[name] = area_name
                print(name)
            print(a)
            for i in range(page):

                if i == 0:
                    driver.find_element_by_xpath(
                        '//*[@id="taplc_main_pagination_bar_dusty_hotels_resp_0"]/div/div/div/a').click()
                elif i == page + 1:
                    pass
                else:
                    driver.find_element_by_xpath(
                        '//*[@id="taplc_main_pagination_bar_dusty_hotels_resp_0"]/div/div/div/a[2]').click()
                time.sleep(5)

            area.click()
            time.sleep(5)

    return a


# 获取类型标签内的信息，返回字典
# 基本思路同上
def type(driver):
    t = {}
    find_pre_page = re.compile('(?<=家企业中有 )(.*?)(?= 家)')
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="component_6"]/div/div[2]/div[5]/div[2]/div[5]').click()
    types = driver.find_elements_by_xpath('//*[@id="component_6"]/div/div[2]/div[5]/div[2]/div')
    time.sleep(5)
    for j in range(len(types) - 1):
        type = driver.find_element_by_xpath(
            '//*[@id="component_6"]/div/div[2]/div[5]/div[2]/div[{}]'.format(str(j + 1)))
        type_name = str(type.text).split('\n')[0]
        number = str(type.text).split('\n')[1]
        print(number)
        if number != '0':
            type.click()
            time.sleep(5)
            pre_page = driver.find_element_by_xpath(
                '//*[@id="taplc_dh_sort_filter_entry_0"]/div[1]/div[1]/div[1]/span').text
            print(pre_page)
            pre_page = re.findall(find_pre_page, pre_page)[0]
            print(pre_page)
            page = int(pre_page) // 30
            print(page)

            html = driver.page_source

            soup = bs4.BeautifulSoup(html, 'html.parser')
            items = soup.find('div', id="taplc_hsx_hotel_list_lite_dusty_hotels_combined_sponsored_0",
                              class_="ppr_rup ppr_priv_hsx_hotel_list_lite").find_all('div',
                                                                                      class_="prw_rup prw_meta_hsx_responsive_listing ui_section listItem")

            for item in items:
                name = item.find('div', class_="listing_title").find('a').get_text()
                t[name] = type_name
                print(name)
            for i in range(page + 1):

                if i == 0:
                    driver.find_element_by_xpath(
                        '//*[@id="taplc_main_pagination_bar_dusty_hotels_resp_0"]/div/div/div/a').click()
                elif i == page + 1:
                    pass
                else:
                    driver.find_element_by_xpath(
                        '//*[@id="taplc_main_pagination_bar_dusty_hotels_resp_0"]/div/div/div/a[2]').click()
                time.sleep(5)

            type.click()
            time.sleep(5)
    return t


# 获取主页面所有酒店的源代码，并保存为文件
def get_page(driver):
    # selenium访问网页
    url = 'https://www.tripadvisor.cn/Hotels-g297472-Wenzhou_Zhejiang-Hotels.html'
    driver.get(url)

    # 阻断selenium，输入页数后开始运行
    for i in range(int(input('请输入页数（17页）：'))):

        # 保存页面源代码
        html = driver.page_source
        with open('{}.txt'.format(str(i + 1)), 'w', encoding='utf-8') as f:
            f.write(html)

        # 翻页
        if i == 0:
            ActionChains(driver).double_click(driver.find_element_by_xpath(
                '//*[@id="taplc_main_pagination_bar_dusty_hotels_resp_0"]/div/div/div/a')).perform()
        elif i == 16:
            pass
        else:
            ActionChains(driver).double_click(driver.find_element_by_xpath(
                '//*[@id="taplc_main_pagination_bar_dusty_hotels_resp_0"]/div/div/div/a[2]')).perform()

        time.sleep(10)


# 解析主页面内的信息，获得酒店名称、链接、当前价格
def get_pri_info(page):
    # 解析页面
    soup = bs4.BeautifulSoup(page, 'html.parser')
    items = soup.find_all('div', class_="prw_rup prw_meta_hsx_responsive_listing ui_section listItem")

    # data_ls用来一会保存数据
    data_ls = []

    # 遍历所有条目，获得酒店名，酒店链接后缀、实时价格
    for item in items:
        data = []
        link = item.find('div', class_="listing_title").find('a')['href']
        name = item.find('div', class_="listing_title").find('a').get_text()

        # 如果找不到价格
        try:
            curr_price = item.find('div', class_="price-wrap").get_text()
        except:
            curr_price = ''

        # 保存数据
        data.append(str(name))
        data.append(str(link))
        data.append(str(curr_price))
        data_ls.append(data)

    return data_ls


# 通过构建链接访问酒店详细信息页面，获取一些信息指标
def spider(link):
    ls = []

    url = 'https://www.tripadvisor.cn{}'.format(link)
    head = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'referer': 'https://cn.tripadvisor.com/Tourism-g297472-Wenzhou_Zhejiang-Vacations.html',
        'cookie': 'TAUnique=%1%enc%3A4w9P9TsHCujD3V%2FPbQf89X3iVuvpJdhKwN%2BE3itCaRPiJ6g91gwMNg%3D%3D; ServerPool=B; TART=%1%enc%3Aw91fz20H%2FPUQCvvGrNGPfQGoYNx%2BouA53Dl8YhSz9dwMFE3PymCTvsKuF0aM5ESWhI5mOGAqLoI%3D; TADCID=CVHT8tvx30oV8um1ABQCjnFE8vTET66GHuEzPi7KfWHKk99xtyJ7QT38aagpI_Xhg9Sp9yeWYt2mOjQQ-bkZVmtJp2zYUP4nfNg; TASSK=enc%3AAH98OTFpBbzUhJmcVnBRhkHv77CsUkhb8%2BEMNlzWxuVmautKAkN24MqY9w5AyoBImCTRbjmv%2FPIbSh%2Bz4AjJCnrDWdn3PUFJ86pXo36KNFRwceUiJdrQqCnJr7%2F8%2BgqqWQ%3D%3D; PMC=V2*MS.33*MD.20201128*LD.20201128; TATrkConsent=eyJvdXQiOiIiLCJpbiI6IkFMTCJ9; __gads=ID=d7c83e60e13cb583:T=1606545026:S=ALNI_Mbz5sGtcZFWHv_En8IrRNG4ccs3_g; TAPD=tripadvisor.cn; BEPIN=%1%1760da5235d%3Bweb271a.a.tripadvisor.com%3A30023%3B; TATravelInfo=V2*AY.2021*AM.5*AD.21*DY.2021*DM.5*DD.22*A.2*MG.-1*HP.2*FL.3*DSM.1606546816485*AZ.1*RS.1; CM=%1%mds%2C1606546816449%2C1606633216%7C; PAC=AJI6paGpdLP7GvLKFKc0X35EZB7bE7SyO87iA1mBTpbaltrf6KR6sYJsZ0FsIZJeVevDQPh9quacVlmUstAKQuqhlLH3nFR3obFwnNiaCkXSvXeOpwHDfRH6kbtcJKLC5A%3D%3D; SRT=%1%enc%3Aw91fz20H%2FPUQCvvGrNGPfQGoYNx%2BouA53Dl8YhSz9dwMFE3PymCTvsKuF0aM5ESWhI5mOGAqLoI%3D; TAReturnTo=%1%%2FHotel_Review-g297472-d504804-Reviews-Overseas_Chinese_Hotel_Wenzhou-Wenzhou_Zhejiang.html; roybatty=TNI1625!AHDebL91gi1wiXqtKsAkLd7CE4uTnPxbfOgrt9yQNAb1o447r85d49SJUYUXFSVvQfe5Tn7p5Uf9Hk4TTTfcYPWQP8gGkhbCdSg4vZ7YDFB%2FeYwsvgFpTcGghrY7ozPTbz%2BqoOrQllizImY9Y9V4jUNw2pUnCY3LgkRRl9Q4Dw2x%2C1; __vt=0PvcTTLtk5lcxbq6ABQCq4R_VSrMTACwWFvfTfL3vxGozPRWLUQzCu5H6hoHd80593zPRIL4zIbCtEmWeo8FkUMUoRxLLTOg4x4hfU2BtclN0ZTJTrhuG6Vgz7Iaqm-PmBUDIyWGarr5zPShT4dHMER5vJc; TASession=V2ID.1A4B00779FC928D82F621ABD2A3EFA61*SQ.140*LS.DemandLoadAjax*GR.89*TCPAR.42*TBR.84*EXEX.19*ABTR.21*PHTB.82*FS.87*CPU.50*HS.recommended*ES.popularity*DS.5*SAS.popularity*FPS.oldFirst*FA.1*DF.0*TRA.true*LD.504804*EAU._; TAUD=LA-1606545021352-1*RDD-1-2020_11_28*HDD-1791304-2021_05_21.2021_05_22.1*HD-1795104-2021_05_21.2021_05_22.297472*G-1795105-2.1.297472.*ARDD-1795106-2021_05_21.2021_05_22*LD-9444473-2021.5.21.2021.5.22*LG-9444476-2.1.T.'}

    response = requests.get(url=url, headers=head)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    # 定位位置信息
    # loc=soup.find('div',class_="hotels-hotel-review-atf-info-parts-BusinessListing__row--24M_7").get_text()

    # 定位相关信息
    rels = soup.find('div',
                     class_="ui_columns hotels-hotel-review-about-with-photos-layout-LayoutStrategy__columns--1uvt4").find_all(
        'div', class_="ui_column")

    # 如果相关信息量大于3，则可能存在评分、评论量、酒店设施、风格、特色信息
    if len(rels) >= 3:

        find_equip = re.compile('(?<="amenityNameLocalized":")(.*?)(?=")')

        # 定位评分信息
        comm = rels[0].find('span',
                            class_="hotels-hotel-review-about-with-photos-Reviews__overallRating--vElGA").get_text()
        comm_num = rels[0].find('span',
                                class_="hotels-hotel-review-about-with-photos-Reviews__seeAllReviews--3PpLR").get_text()
        ls.append(comm)
        ls.append(comm_num)

        # 定位酒店设施信息
        try:
            equipments = str(rels[1].find('div', class_="ssr-init-26f")['data-ssrev-handlers'])
            equip_ls = re.findall(find_equip, equipments)
            ls.append(equip_ls)
        except:
            equipments = str(rels[2].find('div', class_="ssr-init-26f")['data-ssrev-handlers'])
            equip_ls = re.findall(find_equip, equipments)
            ls.append(equip_ls)

        # 定位风格信息
        try:
            features = soup.find_all('div', class_="hotels-hr-about-amenities-AmenityGroup__amenitiesList--3MdFn")[
                1].find_all('div', class_="hotels-hr-about-amenities-Amenity__amenity--3fbBj")
            fea_ls = []
            for tag in features:
                fea_ls.append(str(tag.get_text()))
            ls.append(fea_ls)
        except:
            fea_ls = []
            ls.append(fea_ls)

        # 定位特色信息
        try:
            style = rels[1].find_all('div', class_="hotels-hr-about-layout-TextItem__textitem--2JToc")

            sty_ls = []
            for i in range(len(style) - 1):
                sty = str(style[i].get_text())
                if sty != '':
                    sty_ls.append(sty)
            ls.append(sty_ls)
        except:
            sty_ls = []
            ls.append(sty_ls)

    # 如果相关量小于3，则不存在酒店设施、风格、特色信息
    elif len(rels) < 3:

        # 定位评分信息
        try:
            comm = rels[0].find('span',
                                class_="hotels-hotel-review-about-with-photos-Reviews__overallRating--vElGA").get_text()
            comm_num = rels[0].find('span',
                                    class_="hotels-hotel-review-about-with-photos-Reviews__seeAllReviews--3PpLR").get_text()
        except:
            comm = ''
            comm_num = ''

        equipments = []
        fea_ls = []
        sty_ls = []
        ls.append(comm)
        ls.append(comm_num)
        ls.append(equipments)
        ls.append(fea_ls)
        ls.append(sty_ls)

    return ls


# 写入数据为csv,可以通过pandas或offic转存为xlsx
def write(data_ls):
    with open('./hotel.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["酒店名称", "实时价格", "酒店评分", "评分数量", "酒店类型", '酒店地区', '酒店星级', '酒店设施', '客房特点', '酒店风格'])
        writer.writerows(data_ls)


if __name__ == '__main__':
    driver = webdriver.Chrome(r'./chromedriver')
    get_page(driver)
    t = type(driver)
    s = star(driver)
    a = area(driver)
    driver.quit()
    table = []
    for i in range(17):

        with open('{}.txt'.format(str(i + 1))) as f:
            page = f.read()
        data_ls = get_pri_info(page)

        for data in data_ls:
            tab = []
            name = data[0]
            link = data[1]
            curr_price = data[2]
            type = t.get(name, '')
            area = a.get(name, '')
            star = s.get(name, '')
            print(name)

            try:
                ls = spider(link)
                comm = ls[0]
                comm_num = ls[1]
                equipments = '、'.join(ls[2])
                features = '、'.join(ls[3])
                style = '、'.join(ls[4])
                tab.append(name)
                tab.append(curr_price)
                tab.append(comm)
                tab.append(comm_num)
                tab.append(type)
                tab.append(area)
                tab.append(star)
                tab.append(equipments)
                tab.append(features)
                tab.append(style)
                table.append(tab)
            except:

                comm = ''
                comm_num = ''
                equipments = ''
                features = ''
                style = ''
                tab.append(name)
                tab.append(curr_price)
                tab.append(comm)
                tab.append(comm_num)
                tab.append(type)
                tab.append(area)
                tab.append(star)
                tab.append(equipments)
                tab.append(features)
                tab.append(style)
                table.append(tab)
                print('wrong')
                with open('./wrong', 'a') as f:
                    f.write(name + ',' + link + '\n')
            time.sleep(5)

    write(table)
