#!user/bin/python
# _*_ coding: utf-8 _*_
 
# @File : wordti.py
# @Version : 1.0
# @Author : benty
# @Email : matengmeng@gmail.com
# @Time : 2021/07/12 17:05:39
# Description: 根据2017.docx 提取试题保存到数据库
# Motto: 6Z2S6Z2S5a2Q6KG/IOaCoOaCoOaIkeW/gyDkvYbkuLrlkJvmlYUg5rKJ5ZCf6Iez5LuK 

import os
import time
import traceback
import docx,re


from sql import *



start_pys=time.perf_counter()


# 定义一个返回docx全文内容的函数
def get_text(file_path, indent_size=0):
    '''
    :param file_path: 文件路径
    :param indent_size: 段落缩进空格宽度
    :return:获取文档中的所有内容
    '''
    doc = docx.Document(file_path)
    texts = []
    indent = ''
    for i in range(0, indent_size):
        indent = indent + ' '
    for paragraph in doc.paragraphs:
        texts.append(indent + paragraph.text)
    return '\n'.join(texts)

# 定义从txt文本中获取所有内容
def get_txt(filepath):
    '''定义从txt文本中读取试题'''
    with open(filepath,"r",encoding="utf8") as f:
        contents=f.read()
    return contents

# 定义从一个docx文档提取每一个试题的内容,返回来一个列表
def doc_tilist(doc):
    '''传入doc全文,返回每一个试题的list'''
    questions=re.findall(r"\d+[\.．]\s?(【题目】.*?)(?=\d+[\.．]\s?【题目】|$)",doc,re.DOTALL)
    return questions

# 定义从某一个试题中精确的提取出各个字段
def oneti(que):
    '''传入一个题的模版文本进行解析'''
    data={}
    data["title"]=re.search(r"【题目】(.*?)【题型】",que,re.DOTALL).group(1).strip()
    data["titype"]=re.search(r"【题型】(.*?)【选项】",que,re.DOTALL).group(1).strip()
    data["tioption"]=re.search(r"【选项】(.*?)【答案】",que,re.DOTALL).group(1).strip()
    data["tians"]=re.search(r"【答案】(.*?)【涉及知识点】",que,re.DOTALL).group(1).strip()
    data["tiknow"]=re.search(r"【涉及知识点】(.*?)【解析】",que,re.DOTALL).group(1).strip()
    data["tianalysis"]=re.search(r"【解析】(.*?)$",que,re.DOTALL).group(1).strip()
    data["subject"]="文档名字"
    return data


# 定义连接数据库保存一个试题
def saveti(data):
    '''传入一个字典信息的试题保存到wx_exam数据表中'''
    try:
        k=Sql("wx_exam")
        # mysql版本不通可能会引发错误,需要加引号,应该是有关键词冲突
        sql="insert into `wx_exam` (`id`,`title`,`option`,`answer`,`type`,`analysis`,`subject`,`other`,`show_count`) values (NULL,%s,%s,%s,%s,%s,%s,%s,0)"
        k.execute(sql,(data["title"],data["tioption"],data["tians"],data["titype"],data["tianalysis"],data["subject"],data["tiknow"]) )
        print("成功保存到数据库")
    except Exception as e:
        print(e)
        traceback.print_exception()
    finally:
        k.close()


# print(is_trinity())
if __name__=="__main__":
    DIR=os.path.dirname(__file__)
    # 把word复制粘贴到txt中执行,记得修改上面的试卷分类目录名字,还有在上级目录的sql.py判断是本地更新测试还是直接更新投行通数据库
    filex=os.path.join(DIR,"2018.txt")
    doc=get_txt(filex)
    questions=doc_tilist(doc)
    print(len(questions))
    # print(questions)
    for ti in questions:#遍历所有的试题
        # print(ti)
        data=oneti(ti)
        # 1.导入一个题库先print一下data查看有没有黑框是否正常,全部没有说明显示正常
        # print(data)
        # print("*"*60)
        # 2.如果正常了就注释上面执行下面
        saveti(data)
        # break
    print("试题保存成功")
    endt_pye=time.perf_counter()-start_pys
    print("程序一共耗时 %.3f 秒" % endt_pye)