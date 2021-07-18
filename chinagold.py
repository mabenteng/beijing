# coding:utf-8
'''
# 
# @description 中国黄金财务自动化巡检
# @author benty 2021-05-06 16:18:20
# @param 下面是简写函数位置
# @return 
#
'''
from selenium import webdriver
import time,os,datetime
from selenium.webdriver.common.keys import Keys
# import autopy
from pykeyboard import PyKeyboard
import traceback,re
from conf import AutoConf

#先判断有没有配置文件
path_file="./conf.json"
config=AutoConf(path_file)
conf=config.getconf()
# conf['userinfo']包含帐号信息
userinfo=conf['userinfo']
# 声明重试次数
retry=int(userinfo['retry'])


#以下是测试系统登录地址
'''
ebank_url = 'http://10.40.101.2:7001/toftmerge/ebank/welcome.do'
finance_url = 'http://10.40.101.1:7001/toftmerge/finance/welcome.do'
testlayui_url="http://www.layui.com/demo/"
'''
# 以下是正式系统登录地址
ebank_url = 'http://10.40.32.11:7001/toftmerge/ebank/welcome.do'
finance_url = 'http://10.40.31.21:7001/toftmerge/finance/welcome.do'



# 定义浏览器对象并打开url
def chrome(url="", type="ie", t=8):
    '''初始化浏览器并打开'''
    # global browser
    if type == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument('–log-level=3')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument('disable-infobars')
        # options.add_argument('headless')#静默模式
        browser = webdriver.Chrome(options=options,
                             service_log_path=os.devnull,
                             desired_capabilities=None)
    else:  #不是chrome就是IE
        # path = r'D:\\work\\python\\自动化\\清华控股\\tools\\IEDriverServerqinghua.exe'
        # path = r'D:\\work\\python\\自动化\\中国黄金\\ie\\IEDriverServer.exe'
        path = r'./ie/IEDriverServer.exe'
        browser = webdriver.Ie(executable_path=path)
        time.sleep(0.5)
    browser.implicitly_wait(t)
    browser.get(url)
    # b.byatexts()
    # WebDriverWait(self.b, 10).until(lambda x: self.b.find_element_by_link_text('hao123'))#显式等待
    # print('=========================================================')
    browser.maximize_window()  # 放大页面
    return browser

# 处理浏览器网银弹窗
def bankalert(tmp=retry):
    '''处理网银系统弹窗输入密码'''
    try:
        print('---开始输入key--')
        try:
            browser.switch_to_active_element
        except:
            time.sleep(1)
        confinfo={}
        confinfo['key']="123456"
        time.sleep(2)
        k = PyKeyboard()
        for ikey in range(len(confinfo['key'])):
            time.sleep(0.3)
            if confinfo['key'][ikey].isupper():
                k.press_key(k.shift_key)
                time.sleep(0.3)
                k.tap_key(confinfo['key'][ikey])
                k.release_key(k.shift_key)
            else:
                k.tap_key(confinfo['key'][ikey])
                time.sleep(0.3)
        k.tap_key(k.enter_key)
        time.sleep(1.3)
    except:
        if tmp!=0:
            tmp-=1
            bankalert()

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
        resxx={"status":res,"time":usetime}
        # print(resxx)
        #这里进行判断是否为none是因为func函数用了递归所以要进行判断res是否为none,为none不正常
        # print(res==None)
        return resxx
    #func函数成功执行才返回结果,否则不返回中断
    return inner
# retry=3
def login(browser,user, pwd, key=None,tmp=3):
    '''传入一个浏览器对象,登录金店财务,返回登录是否成功'''
    try:
        # global browser
        browser.byid("userId").send_keys(user)
        browser.byid("password").send_keys(pwd)
        if key:
            #此处存在key需要做处理
            pass
        browser.runjs("LoginByAjax();")
        bankalert()
    except Exception as e:
        print(e)
        if tmp!=0:
            tmp-=1
            browser.byid("userId").clear()
            browser.byid("password").clear()
            login(browser,user, pwd, key=None,tmp=tmp)


