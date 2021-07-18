#!user/bin/python
# _*_ coding: utf-8 _*_
 
# @File : htsc.py
# @Version : 1.0
# @Author : benty
# @Email : matengmeng@gmail.com
# @Time : 2021/06/03 15:45:05
# Description: 华泰证券
# Motto: 6Z2S6Z2S5a2Q6KG/IOaCoOaCoOaIkeW/gyDkvYbkuLrlkJvmlYUg5rKJ5ZCf6Iez5LuK 

import time,re
from collections import defaultdict
import requests,datetime,traceback
from sql import Sql

prev_day=(datetime.datetime.now()- datetime.timedelta(days=1)).strftime("%Y-%m-%d")
headers={
    "Accept":"application/json,*/*",
    "Connection":"keep-alive",
    "Referer":"http://www.hotjob.cn/wt/HTSC/web/index/social",
    "X-Requested-With":"XMLHttpRequest",
    "Accept-Encoding":"gzip,deflate",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
}


def listpage(url,allflag=False):
    '''获取某个类型的json岗位列表,已经包含了所有信息'''
    res=requests.get(url)
    res.encoding=res.apparent_encoding
    result=res.json()
    print(url[134:149]+"---当前页是"+str(result["page"]))
    # 如果结果有值就遍历
    if result["postList"]:
        for onejson in result["postList"]:
            # 每一条的json数据
            jsondata=defaultdict(lambda:"")
            # 发布时间
            jsondata["publish_time"]=onejson["publishDate"]
            # 岗位标题
            jsondata["title"]=onejson["postName"]
            # 所属部门
            jsondata["department"]=onejson["deptOrgName"]
            # 结束时间
            jsondata["end_time"]=onejson["endDate"]
            # 学历要求
            jsondata["job_education"]=onejson.get("education")
            # 工作地点
            jsondata["job_addr"]=onejson["workPlace"]
            # 招聘人数
            jsondata["job_number"]=onejson["recruitNum"]
            # 额外字段拼接信息
            print(onejson["postId"])
            jsondata["others"]="职位类别: "+onejson.get("postType","")+"\n工作类型: "+onejson.get("workType","")+"\n工作年限要求: "+onejson.get("workYears","")
            # json公司名字
            jsondata["securities"]="华泰证券"
            # 招聘类型
            if "recruitType=2" in url:
                jsondata["job_category"]="社会招聘"
            elif "recruitType=12" in url:
                jsondata["job_category"]="实习生招聘"
            elif "recruitType=1" in url:
                jsondata["job_category"]="校园招聘"
            else:
                jsondata["job_category"]="社会招聘"
            # 文章链接 source_url 这里保存
            jsondata["source_url"]="htsc-"+str(onejson["postId"])
            # 文章正文信息
            jsondata["content"]=""
            if onejson.get("workContent"):
                jsondata["content"]+="职位描述: \n"+onejson["workContent"].replace("<br>","\n")+"\n"
            if onejson.get("serviceCondition"):
                jsondata["content"]+="任职要求: \n"+onejson["serviceCondition"].replace("<br>","\n")
            # print(jsondata)
            # break
            if prev_day==jsondata["publish_time"]:#定义是否全爬,否则只比对昨天的文章
                #如果岗位时间是昨天发布的,或者直接全局保存
                k=Sql()
                # 如果数据库中不存在这个url就添加保存
                if not k.qutwo(jsondata["source_url"]):
                    savedb(jsondata)
                else:
                    print("已经添加到数据库")
            else:
                # 如果时间不等于昨天还不是全都爬取,那就退出函数.在for循环之内不能用return
                print("退出函数,不是昨天的岗位信息不往下执行")
                return
    # 进行判断是否到下一页,存在allflag就所有页面全部遍历,否则
    if result["page"]!=result["pageCount"]:
        #将当前页+1访问下一页
        time.sleep(2)
        listpage(re.sub(r'page=\d+',"page="+str(result["page"]+1),url))






