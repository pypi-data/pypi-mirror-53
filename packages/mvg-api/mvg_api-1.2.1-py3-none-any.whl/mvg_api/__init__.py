# coding=utf-8

import requests
import json
import datetime
from time import mktime

api_key = "5af1beca494712ed38d313714d4caff6"
query_url_name = "https://www.mvg.de/api/fahrinfo/location/queryWeb?q={name}" #for station names
query_url_id = "https://www.mvg.de/api/fahrinfo/location/query?q={id}" #for station ids
departure_url = "https://www.mvg.de/api/fahrinfo/departure/{id}?footway=0"
nearby_url = "https://www.mvg.de/api/fahrinfo/location/nearby?latitude={lat}&longitude={lon}"
routing_url = "https://www.mvg.de/api/fahrinfo/routing/?"
interruptions_url = "https://www.mvg.de/.rest/betriebsaenderungen/api/interruptions"


def _perform_api_request(url):
    resp = requests.get(url, headers={'X-MVG-Authorization-Key': api_key, 'User-Agent': 'python-mvg-api/1 (+https://github.com/leftshift/python_mvg_api)', 'Accept': 'application/json'})
    return resp.json()


def _convert_time(time):
    """Converts unix time in milliseconds to datetime or the other way around

    Parameters
    ----------
    time : int or datetime
        Unix timestamp (in milliseconds, like timestamp * 1000) or datetime.

    Returns
    -------
    int or datetime
        The opposite of the input.
    """
    if isinstance(time, datetime.datetime):
        return int(mktime(time.timetuple()))*1000
    else:
        try:
            timestamp = time / 1000
            return datetime.datetime.fromtimestamp(timestamp)
        except Exception as e:
            raise


def get_nearby_stations(lat, lon):
    """Stations nearby the given location.

    Parameters
    ----------
    lat : float
        Latitude
    lon : float
         and longitude of the desired location.


    Returns a list which is formated in this fassion::

        [
            {
                'lines':
                    {
                    'nachtbus': [],
                    'ubahn': ['2', '5', '7'],
                    'tram': [],
                    'sbahn': [],
                    'otherlines': [],
                    'nachttram': [],
                    'bus': []
                    },
                'hasLiveData': True,
                'place': 'München',
                'products': ['BUS', 'TRAM', 'UBAHN', 'SBAHN'],
                'id': 1060,
                'type': 'nearbystation',
                'name': 'Innsbrucker Ring',
                'hasZoomData': True,
                'distance': 59,
                'longitude': 11.619138,
                'latitude': 48.120408
             },
         ]

    """
    if lat == 0 or lon == 0:
        return None

    if not (isinstance(lat, float) and isinstance(lon, float)):
        raise TypeError()

    url = nearby_url.format(lat=lat, lon=lon)

    results = _perform_api_request(url)
    return results['locations']


def get_id_for_station(station_name):
    """Returns the station_id for the given station name.

    If more than one station match, the first result is given.
    `None` is returned if no match was found.
    """
    try:
        station = get_stations(station_name)[0]
    except IndexError:
        return None
    return station['id']


def get_locations(query):
    """Returns all matches from the search for the given query string.

    `query` can either be a name of a station or of a street, square, etc.

    Returns a list wich looks somewhat like this::

        [
            {
                'lines':
                    {
                    'nachtbus': [],
                    'ubahn': ['2', '5', '7'],
                    'tram': [],
                    'sbahn': [],
                    'otherlines': [],
                    'nachttram': [],
                    'bus': []
                    },
                'hasLiveData': True,
                'place': 'München',
                'products': ['u'],
                'id': 1060,
                'type': 'nearbystation',
                'name': 'Innsbrucker Ring',
                'hasZoomData': True,
                'distance': 59,
                'longitude': 11.619138,
                'latitude': 48.120408
            },
        ]

    """
    try:
        query = int(query)  # converts station ids to int if thay aren't already
    except(ValueError):  # happens if it is a station name
        url = query_url_name.format(name=query)
    else:  # happens if it is a station id
        url = query_url_id.format(id=str(query))

    results = _perform_api_request(url)
    return results["locations"]


def get_stations(station):
    """Like :func:`.get_locations`, but filters out all results which
    are not stations.
    """
    results = get_locations(station)
    stations = []
    for result in results:
        if result['type'] == 'station':
            stations.append(result)
    return stations