def logout(browser,tmp=retry):
    '''传入浏览器对象并退出登录'''
    try:
        browser.todefault()
        browser.runjs("logout();")
        time.sleep(0.5)
        browser.switch_to.alert.accept()
    except Exception as e:
        print(e)
        if tmp!=0:
            tmp-=1
            browser.runjs("logout();")
            time.sleep(0.5)
            browser.switch_to.alert.accept()
            logout(browser,tmp=tmp)


def getalert(browser):
    '''传入浏览器对象获取浏览器弹窗文本并确定'''
    pass


#网银电子票据--->系统管理--->本企业账户资料设置 网页正常说明接口正常====================1
@timek
def profiletest(browser,tmp=retry):
    '''传入浏览器对象自动点击判断接口是否正常'''
    def _profiletest(browser,tmp):
        try:
            time.sleep(1)
            browser.todefault()
            time.sleep(1)
            xx=browser.byname("module")
            browser.toframe(xx)
            time.sleep(1)
            xx=browser.byid("module_404291396468370")
            time.sleep(0.4)
            browser.execute_script("arguments[0].click();",xx)
            browser.todefault()
            xx=browser.byname("tree")
            browser.switch_to.frame(xx)
            time.sleep(0.3)
            xx=browser.byatext('系统管理')
            browser.execute_script("arguments[0].click();",xx)
            xx=browser.byid("sd3") #id ==sd3 本企业账户资料设置
            browser.execute_script("arguments[0].click();",xx)
            #切换到frame为main的内容
            time.sleep(0.5)
            browser.todefault()
            time.sleep(0.5)
            xx=browser.byname("main")
            browser.toframe(xx)
            tmp = browser.byclass("pageTitle").text
            # browser.todefault()
            if tmp=="本企业开户资料设置":
                return "接口正常"
            else:
                return "接口异常"
        except:
            traceback.print_exc()
            # print(e)
            if tmp!=0:
                print(tmp)
                tmp-=1
                time.sleep(0.3)
                # browser.todefault()
                return _profiletest(browser,tmp=tmp)
            else:
                return "未知错误"
    return _profiletest(browser,tmp)

#finance的init帐号登录检测功能==========================2
def financeinit(browser):
    '''finance资金管理系统的init帐号检测'''
    dc={}
    login(browser,userinfo["finance_user1"], userinfo["finance_user1_pwd"])  #传入浏览器对象登录系统
    # 1.遍历银行余额接口
    dc['initbank']=initbank(browser)
    # exit()
    # 2.测试财务接口连接是否正常
    dc['financeapi']=initconnect(browser)
    # 3.国资委监管测试
    # 2021年5月7日 17:46:04
    dc['gzw_supervision']=initgzw_supervision(browser)
    #最后退出登录并返回上面执行的结果
    logout(browser)
    return dc

