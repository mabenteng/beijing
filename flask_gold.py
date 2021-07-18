#!user/bin/python
# _*_ coding: utf-8 _*_
 
# @File : flask_gold.py
# @Version : 1.0
# @Author : benty
# @Email : matengmeng@gmail.com
# @Time : 2021/06/22 14:58:40
# Description: flask单文件版本,方便打包exe使用.包含模型,sql数据库等
# Motto: 6Z2S6Z2S5a2Q6KG/IOaCoOaCoOaIkeW/gyDkvYbkuLrlkJvmlYUg5rKJ5ZCf6Iez5LuK 

from flask import Flask,render_template
from flask.globals import request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os,sys
from random import randrange,choice
from datetime import datetime,timedelta
from collections.abc import Iterable
from sqlalchemy import extract
import webbrowser

def cur_dir():
    '''不论exe还是py代码,都返回当前同级目录'''
    if hasattr(sys,"frozen"):#exe有这个属性
        return os.path.dirname(sys.executable)
    return os.path.dirname(__file__)


#  开启不够帅的代码
# 这里的目录判断写的不够优美,应该做个函数引用上面的cur_dir
# CUR_DIR=os.path.dirname(os.path.abspath(__file__))
# print("当前目录: "+CUR_DIR)
# # print() #这里会输出exe所在的目录,所以根据这个来定义模版目录也是可以的
# EXE_DIR=os.path.dirname(sys.executable)

# #判断sqllite的绝对位置是当前目录还是exe目录
# if "python.exe" in sys.executable:
#     #如果是py文件就用当前目录
#     EXE_DIR=CUR_DIR
# print("exe_dir:::::"+EXE_DIR )
#  结束不够帅的代码

EXE_DIR=cur_dir()

sqldir=os.path.join(EXE_DIR,"chinagold.db").replace('\\','/')
template_dir=os.path.join(EXE_DIR,"inspection").replace("\\","/")
print("template_dir::::"+template_dir)
class Config: #SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_DATABASE_URI=r"sqlite:///"+sqldir # 这是sqlite的配置
    # print(SQLALCHEMY_DATABASE_URI)
    SECRET_KEY="dkjfkjdlafjaefjkreealfkaip"
    DEBUG=True
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    # SESSION_TYPE='redis'


# 上面输出:D:\work\python\自动化\....\dist\flask_gold\flask_gold.exe
app=Flask(__name__,template_folder=template_dir,static_folder=template_dir+"/static")
app.config.from_object(Config)
# print(app.config)
app.jinja_env.variable_start_string="[["
app.jinja_env.variable_end_string="]]"
CORS(app, supports_credentials=True)
db=SQLAlchemy(app)


class Gold(db.Model):
    '''定义金店每次执行的网站日志'''
    id=db.Column(db.Integer,primary_key=True)
    exe_time=db.Column(db.DateTime,index=True) #运行时间,精确到执行时间
    profiletest=db.Column(db.String(20),default="正常")
    financeapi=db.Column(db.String(20),default="正常")
    gzw_supervision=db.Column(db.String(20),default="正常")
    ecds_log=db.Column(db.String(20),default="正常")
    untreated_bill=db.Column(db.String(20),default="正常")
    smstest=db.Column(db.String(20),default="正常")
    bank_abc=db.Column(db.String(20),default="正常")
    bank_icbc=db.Column(db.String(20),default="正常")
    bank_bcm=db.Column(db.String(20),default="正常")
    bank_citic=db.Column(db.String(20),default="正常")
    bank_ccb=db.Column(db.String(20),default="正常")
    bank_cib=db.Column(db.String(20),default="正常")
    bank_boc=db.Column(db.String(20),default="正常")
    def save(self):
        db.session.add(self)
        db.session.commit()

@app.route("/")
def index():
    # db.create_all()#初始化gold数据表
    return render_template("index.html")

