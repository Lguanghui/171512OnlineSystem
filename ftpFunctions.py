# -*- coding: utf-8 -*-
from ftplib import FTP

#连接ftp
def ftpconnect(host,port, username, password):
    ftp = FTP()
    # 打开调试级别2，显示详细信息
    # ftp.set_debuglevel(2)
    ftp.connect(host, port)
    ftp.login(username, password)
    return ftp

#从ftp下载文件
def downloadfile(ftp, remotepath, localpath):
    # 设置的缓冲区大小
    bufsize = 1024
    fp = open(localpath, 'wb')
    ftp.retrbinary('RETR ' + remotepath, fp.write, bufsize)
    ftp.set_debuglevel(0)# 参数为0，关闭调试模式
    fp.close()

#从本地上传文件到ftp
def uploadfile(ftp, remotepath, localpath):
    bufsize = 1024
    fp = open(localpath, 'rb')
    ftp.storbinary('STOR ' + remotepath, fp, bufsize)
    ftp.set_debuglevel(0)
    fp.close()

#将ftp读取到的txt数据存下来，此过程并没有将txt文件下载
def saveRetrieveData(data):
    global HINT
    HINT = data
    print(HINT)

if __name__ == "__main__":
    global HINT
    #host,port, username, password
    ftp = ftpconnect("...",21,"...", "...") #IP地址、端口、用户名、密码
    #下载文件，第一个是ftp服务器路径下的文件，第二个是要下载到本地的路径文件
    #downloadfile(ftp, "/12.mp3", r"C:\Users\Administrator\Desktop\ftp\download\test.mp3")
    # 上传文件，第一个是要上传到ftp服务器路径下的文件，第二个是本地要上传的的路径文件
    # uploadfile(ftp,"/home/yunyi/Desktop/FTP收件箱/1.docx",'/Users/yunyi/Desktop/1.docx')
    # #调用本地播放器播放下载的视频
    # os.system('start D:\soft\kugou\KGMusic\KuGou.exe C:\Users\Administrator\Desktop\ftp\test.mp3')

    # print(ftp.getwelcome())# 打印出欢迎信息
    # 获取当前路径
    pwd_path = ftp.pwd()
    ftp.cwd('/home/yunyi/Desktop/FTP收件箱/')
    print("FTP当前路径:", pwd_path)
    files = ftp.nlst()
    print(files)
    # 显示目录下所有目录信息
    # ftp.dir()
    # 设置FTP当前操作的路径
    # ftp.cwd('/root/testFTP/')
    # 返回一个文件名列表
    # filename_list = ftp.nlst()
    # print(filename_list)

    # #ftp.mkd('目录名')# 新建远程目录
    # #ftp.rmd('目录名')  # 删除远程目录
    # ftp.delete('文件名')  # 删除远程文件
    # ftp.rename('fromname', 'toname')  # 将fromname修改名称为toname

    # 逐行读取ftp文本文件
    file = '/home/yunyi/Desktop/FTP收件箱/systemHINT.txt'
    ftp.retrlines('RETR %s' % file, saveRetrieveData)
    print(HINT)


    #与 retrlines()类似，只是这个指令处理二进制文件。回调函数 cb 用于处理每一块（块大小默认为 8KB）下载的数据
    # ftp.retrbinary('RETR %s' % file)
    ftp.close()  # 关闭ftp