#finance的init帐号==== 1.银行循环函数 
@timek
def initbank(browser,tmp=retry):
    '''init帐号查看七家银行余额函数'''
    def _initbank(browser,tmp):
        try:
            browser.todefault()
            browser.toframe("module")
            xx=browser.byid("module_12") #点击银企平台
            browser.execute_script("arguments[0].click();",xx)
            browser.todefault()
            #点击直连账户当日余额查询
            xx=browser.byid("node_120000200010").bytagname("a")
            browser.execute_script("arguments[0].click();",xx)
            #接下来查看七家银行开始遍历.
            browser.toframe("main")
            bankstatus=""
            banktotal=len(browser.byname("bankRefCode").bytagnames("option"))
            for ibank in range(1,banktotal):
                #逐个点击银行按钮,先选第一个
                time.sleep(0.5)
                optbank=browser.byname("bankRefCode").bytagnames("option")[ibank]
                optbank.click()
                # browser.execute_script("arguments[0].click();",optbank) #无效
                bankname=optbank.text
                # print(bankname+str(ibank))
                '''
                browser.byname("clientIdCtrl").send_keys("0000")
                time.sleep(0.5)
                browser.byname("clientIdCtrl").send_keys(Keys.ENTER)
                #这里需要等待    然后点击搜索   也要写函数
                time.sleep(3)
                '''
                browser.todefault()
                browser.runjs("$(\"input[name='clientId']\",window.frames['main'].document).val('3');")
                browser.runjs("$(\"input[name='clientIdCtrl']\",window.frames['main'].document).val('01-0000');")
                browser.runjs("$(\"input[name='clientName']\",window.frames['main'].document).val('中国黄金集团财务有限公司');")
                browser.toframe("main")
                browser.execute_script("doSearch();")
                #这里查询时间比较长,更需要等待函数
                # bankwait(browser)
                p=0
                try:#如果存在弹窗关闭 以后可以减少等待时间
                    time.sleep(3)
                    browser.switch_to.alert.accept()
                    p=1
                    time.sleep(0.5)
                except:
                    pass
                try:#如果超过函数的最大超时时间直接返回有故障,但是好像不能返回了.
                    if p==1:
                        bankstatus=bankstatus+bankname+"接口有故障\n"
                        time.sleep(1)
                        continue
                    else:
                        browser.byclasses("ItemBody")[-2].text
                except:
                    bankstatus=bankstatus+bankname+"接口有故障\n"
                    if p==0:#有弹窗就不用执行下面
                        browser.back()
                        time.sleep(1)
                        browser.forward()
                        try:#如果存在弹窗关闭
                            time.sleep(0.5)
                            browser.switch_to.alert.accept()
                            time.sleep(1)
                        except:
                            pass
                    continue #直接下个循环
                
                #ItemTitle是标题,ItemBody是具体数据-2是状态
                if "故障" in browser.byclasses("ItemBody")[-2].text:
                    bankstatus=bankstatus+bankname+"接口有故障\n"
                else:
                    bankstatus=bankstatus+bankname+"接口正常\n"
                browser.runjs("doReturn();")
                time.sleep(0.3)
            return bankstatus
        except Exception as e:
            print(e)
            if tmp!=0:
                tmp-=1
                time.sleep(0.3)
                browser.todefault()
                return _initbank(browser,tmp=tmp)
            else:
                return "未知错误"
    return _initbank(browser,tmp)

#finance的init帐号===2.测试财务接口连接是否正常
@timek
def initconnect(browser,tmp=retry):
    '''init帐号查看财务接口连接是否正常'''
    def _initconnect(browser,tmp):
        try:
            browser.todefault()
            browser.toframe("module")
            xx=browser.byid("module_870015986496205") #点击财务接口
            browser.execute_script("arguments[0].click();",xx)
            browser.todefault()
            # 点击左侧财务接口设置
            xx=browser.byid("node_000010000100001").bytagname("a")
            browser.execute_script("arguments[0].click();",xx)
            # 接下来点击 "1" 进入连接窗口.需要先切回main框架
            browser.toframe('main')
            time.sleep(0.3)
            # xx=browser.byid("row1").byid("id_0")
            # browser.execute_script("arguments[0].click();",xx)
            browser.execute_script('javascript:updateDetail("1")')
            # 点击检查元素
            xx=browser.byname("btnTest")
            browser.execute_script("arguments[0].click();",xx)
            time.sleep(0.5)
            # 获取弹窗结果
            xx=browser.switch_to.alert
            xxtext=xx.text
            # time.sleep(0.5)
            xx.accept()
            
            if "成功" in xxtext:
                return "财务接口连接成功"
            elif "失败" in xxtext:
                return "财务接口连接失败"
        except Exception as e:
            print(e)
            if tmp!=0:
                tmp-=1
                time.sleep(0.3)
                return _initconnect(browser,tmp=tmp)
            else:
                return "未知错误"
    return _initconnect(browser,tmp)

