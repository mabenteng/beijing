#!user/bin/python
# _*_ coding: utf-8 _*_
 
# @File : htzq.py
# @Version : 1.0
# @Author : benty
# @Email : matengmeng@gmail.com
# @Time : 2021/05/26 09:54:35
# Description: 采集海通证券的前程无忧项目
# Motto: 6Z2S6Z2S5a2Q6KG/IOaCoOaCoOaIkeW/gyDkvYbkuLrlkJvmlYUg5rKJ5ZCf6Iez5LuK 

import time,math,collections
import requests
import re,json,random
from bs4 import BeautifulSoup as bs
from hashlib import md5
from sql import *
import traceback



start_pys=time.perf_counter()

headers= {
    # 'Host': 'weixin.sogou.com',
    'Connection': 'keep-alive',
    # 'Accept': 'text/html, */*; q=0.01',
    # 'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    # 'Referer': 'https://weixin.sogou.com/weixin?query=%E5%86%9B%E6%B0%91%E8%9E%8D%E5%90%88&_sug_type_=&s_from=input&_sug_=n&type=2&page=5&ie=utf8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    # 'Set-Cookie':'SNUID=1; domain=.sogou.com; path=/; expires=Thu, 01-Dec-1994 16:00:00 GMT'
    # 'cookie':'UM_distinctid=17849b7fde95a7-03eff9e74a246a-5771031-1fa400-17849b7fdea6e7; aliyungf_tc=0ad34eaa0bc833366341a163101e37f326a55e86b84bd6819ac56c2487e694ad; route=030e64943c5930d7318fe4a07bfd2a3c; JSESSIONID=C27824A0F7F089A9CA374ACB3A823D18; uuid=e52f2562-34cd-478a-a25e-d475921f180b; SERVERID=srv-omp-ali-portal11_80; Hm_lvt_94a1e06bbce219d29285cee2e37d1d26=1616144498,1616658796,1616721884; paperSearhType=1; CNZZDATA1261102524=591838861-1616142188-%7C1616750557; Hm_lpvt_94a1e06bbce219d29285cee2e37d1d26=1616755493'
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



def paper(url,jdata):
    '''海通证券的前程无忧招聘页面内容'''
    print("=======当前招聘详情页面是%s" % url)
    info=requests.get(url,headers=headers)
    info.encoding=info.apparent_encoding
    soup=bs(info.text,"html.parser")
    data=collections.defaultdict(lambda:None)
    # 岗位名称
    data["title"]=jdata["title"]
    # 招聘部门
    data["securities"]="海通证券"
    # others定义为分公司
    data["others"]=jdata["others"]
    # 工作地点
    data["job_addr"]=jdata["job_addr"]
    # 工作经验要求
    '''
    '''
    # 学历要求
    data["job_education"]=jdata["job_education"]
    # 招聘人数
    data["job_number"]=jdata["job_number"]
    # 发布时间=========05-11发布
    data["publish_time"]=jdata["publish_time"]
    # 所属部门
    data["department"]=jdata["department"]
    # 职位详细信息
    # 先删除职位下的div无用元素
    xx=soup.find_all(class_="tCompany_main")[0].select("div.tBorderTop_box div.bmsg.inbox")[0].find_all("div",recursive=False)
    [x.extract() for x in xx]
    data["content"]=soup.find_all(class_="tCompany_main")[0].select("div.tBorderTop_box div.bmsg.inbox")[0].decode_contents()
    data['content']=content_filter(data['content']) #过滤标签并转换为\n
    # url去掉html后面的后缀,以免以后参数变化导致不能去重
    data["source_url"]=url.replace("?s=01&t=7","")
    # 时间和招聘类型可以由上个页面传递过来.
    data["job_category"]="社会招聘"
    # print(data)
    if data["title"]:
        # 保存的数据库
        savedb(data)
    return data

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

def listpage(curpage=1,allflag=False):
    '''海通证券列表页的处理,注意这里要进行解密操作才可以'''
    # 参数从第一页开始爬,第二个参数是要不要爬全部数据(递归爬)
    # 注意这里的allflag有两个作用,1.是否判断时间是否等于昨天才访问详情页 2.是否为true就往下一页递归
    print("============正在访问第%d页================" % curpage)
    key="tuD&#mheJQBlgy&Sm300l8xK^X4NzFYBcrN8@YLCret$fv1AZbtujg*KN^$YnUkh"
    keyindex=random.randint(1,41) #返回随机下标
    keyindex=7
    pagecount=10 #每页多少条数据
    key15=key[keyindex:keyindex+15] #取15个随机数
    # print(key15)
    oParams = { "ctmid":"1714988","pagesize":pagecount,"pagenum":str(curpage),"coid":"","divid":"","jobarea":"","keyword":""}
    sParams=json.dumps(oParams).replace(" ","")
    md5_value="coapi"+sParams+key15
    obj={"key":keyindex,"sign":md5(md5_value.encode()).hexdigest(),"params":sParams}
    # 定义一个当前时间戳
    cur_timep=int(time.time()*1000)
    # api 地址
    url="https://coapi.51job.com/job_list.php?jsoncallback=jQuery300004316137724455249_"+str(cur_timep)+"&key="+str(keyindex)+"&sign="+obj["sign"]+"&params="+sParams
    info=requests.get(url,headers=headers)
    info.encoding=info.apparent_encoding
    # 解析jsonp为json格式
    infojson=info.text[42:-1]
    infojson=json.loads(infojson)
    infobody=infojson["resultbody"]
    # print(infobody)
    if "调用成功" in infojson["message"]:
        # 提取每一条json数据进行遍历
        for jobjson in infobody["joblist"]:
            jdata={}
            jdata["publish_time"]=re.match(r"(\d{4}-\d{2}-\d{2})",jobjson["issuedate"]).group(1)
            if prev_day==jdata["publish_time"]:#这里精确判断时间
                jdata["others"]=jobjson["coname"] #分公司名字
                jdata["department"]=jobjson["divname"] #所属部门
                jdata["title"]=jobjson["jobname"]
                jdata["job_education"]=jobjson["degreefrom"]
                jdata["job_number"]=jobjson["jobnum"]
                jdata["job_addr"]=jobjson["workareaname"]
                paperurl="https://jobs.51job.com/all/"+jobjson["jobid"]+".html?s=01&t=7"
                # print(jdata)
                time.sleep(2)
                paper(paperurl,jdata)
            else:
                print("时间不等于昨天不采集")
            # break
        # 判断需要分多少页数据,向上取整
        endpage=math.ceil(int(infobody["totalnum"])/pagecount) #14页
        if curpage < endpage: # 不是最后一页继续往下请求,这里不能用allflag阻止下一页,因为岗位不按日期排序,所以要全部遍历
            time.sleep(2)
            listpage(curpage=curpage+1,allflag=allflag)
    else:
        print(infojson)

        





'''
#列表页剖析: 目前是网页打开会自动加载ajax并init数据,如果想要爬取多页,必须分析构造url的api
获得工作地址列表的api:
https://coapi.51job.com/job_list.php?jsoncallback=jQuery300004316137724455249_1622019039930&key=13&sign=签名&params=字典参数&_=时间戳
jQuery30008665280730187643_1622081654361(
传入的params字典参数是: 看js源码注释.最多500页,每页100条数据
params: {"ctmid":"1714988","pagesize":10,"pagenum":"1","coid":"","divid":"","jobarea":"","keyword":""}

查看js的加密key为:key: "tuD&#mheJQBlgy&Sm300l8xK^X4NzFYBcrN8@YLCret$fv1AZbtujg*KN^$YnUkh",//这里一共有64个字符
var keyindex = Math.floor(40 * Math.random()) + 1,//初始化keyindex为1-40
            sParams = JSON.stringify(oParams); params参数序列化为json格式
return {
            key: keyindex,#随机返回一个下标,比如14
            sign: md5("coapi" + sParams + this.key.substr(keyindex, 15)),#生成一个md5用来验证
            params: sParams
        }
目前请求返回的json数据是jsonp格式,用来跨域调用,需要构造key是索引下标,sign是签名比对,params是传递的json字符串

2021年5月27日 18:06:15
现在可以采用策略自取爬取更新,但是每一页都要一个一个访问才能判断是否重复,变相的增大了访问量.
最好的方式是获得列表页的10个结果.然后遍历一遍id进行去重
最好的办法是提取年月日与昨天对比,如果时间相等就进行访问,否则就不进行访问

'''
'''
# 大部分爬虫通用,先爬列表页,然后提取详情页,之后对比是否是昨天的文章进行采集
# @description 海通证券
# @author benty 2021-05-28 15:36:25
# @allflag 参数说明 是否要跟踪下一页以及是否比对昨天时间 true比对时间或者可以进入下一页.
# @info 以后自动执行定时任务时allflag参数为True,因为海通证券的招聘职位不按时间排序,所以所有页面都要遍历一遍,且这里的allflag不能对下一页判断
#
'''


if __name__=="__main__":
    infourl="https://jobs.51job.com/all/115616698.html?s=01&t=7" #招聘详情页
    urls=["https://jobs.51job.com/all/115616698.html?s=01&t=7"]
    # paper(infourl)
    # 直接初始化51job的api接口并进行调用
    listpage(1,allflag=True)
    endt_pye=time.perf_counter()-start_pys
    print("程序一共耗时 %.3f 秒" % endt_pye)