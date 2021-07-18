from sql import *
from bs4 import BeautifulSoup as bs
import re
k=Sql("wx_jobs999")

'''

#
# 此文件的作用是剔除wx_jobs数据表中content字段的html标签,并替换为不连续\n并更新到数据库
# 
# 
# 
# '''
maxid=k.maxid
i=1
while i<=1:# 这里是maxid
    #遍历整个数据库格式化content
    sql="select * from wx_jobs where id='"+str(i)+"';"
    data=k.query(sql)
    if data:#有值说明当条信息有值
        content=data[0]["content"]
        # print(content)
        # print("==="*15)
        soup=bs(content,"html.parser")
        pre_content=soup.get_text("\n")
        # #替换特殊字符
        pre_content=pre_content.replace("\uf09f","")
        #下面是将多个换行替换成一个
        pre_content=re.sub(r"\n{1,}","\n",content)
        # print(pre_content)
        # logwrite("xx",pre_content)
        if content!=pre_content:
            print(i)
            sql="update `wx_jobs` set `content`=%s where id=%s;"
            k.execute(sql,[pre_content,str(i)])
    i+=1
print("格式转换完成")