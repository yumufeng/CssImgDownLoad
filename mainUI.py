# coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from saveCssImg import *

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)


class UI_getImg(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(UI_getImg, self).__init__(parent)
        self.setupUi(self)
        self.lineEdit.setText('http://simg.sinajs.cn/blog7style/css/conf/blog/article.css')
        self.textBrowser.setOpenExternalLinks(True)
        self.textBrowser.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.textBrowser.setStyleSheet("QTextBrowser {background: #eee; }")
        self.pushButton.clicked.connect(self.goWork)

    def goWork(self):
        self.thread = WorkerThread()
        self.thread.sinOut.connect(self.outText)
        self.thread.finished.connect(self.workFinished)

        cssUrl = str(self.lineEdit.text())
        savePath = 'downImgs'
        self.textBrowser.setText(u'CSS文件地址: <a href="%s">%s</a><br>__________<br>' % (cssUrl, cssUrl))
        self.pushButton.setDisabled(True)

        self.thread.setEvr(cssUrl, savePath)

    def outText(self, info):
        self.textBrowser.append(info)

    def workFinished(self):
        self.outText(u'__________<br>图片已全部下载到当前目录 <b>downImgs</b> 中！')
        self.pushButton.setDisabled(False)

    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(800, 407)
        #####设置log
        icon = QIcon()
        icon.addFile("./image/logo.ico")
        Dialog.setWindowIcon(icon)

        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(700, 20, 75, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(10, 60, 780, 341))
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(10, 20, 670, 20))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "下载Css文件图片", None))
        self.pushButton.setText(_translate("Dialog", "下载", None))
        self.lineEdit.setPlaceholderText(_translate("Dialog", "请输入css文件的URL地址", None))


class WorkerThread(QtCore.QThread):
    sinOut = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(WorkerThread, self).__init__(parent)

    def setEvr(self, cssUrl, savePath):
        self.cssUrl = cssUrl
        self.savePath = savePath
        self.start()

    def outInfo(self, info):
        self.sinOut.emit(info)

    def run(self):
        self.saveimg = saveCssBackImg(self.cssUrl, self.savePath, self.outInfo)
        self.saveimg.saveImg()


if __name__ == "__main__":
    app = QApplication([])
    ui = UI_getImg()
    ui.setWindowFlags(QtCore.Qt.MSWindowsFixedSizeDialogHint)
    ui.show()
    app.exec_()
