# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 12:56:52 2021

@author: HUANGYANGLAI
"""
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import serial
import serial.tools.list_ports
from PyQt5.QtCore import QObject
from PyQt5.QtGui import *
import time
import os
import torch
import sys
from PyQt5.QtCore import pyqtSignal, QThread 
from PyQt5.QtSerialPort import QSerialPortInfo, QSerialPort
from PyQt5.QtWidgets import (QWidget, QPushButton,QLCDNumber,QTextEdit,
                             QLineEdit,
                             QSlider,QVBoxLayout,QApplication,QTextBrowser)
from PyQt5.Qt import QThread,QMutex
from fu import Ui_MainWindow
from test_bytes import bytes_link
import cv2
q_thread_1=QMutex()#创建线程锁
flag=0
last_img_decode=0


class Thread_1(QThread):#线程1用来控制退出程序
    def __init__(self):
        super().__init__()
    def run(self):
        q_thread_1.lock()
        app.quit()
        q_thread_1.unlock()
        
class UartRecieveThread(QThread):
    def __init__(self, run):
        super(UartRecieveThread, self).__init__()
        self.runfun = run
    def run(self):
        self.runfun()  #线程相关代码

class My_window(QMainWindow,Ui_MainWindow,QObject):
    signalRecieve = pyqtSignal(object)
    global last_img_decode
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        QObject.__init__(self)
        self.setupUi(self)
        self.mSerial=serial.Serial()#串口操作
        self.get_all_port()#串口检测
        self.button_start_uart.clicked.connect(self.port_open)#打开串口
        self.button_close_uart.clicked.connect(self.port_close)#关闭串口
        self.mThread = UartRecieveThread(self.data_receive) #子进程
        self.button_send_data.clicked.connect(self.send_data)#发送数据
        self.button_end.clicked.connect(self.click_1)#子线程
        self.button_clear.clicked.connect(self.textBrowser.clear)
        self.yolosetnet()#导入网络以及数据
        
    def click_1(self):
        self.Thread_1=Thread_1()
        self.Thread_1.start()
        
    def yolosetnet(self):
        self.net=cv2.dnn.readNet('yolov3.weights','yolov3.cfg')
        with open('coco.names','r')as f:
            self.classes=f.read().splitlines()   
    def get_all_port(self):#检测所存在的串口
        self.port_list_name=[]
        port_list=list(serial.tools.list_ports.comports())
        i=0
        if len(port_list)<=0:
            return []
        else:
            for port in port_list:
                i=i+1
                self.comboBox_uart_num.addItem(port[0])#将串口表放在串口选择框
    def port_open(self):
        self.mSerial.port=self.comboBox_uart_num.currentText()#获取端口号
        self.mSerial.baudrate=self.comboBox_rate.currentText()#获取波特率
        self.mSerial.bytesize =8        #数据位
        self.mSerial.stopbits = 1      #停止位
        self.mSerial.parity = serial.PARITY_NONE  #奇偶校验位
        try:
            self.mSerial.open()
            flag=1
            print("串口打开成功")
        except:
            print("串口打开失败")
            return False
        if not self.mThread.isRunning():
            self.mThread.start()#打开线程
        return True
    
    def port_close(self):#关闭串口
        try:
            print("串口关闭成功")
            self.mSerial.close()
            flag=0
        except:
            print("串口关闭失败")
            return False
        self.mThread.quit()
        return True
    
    def data_receive(self):
        while(self.mSerial.isOpen()):
            try:
                num=self.mSerial.inWaiting()
                #print("num是啥",num)
            except:
                self.mSerial.close()
                self.data=0
                self.signalRecieve.emit(self.data)
            if num>5000:
                 if self.mSerial.isOpen():
                     self.data=self.mSerial.read(num)#16进制
                     # self.data = self.mSerial.read(num).decode("gbk") #串口接收数据gbk
                     data=self.data
                     print("接受到数据了")

                     need_data=bytes_link(data)
                     if(sum(need_data)==0):
                         img_decode=last_img_decode
                     else:
                         img_decode=cv2.imdecode(need_data,cv2.IMREAD_COLOR)
                     last_img_decode=img_decode
                     print(img_decode.shape)
                     #img_decode=cv2.resize(img_decode,(561, 251),interpolation=cv2.INTER_AREA )
                     img_decode=cv2.cvtColor(img_decode,cv2.COLOR_BGR2RGB)
                     img_decode=self.process_frame(img_decode)
                     self.Qframe=QImage(img_decode.data,img_decode.shape[1],img_decode.shape[0],QImage.Format_RGB888)
                     md.label_view.setPixmap(QPixmap.fromImage(self.Qframe))
                     
                     #self.textBrowser.insertPlainText(data1)
                     #self.textBrowser.moveCursor(self.textBrowser.textCursor().End)
            time.sleep(0.001)
            md.update()
    def process_frame(self,img):
        print("hhhhhhhh",img.shape)
        height,width,_=img.shape
        blob=cv2.dnn.blobFromImage(img,1/255,(416,416),(0,0,0),swapRB=True,crop=False)
        #print(blob.shape)
        md.net.setInput(blob)
        #print(net.getLayerNames())#获取网络所有层名字
        #print(net.getUnconnectedOutLayers())获取三个尺度输出层的索引号
        layersNames=md.net.getLayerNames()
        #print('test',layersNames)
        output_layers_names=[layersNames[i[0]-1] for i in md.net.getUnconnectedOutLayers()]
        #print(output_layers_names)
        
        ###################开始推断过程
        prediction=md.net.forward(output_layers_names)
        #print('三种采样输出',prediction)
        ##################开始获取框框
        boxes=[]#存放预测框坐标
        objectness=[]#存放置信度
        class_probs=[]#存放类别概率
        class_ids=[]#存放预测框类别索引号
        class_names=[]#存放预测框类别名称
        
        for scale in prediction:#遍历三种尺度
            for bbox in scale:#遍历每个预测框
                obj=bbox[4]#获取该预测框的confidence
                class_scores=bbox[5:]#获取80个类别概率
                class_id=np.argmax(class_scores)#获取概率最高索引号
                class_name=md.classes[class_id]#获取概率最高类别的名称
                class_prob=class_scores[class_id]#获取概率最高类别概率
                #print(bbox[0])
                
                #获取预测框中心点坐标，预测框宽高
                center_x=int(bbox[0]*width)
                center_y=int(bbox[1]*height)
                w=int(bbox[2]*width)
                h=int(bbox[3]*height)
                #计算预测框左上角坐标
                x=int(center_x-w/2)
                y=int(center_y-h/2)
                #将每个预测框的结果存放在上面的列表
                boxes.append([x,y,w,h])
                objectness.append(float(obj))
                class_ids.append(class_name)
                class_names.append(class_name)
                class_probs.append(class_prob)
            
        confidences=np.array(class_probs)*np.array(objectness)
        CONF_THRES=0.1#指定置信度阈值，阈值越大，置信度过滤越强
        NMS_THRES=0.4#指定NMS阈值，阈值越小，NMS越强(非极大值抑制)
        indexes=cv2.dnn.NMSBoxes(boxes,confidences,CONF_THRES,NMS_THRES)
        print("indexes是啥",indexes)
        if(sum(indexes)==0):
            return img
        indexes.flatten()
        #print("gggg",len(indexes.flatten()))
        #随机给预测框颜色
        colors=[[255,0,255],[0,0,255],[0,255,255],[0,255,0],[255,255,0],[255,0,0],[180,187,28],[223,155,6],[94,218,121]]
        for i in indexes.flatten():
            #获取坐标
            x,y,w,h=boxes[i]
            #获取置信度
            confidence=str(round(confidences[i],2))
            #获取颜色画框
            color=colors[i%len(colors)]
            cv2.rectangle(img,(x,y),(x+w,y+h),color,8)
            #写类名和置信度
            #图片，添加名字，左上角坐标，字体，字体颜色，粗细
            string='{} {}'.format(class_names[i],confidence)
            cv2.putText(img,string,(x,y+20),cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),5)
        return img
    
    def send_data(self):
        try:
            send_datas=self.textEdit_send_data.toPlainText()#输入要发送的数据
            self.mSerial.write(bytes(send_datas))
        except Exception as exc:
            print("发送异常", exc)
                     
                 
if __name__=="__main__":
    app=QApplication(sys.argv)
    md=My_window()
    md.show()
    
    sys.exit(app.exec_())









