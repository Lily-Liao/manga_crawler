# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 16:50:58 2020

@author: user
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import os
from random import randint
import datetime
from datetime import timedelta
import locale



token="your token"

def lineNotify(token, msg, picURI):#
    url = "https://notify-api.line.me/api/notify"
    headers = {
        "Authorization": "Bearer " + token    
    }
   
    payload = {'message': msg}
    files = {'imageFile': open(picURI, 'rb')}
    r = requests.post(url, headers = headers, params = payload, files = files)
    return r.status_code


# =============================================================================
# #自定義想取得的前前陣子天數漫畫
# today = datetime.datetime.today().date()
# print('today:',today)
# aday=timedelta(days=3)
# locale.setlocale(locale.LC_CTYPE,'chinese')
# day=(today - aday).strftime("%m月%d")
# =============================================================================
    
yesterday = "昨天"

driver = webdriver.Chrome('D:\\Program File\\Chrome Driver\\chromedriver.exe')

comic_url='https://www.manhuaren.com/'
currenturl=comic_url+"manhua-yiquanchaoren/"

driver.get(currenturl)
driver.maximize_window()

soup1=BeautifulSoup(driver.page_source,'lxml')
upload_date=soup1.find('span',class_='detail-list-title-3').text.split(" ")[0]
#print(upload_date)

#取得自定義天數的上傳日期
#upload_date=soup1.find('span',class_='detail-list-title-3').text.split("号")[0]

if str(upload_date).strip() == str(yesterday).strip() :
    driver.find_element_by_xpath('//*[@id="detail-list-select-1"]/li[1]/a').click()
    #取得點擊過後的網址連結
    currenturl=driver.current_url
    driver.get(currenturl)
    print("currenturl:",currenturl)

    soup = BeautifulSoup(driver.page_source,'lxml')
    
    toolbar=soup.find("div",class_="view-fix-top-bar")
    toolbar_title=toolbar.find("p",class_="view-fix-top-bar-title").text
    #toolbar_title內容為 一拳超人第177话-1/32
    
    chapter=toolbar_title.split("人")[1].split("-")[0]
    #取得此畫漫畫全部頁數
    totalpage=int(toolbar_title.split("/")[1])

    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                   "AppleWebKit/537.36 (KHTML, like Gecko)"
                   "Chrome/63.0.3239.132 Safari/537.36"}
    path="C:\\Users\\user\\Desktop\\one punch man"
    filepath=os.path.join(path,chapter)
    
    for i in range(1,totalpage+1):
        pic_loc=soup.find('div',{'id':'cp_img'})
        pic_loc1=pic_loc.find('img',class_="lazy")
        pic_url=pic_loc1['src'].split('?')[0]
        print(pic_url)       
        
        res=requests.get(pic_url, headers=headers)
        
        try:
            os.makedirs(filepath)
            imagename="page {}.jpg".format(i)
            imagepath=os.path.join(filepath,imagename)
            with open(imagepath,"wb") as f:
                f.write(res.content) 
            #取得網頁元素包含"下一页"的元件並點擊
            driver.find_element_by_link_text("下一页").click()
            #休息一下，讓網頁載入圖片
            time.sleep(randint(2,5))
            soup = BeautifulSoup(driver.page_source,'lxml')
        except FileExistsError:
            imagename="page {}.jpg".format(i)
            imagepath=os.path.join(filepath,imagename)
            with open(imagepath,"wb") as f:
                f.write(res.content)
            driver.find_element_by_link_text("下一页").click()
            time.sleep(randint(2,5))
            soup = BeautifulSoup(driver.page_source,'lxml')
    #關閉視窗
    driver.quit()
    
    try:
        os.chdir(filepath)
        print("檔案存在。")
        ary=[]
        for img in os.listdir(filepath):
            ary.append(int(img.replace('.jpg', '').split(" ")[1]))
        ary.sort()   
        for read_img in ary:
            img1="Page "+str(read_img)+".jpg"
            img_url=os.path.join(filepath,img1)
            print(img_url)
            msg="一拳超人"+"\n"+chapter+"-"+str(read_img)
            lineNotify(token, msg, img_url)
        print("success!!")    
    except FileNotFoundError:
        print("檔案不存在。")
        
else:
    print("漫畫沒有更新喔~~")
    driver.quit()
 

         
    





