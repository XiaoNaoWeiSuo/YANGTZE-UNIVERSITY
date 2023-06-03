import requests
import ctypes
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineSettings
import webbrowser
import time
import json
#毛玻璃外部支持
# from ctypes import cdll
# from ctypes.wintypes import HWND, DWORD
from Ui_UI import Ui_MainWindow
from listButton import Sbutton
from FontDefine import SFont
from function import LoginImage
import sys

def FileChange(name,dat,path="data.json"):
        with open(path,"r+") as file:
                data=json.load(file)
        if isinstance(name,str):
            set_file=open("data.json","r+")
            set_file_dta=set_file.read()
            set_file.close()
            #print(set_file_dta)
            #print(type(set_file_dta))
            set_file_dta=json.loads(set_file_dta)
            if dat==None:
                return str(set_file_dta[name])
            else:
                set_file_dta[name]=dat
                file_data=open("data.json","w+")
                file_data.write(json.dumps(set_file_dta))
            set_file.close()
        else:
            if dat !=None:
                    with open(path,"w+") as file:
                            if len(name)==2:
                                    data[name[0]][name[1]]=dat
                            elif len(name)==3:
                                    data[name[0]][name[1]][name[2]]=dat
                            elif len(name)==4:
                                    data[name[0]][name[1]][name[2]][data[3]]=dat
                            json.dump(data,file)
            else:
                    with open(path,"r+") as file:
                            if len(name)==2:
                                    return data[name[0]][name[1]]
                            elif len(name)==3:
                                    return data[name[0]][name[1]][name[2]]
                            elif len(name)==4:
                                    return data[name[0]][name[1]][name[2]][data[3]]


