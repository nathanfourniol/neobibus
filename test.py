

import webbrowser
import os
import folium
import requests
import json
"""
c= folium.Map(location=[48.4, -4.48],
)

folium.Marker(
    location=[45.3288, -121.6625],
    popup='Mt. Hood Meadows',
    icon=folium.Icon(icon='cloud')
).add_to(c)
c.save('maCarte.html')
webbrowser.open(os.getcwd()+"/maCarte.html")
"""
payload = {'format':'json','stop_name':'malakoff'}
req = requests.get('https://applications002.brest-metropole.fr/WIPOD01/Transport/REST/getStop',params = payload)
b=req.text  #jsontext

a = json.loads(b) #to a dictionnarie

print(a[1])
print(type(a[1]))

"""

import sys
from PyQt5 import QtGui, QtCore, QtWidgets, uic
from PyQt5.QtCore import QUrl
from PyQt5 import QtWebKit


class Browser(QWebView):

    def __init__(self):
        QWebView.__init__(self)
        self.loadFinished.connect(self._result_available)

    def _result_available(self, ok):
        frame = self.page().mainFrame()
        #print unicode("helloe")

        #http://i-miss-erin.blogspot.com/2009/03/write-web-browser-by-python.html


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = Browser()
    view.load(QUrl('http://www.google.com'))
    app.exec_()

    """
