import sys
import os
import inspect
import time
import json
from PyQt5 import QtGui, QtCore, QtWidgets, uic
from PyQt5.QtGui import QPainter, QPixmap, QImage, QPalette, QBrush, QColor
from PyQt5.QtCore import Qt
#from PyQt5.QtWebKitWidgets import QWebView
from PyQt5 import QtWidgets, QtWebEngineWidgets

import requests
import folium
import webbrowser


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
        #comboBox Next stop
        self.comboBox_route_list.addItems(['Choose a route ...']+LINES)
        self.comboBox_stop_list.addItems(['Choose a stop ...']+STOP_A)
        self.comboBox_trip_headsign_list.addItems(['Choose a headsign ...']+\
                TRIP_HEADSIGN)

        #ComboBox Store a Stop
        self.comboBox_route_list_2.addItems(['Choose a route ...']+LINES)
        self.comboBox_stop_list_2.addItems(['Choose a stop ...']+STOP_A)
        self.comboBox_trip_headsign_list_2.addItems(['Choose a headsign ...']+\
                TRIP_HEADSIGN)

        # Button
        self.pushButton_send_request.clicked.connect(self._send_request)
        self.pushButton_send_request_user_best_stop.clicked.connect(self._send_request_user_best_stop)
        self.pushButton_store_stop.clicked.connect(self._store_stop)
        self.pushButton_test_api.clicked.connect(self.test_API)

        #load data
        self.user_stop = self._load_stop("user_stop.conf")

        #Map
        self.view = QtWebEngineWidgets.QWebEngineView()
        self.map_layout.addWidget(self.view, 0)
        self.map_layout.setContentsMargins(0, 0, 0, 0)
        #self.map_layout.setLayout(layout)

        self.page = QtWebEngineWidgets.QWebEnginePage()


    def _send_request(self):
        """Call when Let's Go  button is clicked
        """
        route_chosen = self.comboBox_route_list.currentText()
        route_id = route_chosen.split(',')[0] #to get the id of the route
        trip_headsign_chosen = self.comboBox_trip_headsign_list.currentText()
        stop_chosen = self.comboBox_stop_list.currentText()
        self.request(route_id, trip_headsign_chosen, stop_chosen)

    def _send_request_user_best_stop(self):
        """Executed when user prest user best stop
        Launch the request function
        """
        self.request(self.user_stop["route_id"], self.user_stop["trip_headsign"], self.user_stop["stop_chosen"])


    def drawBackground(self):
        palette = QPalette()

        palette.setBrush(10, QColor(30,123,30)) #background color in RGB style
        self.setPalette(palette)

    def _load_stop(self, confFile):
        """Call by init and after the user save a new preferred stop"""
        with open(FOLDERPATH + "guidata/user_stop.conf", "r") as f:
            user_stop = json.load(f)
            print("USER STOP CORRECTLY LOAD : ", user_stop)

        buff = user_stop["route_id"] + " -> " + user_stop["trip_headsign"] + " : " + user_stop["stop_chosen"]
        #For tab "Store your best stop"
        self.label_current_stop_stored.setText(buff)
        #For tab "Next Stop"
        self.label_current_stop_stored_2.setText(buff)
        return user_stop

    def _store_stop(self):
        """Call when Store Stop button is clicked
        """
        struct_stop={"route_id":None, "trip_headsign":None, "stop_chosen":None}
        #to get the id of the route
        struct_stop["route_id"]= self.comboBox_route_list_2.currentText().\
                split(',')[0]
        struct_stop["trip_headsign"]= self.comboBox_trip_headsign_list_2.\
                currentText()
        struct_stop["stop_chosen"]= self.comboBox_stop_list_2.currentText()
        with open(FOLDERPATH + "user_stop.conf", "w") as f:
            buff=json.dumps(struct_stop, ensure_ascii=False)
            f.write(json.dumps(struct_stop))
            print("STOP STORED : ",buff )
        self.user_stop = self._load_stop(FOLDERPATH + "user_stop.conf")

    def display(self,text):
        """
        Display text
        """
        self.textBrowser_display.setText(text)

    def request(self, route_id,trip_headsign,stop_name):
        payload = {'format': 'json', 'route_id': route_id, 'trip_headsign': trip_headsign, 'stop_name': stop_name}
        req = requests.get('https://applications002.brest-metropole.fr/WIPOD01/Transport/REST/getRemainingTimes',params=payload)
        print("URL_REQUEST :", req.url)
        print("ANSWER : ", req.text)
        if len(req.text) < 100 :
            self.display(" Something wrong occurs :(\n\n Impossible combination OR\n Next arrival > 20 min OR\n API not responding... \n\n Please Retry Later")
        else :
            next_arrival = req.text[39:47]
            self.display("ROUTE_ID             : "+route_id + 
                       "\nTRIP_HEADSIGN : "+trip_headsign+
                       "\nSTOP                      : "+stop_name+
                       "\nNEXT_ARRIVAL  : "+next_arrival)

            self.web(stop_name)

    def affiche(self):
        """affiche le fichier web donné
        """
        self.fichierweb = "file:///"+  os.getcwd()+"/guidata/maCarte.html"
        self.page.setUrl(QtCore.QUrl(self.fichierweb))
        self.view.setPage(self.page)
        self.view.show()

    def web(self, stop_name):
        payload = {'format':'json', "stop_name":stop_name}
        req = requests.get('https://applications002.brest-metropole.fr/WIPOD01/Transport/REST/getSTop',params=payload)
        dic = json.loads(req.text)
        lat = dic[1]['Stop_lat']
        longi = dic[1]['Stop_lon']
        print("STOP : {}, LAT : {}, LONGI : {}".format(stop_name, lat, longi))

        Brest = [48.4, -4.48]
        c= folium.Map(location=Brest,
            zoom_start=12)

        folium.Marker(
            location=[lat, longi],
            popup='Mt. Hood Meadows',
            icon=folium.Icon(icon='cloud'),
        ).add_to(c)
        c.save('guidata/maCarte.html')
        #webbrowser.open(os.getcwd()+"/maCarte.html")
        self.affiche()


        #info_sups : https://python-visualization.github.io/folium/quickstart.html
        #http://esaid.free.fr/QtPython/calculatrice/Python_et_Qt.pdf
        #http://kib2.free.fr/pyqt4/pyqt4.html

    def test_API(self):
        """To test the API"""
        print("Test API ...")
        t0 = time.time()
        c = 0
        for trip_headsign in TRIP_HEADSIGN:
            for stop in STOP_A:
                payload = {'format': 'json', 'route_id': "A", 'trip_headsign': trip_headsign, 'stop_name': stop}
                req = requests.get('https://applications002.brest-metropole.fr/WIPOD01/Transport/REST/getRemainingTimes',params=payload)
                if len(req.text) < 100 : #API answer 189 characters if it works well
                    print("API not responding for parameters : {}, {} ".format(trip_headsign, stop))
                    c += 1
                else :
                    print("Params : {}, {} : {}".format(trip_headsign, stop, req.text))
        duration = time.time() - t0
        print("END OF TEST : duration : {} s, {} requests failed".format(duration, c))




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_()