#finance的init帐号===3.测试国资委监管-数据报送状态查询 
@timek
def initgzw_supervision(browser,tmp=retry):
    '''init帐号查看国资委数据报送'''
    def _initgzw_supervision(browser,tmp):
        try:
            #先切换到module frame然后点击国资委监管
            browser.todefault()
            browser.toframe("module")
            xx=browser.byid("module_685259563499888") #点击国资委监管
            browser.execute_script("arguments[0].click();",xx)
            browser.todefault()
            xx=browser.byatext("数据报送") #点击左侧数据报送
            browser.execute_script("arguments[0].click()",xx)
            xx=browser.byatext("报送状态查询") #点击左侧报送状态查询
            browser.execute_script("arguments[0].click()",xx)
            time.sleep(0.8)
            browser.execute_script("arguments[0].click()",xx)
            # 有时候点击一次没有数据?还是没有触发ajax?
            #这里未完成,需要进行下一步操作.测试环境不能访问.
            kaiji_time=browser.byid("openDateSpan").text
            #切换到main框架
            xx=browser.byname("main")
            browser.toframe(xx)
            update_times=browser.byclass("datagrid-btable").byxpaths(".//tr[contains(@id,'datagrid-row-r1-2')]")
            gzwok=0
            for i in range(len(update_times)):
                # 如果开机时间存在表格这一行中就说明成功
                if kaiji_time in update_times[i].text:
                    gzwok=1
                    break
            if gzwok==0:
                return "国资委报送状态查询失败"
            return "国资委报送状态查询成功"
        except Exception as e:
            print(e)
            if tmp!=0:
                tmp-=1
                time.sleep(0.3)
                return _initgzw_supervision(browser,tmp=tmp)
            else:
                return "未知错误"
    return _initgzw_supervision(browser,tmp)

# finance的admin1帐号===电票接口--票据交易系统--短信平台==========================3
def financeadmin1(browser):
    '''finance资金管理系统的admin1帐号检测'''
    dc={}
    #先登录帐号
    login(browser,userinfo["finance_user2"], userinfo["finance_user2_pwd"])
    # 1.测试电票ecds接口-日志查询--报文日志查询
    dc["ecds_log"]=ecds_log(browser)
    # 2.票据交易系统--报文查询--未处理报文查询--点右侧查询
    dc['untreated_bill']=untreated_bill(browser,tmp=retry)
    # print(dc['untreated_bill'])
    # 3.短信平台--手工短信发送--输入18610966019--发送--接收弹窗信息
    dc['smstest']=smstest(browser)
    #最后退出登录并返回数据
    return dc

# finance的admin1帐号===1.测试电票ecds接口-日志查询--报文日志查询
@timek
def ecds_log(browser,tmp=retry):
    '''admin1帐号测试电票接口对的报文日志查询'''
    def _ecds_log(browser,tmp):
        try:
            time.sleep(0.3)
            browser.todefault()
            time.sleep(0.3)
            xx=browser.byname("module")
            browser.toframe(xx)
            xx=browser.byid("module_404291396468372") #点击电票接口
            browser.execute_script("arguments[0].click();",xx)
            #点击日志查询
            browser.todefault()
            xx=browser.byatext("日志查询")
            browser.execute_script("arguments[0].click();",xx)
            #点击报文日志查询
            xx=browser.byatext("报文日志查询")
            browser.execute_script("arguments[0].click();",xx)
            #进入右侧main框架输入054报文类型编码
            browser.toframe("main")
            browser.byname("messageCode").send_keys("054")
            browser.execute_script("doQuery();") #点击查询
            # pagewaitq(browser)
            pagewaitnotin("找不到", browser.byclass("pPageStat").text)
            #id为flexlist下面的tr行有数据才有,否则就没有tr
            if browser.byid("flexlist").text:
                return "电票报文日志接口正常"
            else:
                return "电票报文日志接口结果为空"
        except Exception as e:
            print(e)
            if tmp!=0:
                tmp-=1
                time.sleep(0.3)
                return _ecds_log(browser,tmp=tmp)
            else:
                return "未知错误"
    return _ecds_log(browser,tmp)

