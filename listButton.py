import sys
import json
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui,QtWidgets,QtCore
class Sbutton(QtWidgets.QWidget):
    #信号
    clicked = pyqtSignal()
    def __init__(self,con,tex,ti,x,y,w,h,strsha,parent=None):
        super().__init__(parent)
        self.wid=w
        self.hei=h
        self.widgetA=QtWidgets.QWidget(self)
        if x ==None:
            self.widgetA.resize(w,h)
            self.resize(w,h)
            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        else:
            self.widgetA.setGeometry(x,y,w,h)
        self.Icon = ""
        self.Title=ti
        self.Text=tex
        self.Title_font=QFont()
        self.Title_font.setFamily("微软雅黑")
        
        self.Title_font.setHintingPreference(QFont.HintingPreference.PreferNoHinting)
        self.Text_font=QFont()
        self.Text_font.setFamily("微软雅黑")
        
        self.Text_font.setHintingPreference(QFont.HintingPreference.PreferNoHinting)
        self.label_icon=QPushButton(self.widgetA)
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(con), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.label_icon.setIcon(icon)
        self.label_icon.setStyleSheet("background-color:rgb(219,84,97);")
        

        self.label_title=QLabel(self.widgetA)
        
        self.label_title.setText(self.Title)
        
        self.label_text=QLabel(self.widgetA)
        
        self.label_text.setText(self.Text)
        self.setStyleSheet("background-color:rgb(219,84,97);\n"
                                   "border-radius:20px;\n"
                                   )
        #self.widgetA.setStyleSheet("background-color:blue;")
        self.shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.shadow.setOffset(0,0) # 偏移
        self.shadow.setBlurRadius(strsha) # 阴影半径
        self.shadow.setColor(QtCore.Qt.black) # 阴影颜色
        self.setGraphicsEffect(self.shadow)
    def resizeEvent(self, event):
        self.Title_font.setPointSize(int(self.widgetA.height()/4))
        self.Text_font.setPointSize(self.widgetA.height()//8)
        self.label_text.setFont(self.Text_font)
        self.label_title.setFont(self.Title_font)
        self.label_icon.setGeometry(self.widgetA.height()//6,self.widgetA.height()//6,int(self.widgetA.height()//1.5),int(self.widgetA.height()//1.5))
        self.label_icon.setIconSize(QSize(int(self.widgetA.height()//1.5),int(self.widgetA.height()//1.5)))
        self.label_title.setGeometry(self.widgetA.height(),self.widgetA.height()//6,int(self.widgetA.width()//1.5),int(self.widgetA.height()*5/12))
        self.label_text.setGeometry(self.widgetA.height(),int(self.widgetA.height()*8/12),self.widgetA.width()//2,self.widgetA.height()//6)
        
        # 调用父类的resizeEvent方法
        super().resizeEvent(event)
    def mousePressEvent(self,event):
        #发射信号
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
            self.repaint()