class Label(QLabel):#绘制头像
    def __init__(self, *args,type="he.jpg",len,x,y, antialiasing=True, **kwargs):
        super(Label, self).__init__(*args, **kwargs)
        self.Antialiasing = antialiasing
        self.setMaximumSize(len, len)
        self.setMinimumSize(len, len)
        self.move(x,y)
        self.radius = len//2
        #####################核心实现#########################
        self.target = QPixmap(self.size())  # 大小和控件一样
        self.target.fill(Qt.transparent)  # 填充背景为透明
        p = QPixmap(type).scaled(  # 加载图片并缩放和控件一样大
            len, len, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        painter = QPainter(self.target)
        #if self.Antialiasing:
            # 抗锯齿
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        #painter.setPen(QPen(Qt.black, 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), self.radius, self.radius)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, p)
        self.setPixmap(self.target)

class WebEngineView(QtWebEngineWidgets.QWebEngineView):

    def __init__(self):
        super(WebEngineView, self).__init__()

    def createWindow(self, QWebEnginePage_WebWindowType):
        return self

class Main(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        super(Main,self).__init__(parent)
        self.setupUi(self)
        width=QApplication.desktop().screenGeometry().width()
        height=QApplication.desktop().screenGeometry().height()
    #启动初始化
        self.stackedWidget_right.setMinimumSize(int(width*0.57),0)
        self.stackedWidget_right.setMaximumSize(int(width*0.57),height)

        self.setWindowIcon(QIcon("jixielogo.ico"))
        #侧边栏字体
        self.fontall=SFont("微软雅黑",int(height*0.013))
        #其它部分字体
        self.orfont=SFont("Microsoft YaHei UI",int(height*0.009))
        self.pushButton_person.setFont(self.orfont)
        #self.pushButton_person.setIconSize(QSize(int(height*0.022),int(height*0.022)))
        self.label_name.setFont(self.orfont)
        #self.label_daytxt.setFont(self.fontall)
        self.comboBox_1.setFont(self.fontall)
        self.comboBox_2.setFont(self.fontall)
        self.comboBox_3.setFont(self.fontall)
        #阴影特效开关
        if bool(int(FileChange("ui",None))):
            self.add_shadow(self.gridWidget,25)
            #self.addblur(self.gridWidget)
            self.add_shadow(self.widget_left,12)
            self.add_shadow(self.widget_top,12)
        #self.setWindowFlag(QtCore.Qt.Tool)
        self.setWindowFlags(Qt.FramelessWindowHint)#无边框
        self.setAttribute(Qt.WA_TranslucentBackground)#背景透明
        self.base_widget = QtWidgets.QWidget() # 创建透明窗口
        # hWnd = HWND(int(self. winId()))
        # gradientColor = DWORD(0x50F2F2F2)
        # cdll.LoadLibrary('acrylic_dll\\acrylic.dll').setBlur(hWnd, gradientColor)
        self.gridLayout_2.addWidget(self.main_widget, 0, 0, 1, 1)
        index=FileChange("index",None)
        self.stackedWidget_right.setCurrentIndex(int(index))
        self.pushButton_home.setChecked(True)
        self.image_show=QLabel(self.page1)#初始化
        self.image_show.setObjectName("photo_show")
        self.image_show.setVisible(False)
        #self.pushButton_max.clicked.connect(lambda:self.max_n())

        self.resize(int(width//1.5),int(height//1.37))
        FileChange("width",width)
        self.w=int(width//1.5)
        FileChange("height",height)
        self.h=int(height//1.37)
        self.widget_left.setMaximumSize(int(self.w*0.142),99999)
        self.widget_left.setMinimumSize(int(self.w*0.142),0)
        self.widget_top.setMinimumHeight(int(self.h*0.0426))
        self.pushButton_min.setMinimumSize(QSize(int(self.h*0.02),int(self.h*0.02)))
        self.pushButton_person.setIconSize(QSize(int(self.h*0.02),int(self.h*0.02)))
        self.pushButton_close.setMinimumSize(QSize(int(self.h*0.02),int(self.h*0.02)))
        self.pushButton_left.setMinimumSize(QSize(int(self.h*0.02),int(self.h*0.02)))
        self.pushButton_reload.setMinimumSize(QSize(int(self.h*0.02),int(self.h*0.02)))
        self.pushButton_right.setMinimumSize(QSize(int(self.h*0.02),int(self.h*0.02)))
        #self.label_name.setWordWrap(True)

        #头像初始化
        self.label_logo_2=Label(self.page_person,type="./image/profile.png",len=int(self.h*0.146),x=20,y=30)
        self.label_logo.setMinimumSize(int(self.w*0.078),int(self.w*0.078))
        self.label_logo=Label(self.widget_left,type="./image/profile.png",len=int(self.w*0.078),x=int(self.w*0.032),y=10)
    #启动动画
        self.animation_sta = QPropertyAnimation(self.widget_left, b'geometry')
        self.animation_sta.setDuration(1000)
        self.animation_sta.setStartValue(QRect(9, 9, int(self.w*0.146), 0))
        self.animation_sta.setEndValue(QRect(9, 9, int(self.w*0.146), self.h-36))
        self.animation_sta.setEasingCurve(QEasingCurve.OutQuint)#缓冲曲线
        #self.animation.setLoopCount(-1)
        self.animation_sta.start()
    #配置浏览器
        self.webEngineView.settings().setAttribute(QWebEngineSettings.WebAttribute.ShowScrollBars,False)#删除webengineview的滑动条
        self.webEngineView.urlChanged.connect(lambda:self.label_name.setText(self.webEngineView.url().toDisplayString()))
        settings = QWebEngineSettings.globalSettings()
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        #self.webEngineView.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled,True)
        self.pushButton_left.clicked.connect(lambda:self.webEngineView.back())
        self.pushButton_right.clicked.connect(lambda:self.webEngineView.forward())
        self.pushButton_reload.clicked.connect(lambda:self.webEngineView.reload())
        self.pushButton_close.clicked.connect(lambda:self.close())
        self.pushButton_min.clicked.connect(lambda:self.showMinimized())
    #home page
        initlist=[self.pushButton_home,
                  self.pushButton_dianjing,
                  self.pushButton_bangong,
                  self.pushButton_ps,
                  self.pushButton_jianying,
                  self.pushButton_yingjian,self.pushButton_xinmeiti,
                  self.pushButton_net,
                  self.pushButton_code,
                  self.pushButton_yidong,
                  self.pushButton_jianyi,
                  self.pushButton_setting,
                  self.pushButton_tools,
                  ]
        self.comboBox_1.activated.connect(lambda:self.pageEX("1"))
        self.comboBox_2.activated.connect(lambda:self.pageEX("2"))
        self.comboBox_3.activated.connect(lambda:self.pageEX("3"))
        for x in initlist:
            x.setMinimumSize(0,int(self.h*0.0526))
            x.setMaximumSize(999,int(self.h*0.0526))
            x.setFont(self.fontall)
            x.setIconSize(QSize(int(height*0.022),int(height*0.022)))
        self.pushButton_home.clicked.connect(lambda:self.PageChange(0))
        self.pushButton_dianjing.clicked.connect(lambda:self.PageChange(1))
        self.pushButton_bangong.clicked.connect(lambda:self.PageChange(2))
        self.pushButton_ps.clicked.connect(lambda:self.PageChange(3))
        self.pushButton_jianying.clicked.connect(lambda:self.PageChange(4))
        self.pushButton_yingjian.clicked.connect(lambda:self.PageChange(5))
        self.pushButton_xinmeiti.clicked.connect(lambda:self.PageChange(6))
        self.pushButton_net.clicked.connect(lambda:self.PageChange(7))
        self.pushButton_code.clicked.connect(lambda:self.PageChange(8))
        self.pushButton_yidong.clicked.connect(lambda:self.PageChange(9))
        self.pushButton_jianyi.clicked.connect(lambda:self.PageChange(10))
        self.pushButton_setting.clicked.connect(lambda:self.PageChange(11))
        self.pushButton_tools.clicked.connect(lambda:self.PageChange(12))
        self.pushButton_person.clicked.connect(lambda:self.PageChange(13))
    #setting type
        #self.horizontalSlider_width.valueChanged.connect(lambda:print(self.verticalSlider_height.value()))
    #账户页面设置
        self.add_shadow(self.stackedWidget,15)
        self.stackedWidget.hide()

        self.font_title=SFont("微软雅黑",int(self.h*0.025))
        self.label_user.setGeometry(QtCore.QRect(int(self.h*0.016),0,int(self.h*0.12),int(self.h*0.04)))
        self.label_user.setFont(self.font_title)

        self.label_logo_2.setGeometry(QtCore.QRect(int(self.h*0.016),int(self.h*0.05),int(self.h*0.146),int(self.h*0.146)))

        self.font_text=SFont("微软雅黑",int(self.h*0.015))
        self.label_username.setGeometry(QtCore.QRect(int(self.h*0.17),int(self.h*0.05),int(self.h*0.48),int(self.h*0.025)))
        self.label_username.setFont(self.font_text)
        self.label_emailcode.setGeometry(QtCore.QRect(int(self.h*0.17),int(self.h*0.08),int(self.h*0.48),int(self.h*0.025)))
        self.label_emailcode.setFont(self.font_text)
        self.label_userjob.setGeometry(QtCore.QRect(int(self.h*0.17),int(self.h*0.11),int(self.h*0.48),int(self.h*0.025)))
        self.label_userjob.setFont(self.font_text)
        self.label_daytxt.setGeometry(QtCore.QRect(int(self.h*0.17),int(self.h*0.14),int(self.h*0.48),int(self.h*0.05)))
        self.label_daytxt.setFont(self.font_text)
        self.label_daytxt.setWordWrap(True)

        self.verticalLayoutWidget.setGeometry(QtCore.QRect(int(self.h*0.016),int(self.h*0.22),int(self.h*1.2),int(self.h/2)))
        self.verticalLayoutWidget.lower()
        self.verticalLayout_7.setContentsMargins(9, 0, 9, 0)

        FileChange("state","T")
        self.tip=0
        self.usermassage=Sbutton("./image/person_txt.png","Set up your personal information.","账号信息",None,None,self.h,int(self.h*0.085),10,self.verticalLayoutWidget)
        self.verticalLayout_7.addWidget(self.usermassage)
        self.usermassage.clicked.connect(lambda:self.animation_mas(0))
        self.checkupdate=Sbutton("./image/update.png","Set login information","到梦空间登录.",None,None,self.h,int(self.h*0.085),10,self.verticalLayoutWidget)
        self.verticalLayout_7.addWidget(self.checkupdate)
        self.checkupdate.clicked.connect(lambda:self.animation_mas(1))
        self.change=Sbutton("./image/account.png","Apply for a position in the association.","Your Job",None,None,self.h,int(self.h*0.085),10,self.verticalLayoutWidget)
        self.verticalLayout_7.addWidget(self.change)
        self.change.clicked.connect(lambda:self.animation_mas(2))
        self.work=Sbutton("./image/job.png","Switching login account.","Change Account",None,None,self.h,int(self.h*0.085),10,self.verticalLayoutWidget)
        self.verticalLayout_7.addWidget(self.work)
        self.work.clicked.connect(lambda:self.animation_mas(3))
        
        #每日一句
        try:
            x=requests.get("https://www.mxnzp.com/api/daily_word/recommend?count=1&app_id=tlhvmqelog8urhpf&app_secret=TC9pL1JYRjI2U0QvQ2Jld1R5OEw5Zz09")
            self.label_daytxt.setText(x.json()["data"][0]["content"])
        except:
            print("无网络")
    #right list
        #输入框限制和完善
        myValidator = QRegExpValidator(QRegExp("^[0-9]\d{10}$"))
        self.lineEdit_account.setValidator(myValidator)
        self.lineEdit_phone.setValidator(myValidator)
        self.lineEdit_account.setContextMenuPolicy(Qt.NoContextMenu)
        self.lineEdit_phone.setContextMenuPolicy(Qt.NoContextMenu)
        #check=QRegExpValidator(QRegExp("^[0-9]\d{4}$"))#验证码文本限制
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.lineEdit_password.setContextMenuPolicy(Qt.NoContextMenu)

        #登录页设置
        listlabel=[self.label_QQ,self.label_phone,self.label_Email,self.label_Name,self.label_Code,self.label_School]
        listlabelnum=[self.label_QQnum,
                      self.label_phonenum,
                      self.label_Emailnum,
                      self.label_Namenum,
                      self.label_Codenum,
                      self.label_Schoolnum,
                      self.lineEdit_account,
                      self.lineEdit_password,
                      self.lineEdit_phone,
                      self.pushButton_login,
                      self.pushButton_login_2,
                      self.pushButton_enrool,
                      self.pushButton_backlogin,
                      self.label_zhu
                      ]
        for x in listlabel:
            x.setFont(self.fontall)
        for x in listlabelnum:
            x.setFont(self.font_text)
        listbutt=[self.pushButton_login,
                  self.pushButton_enrool,
                  self.pushButton_backlogin,
                  self.pushButton_login_2]
        listedit=[self.lineEdit_account,
                  self.lineEdit_password,
                  self.lineEdit_phone]
        for x in listedit:
             x.setMinimumSize(QSize(int(self.h*0.35),int(self.h*0.0526)))
             x.setStyleSheet("border-radius:%spx;\n"
                             "background-color:white;"%int(self.h*0.0526//5)
                             )
             x.setAlignment(Qt.AlignHCenter)
             x.setClearButtonEnabled(True)
        for i in listbutt:
             i.setMinimumSize(QSize(int(self.h*0.2),int(self.h*0.0526)))
        #信息初始化
        if FileChange(["user","statu"],None)=="100":
            self.pushButton_person.setText(FileChange(["user","name"],None))
            self.label_username.setText(FileChange(["user","name"],None))
            self.label_phonenum.setText(FileChange(["user","phone"],None))
            self.label_Emailnum.setText(FileChange(["user","email"],None))
            self.label_emailcode.setText(FileChange(["user","email"],None))
            self.label_Namenum.setText(FileChange(["user","name"],None))
            self.label_Codenum.setText(FileChange(["user","ID"],None))
            self.label_Schoolnum.setText(FileChange(["user","school"],None))
            self.label_QQnum.setText("当前采用到梦空间登录方式")
        elif FileChange(["user","statu"],None)=="200":
            self.pushButton_person.setText(FileChange(["user","account"],None))
            self.label_username.setText(FileChange(["user","account"],None))
            self.label_QQnum.setText(FileChange(["user","account"],None))
            self.label_phonenum.setText("=")
            self.label_Emailnum.setText("=")
            self.label_Namenum.setText("=")
            self.label_Codenum.setText("=")
            self.label_Schoolnum.setText("=")
        else:
             self.pushButton_person.setText("未登录")
        self.webEngineView_shua.setUrl(QtCore.QUrl("https://clown.pxtl.com.cn/"))
        self.webEngineView_shua.settings().setAttribute(QWebEngineSettings.WebAttribute.ShowScrollBars,False)#删除webengineview的滑动条
    
        self.pushButton_enrool.clicked.connect(lambda:self.stackedWidget.setCurrentIndex(2))
        self.pushButton_backlogin.clicked.connect(lambda:self.stackedWidget.setCurrentIndex(1))
        self.pushButton_login.clicked.connect(lambda:LoginImage.image(self.lineEdit_phone.text()))
        self.pushButton_login.clicked.connect(lambda:self.loginexe(2))
        self.pushButton_login_2.clicked.connect(lambda:LoginImage.dmkj(self.lineEdit_account.text(),self.lineEdit_password.text()))
        self.pushButton_login_2.clicked.connect(lambda:self.loginexe(1))

        #信息页设置
        self.tip_anima=True
        self.tip_butt=None
    #电竞部测试
        Icon="c:\\Users\\35170\\Desktop\\+\\Yangtze Uniersity\\image/camera.png"
        #print(width,self.w,self.page_dianjin.width())
        self.button=Sbutton(Icon,"This is a test sentence.","Title",int(self.h*0.016),int(self.h*0.016),int(self.h//1.3),int(self.h*0.085),10,self.page_dianjin)
    #配置建议页
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(int(self.h*0.01),int(self.h*0.01),int(self.h*1.2),int(self.h/1.5)))
        self.verticalLayoutWidget_2.lower()
        self.verticalLayout_8.setContentsMargins(9, 0, 9, 0)
        self.advic1=Sbutton("./image/person_txt.png","提供开发建议，使用反馈等","联系开发者",None,None,self.h,int(self.h*0.085),10,self.verticalLayoutWidget_2)
        self.verticalLayout_8.addWidget(self.advic1)
        self.advic2=Sbutton("./image/person_txt.png","协会发展建设建议","长大计协理事会",None,None,self.h,int(self.h*0.085),10,self.verticalLayoutWidget_2)
        self.verticalLayout_8.addWidget(self.advic2)
        self.advic3=Sbutton("./image/person_txt.png","提供协会建设意见和反馈","协会管理层",None,None,self.h,int(self.h*0.085),10,self.verticalLayoutWidget_2)
        self.verticalLayout_8.addWidget(self.advic3)
        self.advic4=Sbutton("./image/person_txt.png","反馈部门建议","各部门部长",None,None,self.h,int(self.h*0.085),10,self.verticalLayoutWidget_2)
        self.verticalLayout_8.addWidget(self.advic4)
        self.advic5=Sbutton("./image/person_txt.png","向指定协会干事发送反馈建议","自定义对象",None,None,self.h,int(self.h*0.085),10,self.verticalLayoutWidget_2)
        self.verticalLayout_8.addWidget(self.advic5)
        self.advic6=Sbutton("./image/person_txt.png","协会成员联系方式","协会通讯录",None,None,self.h,int(self.h*0.085),10,self.verticalLayoutWidget_2)
        self.verticalLayout_8.addWidget(self.advic6)
    #配置工具页
        self.pushButton_loginweb.clicked.connect(lambda:webbrowser.open("10.151.0.249/0.htm"))
        self.pushButton_warning.clicked.connect(lambda:self.max_n("测试","This is a test sentence"))
    #配置设置页
        num=FileChange("ui",None)
        self.checkBox_ui.setChecked(bool(int(num)))
        self.checkBox_ui.stateChanged.connect(lambda:self.setting_ui())

        self.setting_check=Sbutton("./image/job.png","Obtain the latest version.","Check Updates",int(self.h*0.016),int(self.h*0.016),int(self.h//1.3),int(self.h*0.085),10,self.page_tools)
        self.setting_check.clicked.connect(lambda:self.max_n("更新","当前已是最新版本"))
    def loginexe(self,state):
        time.sleep(1)
        check = FileChange(["user","statu"],None)
        if check =="100" or check =="200":
            if state==1:#到梦空间登录
                self.stackedWidget.setCurrentIndex(0)
                self.label_QQnum.setText("None")
                self.label_phonenum.setText(FileChange(["user","phone"],None))
                self.label_Emailnum.setText(FileChange(["user","email"],None))
                self.label_emailcode.setText(FileChange(["user","email"],None))
                self.label_Namenum.setText(FileChange(["user","name"],None))
                self.pushButton_person.setText(FileChange(["user","name"],None))
                self.label_username.setText(FileChange(["user","name"],None))
                self.label_Codenum.setText(FileChange(["user","ID"],None))
                self.label_Schoolnum.setText(FileChange(["user","school"],None))

            else:
                self.stackedWidget.setCurrentIndex(0)
                FileChange(["user","account"],self.lineEdit_phone.text())
                self.pushButton_person.setText(self.lineEdit_phone.text())
                self.label_username.setText(self.lineEdit_phone.text())
                self.label_QQnum.setText(self.lineEdit_phone.text())
                self.label_phonenum.setText("None")
                self.label_Emailnum.setText("None")
                self.label_emailcode.setText("None")
                self.label_Namenum.setText("None")
                self.label_Codenum.setText("None")
                self.label_Schoolnum.setText("None")
        else:
            self.max_n("警告","你输入的账号或者密码错误，请检查你的账号密码并重新输入")
            self.lineEdit_account.clear()
            self.lineEdit_password.clear()
    def change(self):
        width=int(self.verticalSlider_height.value())
        heigth=int(self.horizontalSlider_width.value())
        self.resize(heigth,width)
    def pageEX(self,nae):
        if nae=="1":
            self.image_show.setVisible(False)
            self.webEngineView.setVisible(True)
            name=self.comboBox_1.currentText()
            if name=="计协简介":
                self.webEngineView.setUrl(QtCore.QUrl("https://mp.weixin.qq.com/s/N3uN1a2lxzfJb5yOsKTw9g"))
            elif name=="实验部分":
                self.webEngineView.setUrl(QtCore.QUrl("http://mp.weixin.qq.com/mp/homepage?__biz=MzAxOTIxNDMyNg==&hid=8&sn=90a3e45d0101f52fc4b088e737d034ce&scene=18#wechat_redirect"))
        elif nae=="2":
            
            self.image_show.setVisible(False)
            self.webEngineView.setVisible(True)
            name=self.comboBox_2.currentText()
            if name=="资源整合":
                self.webEngineView.setUrl(QtCore.QUrl("https://mp.weixin.qq.com/s/Am6qs5q9u3xrYJsAezNogA"))
            elif name=="其他干货":
                self.webEngineView.setUrl(QtCore.QUrl("http://mp.weixin.qq.com/mp/homepage?__biz=MzAxOTIxNDMyNg==&hid=3&sn=fe1ba0a9e4253765db9b4aacc7a6b223&scene=18#wechat_redirect"))
            elif name=="号内搜索":
                self.webEngineView.setUrl(QtCore.QUrl("https://data.newrank.cn/m/s.html?s=OzAuPi4/Lj02"))
            elif name=="免费福利":
                self.webEngineView.setUrl(QtCore.QUrl("https://mp.weixin.qq.com/s/jekBkkVHyJesl3-f7zngiQ"))
            elif name=="刷赞":
                self.webEngineView.setUrl(QtCore.QUrl("https://clown.pxtl.com.cn/"))
        elif nae=="3":
            name=self.comboBox_3.currentText()
            if name=="西区地图":
                self.image_show.setVisible(False)
                self.webEngineView.setVisible(False)
                self.image_show=QLabel(self.page1)
                self.image_show.setObjectName("photo_show")
                self.image_show.setStyleSheet("image:url(\"image/map.jpg\")")
                self.gridLayout_3.addWidget(self.image_show, 1, 0, 1, 5)
            elif name=="校历":
                self.image_show.setVisible(False)
                self.webEngineView.setVisible(False)
                self.image_show=QLabel(self.page1)
                self.image_show.setObjectName("photo_show")
                self.image_show.setStyleSheet("image:url(\"image/dital.jpg\")")
                self.gridLayout_3.addWidget(self.image_show, 1, 0, 1, 5)
    def PageChange(self,botn):
        self.stackedWidget_right.setCurrentIndex(botn)
    def max_n(self,title="公告",text="公告测试内容"):
        self.hide_widget = QtWidgets.QWidget(self.centralwidget)
        self.hide_widget.setStyleSheet("border-radius:7px;\n""background-color: rgba(29, 29, 29, 95);")
        self.hide_widget.setObjectName("hide_widget")
        self.gridLayout_2.addWidget(self.hide_widget, 0, 0, 1, 1)
        self.w_hide=QtWidgets.QWidget(self.hide_widget)
        self.w_hide.setGeometry(QRect(int(self.w*0.05),self.h//4,int(self.w*0.9),int(self.h*0.35)))
        self.w_hide.setStyleSheet("border-radius:7px;\n""background-color: rgb(255,255,255);")
        self.add_shadow(self.w_hide,25)

        self.Layout_hide=QtWidgets.QVBoxLayout(self.w_hide)
        #self.Layout_hide.setContentsMargins(20, 20, 20, 20)

        self.label_h_title = QtWidgets.QLabel(self.w_hide)
        self.label_h_title.setMinimumSize(QtCore.QSize(0,self.w_hide.height()//8))
        self.label_h_title.setMaximumSize(QtCore.QSize(9999,self.w_hide.height()//8))
        self.label_h_title.setStyleSheet("text-align:center;")
        self.label_h_title.setText(title)
        titlefont=SFont("微软雅黑",int(self.w_hide.height()*0.07))
        self.label_h_title.setFont(titlefont)
        self.label_h_title.setObjectName("label_h_title")
        self.Layout_hide.addWidget(self.label_h_title, 0, QtCore.Qt.AlignCenter)

        self.label_line=QtWidgets.QLabel(self.w_hide)
        self.label_line.setMinimumSize(QtCore.QSize(0,4))
        self.label_line.setMaximumSize(QtCore.QSize(9999,4))
        self.label_line.setStyleSheet("border-radius:2px;\n""background-color:rgb(85, 85, 255);")
        self.label_line.setObjectName("label_line")
        self.Layout_hide.addWidget(self.label_line, 0, QtCore.Qt.AlignCenter)

        self.label_h_txt = QtWidgets.QTextBrowser(self.w_hide)
        self.label_h_txt.setMinimumSize(QSize(int(self.w*0.8),int(self.w_hide.height()//7*3)))
        textfont=SFont("微软雅黑",int(self.w_hide.height()*0.05))
        self.label_h_txt.setStyleSheet("text-align:center;\n"
                                       "background-color:white;")
        self.label_h_txt.setText(text)
        #self.label_h_txt.setWordWrap(True)
        self.label_h_txt.setFont(textfont)
        self.label_h_txt.setObjectName("label_h_txt")
        self.label_h_txt.setContextMenuPolicy(Qt.NoContextMenu)#禁用右键菜单栏
        self.Layout_hide.addWidget(self.label_h_txt, 0, QtCore.Qt.AlignCenter)

        self.hide_pushbutton = QtWidgets.QPushButton(self.w_hide)
        self.hide_pushbutton.setMinimumSize(QtCore.QSize(int(self.h*0.2),int(self.h*0.0526)))
        self.hide_pushbutton.setMaximumSize(QtCore.QSize(int(self.h*0.2),int(self.h*0.0526)))
        self.hide_pushbutton.setText("确定")
        self.hide_pushbutton.setFont(textfont)
        self.hide_pushbutton.setObjectName("hide_pushButton")
        self.hide_pushbutton.clicked.connect(lambda:self.hide_widget.hide())
        self.hide_pushbutton.setStyleSheet("QPushButton{\n"
"    background-color: rgb(255, 255, 255);\n"
"    border-radius:5px;\n"
"    border:1px solid rgb(85, 85, 255);\n"
"\n"
"}\n"
"QPushButton:hover{\n"
"    background-color:rgb(170, 170, 255);\n"
"    border-radius:5px;\n"
"}\n"
)
        self.Layout_hide.addWidget(self.hide_pushbutton, 0, QtCore.Qt.AlignCenter)


        self.hide_anima=QPropertyAnimation(self.label_line,b"geometry",self)
        self.hide_anima.setDuration(1800)
        self.hide_anima.setStartValue(QRect(self.w//2,self.w_hide.height()//5,0,4))
        self.hide_anima.setEndValue(QRect(int(self.w*0.05),self.w_hide.height()//5,int(self.width()*0.8),4))
        self.hide_anima.setEasingCurve(QEasingCurve.OutQuint)
        self.hide_anima.start()
    def mousePressEvent(self, event):
        if event.button()==Qt.LeftButton:
            self.m_flag=True
            self.m_Position=event.globalPos()-self.pos() #获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  #更改鼠标图标
    def mouseMoveEvent(self, QMouseEvent):
        try:        #因为在某些非容器控件上依然可以长按拖动，会造成数据错误，故写此
            if Qt.LeftButton and self.m_flag:
                self.move(QMouseEvent.globalPos()-self.m_Position)#更改窗口位置
                QMouseEvent.accept()
        except:
            print("EventError")
            QMouseEvent.accept()
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag=False
        self.setCursor(QCursor(Qt.ArrowCursor))
    def setting_ui(self):
        if self.checkBox_ui.isChecked():
            FileChange("ui",1)
        else:
            FileChange("ui",0)
    def add_shadow(self,name,str):#控件阴影
        self.effect_shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.effect_shadow.setOffset(0,0) # 偏移
        self.effect_shadow.setBlurRadius(str) # 阴影半径
        self.effect_shadow.setColor(QtCore.Qt.black) # 阴影颜色
        name.setGraphicsEffect(self.effect_shadow)
    def addblur(self,name):#添加模糊
        self.effect_blur=QtWidgets.QGraphicsBlurEffect(self)
        self.effect_blur.setBlurHints(QtWidgets.QGraphicsBlurEffect.QualityHint)
        self.effect_blur.setBlurRadius(4)
        name.setGraphicsEffect(self.effect_blur)
    def animation_mas(self,butt):
        animation1 = QPropertyAnimation(self.usermassage, b"size",self)
        animation2 = QPropertyAnimation(self.checkupdate, b"size",self)
        animation3 = QPropertyAnimation(self.change, b"size",self)
        animation4 = QPropertyAnimation(self.work, b"size",self)
        animation5=  QPropertyAnimation(self.stackedWidget, b"geometry",self)
        animationlist=[animation1,animation2,animation3,animation4]


        if FileChange("state",None)=="T":
            animation5.setDuration(750)
            animation5.setStartValue(QRect(int(self.w*1.2),int(self.h*0.05),int(self.h//2),int(self.h*0.78)))
            animation5.setEndValue(QRect(self.w//2,int(self.h*0.05),int(self.h//2),int(self.h*0.78)))
            animation5.setEasingCurve(QEasingCurve.OutQuint)
            self.stackedWidget.setCurrentIndex(butt)
            for ani in animationlist:
                ani.setDuration(750)
                ani.setStartValue(QSize(self.h,int(self.h*0.085)))
                ani.setEndValue(QSize(int(self.w//2.2),int(self.h*0.085)))
                ani.setEasingCurve(QEasingCurve.OutQuint)
            FileChange("state","F")
            self.tip=butt
        else:
            if butt==self.tip:
                animation5.setDuration(750)
                animation5.setStartValue(QRect(self.w//2,int(self.h*0.05),int(self.h//2),int(self.h*0.78)))
                animation5.setEndValue(QRect(int(self.w*1.2),int(self.h*0.05),int(self.h//2),int(self.h*0.78)))
                animation5.setEasingCurve(QEasingCurve.OutQuint)
                for ani in animationlist:
                    ani.setDuration(750)
                    ani.setStartValue(QSize(int(self.w//2.2),int(self.h*0.085)))
                    ani.setEndValue(QSize(self.h,int(self.h*0.085)))
                    ani.setEasingCurve(QEasingCurve.OutQuint)
                FileChange("state","T")
            else:
                self.stackedWidget.setCurrentIndex(butt)
            self.tip=butt
        animation1.start()
        animation2.start()
        animation3.start()
        animation4.start()
        self.stackedWidget.show()
        animation5.start()
        
    def selectfile(self):
        filename,filetype=QFileDialog.getOpenFileName(self.stackedWidget,"选择图片","*.jpg;;*.png;;*.jpeg")
        if filename!="":
            FileChange("logofile",filename)
    def paintEvent(self, event):
        # 重写 paintEvent 方法来设置抗锯齿属性
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        # 调用父类的 paintEvent 方法绘制标签
        super().paintEvent(event)

if __name__=="__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)#自适应窗口分辨率
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    app=QApplication(sys.argv)
    window=Main()
    window.show()
    sys.exit(app.exec())