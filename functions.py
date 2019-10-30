import requests

def getRemainingTimes(route_id, trip_headsign, stop_name):
    """Get waiting times before next arrival
    PARAMETERS
    ----------
    route_id : string, number of the route
    trip_headsign : string, name of the destination
    stop_name : string, name of the stop

    RETURN
    ------
    json string
    """
    payload = {'format': 'json', 'route_id': route_id, 'trip_headsign': trip_headsign, 'stop_name': stop_name}
    req = requests.get('https://applications002.brest-metropole.fr/WIPOD01/Transport/REST/getRemainingTimes',params=payload)
    return req.text

def getDestination(route_id):
    """Get destination (trip_headsign) for a route
    PARAMETER
    ---------
    route_id : string, number of the route

    RETURN
    ------
    json string 
    """
    req = requests.get("https://applications002.brest-metropole.fr/WIPOD01/Transport/REST/getDestinations?format=json&route_id={}".format(route_id))
    return req.text

def getStops_route(route_id, trip_headsign):
    """Get stop of a line
    PARAMETERS
    ----------
    route_id : string, number of the route
    trip_headsign : string, name of destination

    RETURN
    ------
    json string
    """
    payload = {'format': 'json', 'route_id': route_id, 'trip_headsign': trip_headsign}
    req = requests.get("https://applications002.brest-metropole.fr/WIPOD01/Transport/REST/getStops_route?format=json&route_id={}&trip_headsign={}".format(route_id, trip_headsign))
    return req.text

if __name__ == "__main__":
#    print("TEST getDestination : ", getDestination("A")) 
    print("TEST getStops_route : ", getStops_route("A","Porte de Gouesnou"))
    #print("TEST getRemainingTimes : ", getRemainingTimes("A", "Porte de Gouesnou", "Octroi"))
