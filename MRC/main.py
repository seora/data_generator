import csv
import os
import sys
import xlrd
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, \
    QListWidgetItem, QListWidget, QTextBrowser, \
    QDialog, QTableWidget, QTableWidgetItem, QAction, QFileDialog, QMessageBox

from createdata import ChatWindow
from ui.mainwindow_ui import Ui_MainWindow

class MainWindow(Ui_MainWindow):

    global filename
    filename = ""
    global datalist
    datalist = []
    global currentPage
    currentPage = 1
    global totalPage;      totalPage = 0
    global PageIdxlist;    PageIdxlist = []
    global idx; idx=0
    global lenDatalist;     lenDatalist = 0

    def __init__(self, mw):
        Ui_MainWindow.__init__(self)
        self.setupUi(mw)
        self.create_window.clicked.connect(self.CreateData)

        self.loadAction.triggered.connect(self.loadData)
        self.saveAction.triggered.connect(self.saveData)
        self.refreshAction.triggered.connect(self.refreshData)

        self.searchBtn.clicked.connect(self.searchData)

        self.prevBtn.clicked.connect(self.onPrevPage)
        self.nextBtn.clicked.connect(self.onNextPage)


    def loadData(self):
        global filename
        global datalist
        global my_file

        popup = QMessageBox()
        popup.setStandardButtons(QMessageBox.Ok)

        fname = QFileDialog.getOpenFileName(None, 'Dialog Title', './', filter='*.csv *.xlsx')
        if fname[0]:
            filename = fname[0]
            try:
                with open(filename, encoding = 'utf-8') as csv_file:
                    self.data_table.setRowCount(0)
                    self.data_table.setColumnCount(12)
                    my_file = csv.reader(csv_file)
                    self.initializeData()

            except FileNotFoundError:
                popup.setText("파일이 존재하지 않습니다")
                popup.exec_()
                pass

        else:
            popup.setText("파일을 선택해주세요")
            popup.exec_()


    def saveData(self):
        popup = QMessageBox()
        popup.setStandardButtons(QMessageBox.Ok)

        filename, selectedFilter = QFileDialog.getSaveFileName(None, 'Save Data', 'test.csv', "Excel (*.csv *.xlsx )")
        if filename:
            try:
                with open(filename, "w", encoding='utf-8') as csv_file:
                    writer = csv.writer(csv_file)


                    for row in datalist:
                        writer.writerrow(row)
                        """
                        row_data = []
                        for column in range(self.data_table.columnCount()):
                            item = self.data_table.item(row, column)
                            if item is not None:
                                row_data.append(item.text())
                            else:
                                row_data.append('')
                        writer.writerow(row_data)
                        print(row_data)
                        """

                popup.setText("데이터가 저장되었습니다")
                popup.exec_()

            except:
                popup.setText("데이터가 저장되지 않았습니다")
                popup.exec_()

        else:
            popup.setText("데이터가 저장되지 않았습니다")
            popup.exec_()

    def refreshData(self):
        global filename
        try:
            with open(filename, encoding='utf-8') as csv_file:
                self.data_table.setRowCount(0)
                self.data_table.setColumnCount(12)
                my_file = csv.reader(csv_file)
                for row_data in my_file:
                    row = self.data_table.rowCount()
                    self.data_table.insertRow(row)
                    for column, stuff in enumerate(row_data):
                        item = QTableWidgetItem(stuff)
                        self.data_table.setItem(row, column, item)

                col_headers = ['SPEAKER', 'SENTENCE', 'DATAID', 'DOMAINID', 'DOMAIN', 'CATEGORY', 'SPEAKERID',
                               'SENTENCEID',
                               'MAIN', 'SUB', 'QA', 'QACNCT']
                self.data_table.setHorizontalHeaderLabels(col_headers)

        except:
            popup = QMessageBox()
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setText("업데이트할 파일이 없습니다")
            popup.exec_()
            pass

    #검색 기능
    def searchData(self):
        keyword = self.searchtext.text()
        print(keyword)
        count = 0

        allitems = self.data_table.findItems("", QtCore.Qt.MatchContains)
        selected_items = self.data_table.findItems(keyword, QtCore.Qt.MatchContains)
        for item in allitems:
            if item in selected_items:
                # item.setData(QtCore.Qt.DecorationRole, keyword if item in selected_items else None)
                item.setBackground(QtGui.QColor(245, 218, 227))
                count += 1

        if count == 0:
            popup = QMessageBox()
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setText("찾으려는 텍스트가 존재하지 않습니다")
            popup.exec_()

    def initializeData(self):
        global datalist
        global my_file
        global totalPage
        global currentPage
        global lenDatalist

        for row_data in my_file:
            row_list = []
            row = self.data_table.rowCount()
            #self.data_table.insertRow(row)
            for column, stuff in enumerate(row_data):
                item = QTableWidgetItem(stuff)
                #self.data_table.setItem(row, column, item)
                row_list.append(stuff)

            datalist.append(row_list)

        lenDatalist = len(datalist)

        col_headers = ['SPEAKER', 'SENTENCE', 'DATAID', 'DOMAINID', 'DOMAIN', 'CATEGORY', 'SPEAKERID', 'SENTENCEID',
                       'MAIN', 'SUB', 'QA', 'QACNCT']
        self.data_table.setHorizontalHeaderLabels(col_headers)

        for a in datalist:
            if a[7] == "1":
                totalPage += 1
                PageIdxlist.append(datalist.index(a))

        PageIdxlist.append(lenDatalist)

        self.max_page.setText(str(totalPage))

        print("대화 첫번째항 리스트", PageIdxlist)
        self.updateStatus()


    def onPrevPage(self):
        global idx
        idx -= 1

        popup = QMessageBox()
        popup.setStandardButtons(QMessageBox.Ok)

        if idx <= 0 :
            popup.setText("이전 페이지가 없습니다")
            popup.exec_()
            self.prevBtn.setEnabled(False)

        else:
            self.updateStatus()
            print(idx)


    def onNextPage(self):
        global idx
        global lenDatalist

        idx += 1
        print("next누르고 난 후, ", idx)

        popup = QMessageBox()
        popup.setStandardButtons(QMessageBox.Ok)

        if PageIdxlist[idx] == lenDatalist:
            popup.setText("다음 페이지가 없습니다")
            popup.exec_()
        else:
            self.updateStatus()
            print(idx)

    def updateStatus(self):
        global datalist
        global PageIdxlist
        global idx

        self.data_table.clearContents()
        self.currentPage.setText(str(idx+1))

        for row_data in datalist[PageIdxlist[idx]:PageIdxlist[idx+1]]:
            row = self.data_table.rowCount()
            print(row)
            self.data_table.insertRow(row)
            for column, stuff in enumerate(row_data):
                item = QTableWidgetItem(stuff)
                self.data_table.setItem(row - PageIdxlist[idx] + 1, column, item)


    def CreateData(self):
        chw = QDialog()
        ui = ChatWindow(chw)
        chw.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = QMainWindow()
    ui = MainWindow(mw)
    mw.show()
    app.exec_()