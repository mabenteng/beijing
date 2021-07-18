# 投行通自动更新爬虫

目前已部署在linux的定时任务中，每天凌晨1点自动执行everyday.py将得到的最新岗位信息保存到线上数据库。


## 规则

大部分招聘页面都有招聘岗位的时间,通过比对是否是在昨天发布的时间进行添加到数据库,采用python的request库以及自己封装的sql类来实现其功能

## 本地数据库thtjobs更新到投行通wx_jobs

- 删除id字段 alter table thtjobs_bak drop id;
- 添加id字段默认为null   alter table thtjobs_bak add id char(3) first;
- 导出数据表为sql
- 替换这个thtjobs_bak 为wx_jobs准备导入

之前1148

2021年7月1日 17:32:20导入中信两个和华泰的岗位总数量为1528
# 爬取顺序

- 中金公司cicc.py
- 国泰君安 gtja.py
- 海通证券 htzq.py
- 中信证券 citics.py
- 中信建投证券 csc.py
- 华泰证券  htsc.py
