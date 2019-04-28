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

import os


def load_page3(url, headers):

    response = requests.get(url, headers=headers, verify=False)#

    text = response.content.decode("utf-8", 'ignore')

    #print(text)
    return text


def save_pic(path, img):   
    
    with open(path, 'wb') as f:        
        f.write(img)
        

def isexist():
    '''
    1 检查是否与历史爬取重复
    2 删除重复项
    3 返回[(),...()]
    '''
    未完


def laifu():
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.8)"} 
    url = r"http://www.laifudao.com/tupian/index_2.htm"
    rq = load_page3(url, headers)
    
    selector = etree.HTML(rq)
    pics = selector.xpath("//section[@class='pic-content']/a/img/@src") 
    title = selector.xpath("//section[@class='pic-content']/a/img/@alt") 
    
    isexist(list(zip(pics, title)))
    
    for k, v in zip(pics, title):
        
        pic = requests.get(k).content
        path = r"C:\Users\Administrator\Desktop\pic\{0}.jpg".format(v)
        save_pic(path, pic)
        
        #time.sleep(1)
    
    
    
if __name__ == '__main__':
    
    laifu()
