#!user/bin/python
# _*_ coding: utf-8 _*_
 
# @File : citics.py
# @Version : 1.0
# @Author : benty
# @Email : matengmeng@gmail.com
# @Time : 2021/05/28 16:08:53
# Description:   中信证券
# Motto: 6Z2S6Z2S5a2Q6KG/IOaCoOaCoOaIkeW/gyDkvYbkuLrlkJvmlYUg5rKJ5ZCf6Iez5LuK 

from csc import savedb
import time,requests
import datetime
from sql import Sql
import traceback
import math,re
from bs4 import BeautifulSoup as bs
from collections import defaultdict
start_pys=time.perf_counter()
headers={
    "Content-Type":"application/x-www-form-urlencoded",
    "Connection":"keep-alive",
    "Referer":"https://careers.citics.com/",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
    "Accept":"application/json,*/*;"
}

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
def paper(jsondata):
    '''获取中信详情页的页面,需要携带cookie登录才可以查看'''
    # 这里不用考虑去重,因为在list页遍历的时候做了判断数据库中没有才访问的这个详情页,也就是说只要访问这里就一定要保存
    jsonurl="https://global.kong.citics.com/api/v1/recruit/getPositionInfo?sysNo=CSE001&deptNo="+jsondata["deptNo"]+"&positionNo="+jsondata["positionid"]+"&recruitType=05&deptype=Branch&practice="
    res=requests.get(jsonurl,headers=headers)
    res.encoding=res.apparent_encoding
    infojson=res.json()["positionInfo"]
    # 招聘类型
    jsondata["job_category"]=infojson["type"]
    # 招聘正文 这里需要拼接
    jsondata["content"]=""
    if infojson["positionDesc"]:
        jsondata["content"]+="岗位职责说明\n"+infojson["positionDesc"]
    if infojson["qualification"]:
        jsondata["content"]+="\n任职资格要求\n"+infojson["qualification"]
    # 招聘发布时间,没有此选项就定为采集的今天
    jsondata["publish_time"]=datetime.datetime.now().strftime("%Y-%m-%d")
    # 来源url,这里定义为部门id-文章id
    jsondata["source_url"]=infojson["deptNo"]+"-"+infojson["positionNo"]
    # 定义哪个证券公司
    jsondata["securities"]="中信证券"
    if jsondata["title"]:
        savedb(jsondata)


def savedb(data):
    k=Sql()
    try:
        sql="INSERT INTO `"+k.table+"` (`id`, `securities`, `title`, `content`, `job_addr`, `job_category`, `publish_time`, `department`, `job_number`, `job_education`, `end_time`, `others`, `source_url`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        k.execute(sql,[data['securities'],data['title'],data['content'],data['job_addr'],data['job_category'],data['publish_time'],data['department'],data['job_number'],data['job_education'],data['end_time'],data['others'],data['source_url']])
        print("__成功添加到数据库__"+data["source_url"])
    except:
        traceback.print_exc()
        print("保存数据库异常")
    finally:
        k.close()

def listpage(page=1):
    '''先获取json职位列表,这里需要遍历所有'''
    url="https://global.kong.citics.com/api/v1/recruit/getPositionList"
    print("当前正在请求页:::"+str(page))
    data={
    "sysNo": "CSE001",
    "recruitType": "05",
    "deptype": "Branch",
    "size": 20,
    "start": page
    }
    res=requests.post(url,headers=headers,data=data)
    res.encoding=res.apparent_encoding
    result=res.json()["positionList"]
    if len(result)==0:
        print("空数据")
        return
    # 遍历岗位的每一条具体信息
    for onejson in result:
        tabledata=defaultdict(lambda:None)
        # 所属分公司
        tabledata["others"]=onejson["companyName"]
        # 所属部门
        tabledata["department"]=onejson["deptName"]
        # 到期时间
        tabledata["end_time"]=onejson["reqendDate"]
        # 岗位名称
        tabledata["title"]=onejson["positionName"]
        # 岗位id
        tabledata["positionid"]=onejson["positionNo"]
        # 部门id
        tabledata["deptNo"]=onejson["deptNo"]
        # 工作地点
        tabledata["job_addr"]=onejson["workplace"]
        # 定义一个source_url
        source_url=tabledata["deptNo"]+"-"+tabledata["positionid"]
        # 开始把字典信息传递给详情页
        k=Sql()
        # 判断是否存在唯一id,存在说明不用添加数据库了
        if not k.qutwo(source_url):
            paper(tabledata)
            time.sleep(1)
        else:
            print("数据已经存在!")
        # break
    # 判断是否需要到下一页
    endpage=math.ceil(res.json()["count"]/20)
    if page< endpage:#不是最后一页就一直递归
        time.sleep(2)
        listpage(page=page+1)



'''
# 大部分爬虫通用,先爬列表页,然后提取详情页,之后对比是否是昨天的文章进行采集
# @description 
# @author benty 2021年6月3日 14:59:58
# @mail matengmeng@gmail.com
# @allflag 参数说明 是否要跟踪下一页以及是否比对昨天时间 true比对时间或者可以进入下一页.
# @info 以后自动执行定时任务时allflag参数为
# 分支机构社会招聘  https://careers.citics.com/jobs/professionals_WM/
# 其他岗位没有具体信息 点击详情需要登录才可以进行查看....

岗位列表在这个链接中请求:POST   https://global.kong.citics.com/api/v1/recruit/getPositionList
列表POST数据
data={
    "sysNo": "CSE001"
    "recruitType": "05"
    "deptype": "Branch"
    "size": 20
    "start": 1
}



以后执行这个爬虫只用执行listpage()就ok,没有allflag选项,因为列表岗位没有时间属性页没有按照时间属性排序

'''

if __name__=="__main__":
    listpage()















    endt_pye=time.perf_counter()-start_pys
    print("程序一共耗时 %.3f 秒" % endt_pye)