def get_route(start, dest,
              time=None, arrival_time=False,
              max_walk_time_to_start=None, max_walk_time_to_dest=None,
              change_limit=None):
    """Plans a route from start to dest

    Parameters
    ----------
    start : int/tuple
        The `station_id` of the starting station or a tuple of coordinates
    dest : int/tuple
        `station_id` of the destination station or a tuple of coordinates
    time : datetime, optional
    arrival_time : bool, optional
        Specifies if `time` is the starting time (which is default) or
        the desired time of arrival.
    max_walk_time_to_start, max_walk_time_to_dest : int, optional
        Maximum time of walking in minutes required to reach the start/dest.
    """
    url = routing_url
    options = []

    if isinstance(start, int):
        options.append("fromStation=" + str(start))
    elif isinstance(start, tuple) and len(start) == 2:
        options.append("fromLatitude=" + str(start[0]))
        options.append("fromLongitude=" + str(start[1]))
    else:
        raise ValueError("A start must be given;\
                          either int station id or tuple latitude longitude")

    if isinstance(dest, int):
        options.append("toStation=" + str(dest))
    elif isinstance(dest, tuple) and len(dest) == 2:
        options.append("toLatitude=" + str(dest[0]))
        options.append("toLongitude=" + str(dest[1]))
    else:
        raise ValueError("A destination must be given;\
                          either int station id or tuple latitude longitude")

    if time:
        if isinstance(time, datetime.datetime):
            time = _convert_time(time)
        options.append("time=" + str(time))
        if arrival_time:
            options.append("arrival=true")
    if max_walk_time_to_start:
        options.append("maxTravelTimeFootwayToStation=" +
                       str(max_walk_time_to_start))
    if max_walk_time_to_dest:
        options.append("maxTravelTimeFootwayToDestination=" +
                       str(max_walk_time_to_dest))

    if change_limit is not None: # 'if change_limit:' would not work for 0
        if isinstance(change_limit, int):
            options.append("changeLimit=" + str(change_limit))

    options_url = "&".join(options)
    url = routing_url + options_url
    results = _perform_api_request(url)
    for connection in results["connectionList"]:
        connection["departure_datetime"] = \
            _convert_time(connection["departure"])
        connection["arrival_datetime"] = _convert_time(connection["arrival"])
    return results["connectionList"]


def get_departures(station_id):
    """Get the next departures for `station_id`.

    To get the `station_id` associated with a station name,
    use :func:`get_id_for_station`.

    Returns a list like::

        [
            {
                'departureTimeMinutes': 0,
                'destination': 'Laimer Platz',
                'sev': False,
                'departureId': 1188266868,
                'live': True,
                'departureTime': 1478644495000,
                'lineBackgroundColor': '#b78730',
                'label': '5',
                'product': 'u'
            },
        ]

    `departureTimeMinutes`, the time left to the departure in minutes,
    is added to the response from the api for your convenience.
    """
    if not isinstance(station_id, int):
        raise TypeError("Please give the int station_id of the station.\
                         You can find it out by running \
                         get_id_for_station('Station name')")
    url = departure_url.format(id=str(station_id))
    departures = _perform_api_request(url)['departures']
    for departure in departures:
        # For some reason, mvg gives you a Unix timestamp, but in milliseconds.
        # Here, we convert it to datetime
        time = _convert_time(departure['departureTime'])
        relative_time = time - datetime.datetime.now()
        departure[u'departureTimeMinutes'] = relative_time.seconds // 60
    return departures


def get_interruptions():
    url = interruptions_url
    interruptions = _perform_api_request(url)
    return interruptions


class Station:
    """Gives you a proxy to get the next departures for a particular
    station.

    Either give it an exact station name (like "Hauptbahnhof")
    or a station_id.

    Deprecated-ish: This is not really all that useful.
    Just using :func:`get_id_for_station` and :func:`get_departures`
    really is the nicer way in most cases.
    """

    def __init__(self, station):
        matching_stations = get_stations(station)
        if matching_stations == []:
            raise NameError("No matching station found")
        else:
            self.id = matching_stations[0]["id"]
            self.name = matching_stations[0]["name"]
            self.latitude = matching_stations[0]["latitude"]
            self.longitude = matching_stations[0]["longitude"]

    def get_departures(self):
        return get_departures(self.id)

    def __repr__(self):
        return "Station(id=%s, name='%s')" % (self.id, self.name)
