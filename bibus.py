import requests
import json
import tkinter as tk
import tkinter.ttk as ttk

# ==> Test...
"""getRemainingTimes
payload = {'format': 'json', 'route_id': "A", 'trip_headsign': 'Porte de Plouzane', 'stop_name':'Octroi'}
#r = requests.get('https://applications002.brest-metropole.fr/WIPOD01/Transport/REST/getRemainingTimes?format=json&route_id=3&trip_headsign=oceanopolis&stop_name=Malakoff')
r2 = requests.get('https://applications002.brest-metropole.fr/WIPOD01/Transport/REST/getRemainingTimes', params=payload)
#r1=r2[1]
print(r2.text)
print(type(r2.text))
next_bus_arrival = r2.text[39:47]
print(next_bus_arrival)

"""


#Callback : Update data from Combobox
def callback_combobox(event):
    current=combo.get()
    station.config(text=current)
    payload = {'format': 'json', 'route_id': "A", 'trip_headsign': 'Porte de Plouzane', 'stop_name': current}
    r2 = requests.get('https://applications002.brest-metropole.fr/WIPOD01/Transport/REST/getRemainingTimes',params=payload)
    next_bus_arrival = r2.text[39:47]
    label_result.config(text=next_bus_arrival)
    print(current)
    print(next_bus_arrival)



root = tk.Tk()
root.title("Neobibus")
root.resizable(True,False)
root.geometry("300x400-10+100")
main_title = tk.Label(root, text = 'Timetable_Brest_Tramway', width = 50, height = 3, background = "#FFAAAA")
selection=tk.Frame(root, bd=1, relief='solid')
result=tk.Frame(root,bd=1, relief='solid')

#First Frame : Selection
list=['Octroi','Liberte','Saint Martin','Siam']
result_combo=tk.StringVar()
combo=ttk.Combobox(selection, textvariable=result_combo, state='readonly',values=list)
combo.bind('<<ComboboxSelected>>', callback_combobox)
combo.grid(row=0,column=0)
station=tk.Label(selection, text="Choose a station")
station.grid(row=1, column=0)

#Second Frame : Result
label_title = tk.Label(result, text='Next Arrival time', width =50)
label_result = tk.Label(result, text = "Choose !")
label_title.grid(column=0, row=0)
label_result.grid(column=0, row=1)

#Frame Organisation
main_title.grid(row=0,column=0)
selection.grid(row=2,column=0)
result.grid(row=18, column=0)


root.mainloop() #