import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QFrame, QLineEdit, QMessageBox, QPushButton,QWidget
from PyQt5.QtWidgets import QLabel,QGridLayout
from PyQt5.QtGui import QColor, QFont, QIcon
import os,json


class Tesla(QWidget):
    def __init__(self):
        super().__init__()
        self.initui()
    def initui(self):
        '''这里写exe的具体过程'''
        self.resize(400,200)
        colorbg=QColor(255,255,255)
        # 设置背景颜色
        # self.setStyleSheet("QWidget {background-color:white}")
        # 设置标题
        self.setWindowTitle("中国黄金自动化测试帐号配置工具")
        # 设置图标logo
        self.setWindowIcon(QIcon('xx.ico'))
        self.setFont(QFont("Microsoft YaHei"))
        # self.setToolTip("我是鼠标悬停的小提示")
        # 创建一个frame
        self.frm=QFrame(self)
        # vh3=QHBoxLayout(self)
        # vh3.addWidget(QLabel("<h3 align='center' style='color:grey;'>中国黄金自动化巡检帐号配置</h3>"))
        # vh3.setGeometry(10,10,400,500)
        # 这里添加一个标题头,但是对齐方式不好就注释了
        # lbl=QLabel("                  中国黄金自动化巡检帐号配置           \n",self)
        # # lbl.setContentsMargins(50,20,30,0)
        # lbl.setStyleSheet("QLabel {margin-top:15px;border:0px solid #014F84;}")
        # lbl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # # lbl.resize(400,200)
        # lbl.adjustSize()
        # lbl.setAlignment(Qt.AlignCenter)
        # # lbl.setContentsMargins(25,10,30,20)
        # gold=QHBoxLayout()
        # gold.addWidget(lbl,1,Qt.AlignCenter)
        # gold.setAlignment(Qt.AlignBottom)
        # 栅格布局放置帐号配置信息
        grid=QGridLayout()
        # grid.setSpacing(30) # 网格行间距的距离大小
        # grid.addWidget(QLabel("<hr>",self),1,0,1,2)
        ebankuser=QLabel("ebank帐号: ",self)
        ebankuser.setToolTip("ebank帐号是网上金融管理系统的帐号")
        ebankuser.setAlignment(Qt.AlignRight|Qt.AlignCenter)
        self.ebankedit=QLineEdit()
        self.ebankedit.setToolTip("ebank帐号是网上金融管理系统的帐号")
        ebankpwd=QLabel("ebank密码: ",self) #如果不addWidget到网格会出现在左上角
        ebankpwd.setAlignment(Qt.AlignRight|Qt.AlignCenter)
        self.ebankpwdedit=QLineEdit()
        self.ebankpwdedit.setEchoMode(QtWidgets.QLineEdit.Password) #密码不显示明文
        inituser=QLabel("init帐号: ",self)
        inituser.setAlignment(Qt.AlignRight|Qt.AlignCenter)
        inituser.setToolTip("init帐号是资金管理系统处理银企平台、财务接口、国资委监管等接口的帐号")
        self.initedit=QLineEdit()
        self.initedit.setToolTip("init帐号是资金管理系统处理银企平台、财务接口、国资委监管等接口的帐号")
        initpwd=QLabel("init密码: ",self) #如果不addWidget到网格会出现在左上角
        initpwd.setAlignment(Qt.AlignRight|Qt.AlignCenter)
        self.initpwdedit=QLineEdit()
        self.initpwdedit.setEchoMode(QtWidgets.QLineEdit.Password) #密码不显示明文
        # alink.setOpenExternalLinks(True)
        grid.addWidget(ebankuser,0,0)
        grid.addWidget(self.ebankedit,0,1)
        grid.addWidget(ebankpwd,1,0)
        grid.addWidget(self.ebankpwdedit,1,1)
        grid.addWidget(inituser,2,0)
        grid.addWidget(self.initedit,2,1)
        grid.addWidget(initpwd,3,0)
        grid.addWidget(self.initpwdedit,3,1)
        # 添加一个空行
        # grid.addWidget(QLabel("<hr>"))
        #======================
        adminuser=QLabel("admin帐号: ",self)
        adminuser.setAlignment(Qt.AlignRight|Qt.AlignCenter)
        adminuser.setToolTip("admin帐号是资产管理系统处理票据交易系统、电票接口、手工短信等接口的帐号")
        self.adminedit=QLineEdit()
        self.adminedit.setToolTip("admin帐号是资产管理系统处理票据交易系统、电票接口、手工短信等接口的帐号")
        adminpwd=QLabel("admin密码: ",self) #如果不addWidget到网格会出现在左上角
        adminpwd.setAlignment(Qt.AlignRight|Qt.AlignCenter)
        self.adminpwdedit=QLineEdit()
        self.adminpwdedit.setEchoMode(QtWidgets.QLineEdit.Password) #密码不显示明文
        keypwd=QLabel("网银Key: ",self) #如果不addWidget到网格会出现在左上角
        keypwd.setToolTip("设置网银U盾的key")
        keypwd.setAlignment(Qt.AlignRight|Qt.AlignCenter)
        self.keypwdedit=QLineEdit()
        self.keypwdedit.setToolTip("设置网银U盾的key")
        self.keypwdedit.setEchoMode(QtWidgets.QLineEdit.Password) #密码不显示明文
        # self.keypwdedit.setText("hello world") #设置默认值
        # alink.setOpenExternalLinks(True)
        grid.addWidget(adminuser,4,0)
        grid.addWidget(self.adminedit,4,1)
        grid.addWidget(adminpwd,5,0)
        grid.addWidget(self.adminpwdedit,5,1)
        grid.addWidget(keypwd,6,0)
        grid.addWidget(self.keypwdedit,6,1)
        # grid.addWidget(QLabel("3333",self),6,0)
        phone=QLabel("手机号: ",self)
        phone.setAlignment(Qt.AlignRight|Qt.AlignCenter)
        phone.setToolTip("请指定测试手工短信发送的手机号")
        self.phoneedit=QLineEdit()
        self.phoneedit.setToolTip("请指定测试手工短信发送的手机号")
        grid.addWidget(phone,7,0)
        grid.addWidget(self.phoneedit,7,1)
        # lbl4=QLabel("我是第四行",self)
        # grid.addWidget(lbl4,7,0)
        # grid.addWidget(QLabel())
        retry=QLabel("重试次数: ",self)
        self.retryedit=QLineEdit()
        retry.setAlignment(Qt.AlignCenter|Qt.AlignRight)
        retry.setToolTip("请输入程序报错重试的次数")
        self.retryedit.setToolTip("请输入程序报错重试的次数")
        savebtn=QPushButton("保存",self)
        savebtn.clicked.connect(self.savedata)
        # savebtn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # savebtn.setStyleSheet("QPushButton{color:black}"
        #             "QPushButton{background-color:grey}"
        #             "QPushButton{border:2px}"
        #             "QPushButton{border-radius:10px}"
        #             "QPushButton{padding:2px 4px}")
        # quitbtn=QPushButton("退出",self)
        grid.addWidget(retry,8,0)
        grid.addWidget(self.retryedit,8,1)
        grid.addWidget(QLabel("<b>注意: </b>点击保存即可更新配置文件,以上字段不能为空",self),9,0,1,2)
        grid.addWidget(savebtn,10,0,1,2)
        # grid.addWidget(quitbtn,8,1)
        self.setLayout(grid)
        # self.setFixedSize(self.width(),self.height())#禁止调整窗口大小
        # 如果存在配置文件就初始化信息到edit中
        self.initjson()
        self.show()
        
    def savedata(self):
        '''点击保存按钮保存输入的帐号信息'''
        ebank_user=self.ebankedit.text() # ebank帐号信息
        ebank_pwd=self.ebankpwdedit.text()
        init_user=self.initedit.text() #init帐号信息
        init_pwd=self.initpwdedit.text()
        admin_user=self.adminedit.text() # admin 帐号信息
        admin_pwd=self.adminpwdedit.text() # admin 帐号密码
        bank_key=self.keypwdedit.text()
        phone=self.phoneedit.text()
        retry=self.retryedit.text()
        # 判断值不能为空
        if "" in [init_user,init_pwd,admin_user,admin_pwd,bank_key,phone,ebank_pwd,ebank_user]:
            print("不能存在空值")
            QMessageBox.information(self,"信息提示","信息不完整,请重新定义帐号信息",QMessageBox.Yes)
            return
        # 弹出一个信息提示框
        tmpdict={}
        tmpdict["ebank_user"]=ebank_user
        tmpdict["ebank_pwd"]=ebank_pwd
        tmpdict["finance_user1"]=init_user
        tmpdict["finance_user1_pwd"]=init_pwd
        tmpdict["finance_user2"]=admin_user
        tmpdict["finance_user2_pwd"]=admin_pwd
        tmpdict["key"]=bank_key
        tmpdict["retry"]=retry
        tmpdict["phone"]=phone
        tmptdict={}
        tmptdict["userinfo"]=tmpdict
        with open("./conf.json","w",encoding="utf8") as f:
            json.dump(tmptdict,f)#ensure_ascii=False参数是否开启中文unicode转码
        # 弹窗提示结果
        QMessageBox.information(self,"信息提示","\n 成功更新到配置文件",QMessageBox.Yes)
        QApplication.instance().quit()


    def initjson(self):
        '''将json格式的配置文件加载到exe中'''
        if os.path.exists("./conf.json"):
            with open("./conf.json","r",encoding="utf8") as f:
                userinfo=json.load(f)
                # print(userinfo)
                userinfo=userinfo["userinfo"]
                self.ebankedit.setText(userinfo["ebank_user"])
                self.ebankpwdedit.setText(userinfo["ebank_pwd"])
                self.initedit.setText(userinfo["finance_user1"])
                self.initpwdedit.setText(userinfo["finance_user1_pwd"])
                self.adminedit.setText(userinfo["finance_user2"])
                self.adminpwdedit.setText(userinfo["finance_user2_pwd"])
                self.keypwdedit.setText(userinfo["key"])
                self.phoneedit.setText(userinfo["phone"])
                self.retryedit.setText(userinfo["retry"])
        else:
            QMessageBox.information(self,"信息提示","配置文件不存在,请先填写帐号信息进行初始化",QMessageBox.Yes)



if __name__ == '__main__':
    app=QApplication(sys.argv)
    ex=Tesla()
    sys.exit(app.exec_())
    