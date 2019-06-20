# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 14:43:42 2019

@author: chensheng
"""

import requests
from lxml import etree
import re
import datetime
import time
import random
import json
import csv
import pandas as pd
import multiprocessing


def write(pt_name, rows):
    
    today = datetime.date.today()

    with open(r"C:\Users\chensheng\Desktop\赚客\%s_%s.csv"%(pt_name, today), "a",
              encoding="utf-8-sig", newline='') as f:
        
        writer = csv.writer(f) 
        writer.writerows(rows)
        
        
def load_page4(url, headers):#, proxies

    response = requests.get(url, headers=headers, verify=False)#, proxies=proxies

    text = response.content.decode("gbk", 'ignore')

    #print(text)
    return text  
       
#http://www.zuanke8.com/home.php?mod=space&uid=533904&do=index
#http://www.zuanke8.com/home.php?mod=space&uid=6968&do=profile 个人资料页 最全
#2019-06-11 最大uid 993291 最小uid 2
#"您指定的用户空间不存在" 
def zuanke(save_uid, final_uid):
    
    global save_uids
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
        "Cookie": "_uab_collina=156023877583519853668681; ki1e_2132_saltkey=LZX1FRWR; ki1e_2132_lastvisit=1560402302; ki1e_2132_connect_is_bind=0; ki1e_2132_nofavfid=1; ki1e_2132_atarget=1; ki1e_2132_smile=1D1; Hm_lvt_da6569f688ba2c32429af00afd9eb8a1=1560419049,1560737302,1560822348,1560908754; ki1e_2132_auth=aa17bEiQIn%2FUhTPqdOHnhSwMvxjChtsEIrzHa1Y%2BYYvyf7dJw0sgUircrJ6g123ksu%2BiKmzhOJjjqjfAWuHzMGxNU8E; ki1e_2132_lip=101.230.10.253%2C1560909088; ki1e_2132_home_diymode=1; ki1e_2132_pc_size_c=0; ki1e_2132_home_readfeed=1560934290; ki1e_2132_viewid=tid_6163119; ki1e_2132_forum_lastvisit=D_19_1560915214D_15_1560994552; ki1e_2132_ulastactivity=1560994552%7C0; td_cookie=552492724; ki1e_2132_sendmail=1; ki1e_2132_lastcheckfeed=877429%7C1560995258; ki1e_2132_checkfollow=1; ki1e_2132_checkpm=1; ki1e_2132_lastact=1560995258%09connect.php%09check; Hm_lpvt_da6569f688ba2c32429af00afd9eb8a1=1560995259; amvid=9398739f8adfc2e684122d5c11f9b1df"
    }
    
    try:
        for uid in range(save_uid, final_uid):
            
            print(uid)
            save_uids[0] = uid
            
            url = "http://www.zuanke8.com/home.php?mod=space&uid={0}&do=profile".format(uid)
            
            proxies = {'http': '47.112.80.214:8118'}
            html = load_page4(url, headers)#, proxies 
            #print(html)
            
            keywords = ["请重新注册", "用户空间不存在", "空间已被锁定"]
            
            #all函数测试迭代对象中是否所有条件都成立
            #all([True,False,True]) 结果为False
            #any测试是否至少有一个条件成立
            #any([True,False,False]) 结果为True
            
            if all(keyword not in html for keyword in keywords):
                
                selector = etree.HTML(html)
                              
                #回贴数
                aa = selector.xpath("//ul[@class='cl bbda pbm mbm']/li/a[3]/text()")[0]
                response = aa.replace("回帖数", "").replace(" ","")
                #print(response)

                #主题数
                bb = selector.xpath("//ul[@class='cl bbda pbm mbm']/li/a[4]/text()")[0]
                topic = bb.replace("主题数", "").replace(" ","")
                #print(topic)
                
                #昵称
                nickname = selector.xpath("//h2[@class='xs2']/a/text()")[0]
                #print(nickname)
                
                #用户组                
                user_group = selector.xpath("//div[@class='pbm mbm bbda cl'][2]/ul[1]/li/span/a/text()")[0]
                #print(user_group)
                
                #注册时间 
                if "在线时间" in html:                            
                    ee = selector.xpath("//div[@class='pbm mbm bbda cl'][2]/ul[@id='pbbs']/li[2]/text()")[0]
                else:
                    ee = selector.xpath("//div[@class='pbm mbm bbda cl'][2]/ul[@id='pbbs']/li[1]/text()")[0]
                register_time = ee.replace("注册时间", "")
                #print(register_time)

                #最后访问时间
                if "在线时间" in html: 
                    ff = selector.xpath("//div[@class='pbm mbm bbda cl'][2]/ul[@id='pbbs']/li[3]/text()")[0]
                else:
                    ff = selector.xpath("//div[@class='pbm mbm bbda cl'][2]/ul[@id='pbbs']/li[2]/text()")[0]
                last_login_time = ff.replace("最后访问", "")
                #print(last_login_time)
                
                #上次活动时间
                if "在线时间" in html:
                    gg = selector.xpath("//div[@class='pbm mbm bbda cl'][2]/ul[@id='pbbs']/li[4]/text()")[0] 
                else:
                    gg = selector.xpath("//div[@class='pbm mbm bbda cl'][2]/ul[@id='pbbs']/li[3]/text()")[0]
                lacst_active_time = gg.replace("上次活动时间", "") 
                #print(lacst_active_time)
                
                kws = ["买家信用", "卖家信用"]
                                  
                #积分数
                if all(kw in html for kw in kws):
                    hh = selector.xpath("//div[@class='bm_c u_profile']/div[@id='psts']/ul[@class='pf_l']/li[4]/text()")[0]
                elif any(kw in html for kw in kws):
                    hh = selector.xpath("//div[@class='bm_c u_profile']/div[@id='psts']/ul[@class='pf_l']/li[3]/text()")[0]
                else:
                    hh = selector.xpath("//div[@class='bm_c u_profile']/div[@id='psts']/ul[@class='pf_l']/li[2]/text()")[0]
                point = hh.replace("积分", "") 
                #print(point)
                
                #果果数
                if all(kw in html for kw in kws):
                    ii = selector.xpath("//div[@class='bm_c u_profile']/div[@id='psts']/ul[@class='pf_l']/li[5]/text()")[0]
                elif any(kw in html for kw in kws):
                    ii = selector.xpath("//div[@class='bm_c u_profile']/div[@id='psts']/ul[@class='pf_l']/li[4]/text()")[0]
                else:    
                    ii = selector.xpath("//div[@class='bm_c u_profile']/div[@id='psts']/ul[@class='pf_l']/li[3]/text()")[0]                   
                guo = ii.replace("果果", "") 
                #print(ii)
                
                #好友数
                kk = selector.xpath("//ul[@class='cl bbda pbm mbm']/li/a[1]/text()")[0]
                friend = kk.replace("好友数", "").replace(" ","")  
                #print(friend)
                
                               
                row = [
                    response, topic, 
                    nickname, user_group, 
                    register_time, last_login_time,
                    lacst_active_time, point,
                    guo, friend, uid
                ]
                
                print(row)
                
                write("zuanke_users_info", [row])
                
            if uid%2 == 0: 
                time.sleep(random.randint(1, 2))
                        
    except Exception as e:
        
        print(str(e))
        
        
if __name__ == '__main__':
    
    save_uids = [328794, 600001]#993291 600001
    
    while True: 
        
        start = time.time()
        
        save_uid = save_uids[0]
        final_uid = save_uids[1]
        
        #赚客吧注册用户info
        zuanke(save_uid, final_uid)            
        
        print('总耗时step_href：%.5f秒' % float(time.time()-start))
        print('save_uids: %s' % save_uids[0])
        print('final_uids: %s' % save_uids[1])
        
        if save_uid == final_uid-1:
            break
        
        time.sleep(random.randint(30, 45))
        