#finance的admin1帐号===2.票据交易系统--报文查询--未处理报文查询--点右侧查询 ----
@timek
def untreated_bill(browser,tmp=retry):
    '''admin1帐号对未处理票据报文的查询'''
    def _untreated_bill(browser,tmp):
        try:
            browser.todefault()
            xx=browser.byname("module")
            browser.toframe(xx)
            xx=browser.byid("module_637152676658002")
            browser.execute_script("arguments[0].click()",xx)
            browser.todefault()
            xx=browser.byatext("报文查询")
            browser.execute_script("arguments[0].click()",xx)
            xx=browser.byatext("未处理报文查询及处理")
            browser.execute_script("arguments[0].click()",xx)
            # 点击右侧查询 ccm... 测试环境不可访问.
            xx=browser.byname("main")
            browser.toframe(xx)
            #点击查询按钮
            xx=browser.byid("btnShowQuery")
            browser.execute_script("arguments[0].click();",xx)
            formquery=browser.byid("condition")
            #在main环境框架中不用加,window.frames['main'].document
            browser.runjs("$(\"#mesgType\").val('CCM.004.001');")
            browser.runjs("$(\"#dealStatus\").val('');")
            #点击确定
            xx=browser.byid('btnQuery')
            browser.execute_script("arguments[0].click();",xx)
            #这里强行等待2s,之后对tr进行计数,一般都是会有值的,所以不考虑进行等待.
            time.sleep(2.3)
            trcount=browser.byclass("datagrid-btable").byxpaths(".//tr[contains(@id,'datagrid-row-r1-2')]")
            if len(trcount)!=0:
                return "未处理报文查询成功"
            return "未处理报文查询失败"
        except Exception as e:
            print(e)
            if tmp!=0:
                tmp-=1
                time.sleep(0.3)
                return _untreated_bill(browser,tmp=tmp)
            else:
                return "未知错误"
    return _untreated_bill(browser,tmp)

#finance的admin1帐号===3.短信平台--手工短信发送--输入18610966019--发送--接收弹窗信息
@timek
def smstest(browser,tmp=retry):
    '''admin1帐号对短信平台手动核验'''
    def _smstest(browser,tmp):
        try:
            #开头考虑第二次有弹窗
            browser.todefault()
            xx=browser.byname("module")
            browser.toframe(xx)
            xx=browser.byid("module_586708682065679") #点击短信平台
            browser.execute_script("arguments[0].click()",xx)
            browser.todefault()
            #点击手工短信发送
            xx=browser.byatext("手工短信发送")
            browser.execute_script("arguments[0].click();",xx)
            browser.todefault()
            xx=browser.byname("main")
            browser.toframe(xx)
            time.sleep(0.3)
            xx=browser.byname("sMPNumber")
            browser.execute_script("arguments[0].click();",xx)
            time.sleep(0.5)
            # 输入手机号码回车准备发送短信
            xx.send_keys(userinfo['phone'])
            time.sleep(0.3)
            xx.send_keys(Keys.ENTER)
            browser.byname("sMessageContent").send_keys("测试短信接口")
            xx=browser.byname("send")
            browser.execute_script("arguments[0].click();",xx)
            # time.sleep(0.8)
            waitalert(browser)
            browser.switch_to.alert.accept()
            waitalert(browser)
            xx=browser.switch_to.alert
            xxtext=xx.text
            # print(xxtext)
            xx.accept()
            #退出登录
            logout(browser)
            if "完成" in xxtext:
                return "短信发送成功"
            elif "失败" in xxtext:
                return "短信发送失败"
        except Exception as e:
            print(e)
            if tmp!=0:
                tmp-=1
                time.sleep(0.3)
                return _smstest(browser,tmp=tmp)
            else:
                return "未知错误"
    return _smstest(browser,tmp)