#### gold表需要的字段
'''
resdict={}
    resdict['profiletest']="\n中国黄金ebank网银电子票据接口状态:   "
    resdict['init']="\n中国黄金finance资金管理init操作:   "-------------------
    resdict['admin1']="\n中国黄金finance资金管理admin1操作:   "-----------------
    resdict['total_time']="\n总耗时:   "--------------------------------------
    resdict['financeapi']="财务接口状态:"
    resdict['initbank']="直接账户余额查询:"------------
    resdict['gzw_supervision']="国资委报送状态查询:"
    resdict['ecds_log']="ECDS电票接口报文日志状态:"
    resdict['untreated_bill']="票据交易系统未处理报文查询:"
    resdict['smstest']="手工短信验证状态:"
id,时间time,profiletest,financeapi,银行接口七家银行,国资委报送状态,ecds电票接口报文状态,未处理报文查询,smstest手工短信
 银行有,农业abc,工商icbc,交通bcm,中信citic,建设ccb,兴业cib,中国银行boc 7个银行,6个接口共13个字段,
'''


#定义日志文件写入
# def logwrite(cont):
#     file=datetime.now().strftime("%Y-%m-%d")
#     if not os.path.exists("./log"):
#         os.mkdir("log")
#     with open('./log/'+file+".txt",'a+',encoding='utf-8') as f:
#         f.write(cont)



# 将一行结果转换为web需要的json格式
def oldtonew(olddict):
    newdict={}
    newdict["errorResult"]={}
    newdict["errorResult"]["data"]=[]
    newdict["successResult"]={}
    newdict["successResult"]["data"]=[]

    for oldkey,oldval in olddict.items():
        tmpobj={}
        if oldkey=="id":
            newdict["id"]=oldval
            continue
        elif oldkey=="exe_time":
            newdict["resTime"]=oldval
            continue
        elif "bank_" in oldkey:
            tmpbkobj={}
            if oldkey=="bank_abc":
                tmpbkobj["InterfaceName"]="中国农业银行"
            elif oldkey=="bank_icbc":
                tmpbkobj["InterfaceName"]="中国工商银行"
            elif oldkey=="bank_bcm":
                tmpbkobj["InterfaceName"]="交通银行"
            elif oldkey=="bank_citic":
                tmpbkobj["InterfaceName"]="中信银行"
            elif oldkey=="bank_ccb":
                tmpbkobj["InterfaceName"]="中国建设银行"
            elif oldkey=="bank_cib":
                tmpbkobj["InterfaceName"]="兴业银行"
            elif oldkey=="bank_boc":
                tmpbkobj["InterfaceName"]="中国银行"
            if oldval=="正常":
                tmpbkobj["info"]="接口正常"
                newdict["successResult"]["data"].append(tmpbkobj)
            else:
                tmpbkobj["info"]="接口异常"
                newdict["errorResult"]["data"].append(tmpbkobj)
            continue
        elif oldkey=="profiletest":
            #如果是ebank网银电子票据接口
            tmpobj["InterfaceName"]="ebank网银电子票据接口"
        elif oldkey=="financeapi":
            tmpobj["InterfaceName"]="财务接口状态"
        elif oldkey=="gzw_supervision":
            tmpobj["InterfaceName"]="国资委报送状态查询"
        elif oldkey=="ecds_log":
            tmpobj["InterfaceName"]="ECDS电票接口报文日志状态"
        elif oldkey=="untreated_bill":
            tmpobj["InterfaceName"]="票据交易系统未处理报文查询"
        elif oldkey=="smstest":
            tmpobj["InterfaceName"]="手工短信验证状态"
        else:
            tmpobj["InterfaceName"]="未命名"
        if "正常" not in oldval:
            tmpobj["info"]="接口异常"
            newdict["errorResult"]["data"].append(tmpobj)
        else:
            tmpobj["info"]="接口正常"
            newdict["successResult"]["data"].append(tmpobj)

    newdict["successResult"]["total"]=len(newdict["successResult"]["data"])
    newdict["successResult"]["resultName"]="正常"
    newdict["errorResult"]["total"]=len(newdict["errorResult"]["data"])
    newdict["errorResult"]["resultName"]="异常"
    newdict["total"]=newdict["successResult"]["total"]+newdict["errorResult"]["total"]
    # 返回接口成功比率,80就是80%
    newdict["InterfaceStatus"]=int((newdict["successResult"]["total"]/newdict["total"])*100)
    newdict["resCode"]="0"
    newdict["resMsg"]="检测结果全部正常"
    if newdict["InterfaceStatus"]<21:
        newdict["resMsg"]="检测结果大部分异常"
    elif newdict["InterfaceStatus"]<51:
        newdict["resMsg"]="检测结果部分异常"
    elif newdict["InterfaceStatus"]<100 :
        newdict["resMsg"]="检测结果少部分异常"
    return newdict


