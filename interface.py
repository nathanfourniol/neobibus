import sys
import os
import inspect
import json
from PyQt5 import QtGui, QtCore, QtWidgets, uic
from PyQt5.QtGui import QPainter, QPixmap, QImage
import requests

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
        #comboBox
        self.comboBox_route_list.addItems(LINES)
        self.comboBox_stop_list.addItems(STOP_A)
        self.comboBox_trip_headsign_list.addItems(TRIP_HEADSIGN)
        # Button
        self.pushButton_send_request.clicked.connect(self._send_request)
        # Pictures      
        self.drawBackground()

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
    
    def drawBackground(self):
        
        oImage = QImage(FOLDERPATH + "pictures/tram1.jpg")
        oLayout = QtWidgets.QVBoxLayout()
        oLayout.addWidget(oImage)

        self.setLayout(oLayout)
        #tram = QPixmap(FOLDERPATH + "pictures/tram1.jpg")
        #self.label_background.setPixmap(tram)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_()
