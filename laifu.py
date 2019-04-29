# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 23:42:25 2019
@author: Administrator
"""

import requests
from lxml import etree
import re
import datetime
import time
import random
import json
import csv
import pickle


def load_page3(url, headers):

    response = requests.get(url, headers=headers, verify=False)#

    text = response.content.decode("utf-8", 'ignore')

    #print(text)
    return text


def save_pic(path, img):   
    
    with open(path, 'wb') as f:        
        f.write(img)
            
                   
def write_pickle(content):
    
    with open(r"E:\laugh\laugh_dict", "wb") as f:
        pickle.dump(content,f)
 
        
def read_pickle():
    
    with open(r"E:\laugh\laugh_dict", "rb") as f:        
        content = pickle.load(f)
    
    return content
    
    
def laifu():
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.8)"} 
    
    laugh = set()

    for page in range(2, 101):
        
        url = r"http://www.xxxx.com/tupian/index_{0}.htm".format(page)
        rq = load_page3(url, headers)
                
        selector = etree.HTML(rq)
        pics = selector.xpath("//section[@class='pic-content']/a/img/@src") 
        title = selector.xpath("//section[@class='pic-content']/a/img/@alt") 
        
        #剔除重复值
        fetch = set(zip(pics, title))
        link_title = read_pickle() #读出所有键，集合化
        rest_fetch = fetch - link_title #求集合差集
        
        for item in (x for x in rest_fetch):
            
            if "jpg" in item[0]:
                pic = requests.get(item[0]).content
                path = r"E:\laugh\imgs\{0}.jpg".format(item[1])
                time.sleep(random.randint(1, 5))
                save_pic(path, pic)
                
                laugh.add(item)
    
        write_pickle(laugh)
        print(page)            
    
if __name__ == '__main__':
    
    laifu()