# 等待alert出现,否则一直等
def waitalert(browser,time=8):
    '''等待alert出现,否则就等0.5秒,超过8秒跳过'''
    try:
        browser.switch_to.alert
    except:
        print("等待alert出现")
        timetmp=0
        alertstatus=0
        while alertstatus==0:
            if timetmp<8:
                timetmp+=0.5
                time.sleep(0.5)
                waitalert(browser,time=8)
            else:
                break
# 判断关键词keyword是否在text中 ====暂时可能有问题,用pagewaitq
def pagewait(keywords, textobj, waittime=5):
    '''判断关键词keywords是否在textobj,不在一直等,存在返回1,主要对ajax页面进行分析'''
    # global browser
    ppagestat = 0
    timek = 0
    while ppagestat == 0:
        if "请稍等" not in textobj:
            ppagestat = 1
        elif keywords in textobj:
            ppagestat = 1
        else:
            print("else等待元素出现")
            time.sleep(0.1)
            timek += 1
            if timek > waittime * 2:
                #默认最大等待时间30s,超时跳出
                break
    return ppagestat

# 切换银行帐号的等待函数
def bankwait(browser,t=1):
    '''切换七家银行的等待时间'''
    try:
        print("又一次等待银行返回数据")
        browser.byclass("ItemBody")
        print("找到返回元素了....")
    except:#异常只执行一次
        if t<4:
            t+=1
            bankwait(browser,t)
        

# 判断关键词keyword不在text中就等待
def pagewaitnotin(keywords, textobj, waittime=5):
    '''判断关键词keywords是否在textobj,不在一直等,存在返回1,主要对ajax页面进行分析'''
    # global browser
    ppagestat = 0
    timek = 0
    while ppagestat == 0:
        if keywords not in textobj:
            ppagestat = 1
        else:
            print("else等待元素出现")
            time.sleep(0.5)
            timek += 1
            if timek > waittime * 2:
                #默认最大等待时间30s,超时跳出
                break
    return ppagestat

def pagewaitq(browser):
    ppagestat=0
    # print("进入循环等待")
    info=0
    while ppagestat==0:
        wtmp=browser.find_element_by_class_name('pPageStat').text
        # print(wtmp)
        if "找不到" in wtmp:
            ppagestat+=1
        elif "请稍候" not in wtmp:
            ppagestat+=1
            info=1
        else:
            print("else等待元素出现")
            time.sleep(0.5)
    return info




#定义日志文件写入
def logwrite(cont):
    file=datetime.datetime.now().strftime("%Y-%m-%d")
    if not os.path.exists("./log"):
        os.mkdir("log")
    with open('./log/'+file+".txt",'a+',encoding='utf-8') as f:
        f.write(cont)

# 从银行名字返回对应的key名
def bank_key(bkname):
    if "中国农业银行" in bkname:
        return "bank_abc"
    elif "中信银行" in bkname:
        return "bank_citic"
    elif "兴业银行" in bkname:
        return "bank_cib"
    elif "工商银行" in bkname:
        return "bank_icbc"
    elif "交通银行" in bkname:
        return "bank_bcm"
    elif "建设银行" in bkname:
        return "bank_ccb"
    elif "中国银行" in bkname:
        return "bank_boc"
    else:
        return "未知银行"