def savedb(data):
    k=Sql()
    try:
        if not data["publish_time"]:
            data["publish_time"]=prev_day
        sql="INSERT INTO `"+k.table+"` (`id`, `securities`, `title`, `content`, `job_addr`, `job_category`, `publish_time`, `department`, `job_number`, `job_education`, `end_time`, `others`, `source_url`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        k.execute(sql,[data['securities'],data['title'],data['content'],data['job_addr'],data['job_category'],data['publish_time'],data['department'],data['job_number'],data['job_education'],data['end_time'],data['others'],data['source_url']])
        print("__成功添加到数据库__"+data["source_url"])
    except:
        traceback.print_exc()
        print("保存数据库异常")
    finally:
        k.close()



start_pys=time.perf_counter()








'''
# 
# @description 华泰证券 ----有社会招聘/校园招聘/实习生招聘   这个有时间可做昨天时间判断
# @author benty 2021-06-03 15:47:37
# @param 
# @return 
# 
社会招聘   http://www.hotjob.cn/wt/HTSC/web/json/position/list?positionType=&comPart=&sicCorpCode=&brandCode=1&releaseTime=&trademark=1&useForm=&recruitType=2&projectId=&lanType=1&workPlace=&page=1&site=&keyWord=
校园招聘   http://www.hotjob.cn/wt/HTSC/web/json/position/list?positionType=&comPart=&sicCorpCode=&brandCode=1&releaseTime=&trademark=1&useForm=&recruitType=1&projectId=&lanType=1&workPlace=&page=1&site=&keyWord=
实习生招聘 http://www.hotjob.cn/wt/HTSC/web/json/position/list?positionType=&comPart=&sicCorpCode=&brandCode=1&releaseTime=&trademark=1&useForm=&recruitType=12&projectId=101501&lanType=1&workPlace=&page=1&site=&keyWord=
实习生2    http://www.hotjob.cn/wt/HTSC/web/json/position/list?positionType=&comPart=&sicCorpCode=&brandCode=1&releaseTime=&trademark=1&useForm=&recruitType=12&projectId=100203&lanType=1&workPlace=&page=1&site=&keyWord=
# 上面是三个类型的url,是get方式获取,返回json类型
postSyncToXiaojianren: 1 同步给谁?




以后部署到后台就直接执行listpage(url)就可以,因为按时间排序,所以只判断昨天的岗位,如果不是就停止当前类型的向下抓取
'''
if __name__=="__main__":
    urls=[# 三个url分别对应社会招聘/校园招聘/实习生招聘/实习生招聘2
        "http://www.hotjob.cn/wt/HTSC/web/json/position/list?positionType=&comPart=&sicCorpCode=&brandCode=1&releaseTime=&trademark=1&useForm=&recruitType=2&projectId=&lanType=1&workPlace=&page=1&site=&keyWord=",
        "http://www.hotjob.cn/wt/HTSC/web/json/position/list?positionType=&comPart=&sicCorpCode=&brandCode=1&releaseTime=&trademark=1&useForm=&recruitType=1&projectId=&lanType=1&workPlace=&page=1&site=&keyWord=",
        "http://www.hotjob.cn/wt/HTSC/web/json/position/list?positionType=&comPart=&sicCorpCode=&brandCode=1&releaseTime=&trademark=1&useForm=&recruitType=12&projectId=101501&lanType=1&workPlace=&page=1&site=&keyWord=",
        "http://www.hotjob.cn/wt/HTSC/web/json/position/list?positionType=&comPart=&sicCorpCode=&brandCode=1&releaseTime=&trademark=1&useForm=&recruitType=12&projectId=100203&lanType=1&workPlace=&page=1&site=&keyWord="
        ]
    for url in urls:
        listpage(url)
        # break
    endt_pye=time.perf_counter()-start_pys
    print("程序一共耗时 %.3f 秒" % endt_pye)


