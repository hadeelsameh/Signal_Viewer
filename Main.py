from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import os
from biosppy.signals import bvp
from os import path
import sys
import pyqtgraph as pg
from PyQt5.QtCore import QTimer
import time
from PyQt5.QtWidgets import QApplication , QMainWindow ,QFileDialog
FORM_CLASS,_=loadUiType(path.join(path.dirname(__file__),"final.ui"))
import pandas as pd
import numpy as np
from PyQt5.QtGui import QIcon
class QTimerWithPause (QTimer):
     def _init_ (self, parent = None, name = ""):
           QTimer.__init__ (self, parent, name)

           self.startTime = 0
           self.interval  = 0

class MainApp(QMainWindow,FORM_CLASS):
     def __init__(self, parent = None):
          super(MainApp,self).__init__(parent)
          QMainWindow.__init__(self)
          self.setupUi(self)
          self.pushButton_3.clicked.connect(self.pushButton_handler)
          self.pushButton_6.clicked.connect(self.pushButton_handler)
          self.pushButton_11.clicked.connect(self.pushButton_handler)
          self.pushButton_2.clicked.connect(self.resume)
          self.pushButton.clicked.connect(self.pause)
          self.pushButton_9.clicked.connect(self.resume_1)
          self.pushButton_10.clicked.connect(self.pause_1)
          self.pushButton_14.clicked.connect(self.resume_2)
          self.pushButton_15.clicked.connect(self.pause_2)
          
     
     def startTimer (self, interval):
        self.interval    = interval
        self.startTime = time.time ()
        QTimer.start (self, interval, True) 
     def pause(self):
          self.timer.stop()
     
     def resume (self):
          self.timer.start()

     def pause_1(self):
          self.timer_1.stop()
     
     def resume_1 (self):
          self.timer_1.start()

     def pause_2(self):
          self.timer_2.stop()
     
     def resume_2 (self):
          self.timer_2.start()

     def pushButton_handler(self):
             print("Button pressed")
             self.open_dialog_box()

     def open_dialog_box(self):
          filename = QFileDialog.getOpenFileName(self)
          path = filename[0]
          print(path)
          print(filename)
          try:
             e=path.split('.')
             if (e[1]=='txt'):
                 self.y1,self.x=np.loadtxt(path, unpack=True, delimiter='\t')
                 self.y = []
                 self.z = [] 
                 self.i = 0
                 self.timer = QTimer()
                 self.timer.setInterval(50)
                 self.timer.timeout.connect(self.update_plot_data)
                 self.timer.start()
                 self.update_plot_data()

             elif (e[1]=='csv'):
                 self.data =pd.read_csv(path)
                 self.x_1 = self.data['x_value']
                 self.y1_1= self.data['total_1']
                 self.y_1 = []
                 self.z_1 = [] 
                 self.k = 0
                 self.timer_1 = QTimer()
                 self.timer_1.setInterval(50)
                 self.timer_1.timeout.connect(self.update_plot_data_1)
                 self.timer_1.start()
                 self.update_plot_data_1()
             elif (e[1]=='json'):
                 self.y1_2,self.x_2=np.loadtxt(path, unpack=True, delimiter='\t')
                 self.y_2 = []
                 self.z_2 = [] 
                 self.j = 0
                 self.timer_2 = QTimer()
                 self.timer_2.setInterval(50)
                 self.timer_2.timeout.connect(self.update_plot_data_2)
                 self.timer_2.start()
                 self.update_plot_data_2()
          
             else:
                 print("not supported extention")
                 self.statusBar().showMessage('Not supported')
          except IndexError:
               self.statusBar().showMessage('Not supported extention 11')

    
     def update_plot_data(self):
          print(type(self.x))
          print(type(self.z))
          self.i +=1
          self.z.append(self.x[self.i])  
          self.y.append(self.y1[self.i])  
          print(type(self.x))

          self.graphicsView.plot(self.z, self.y, label='Channel 1')
          if(self.i==(len (self.y1)-1)):
               self.timer.stop()
               self.statusBar().showMessage('Data for ch1 is finished')
               print("data is finished")
               self.pushButton_2.setEnabled(False)

     



     def update_plot_data_1(self):
          print(type(self.x_1))
          print(type(self.z_1))
          self.k +=1
          self.z_1.append(self.x_1[self.k])  
          self.y_1.append(self.y1_1[self.k])  
          print(type(self.x_1))
          self.graphicsView_2.plot(self.z_1, self.y_1, label='Channel 2')
          if(self.k==(len (self.y1_1)-1)):
               self.timer_1.stop()
               self.statusBar().showMessage('Data for ch2 is finished')
               self.pushButton_9.setEnabled(False)

     def update_plot_data_2(self):
          print(type(self.x_2))
          print(type(self.z_2))
          self.j +=1
          self.z_2.append(self.x_2[self.j])  
          self.y_2.append(self.y1_2[self.j])  
          print(type(self.x_2))
          self.graphicsView_3.plot(self.z_2, self.y_2, label='Channel 3')
          if(self.j==(len (self.y1_2)-1)):
               self.timer_2.stop()
               self.statusBar().showMessage('Data for ch3 is finished')
               self.pushButton_14.setEnabled(False)
          
def main():
     app = QApplication(sys.argv)
     window = MainApp()
     window.show()
     app.exec_()
if __name__ == "__main__":
    main()