# 转换为web需要的json格式
def oldtonew(olddict):
    newdict={}
    newdict["errorResult"]={}
    newdict["errorResult"]["data"]=[]
    newdict["successResult"]={}
    newdict["successResult"]["data"]=[]

    for oldkey,oldval in olddict.items():
        tmpobj={}
        if oldkey=="profiletest":
            #如果是ebank网银电子票据接口
            tmpobj["InterfaceName"]="ebank网银电子票据接口"
            tmpobj["InterfaceKey"]="profiletest"
            if "错误" in oldval["status"]:
                tmpobj["info"]="接口异常"
                newdict["errorResult"]["data"].append(tmpobj)
            else:
                tmpobj["info"]="接口正常"
                newdict["successResult"]["data"].append(tmpobj)
        elif oldkey=="init":
            for initkey,initval in oldval.items():
                tmpobj={}
                if initkey=="initbank":
                    banklist=initval["status"].split("\n")
                    for onetxt in banklist:
                        tmpbkobj={}
                        if onetxt:#不是空再判断
                            if "正常" in onetxt:
                                # 正则出银行名字
                                tmpbkobj["InterfaceName"]=re.search(r".*银行",onetxt).group(0)
                                tmpbkobj["InterfaceKey"]=bank_key(tmpbkobj["InterfaceName"])
                                tmpbkobj["info"]="接口正常"
                                newdict["successResult"]["data"].append(tmpbkobj)
                            else:
                                tmpbkobj["InterfaceName"]=re.search(r".*银行",onetxt).group(0)
                                tmpbkobj["InterfaceKey"]=bank_key(tmpbkobj["InterfaceName"])
                                tmpbkobj["info"]="接口异常"
                                newdict["errorResult"]["data"].append(tmpbkobj)
                else:
                    if initkey=="financeapi":
                        tmpobj["InterfaceName"]="财务接口状态"
                        tmpobj["InterfaceKey"]="financeapi"
                    elif initkey=="gzw_supervision":
                        tmpobj["InterfaceName"]="国资委报送状态查询"
                        tmpobj["InterfaceKey"]="gzw_supervision"
                    if "成功" in initval["status"] or "正常" in initval["status"]:
                        tmpobj["info"]="接口正常"
                        newdict["successResult"]["data"].append(tmpobj)
                    else:
                        tmpobj["info"]="接口异常"
                        newdict["errorResult"]["data"].append(tmpobj)

        elif oldkey=="admin1":
            for adminkey,adminval in oldval.items():
                tmpobj={}
                if adminkey=="ecds_log":
                    tmpobj["InterfaceName"]="ECDS电票接口报文日志状态"
                    tmpobj["InterfaceKey"]="ecds_log"
                elif adminkey=="untreated_bill":
                    tmpobj["InterfaceName"]="票据交易系统未处理报文查询"
                    tmpobj["InterfaceKey"]="untreated_bill"
                elif adminkey=="smstest":
                    tmpobj["InterfaceName"]="手工短信验证状态"
                    tmpobj["InterfaceKey"]="smstest"
                else:
                    tmpobj["InterfaceName"]="未命名"
                    tmpobj["InterfaceKey"]="unknown"
                if "成功" in adminval["status"] or "正常" in adminval["status"]:
                    tmpobj["info"]="接口正常"
                    newdict["successResult"]["data"].append(tmpobj)
                else:
                    tmpobj["info"]="接口异常"
                    newdict["errorResult"]["data"].append(tmpobj)
        else:
            pass
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


# 根据webjson的数据返回保存数据库的格式,只用保存异常的字段和时间就行
def tosqldata(webjson):
    if webjson["data"]["errorResult"]["total"]==0:
        return {"exec_time":"error"}
    t=webjson["data"]["errorResult"]
    return {x["InterfaceKey"]:"异常" for x in t}

# 将字典转换为sql语句,key为字段,value为对应的值
def get_insert_str(data_dict):
    key_str = ",".join(list(data_dict.keys()))
    print(key_str)
    value_str = ",".join(map(lambda x: "{}".format(x) if str(x).isdigit() else "'{}'".format(x), data_dict.values()))
    print(value_str)
    insert_str = "INSERT INTO gold ({}) VALUES({});".format(key_str, value_str)
    return insert_str

