# coding=utf-8

from unittest.main import main
import pymysql,random,time,os,datetime



prev_day=(datetime.datetime.now()- datetime.timedelta(days=1)).strftime("%Y-%m-%d")
#定义写文件函数
def logwrite(file,cont):
    if not os.path.exists("./log"):
        os.mkdir("log")
    with open("./log/"+file+".txt","a+",encoding='utf-8') as f:
        f.write(cont)

# 判断py程序所在环境是linux还是windows
def is_win():
    '''判断是否是win环境'''
    if os.environ.get("USERNAME")=="trinity":
        return True
    return False
# 定义一个计时的装饰器
def timek(func):
    # print(args)
    def inner(*args,**kw):
        # print(args)#args是浏览器对象
        # print(kw) #是tmp字典
        start_time=time.perf_counter()
        res=func(*args,**kw)
        # print(res)
        usetime=time.perf_counter()-start_time
        # resxx={"status":res,"time":usetime} #中国黄金的格式
        res['time']=usetime #清华的格式
        # print(resxx)
        #这里进行判断是否为none是因为func函数用了递归所以要进行判断res是否为none,为none不正常
        # print(res==None)
        return res
    #func函数成功执行才返回结果,否则不返回中断
    return inner

'''
# 
# @description 对mysql数据库操作的封装
# @author benty 2021-04-06 10:25:02
# @param 
# @return 
#
'''


class Sql(object):
    '''初始化数据库连接'''
    def __init__(self,tb="wx_jobs"):#thtjobs
        '''定义数据表连接数据库并初始化cursor对象'''
        if is_win():
            self.db = pymysql.connect(host='localhost',user='root',password='root',database='tht',charset='utf8')
        else:# 连接投行通内网数据库
            self.db = pymysql.connect(host='10.xx.xxx.8',user='root',password='123456',database='testxxx',charset='utf8')
        self.table=tb
        # self.cursor = self.db.cursor()
        self.cursor = self.db.cursor(cursor = pymysql.cursors.DictCursor)

    def close(self):
        '''关闭cursor对象和db数据库连接'''
        self.cursor.close()
        self.db.close()

    def query(self, sql):
        '''传入sql返回fetchall所有结果,是字典格式'''
        try:
            self.cursor.execute(sql)
            # self.close()
            return self.cursor.fetchall()
        except Exception as e:
            print(e)
            return []

    def execute(self, sql, params=()):
        '''传入sql和参数用来绑定参数,参数为列表或元组,没有返回值'''
        try:
            self.cursor.execute(sql, params)
            self.db.commit()
            # result=self.cursor.fetchall()
            # self.close()
            # return result
        except Exception as e:
            self.db.rollback()
            print(e)

    def qutwo(self, link):
        '''传入链接对链接进行去重,存在返回True'''
        sql = "select * from "+self.table+" where source_url='" + link + "';"
        # sql="select * from weixin where id>11277 and other='"+link+"';"
        res = self.query(sql)
        # print(res)
        if len(res) >= 1:
            return True
        else:
            return False
    @property
    def maxid(self):
        '''返回当前表的最大id'''
        sql="select max(id) as maxid from "+self.table
        res=self.query(sql)
        #如果以字典输出的游标用maxid,否则用0表示 元组
        return res[0]['maxid']

'''
# 
# @description Head函数,对cookie进行封装操作
# @author benty 2021-04-06 10:28:41
# @param 
# @return 
#
'''


class Head(object):
    '''对cookie常用操作进行封装'''
    def __init__(self):
        self.useragent = [
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
            "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0"
        ]
    

    # ption 随机Useragent
    def suijiua(self):
        '''返回随机useragent'''
        return random.choice(self.useragent)
    
    #将字符串转换为cookie字典
    def strtocookies(self, str):
        '''将chrome的cookie字符串转化为cookie字典'''
        cookie = {}
        for line in str.split(";"):
            key, value = line.split("=", 1)  #参数1表示分割几次
            cookie[key.strip()] = value.strip()
        return cookie

    '''
    # #判断headers是否存在set-Cookie参数并设置新cookie
    # @description 一般headers是requests库之后的info.headers,oldcookie是将字符串转换为字典的cookie
    # @author benty 2021-04-06 10:33:03
    # @param 
    # @return 
    #
    '''

    def newsetcookie(self, headers={}, oldcookie={}):
        '''判断响应头headers如果存在set-Cookie更新到oldcookie中'''
        if "Set-Cookie" in headers:
            dicts = {}
            for ck, ckval in headers.items():
                if ck == "Set-Cookie":
                    ckval = ckval.split(";", 1)
                    ckvallist = ckval[0].split('=', 1)
                    dicts[ckvallist[0].strip()] = ckvallist[1].strip()
            oldcookie.update(dicts)
        return oldcookie





if __name__ == '__main__':
    #测试是否是e14电脑
    print(is_win())
    
