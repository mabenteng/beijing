# coding=utf-8

'''
# 
# @description 中金公司每天更新职位信息
# @author benty 2021-05-25 09:42:44
# @url http://cicc.zhiye.com/szzw
# @return 
# 每天查看三天内的岗位信息,取昨天的日子,如果存在昨天的日期就抓取信息,否则就跳过完成任务.
'''
from sql import *
import requests,re
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup as bs


print(prev_day)
base_url="http://cicc.zhiye.com"

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


def listpage(url,allflag=False):
    '''传入一个列表页进行判断日期,日期相等就调用paper'''
    info=requests.get(url)
    info.encoding=info.apparent_encoding
    doc=pq(info.text)
    jobtr=doc("div.zwlb tr")
    # print(jobtr)
    # 从第二个开始遍历行
    for i in range(1,len(jobtr)):
        #如果招聘的日期等于昨天或者指定全部都要爬
        if prev_day==jobtr.eq(i).find("td").eq(5).text():
            infourl=jobtr.eq(i).find("td a").eq(2).attr("href")
            # 如果没有tr行就是没有结果,为空就return退出
            if infourl is None:
                print("没有任何更新")
                return
            paperurl=base_url+infourl
            print(paperurl+"----------"+jobtr.eq(i).find("td").eq(5).text())
            # 这里设置一个延时,防止访问频率过大被封
            time.sleep(1)
            data=paper(paperurl)
            if data['title']:#存在内容就添加保存到数据库
                savedb(data)
        else:
            print("时间不对不采集")
        # break #只访问一页用来测试.
    #判断分页是否存在下一页
    nextpage=doc("div.page.pt30 a:last").attr("href") #没有元素不会报错会返回None
    if nextpage:#and allflag: allflag为true才访问下一页.这里url获取是三天内数据,不考虑allflag属性
        nexturl=base_url+nextpage
        print("递归到下一页-------"+nexturl)
        return listpage(nexturl,allflag)
            




def paper(url):
    '''传入一个详情页url提取招聘需要的字段内容'''
    info=requests.get(url,headers=headers)
    info.encoding=info.apparent_encoding
    #从info.text中提取岗位信息
    doc=pq(info.text)
    data={}
    # 定义证券公司名字
    data['securities']="中金公司"
    # 标题
    data['title']=doc("h2.title2.pb10").text()
    # 招聘详情
    data['content']=doc("div.zwxq").html()
    data['content']=content_filter(data['content'])
    # 工作地点
    data['job_addr']=doc("li.icon13d span").text()
    # 招聘的分类 社招/校招/实习生
    data['job_category']=doc("li.icon13a span").text()
    # 结束时间
    data['end_time']="" #默认是空,之后做判断
    # 提取所有的时间logo元素
    time_elem=doc("li.icon13c span")
    if len(time_elem)==2:#如果有两个元素那么说明有结束时间
        data['end_time']=time_elem.eq(1).text()
    # 发布时间
    data['publish_time']=time_elem.eq(0).text() if time_elem else prev_day
    # 岗位所属部门
    data['department']=doc("li.icon22 span").text()
    # 招聘人数
    data['job_number']=""
    # 学历要求
    data['job_education']=""
    # 其他额外信息
    data['others']=""
    # 详情页的url
    data['source_url']=url
    return data


def savedb(data):
    '''传入字典文件添加数据库'''
    k=Sql()
    try:
        if not k.qutwo(data['source_url']):
            #如果不存在数据库就进行添加操作
            sql="INSERT INTO `"+k.table+"` (`id`, `securities`, `title`, `content`, `job_addr`, `job_category`, `publish_time`, `department`, `job_number`, `job_education`, `end_time`, `others`, `source_url`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            k.execute(sql,[data['securities'],data['title'],data['content'],data['job_addr'],data['job_category'],data['publish_time'],data['department'],data['job_number'],data['job_education'],data['end_time'],data['others'],data['source_url']])
            print("_____成功添加到数据库______")
        else:
            print("存在相同内容"+"----------------"+data['source_url'])
    except Exception as e:
        print(e)
    finally:
        k.close()


headers= {
    # 'Host': 'weixin.sogou.com',
    'Connection': 'keep-alive',
    'Accept': 'text/html, */*; q=0.01',
    # 'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    # 'Referer': 'https://weixin.sogou.com/weixin?query=%E5%86%9B%E6%B0%91%E8%9E%8D%E5%90%88&_sug_type_=&s_from=input&_sug_=n&type=2&page=5&ie=utf8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    # 'Set-Cookie':'SNUID=1; domain=.sogou.com; path=/; expires=Thu, 01-Dec-1994 16:00:00 GMT'
    # 'cookie':'UM_distinctid=17849b7fde95a7-03eff9e74a246a-5771031-1fa400-17849b7fdea6e7; aliyungf_tc=0ad34eaa0bc833366341a163101e37f326a55e86b84bd6819ac56c2487e694ad; route=030e64943c5930d7318fe4a07bfd2a3c; JSESSIONID=C27824A0F7F089A9CA374ACB3A823D18; uuid=e52f2562-34cd-478a-a25e-d475921f180b; SERVERID=srv-omp-ali-portal11_80; Hm_lvt_94a1e06bbce219d29285cee2e37d1d26=1616144498,1616658796,1616721884; paperSearhType=1; CNZZDATA1261102524=591838861-1616142188-%7C1616750557; Hm_lpvt_94a1e06bbce219d29285cee2e37d1d26=1616755493'
}



'''
# 大部分爬虫通用,先爬列表页,然后提取详情页,之后对比是否是昨天的文章进行采集
# @description 中金公司
# @author benty 2021-05-28 15:45:08
# @mail matengmeng@gmail.com
# @allflag 参数说明 是否要跟踪下一页以及是否比对昨天时间 true比对时间或者可以进入下一页.
# @info 以后自动执行定时任务时allflag参数为True,因为中金公司的招聘职位检索3三天内,没有多少页,所以所有页面都要遍历一遍
#
'''

if __name__ == '__main__':
    #首先定义三个分类的url,都找3天内的招聘信息
    urls=["http://cicc.zhiye.com/szzw?k=&c=-1&p=3^-1,1^-1&day=3&PageIndex=1&class=1#zw","http://cicc.zhiye.com/xzzw?k=&c=-1&p=3^-1,1^-1&day=3&PageIndex=1&class=2#zw","http://cicc.zhiye.com/sxszw?k=&c=-1&p=3^-1,1^-1&day=3&PageIndex=1&class=3#zw"] #3天内岗位
    # urls=["http://cicc.zhiye.com/xzzw"] #一周内
    #遍历三个分类的url来进行获取网页内容
    for url in urls:
        # 解析url最后返回需要的字段,allflag来定义采集全部还是采集昨天日期,还用来定义要不要进行所有翻页遍历,这里三天内数据应该全部遍历
        listpage(url,allflag=False)
        # break
    # paper("http://cicc.zhiye.com/xzzwxq?jobId=150338957")
    print("中金公司执行完成")