if __name__ == '__main__':
    # 开启浏览器
    sttime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st="开始时间: "+sttime
    start_time=time.perf_counter()
    pwd = '123456'
    goldlog = {}
    '''切换网站到10.40.101.2
    #网银电子票据--->系统管理--->本企业账户资料设置 网页正常说明接口正常
    '''
    browser=chrome(ebank_url)
    login(browser,userinfo['ebank_user'], userinfo['ebank_pwd'])  #传入浏览器对象登录系统
    goldlog['profiletest']=profiletest(browser)
    # exit()
    '''
    # 切换网站到10.40.101.1,先用init登录
    '''
    browser.get(finance_url)
    # #开始使用init帐号登录.
    goldlog['init']=financeinit(browser)
    # #开始使用admin1帐号登录
    goldlog['admin1']=financeadmin1(browser)
    # 退出浏览器
    browser.quit()
    goldlog['total_time']=time.perf_counter()-start_time
    print(st)
    print(goldlog)
    #转换为web json格式
    webjson=oldtonew(goldlog)
    webjson["time"]=sttime
    dictsql=tosqldata(webjson)
    if dictsql["exec_time"]=="error":
        # 说明没有异常
        sql="insert into gold (exec_time) values (%s)" % sttime
    else:
        dictsql["exec_time"]=sttime
        sql=get_insert_str(dictsql)
    #上面sql已经生成完毕,下面开始保存到同级目录的sqlite
    import sqlite3
    conn=sqlite3.connect("chinagold.db")
    c=conn.cursor()
    c.execute(sql)
    # 关闭游标对象cursor
    c.close()
    # 提交事务更新到数据表
    conn.commit()
    # 关闭数据库连接
    conn.close()
    # dict.
    '''
    # webjson是返回网页的api格式
    # goldlog是返回原生的json格式,之后根据这个再添加上对应的名字通过logwrite函数写到log文件上
    # dictsql是需要保存到数据库的标准字典.......
    # 为什么格式这么多这么混杂搞的一脸懵逼,因为需求一直在变更就需要一直的在改变啊,为了不影响原来的逻辑,只能在最后返回数据的地方做数据处理......
    
    '''
    logwrite("\n--------------------------------\n")
    logwrite(st+"\n")
    et="\n结束时间: "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(et)
    resdict={}
    resdict['profiletest']="\n中国黄金ebank网银电子票据接口状态:   "
    resdict['init']="\n中国黄金finance资金管理init操作:   "
    resdict['admin1']="\n中国黄金finance资金管理admin1操作:   "
    resdict['total_time']="\n总耗时:   "
    resdict['financeapi']="财务接口状态:"
    resdict['initbank']="直接账户余额查询:"
    resdict['gzw_supervision']="国资委报送状态查询:"
    resdict['ecds_log']="ECDS电票接口报文日志状态:"
    resdict['untreated_bill']="票据交易系统未处理报文查询:"
    resdict['smstest']="手工短信验证状态:"
    for k,v in goldlog.items():
        if k=="profiletest":
            logwrite(resdict[k])
            logwrite(str(v['status']))
        elif k=='init' or k=="admin1":
            logwrite("\n"+resdict[k])
            for x,y in v.items():
                logwrite("\n    "+resdict[x]+"\n")
                logwrite("        "+str(y['status']))
        else:
            logwrite("\n"+resdict[k])
            logwrite(" "+str(v))
    logwrite(et)
    logwrite("\n--------------------------------\n")
    
    # autopy.alert.alert("程序运行完毕!","提示")
    '''这里不再用flask打开网页了,直接os.system(打开历史记录的exe)
    # webjson是打开浏览器的web数据格式.下面引入flask开个多线程就可以实现web结果的展示
    from flask import Flask
    from flask import render_template
    from flask_cors import CORS
    from threading import Thread
    
    app=Flask(__name__,template_folder="inspection",static_folder="inspection/static")
    app.jinja_env.variable_start_string="[["
    app.jinja_env.variable_end_string="]]"
    CORS(app)
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/api/current")
    def current():
        # 将模版替换为带日期选择的模版
        return {"data":[webjson],"msg":"查询成功","total":1}

    # 多线程开启flask,方便后续打开浏览器
    Thread(target=app.run).start()
    '''
    os.system("./历史查询.exe")
    # time.sleep(3)
    #输入盘符 浏览器的地址加参数
    # 示例:: r'C: && "C:\Users\Chrome\chrome.exe" http://127.0.0.1:5000'
    # chromeres=''
    # 通过命令打开浏览器展示界面
    # os.system(chromeres)
    print("正在打开网页服务器")
    ''''''