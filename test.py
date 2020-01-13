"""
import sys
import os
import inspect
import json
from PyQt5 import QtGui, QtCore, QtWidgets, uic
from PyQt5.QtGui import QPainter, QPixmap, QImage, QPalette, QBrush, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QUrl
#from PyQt5.QtWebEngineWidgets import setHtml
#from PyQt5.QtWebEngineWidgets import QWebView
from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView
#from PyQt5.QWebEnginePage as QWebPage
from PyQt5.QtWebEngineWidgets import QWebEngineSettings as QWebSettings
import requests
import folium
import webbrowser
import os

FOLDERPATH = os.path.split(inspect.getfile(inspect.currentframe()))[0]
with open(FOLDERPATH + "guidata/routes.json") as f:
    LINES = json.load(f)
with open(FOLDERPATH +"guidata/stop_A.json") as f:
    STOP_A = json.load(f)
FOLDERPATH = os.path.split(inspect.getfile(inspect.currentframe()))[0]
with open(FOLDERPATH + "guidata/routes.json") as f:
    LINES = json.load(f)
with open(FOLDERPATH +"guidata/stop_A.json") as f:
    STOP_A = json.load(f)


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        #self.drawBackground()
        uic.loadUi(FOLDERPATH+"ui/MainWindow.ui", self)
        self.widget_3 = QWebView()
        self.affichage()

    def affichage (self):
        self.widget_3.load(QWebView.setHtml("//home/clement/Documents/neobibus/maCarte.html"))
        #self.widget_3.load(QUrl("https://www.google.fr/"))
        self.widget_3.show()
        #web_view.load(QUrl('ht"))





if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_()
"""

#!/usr/bin/python
# -*- coding: utf-8 -*-
# Python 3.5, PyQt5 v5.9.2

import sys
import os
from PyQt5 import QtWidgets, QtCore, QtWebEngineWidgets

#############################################################################
class Aide(QtWidgets.QWidget):

    #========================================================================
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Aide")
        self.resize(800, 600)

        self.view = QtWebEngineWidgets.QWebEngineView()

        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(self.view, 0, 0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.page = QtWebEngineWidgets.QWebEnginePage()

    #========================================================================
    def affiche(self, fichierweb):
        """affiche le fichier web donné
        """
        self.page.setUrl(QtCore.QUrl(fichierweb))
        self.view.setPage(self.page)
        self.view.show()

#############################################################################
if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    aide = Aide()
    aide.show()

    #fichierweb = "file:///" + os.path.abspath("maCarte.html").replace("\\", "/") + "#partiecommune"
    fichierweb =  "file:///" +  os.getcwd()+"/maCarte.html"

    aide.affiche(fichierweb)

    sys.exit(app.exec_())
