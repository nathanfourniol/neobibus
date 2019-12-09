import sys
import os
import inspect
import json
from PyQt5 import QtGui, QtCore, QtWidgets, uic
from PyQt5.QtGui import QPainter, QPixmap, QImage, QPalette, QBrush, QColor
from PyQt5.QtCore import Qt
from PyQt45.QtWebKit import QWebView

import requests
import folium
import webbrowser
import os


# To have the folder where the code is stored
FOLDERPATH = os.path.split(inspect.getfile(inspect.currentframe()))[0]
with open(FOLDERPATH + "guidata/routes.json") as f:
    LINES = json.load(f)
with open(FOLDERPATH +"guidata/stop_A.json") as f:
    STOP_A = json.load(f)


TRIP_HEADSIGN = ["Porte de Gouesnou", "Porte de Guipavas", "Porte de Plouzané"]

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi(FOLDERPATH+"ui/MainWindow.ui", self)
        # Pictures
        self.drawBackground()
        #comboBox
        self.comboBox_route_list.addItems(LINES)
        self.comboBox_stop_list.addItems(STOP_A)
        self.comboBox_trip_headsign_list.addItems(TRIP_HEADSIGN)
        # Button
        self.pushButton_send_request.clicked.connect(self._send_request)

    def _send_request(self):
        """Call when Send Request button is clicked
        """
        route_chosen = self.comboBox_route_list.currentText()
        route_id = route_chosen.split(',')[0] #to get the id of the route
        trip_headsign_chosen = self.comboBox_trip_headsign_list.currentText()
        stop_chosen = self.comboBox_stop_list.currentText()
        self.request(route_id, trip_headsign_chosen, stop_chosen)

    def display(self,text):
        """
        Display text
        """
        self.textBrowser_display.setText(text)

    def request(self, route_id,trip_headsign,stop_name):
        payload = {'format': 'json', 'route_id': route_id, 'trip_headsign': trip_headsign, 'stop_name': stop_name}
        req = requests.get('https://applications002.brest-metropole.fr/WIPOD01/Transport/REST/getRemainingTimes',params=payload)
        print("REQUEST : ", req.text)
        next_arrival = req.text[39:47]

        self.display(route_id + "\n"+trip_headsign+"\n"+stop_name+"\n"+next_arrival+"\n")
        self.web(stop_name)

    def drawBackground(self):
        oImage = QImage(FOLDERPATH + "pictures/tramZOOM.jpg")
        palette = QPalette()
        palette.setBrush(10, QBrush(oImage))  # 10 = Windowrole
        self.img.setAutoFillBackground(True)
        self.img.setPalette(palette)
        self.img.show()
        palette.setBrush(10, QColor(153, 153, 102))
        self.setPalette(palette)

        #tram = QPixmap(FOLDERPATH + "pictures/tram1.jpg")
        #self.label_background.setPixmap(tram)
    def web (self, stop_name):
        payload = {'format':'json', "stop_name":stop_name}
        req = requests.get('https://applications002.brest-metropole.fr/WIPOD01/Transport/REST/getSTop',params=payload)
        dic = json.loads(req.text)
        lat = dic[1]['Stop_lat']
        long = dic[1]['Stop_lon']

        lat = float(req.text[35:45])
        long = float(req.text[65:76])
        print("latitude_arret",lat)
        print("longitude_arret",long)

        Brest = [48.4, -4.48]
        c= folium.Map(location=Brest,
            zoom_start=13)

        folium.Marker(
            location=[lat, long],
            popup='Mt. Hood Meadows',
            icon=folium.Icon(icon='cloud'),
        ).add_to(c)


        c.save('maCarte.html')
        webbrowser.open(os.getcwd()+"/maCarte.html")
        #info_sups : https://python-visualization.github.io/folium/quickstart.html
        #http://esaid.free.fr/QtPython/calculatrice/Python_et_Qt.pdf
        #http://kib2.free.fr/pyqt4/pyqt4.html




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_()
