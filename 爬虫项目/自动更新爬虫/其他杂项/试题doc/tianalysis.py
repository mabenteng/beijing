#!user/bin/python
# _*_ coding: utf-8 _*_
 
# @File : tianalysis.py
# @Version : 1.0
# @Author : benty
# @Email : matengmeng@gmail.com
# @Time : 2021/06/08 11:48:32
# Description: 将前28的试题的答案解析
# Motto: 6Z2S6Z2S5a2Q6KG/IOaCoOaCoOaIkeW/gyDkvYbkuLrlkJvmlYUg5rKJ5ZCf6Iez5LuK 

import re,sys
import traceback
sys.path.append("../")

from sql import Sql


filex="./选择答案.txt"

with open(filex,"r",encoding="utf8") as f:
    contents=f.read()

exit()
#
# print(contents)
anss=re.findall(r"\d+\..*?(?=\d+\.【答案】|$)",contents,re.DOTALL)
k=Sql("wx_tiku")
for ans in anss:
    try:
        #遍历每一条试题答案
        ans_id=re.match(r"\d+",ans.strip()).group() # 提取id
        ans_ans=re.search(r"【答案】(.*)",ans).group(1) #提取答案
        ans_other=re.search(r"【涉及知识点】(.*)\n【解析】",ans).group(1) # 提取涉及知识点
        ans_analysis=re.search(r"【解析】\n(.*)",ans,re.DOTALL).group(1).strip() # 提取答案解析,可能有多行
        sql="update wx_tiku set wx_answer=%s,wx_analysis=%s,wx_other=%s where id =%s;"
        k.execute(sql,[ans_ans,ans_analysis,ans_other,ans_id])
    except:
        traceback.print_exc()
        pass
k.close()