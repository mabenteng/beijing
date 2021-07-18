#!user/bin/python
# _*_ coding: utf-8 _*_
 
# @File : everyday.py
# @Version : 1.0
# @Author : benty
# @Email : matengmeng@gmail.com
# @Time : 2021/07/01 17:46:24
# Description:  引入所有的爬虫文件做定时任务
# Linux 脚本 (分钟 小时 第N天 月份 星期几) 10 0 * * * python3 everyday.py  # 每天0:10分执行everyday.py
# Motto: 6Z2S6Z2S5a2Q6KG/IOaCoOaCoOaIkeW/gyDkvYbkuLrlkJvmlYUg5rKJ5ZCf6Iez5LuK 
from datetime import datetime
from sql import logwrite,is_win
import time


start_pys=time.perf_counter()

import os

###   这里最好搞个os环境变量,用来判断是windows本地还是linux服务器
# 动态改变路径
DIR=os.path.dirname(__file__)
if is_win():
    varpy="python "
else:
    varpy="/root/miniconda3/bin/python "
os.system(varpy+os.path.join(DIR,"htsc.py"))
os.system(varpy+os.path.join(DIR,"csc.py"))
os.system(varpy+os.path.join(DIR,"gtja.py"))
os.system(varpy+os.path.join(DIR,"cicc.py"))
os.system(varpy+os.path.join(DIR,"citics.py"))
os.system(varpy+os.path.join(DIR,"htzq.py"))







if __name__=="__main__":
    #/root/miniconda3/bin/python /home/tht/tht_everyday/everyday.py >/home/tht/tht_everyday/log/today.log 2>&1
    endt_pye=time.perf_counter()-start_pys
    # 注意这里的logwrite写的日志文件在定时任务中是在~/log/everyday_tht.txt中
    logwrite("everyday_tht","\n"+datetime.today().strftime("%Y-%m-%d %H:%M:%S")+"\n定时任务完成,程序一共耗时 %.3f 秒" % endt_pye)
    print("程序一共耗时 %.3f 秒" % endt_pye)