def mtd(result):
    # 转换完成后，删除  '_sa_instance_state' 特殊属性
    try:
        if isinstance(result, Iterable):
            tmp = [dict(zip(res.__dict__.keys(), res.__dict__.values())) for res in result]
            for t in tmp:
                t.pop('_sa_instance_state')
        else:
            tmp = dict(zip(result.__dict__.keys(), result.__dict__.values()))
            tmp.pop('_sa_instance_state')
        # 对时间对象进行转换
        tmp['exe_time']=tmp["exe_time"].strftime("%Y-%m-%d %H:%M:%S")
        return tmp
    except BaseException as e:
        print(e.args)
        raise TypeError('Type error of parameter')



@app.route("/xxxxxxxxxxxxxxx/adddata")
def adddata():
    '''添加数据'''
    # datetime.now()
    diy=request.args.get("diy")
    if diy:
        exe_time=datetime.today()
    else:
        # 创造一个随机时间对象
        exe_time=request.form.get("exe_time",datetime.today()-timedelta(days=randrange(1,360)))
    # 创造一个随机字段让其保存为异常
    errtmp=["profiletest"," financeapi"," gzw_supervision"," ecds_log"," untreated_bill"," smstest"," bank_abc"," bank_icbc"," bank_bcm"," bank_citic"," bank_ccb"," bank_cib"," bank_boc"]
    tmpdc={choice(errtmp).strip():"异常","exe_time":exe_time}
    # tmpdc={"profiletest":"测试"}
    c=Gold(**tmpdc)
    # c.exe_time=exe_time #.replace(microsecond=0)
    c.save()
    return "添加数据成功 %s" % exe_time

@app.route("/api/showdata/<ttt>")
def showdata(ttt=datetime.now()):
    '''显示data'''
    # tmp是后期用户传入的数据,记住永远不要相信用户的输入.
    tmp=ttt or "2021-06-23"
    try:
        start=datetime.strptime(tmp,"%Y-%m-%d")
    except:
        # 日期解析不对就默认查询今天的数据
        start=datetime.now()
    # start=datetime.date(year=2021,month=6,day=23)
    # alld=Gold.query.all()
    # 查询时间等于某一天的
    alld=Gold.query.filter(extract('year',Gold.exe_time)==start.year,
                            extract('month',Gold.exe_time)==start.month,
                            extract('day',Gold.exe_time)==start.day
    )
    # print(alld)
    if not alld:
        return {"msg":"没有数据","total":0}
    result=[oldtonew(mtd(x)) for x in alld]
    # 将时间对象转换为固定格式的时间日期
    # result['exe_time']=result["exe_time"].strftime("%Y-%m-%d")
    return {"msg":"查询成功","total":len(result),"data":result}

@app.route("/dbinit")
def dbinit():
    #新建所有表
    pwd=request.args.get("pwd")
    drop=request.args.get("drop")
    if pwd=="123456":
        db.create_all()
        # 删除所有表
        # db.drop_all()
        return "执行成功"
    elif drop=="123456":
        # 删除所有表
        db.drop_all()
        return "执行成功"
    else:
        return "请输入pwd参数重建数据表或drop参数删除数据表,加上密码会覆盖数据请注意"
