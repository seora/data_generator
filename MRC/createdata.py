import sys
import pandas as pd
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, \
    QListWidgetItem, QListWidget, QTextBrowser, QMessageBox,\
    QDialog

from ui.chatwindow_ui import Ui_ChatWindow

class ChatWindow(Ui_ChatWindow):

    global speaker
    global QA
    global category
    category = ""
    global sentence
    sentence = ""
    global intent
    intent = ""

    global l
    l = []
    global num
    num = 0


    def __init__(self, chw):
        Ui_ChatWindow.__init__(self)
        self.Dialog = chw
        self.setupUi(self.Dialog)

        self.speaker1.clicked.connect(self.speakerFunc)
        self.speaker2.clicked.connect(self.speakerFunc)

        self.qa_q.clicked.connect(self.checkQAFunc)
        self.qa_a.clicked.connect(self.checkQAFunc)

        self.category.currentIndexChanged.connect(self.getCategoryFunc)

        self.sentence.textChanged.connect(self.getSentenceFunc)

        self.intent.currentIndexChanged.connect(self.getIntentFunc)

        self.send.clicked.connect(self.sendData)
        self.pushButton.clicked.connect(self.ConnectExcel)


    def speakerFunc(self):
        global speaker
        if self.speaker1.isChecked():
            speaker = "고객"
        elif self.speaker2.isChecked():
            speaker = "점원"

        return speaker

    def checkQAFunc(self):
        global QA
        if self.qa_q.isChecked():
            QA="Q"
        elif self.qa_a.isChecked():
            QA="A"
        return QA

    def getCategoryFunc(self):
        global category
        category = self.category.currentText()
        return category

    def getSentenceFunc(self):
        global sentence
        sentence = self.sentence.toPlainText()
        return sentence

    def getIntentFunc(self):
        global intent
        intent = '*'
        intent = self.intent.currentText()
        return intent

    def sendData(self):
        global l
        global num
        num += 1

        global chat_1
        global chat_2

        chatlist = self.chatlist

        font = QFont()
        font.setPointSize(15)

        popup = QMessageBox()
        popup.setStandardButtons(QMessageBox.Ok)

        if self.speaker1.isChecked():
            #유효성 검사
            if not self.qagroup.checkedButton():
                popup.setText("QA를 선택하세요")
                popup.exec_()

            elif sentence == "":
                popup.setText("문장을 입력하세요")
                popup.exec_()

            elif category == "":
                popup.setText("카테고리를 선택하세요 ")
                popup.exec_()

            elif intent == "":
                popup.setText("문장 의도를 선택해주세요 ")
                popup.exec_()

            else:
                chat_item = QListWidgetItem("고객 : " + sentence, chatlist)
                itemWidget = QTextBrowser()
                itemWidget.setText("고객 : " + sentence)

                chat_item.setSizeHint(QSize(200, 60))
                itemWidget.setStyleSheet("background-color: #FFE304;""border-style: solid;""border-width: 10px;"
                                         "border-color: #FFFFFF;"
                                         "border-radius: 3px")
                chatlist.setItemWidget(chat_item, itemWidget)

                l.append([speaker, sentence, category, 'A', '음식점', '홀서빙음식점', '1', num, intent, ' ', QA])

        elif self.speaker2.isChecked():
            # 유효성 검사
            if not self.qagroup.checkedButton():
                popup.setText("QA를 선택하세요")
                popup.exec_()

            elif sentence == "":
                popup.setText("문장을 입력하세요")
                popup.exec_()

            elif category == "":
                popup.setText("카테고리를 선택하세요 ")
                popup.exec_()

            elif intent == "":
                popup.setText("문장 의도를 선택해주세요 ")
                popup.exec_()

            else:
                chat_item = QListWidgetItem("점원 : " + sentence, chatlist)

                itemWidget = QTextBrowser()
                itemWidget.setText("점원 : " + sentence)

                chat_item.setSizeHint(QSize(200, 60))
                itemWidget.setStyleSheet("background-color: #FFFFFF;""border-style: solid;""border-width: 10px;"
                                         "border-color: #FFFFFF;"
                                         "border-radius: 3px")
                chatlist.setItemWidget(chat_item, itemWidget)

                l.append([speaker, sentence, category, 'A', '음식점', '홀서빙음식점', '0', num, intent, ' ', QA])

        else:
            popup.setText("발화자를 선택해주세요 ")
            popup.exec_()
            self.show()

        print(l)
        self.sentence.clear()

        return l

    def ConnectExcel(self):

        df = pd.DataFrame(l)
        # df = pd.DataFrame(l, columns=['SPEAKER', 'SENTENCE', 'DATAID', 'DOMAINID', 'DOMAIN', 'CATEGORY', 'SPEAKERID', 'SENTENCEID', 'MAIN', 'SUB', 'QA'])
        df.to_csv('test.csv', mode='a', index=False, header=False, encoding='euc-kr', line_terminator = '\n')
        global num
        num = 0
        self.chatlist.clear()
        del l[:]