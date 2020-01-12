import sys
import os
import inspect
import json
from PyQt5 import QtGui, QtCore, QtWidgets, uic
from PyQt5.QtGui import QPainter, QPixmap, QImage, QPalette, QBrush, QColor
from PyQt5.QtCore import Qt
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
    
        #load data
        self.user_stop = self._load_stop("user_stop.conf")
    def _send_request(self):
        """Call when Let's Go  button is clicked
        """
        route_chosen = self.comboBox_route_list.currentText()
        route_id = route_chosen.split(',')[0] #to get the id of the route
        trip_headsign_chosen = self.comboBox_trip_headsign_list.currentText()
        stop_chosen = self.comboBox_stop_list.currentText()
        self.request(route_id, trip_headsign_chosen, stop_chosen)

    def _send_request_user_best_stop(self):
        print("REQUEST : ", self.user_stop)
        pass

    def _load_stop(self, confFile):
        with open(FOLDERPATH + "user_stop.conf", "r") as f:
            user_stop = json.load(f)
            print("LOAD OK : ", user_stop)
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

        oImage = QImage(FOLDERPATH + "pictures/openBibuscrop.jpg")
        palette = QPalette()        
        palette.setBrush(10, QBrush(oImage))  # 10 = Windowrole
        self.img2.setAutoFillBackground(True)
        self.img2.setPalette(palette)
        self.img2.show()

        palette.setBrush(10, QColor(224,224,209)) #background color in RGB style
        self.setPalette(palette)
        #tram = QPixmap(FOLDERPATH + "pictures/tram1.jpg")

        #self.label_background.setPixmap(tram)
    def web(self, stop_name):
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




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_()