# api查看当天时间
@app.route("/api/day/<string:time>")
def daystatus(time):
    '''此方法弃用,合并到/api/showdata接口中'''
    time=time or "null"
    #根据传入的时间到数据库进行查询返回结果的格式
    '''
    {"msg":"获取成功","status":"200","totalresult":len(result),"data":[{数据库一行的信息}]}
    '''
    return time

@app.route("/api/fields")
def fields():
    # keys=Gold.query.first()
    # keyp=[x for x in keys.__dict__.keys() if x!="id"]
    # keyp=[x for x in keyp if x!="_sa_instance_state"]
    # print(current_app.config)
    tmpfields=[{'bank_boc':"中国银行"}, {'bank_ccb':"中国建设银行"}, {'bank_bcm':"交通银行"}, {'bank_icbc':"工商银行"}, {'smstest':"手工短信测试接口"}, {'ecds_log':"ECDS电票接口报文日志状态"}, {'financeapi':"财务接口状态"}, {'bank_cib':"兴业银行"}, {'bank_citic':"中信银行"}, {'bank_abc':"中国农业银行"}, {'untreated_bill':"票据交易系统未处理报文查询"}, {'gzw_supervision':"国资委报送状态查询"}, {'profiletest':"ebank网银电子票据接口"}]
    tmpres=[]
    for x in tmpfields:
        for key,value in x.items():
            tmpdict={}
            tmpdict["dictValue"]=key
            tmpdict["dictName"]=value
            tmpres.append(tmpdict)
        # tmpfields=[{"dictValue":key,"dictName":value} for key,value in x for x in tmpfields]
    dd={}
    dd['fields']=tmpres
    dd['fields_val']=["正常","异常"]
    return dd

# 时间范围查询
@app.route("/api/dayrange",methods=["POST"])
def dayrange():
    start=request.form.get("start","2021-06-07")
    end=request.form.get("end","2029-09-07")
    try:
        start=datetime.strptime(start,"%Y-%m-%d")
    except:
        start=datetime.now()
    try:
        end=datetime.strptime(end,"%Y-%m-%d")
    except:
        end=datetime.now()
    # 更多条件的查询
    tmpfield=request.form.get('fieldname','')
    tmpvalue=request.form.get("fieldval",'')
    tmpdict={tmpfield:tmpvalue}
    # print(tmpfield+"---"+tmpvalue)
    '''
    # 对模型时间字段的区间查询
    start=datetime.date(year=2021,month=6,day=1)
    end=datetime.date(year=2021,month=6,day=10)'''
    alld=Gold.query.filter(Gold.exe_time<=end).filter(Gold.exe_time>=start)
    if tmpfield and tmpvalue:#如果两个字段都有值的话,继续进行下一步其他字段查询
        alld=alld.filter_by(**tmpdict)
    #返回一个列表对象
    # print(alld)
    if not alld:
        return {"msg":"没有数据","total":0,"data":[]}
    result=[oldtonew(mtd(x)) for x in alld]
    # 将时间对象转换为固定格式的时间日期
    # result['exe_time']=result["exe_time"].strftime("%Y-%m-%d")
    return {"msg":"查询成功","total":len(result),"data":result}
    

@app.errorhandler(404)
def ab404(error):
    return {"msg":"URL路径错误","status":404,"data":[]}

if __name__ == '__main__':
    # 打开浏览器
    # pathweb=r'C: && chrome.exe http://127.0.0.1:5001'
    # os.system(pathweb)
    webbrowser.open_new("http://127.0.0.1:5001")
    app.run(port=5001,debug=False,host="0.0.0.0")
    # Thread(target=app.run).start() #新开一个线程去执行方便后续代码的运行
    # 本文件要重新打包---pyweb虚拟环境pyinstaller -i n2.ico -F flask_gold.py

    
