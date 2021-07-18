#!user/bin/python
# _*_ coding: utf-8 _*_
 
# @File : csc.py
# @Version : 1.0
# @Author : benty
# @Email : matengmeng@gmail.com
# @Time : 2021/05/28 18:13:15
# Description:  中信建投证券
# Motto: 6Z2S6Z2S5a2Q6KG/IOaCoOaCoOaIkeW/gyDkvYbkuLrlkJvmlYUg5rKJ5ZCf6Iez5LuK 

import time,re
import datetime
from sql import *
import traceback




start_pys=time.perf_counter()
import requests
from bs4 import BeautifulSoup as bs
import collections

headers={
    "Accept":"text/html",
    "Connection":"keep-alive",
    "Content-Type":"application/x-www-form-urlencoded",
    "Referer":"https://job.csc.com.cn/scripts/mgrqispi.dll?appname=hrsoft2000&prgname=REC2_RESUME_STAFF_P&arguments=-AC,-A,-A,-AB",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
}


def paper(url,data):
    '''获取招聘的详情信息内容'''
    info=requests.get(url,headers=headers)
    info.encoding=info.apparent_encoding
    soup=bs(info.text,"html.parser")
    data["title"]=soup.select_one("div.top_box_m h1").get_text()
    fieldinfo=soup.select("div.main_box_m div.leftbox ul li table tr")
    # 工作地点
    data["job_addr"]=fieldinfo[2].select("td")[-1].get_text()
    # 招聘类型
    # data["job_category"]=fieldinfo[0].select("td")[-1].select_one("span[style*='display:;']").get_text()
    # 所属部门
    data["department"]=fieldinfo[1].select("td")[-1].get_text()
    # 招聘人数
    data["job_number"]=fieldinfo[3].select("td")[-1].get_text()
    # 学历要求
    data["job_education"]=fieldinfo[4].select("td")[-1].get_text()
    # url
    data["source_url"]=url
    # 招聘详情
    soup.select_one("div.main_box_m div.leftbox").extract()
    data["content"]=re.sub(r"\n{1,}","\n",soup.select_one("div.main_box_m").get_text("\n") )
    data["securities"]="中信建投证券"
    if data["title"]:
        savedb(data)
    return data


def listpage(listurl,allflag=False):
    '''获取列表页的内容'''
    listx=["A","B","D"]
    for xstyle in listx:
        params={
        "APPNAME":"HRsoft2000",
        "PRGNAME":"REC2_RESUME_STAFF_P",
        "ARGUMENTS":"-AC,input_select,input_address,REC_STYLE,input_depart",
        "input_select":"",
        "input_depart":"",
        "input_address":"",
        "REC_STYLE":xstyle,
        "Submit":"%CB%D1%CB%F7"
        }
        job_category={"A":"校园招聘","B":"社会招聘","D":"实习生招聘"}
        info=requests.post(listurl,data=params,headers=headers)
        info.encoding=info.apparent_encoding
        soup=bs(info.text,"html.parser")
        joblist=soup.select("div.main_box div.job_list1")[:-1]
        if len(joblist)>0:
            for onejobtr in joblist:
                starttime=onejobtr.select("span.job_list_e1")[0].get_text()
                # print(starttime)
                starttimeobj = datetime.datetime.strptime(starttime, '%d/%m/%Y') #将时间22/04/2021转换为时间对象
                starttime=starttimeobj.strftime("%Y-%m-%d") #将时间对象转换为2021-04-22格式
                endtime=onejobtr.select("span.job_list_e1")[1].get_text()
                endtimeobj=datetime.datetime.strptime(endtime,'%d/%m/%Y')
                endtime=endtimeobj.strftime("%Y-%m-%d")
                data=collections.defaultdict(lambda:None)
                data['publish_time']=starttime or datetime.datetime.now().strftime("%Y-%m-%d")
                data["end_time"]=endtime
                data["job_category"]=job_category[xstyle]
                # data["job_category"]=soup.select_one("select[name='REC_STYLE'] option:checked").get_text()
                tid=onejobtr.select_one("span.job_list_b1 a").get("href")
                PositionID=re.search(r"\d+",tid)[0]
                # 获取当前岗位的url,这里要分析岗位详情
                paperurl="https://job.csc.com.cn/scripts/"+"mgrqispi.dll?Appname=HRsoft2000&Prgname=REC2_RESUME_POSITION_P&ARGUMENTS=-AC,-A  "+PositionID+",-AL"
                # 拼接详情页的url开始请求
                if allflag or prev_day==starttime:#时间等于昨天就访问
                    time.sleep(2)
                    paper(paperurl,data)
                else:
                    print("时间不等于昨天不采集")
                # break
        else:
            print("当前分类没有招聘信息.")


def savedb(data):
    '''判断链接不重复就保存到数据库'''
    k=Sql()
    try:
        if not k.qutwo(data["source_url"]):
            # 如果数据库已经存在这条url,说明以前已经添加过\
            sql="INSERT INTO `"+k.table+"` (`id`, `securities`, `title`, `content`, `job_addr`, `job_category`, `publish_time`, `department`, `job_number`, `job_education`, `end_time`, `others`, `source_url`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            k.execute(sql,[data['securities'],data['title'],data['content'],data['job_addr'],data['job_category'],data['publish_time'],data['department'],data['job_number'],data['job_education'],data['end_time'],data['others'],data['source_url']])
            print("__成功添加到数据库__"+data["source_url"])
        else:
            print("存在相同的内容"+data["source_url"])
    except:
        traceback.print_exc()
    finally:
        k.close()



'''#
# 一共有三个页面.实习生/校招和社会招聘,url=https://job.csc.com.cn/scripts/mgrqispi.dll
POST请求
参数:
# 大部分爬虫通用,先爬列表页,此项目没有下一页.然后提取详情页,之后对比是否是昨天的文章进行采集
# @description 中信建投证券
# @author benty 2021年5月31日 17:06:41
# @mail matengmeng@gmail.com
# @allflag 参数说明 是否要跟踪下一页以及是否比对昨天时间 true比对时间或者可以进入下一页.
# @info 以后自动执行定时任务时allflag参数为True就是所有时间全都过一遍,重复就不保存数据库
# 以后部署线上就需要用allflag=False只采集昨天的内容
'''
if __name__=="__main__":
    url="https://job.csc.com.cn/scripts/mgrqispi.dll" #提交post数据
    listpage(url,False)
    endt_pye=time.perf_counter()-start_pys
    print("程序一共耗时 %.3f 秒" % endt_pye)