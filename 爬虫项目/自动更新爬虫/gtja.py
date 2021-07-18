#!user/bin/python
# _*_ coding: utf-8 _*_
 
# @File : gtja.py
# @Version : 1.0
# @Author : benty
# @Email : matengmeng@gmail.com
# @Time : 2021/05/25 15:03:28
# Description: 国泰君安
# Motto: 6Z2S6Z2S5a2Q6KG/IOaCoOaCoOaIkeW/gyDkvYbkuLrlkJvmlYUg5rKJ5ZCf6Iez5LuK 

import time,requests,re
from pyquery import PyQuery as pq
from sql import *
from bs4 import BeautifulSoup as bs


start_pys=time.perf_counter()

# 过滤content字段函数
def content_filter(content):
    '''过滤content字段剔除html标签为\n'''
    soup=bs(content,"html.parser")
    pre_content=soup.get_text("\n")
    # #替换特殊字符
    pre_content=pre_content.replace("\uf09f","")
    #下面是将多个换行替换成一个
    pre_content=re.sub(r"\n{1,}","\n",pre_content)
    return pre_content


def paper(url):
    '''国泰君安招聘项目,本项目只有一个网址,需用js判断'''
    res=requests.get(url)
    res.encoding=res.apparent_encoding
    doc=pq(res.text)
    evejobs=doc("div.eve-job").length
    for i in range(evejobs):
        data={}
        # 岗位所属部门-----投资银行部
        data['department'] = doc("div.eve-job").eq(i).parent().find("div.department-title").text()
        # 岗位url--用来去重------/career/apply/job/jid/853/
        data['source_url']=doc("div.eve-job").eq(i).find("div.job-title a.apply-btn").attr("href")
        # 岗位title
        data['title']=doc("div.eve-job").eq(i).find("ul.cont div.sm-li span").eq(0).text()
        # 工作地点
        data['job_addr']=doc("div.eve-job").eq(i).find("ul.cont div.sm-li span").eq(1).text()
        # 学历要求
        data['job_education']=doc("div.eve-job").eq(i).find("ul.cont div.sm-li span").eq(2).text()
        # 岗位内容
        data['content']=doc("div.eve-job").eq(i).find("div.bg-li").html()
        data['content']=content_filter(data['content']) #过滤标签并转换为\n
        # 招聘others字段,所属分公司
        data['others']=doc("div.eve-job").eq(i).parent().parent().find("div.business span").text()
        data['end_time']=data['job_number']=data['publish_time']=None
        data['securities']="国泰君安"
        data['job_category']="校园招聘" #它没有社会招聘
        print(data["source_url"])
        if data["title"]:
            time.sleep(0.5)
            savedb(data)


def savedb(data):
    '''将传入的数据保存到数据库'''
    k=Sql()
    try:
        if not k.qutwo(data["source_url"]):
            if not data["publish_time"]:
                data["publish_time"]=prev_day
            sql="INSERT INTO `"+k.table+"` (`id`, `securities`, `title`, `content`, `job_addr`, `job_category`, `publish_time`, `department`, `job_number`, `job_education`, `end_time`, `others`, `source_url`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            k.execute(sql,[data['securities'],data['title'],data['content'],data['job_addr'],data['job_category'],data['publish_time'],data['department'],data['job_number'],data['job_education'],data['end_time'],data['others'],data['source_url']])
            print("__成功添加到数据库__")
        else:
            print("存在相同内容"+"----------------"+data['source_url'])
    except Exception as e:
        print(e)
    finally:
        k.close()




'''
# 大部分爬虫通用,先爬列表页,然后提取详情页,之后对比是否是昨天的文章进行采集
# @description 国泰君安
# @author benty 2021-05-28 15:43:53
# @mail matengmeng@gmail.com
# @allflag 参数说明 是否要跟踪下一页以及是否比对昨天时间 true比对时间或者可以进入下一页.
# @info 国泰君安只有一个页面,没有allflag一说
#
'''

if __name__=="__main__":
    url="https://hr.gtja.com/recruitment/index/campus"
    paper(url)
    # time.sleep(2)
    endt_pye=time.perf_counter()-start_pys
    print("程序一共耗时 %.3f 秒" % endt_pye)
    