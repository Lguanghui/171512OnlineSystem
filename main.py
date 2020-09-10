# -*- coding: utf-8 -*-
import sys, os
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5.QtCore import QFileInfo
from PyQt5.QtWidgets import QApplication,QMainWindow,QMessageBox,QFileDialog
from UIfile import Ui_MainWindow
from ftpFunctions import ftpconnect
import io

class mainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        self.setupUi(self)
        self.IniUI()
    #初始化
    def IniUI(self):
        self.Quantity = 0      #每个人要提交的文件数量
        self.fileNUM = 0    #选择的文件数量
        self.HINT = ''
        self.Remark = ''
        self.StudentName.clear()
        self.StudentNumber.clear()
        self.filename.clear()
        self.remarks.clear()
        self.textEdit_NotSubmitNameList.clear()
        self.ftp = ftpconnect("...",21,"...", "...")    #ip地址、端口、用户名、密码
        self.showCurrentTask()  #显示当前任务
        self.initAllStudentNames()

        #设置触发器
        self.pushButton_selectFile.clicked.connect(self.selectFIlE)
        self.pushButton_submit.clicked.connect(self.submit)
        self.StudentName.editingFinished.connect(self.getStudentName)
        self.StudentNumber.editingFinished.connect(self.getStudentNUM)
        self.pushButton_NotSubStudentList.clicked.connect(self.NotSubmitNameList)

        self.remotePATH = "/home/yunyi/Desktop/FTP收件箱/"   #设置服务器端路径

    def getStudentName(self):
        self.name = self.StudentName.text()

    def getStudentNUM(self):
        self.number = self.StudentNumber.text()

    def getRemarks(self):
        self.Remark = self.remarks.text()

    #查看谁还没有提交文件，或者提交文件数量
    def NotSubmitNameList(self):
        #先遍历所有的文件夹，计数
        self.countQuantity(self.remotePATH + '图片/')
        self.countQuantity(self.remotePATH + 'pdf/')
        self.countQuantity(self.remotePATH + 'doc文件/')
        self.countQuantity(self.remotePATH + 'xlsx文件/')
        self.countQuantity(self.remotePATH + '压缩文件/')
        nameList = ''
        # 去掉已经提交完成的
        for key in self.StudentDict:
            if self.StudentDict[key] == self.Quantity:
                continue
            else:
                dif = self.Quantity - self.StudentDict[key]
                nameList = nameList + key + '还差' + str(dif) + '个文件' + '\n'
        self.textEdit_NotSubmitNameList.setText(nameList)
        # print(self.StudentDict)
        return
    #提交文件按钮被按下
    def submit(self):
        #设置名字学号备注
        self.getStudentNUM()
        self.getStudentName()
        #判断名字是否在名单里
        if not self.name in self.AllStudentName:
            QMessageBox.warning(self, 'warning', "名字不对吧😯", buttons=QMessageBox.Ok)
            return
        if len(self.name) < 2:
            QMessageBox.warning(self, 'warning', "名字不对吧😯", buttons=QMessageBox.Ok)
            return
        if len(self.number) != 8:
            QMessageBox.warning(self, 'warning', "学号不对吧😇", buttons=QMessageBox.Ok)
            return
        self.getRemarks()
        if self.uploadFILE():
            QMessageBox.warning(self, 'Title', "上传成功👍", buttons=QMessageBox.Ok)
            return
            # self.ftp.close()
        else:
            QMessageBox.warning(self, 'Title', "上传失败，你是不是选错文件了😐", buttons=QMessageBox.Ok)
            return

    def uploadFILE(self):
        if self.fileNUM == 0:
            QMessageBox.warning(self, 'question', "你得选个文件上传😐", buttons=QMessageBox.Ok)
            return
        bufsize = 1024
        if len(self.Remark) >0:
            self.writeRemarkFile()  #写入备注
        #上传文件
        for x in range(self.fileNUM):
            localpath = self.filePATH[x]
            fileInfo = QFileInfo(localpath) #文件信息
            # filename = fileInfo.fileName()  #获取带后缀的文件名
            suffix = fileInfo.suffix()  #文件后缀
            filename = self.number + '-' + self.name + '.' + suffix
            fp = open(localpath, 'rb')  #写入流
            #根据文件后缀判断放入那个文件夹
            if suffix == 'docx':
                self.ftp.storbinary('STOR ' + self.remotePATH +'doc文件/'+ filename, fp, bufsize)
                self.ftp.set_debuglevel(0)
            elif suffix == 'pdf':
                self.ftp.storbinary('STOR ' + self.remotePATH + 'pdf/' + filename, fp, bufsize)
                self.ftp.set_debuglevel(0)
            elif suffix == 'xlsx':
                self.ftp.storbinary('STOR ' + self.remotePATH + 'xlsx文件/' + filename, fp, bufsize)
                self.ftp.set_debuglevel(0)
            elif suffix == 'jpg' or suffix == 'jpeg' or suffix == 'png' or suffix == 'bmp' or suffix == 'JPG':
                self.ftp.storbinary('STOR ' + self.remotePATH + '图片/' + filename, fp, bufsize)
                self.ftp.set_debuglevel(0)
            elif suffix == 'zip' or suffix == 'rar' or suffix == '7z' or suffix == 'tar':
                self.ftp.storbinary('STOR ' + self.remotePATH + '压缩文件/' + filename, fp, bufsize)
                self.ftp.set_debuglevel(0)
            else:
                QMessageBox.warning(self, 'critical', "你选的文件格式不对啊🤔", buttons=QMessageBox.Ok)
                return False
            fp.close()
        return True

    def initAllStudentNames(self):
        self.AllStudentName = [...] #学生列表

        #按索引生成字典，存储每个人已经提交的文件数量
        self.StudentDict = {name:0 for name in self.AllStudentName}
        # print(self.StudentDict)



    def selectFIlE(self):
        path, ret = QFileDialog.getOpenFileNames(self, '选取需要提交的文件', '.', '(*.jpg *.png *.bmp *.jpeg *.doc *.docx *.xlsx *.pdf *.JPG *.zip *.rar *.7z *.tar)')
        if ret:
            filename = "\n".join(path)  #添加\n自动换行
            self.fileNUM = len(path)
            self.filePATH = path
        else:
            QMessageBox.warning(self, 'warning', "你需要选择一个文件上传🙄", buttons=QMessageBox.Ok)
            return
        self.filename.setText(filename)

    # 将ftp读取到的txt数据存下来，此过程并没有将txt文件下载
    def saveRetrieveData(self,data):
        self.HINT = self.HINT + data + '\n'  #这样可以处理多行信息
        tmp = data
        # print(len(tmp))
        #借用try来获得需要提交的文件数量，因为并不是每一行文字的最后都是需要提交的文件数量
        try:
            f = int(tmp[-1])    #得到需要提交的文件数量
        except:
            return
        else:
            self.Quantity = f

    #显示目前的任务
    def showCurrentTask(self):
        file = '/home/yunyi/Desktop/FTP收件箱/systemHINT.txt'
        self.ftp.retrlines('RETR %s' % file, self.saveRetrieveData)
        self.current_task.setText(self.HINT)

    #直接用FTP在线上写入文件
    def writeRemarkFile(self):
        file = '/home/yunyi/Desktop/FTP收件箱/备注/' + self.name + '.txt'    #根据姓名创建备注文件
        bio = io.BytesIO(bytes( self.Remark, encoding = "utf8"))        #先需要转化为bytes类型
        self.ftp.storbinary('STOR %s' % file, bio)

    #遍历每个文件夹，如果有名字，则在字典中加一
    def countQuantity(self,filepath):
        self.ftp.cwd(filepath)  #设置ftp工作目录
        filelist = self.ftp.nlst()  #获取文件列表
        for file in filelist:
            file = file.split('.')  #除去后缀
            name = file[0]
            name = name[9:] #除去学号，保留姓名
            self.StudentDict[name] = self.StudentDict[name] + 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = mainWindow()
    win.show()
    sys.exit(app.exec())
