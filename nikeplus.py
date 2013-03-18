import urllib
import urllib2
import json

API_URL = 'https://api.nike.com/me/sport'

# TODO: OAuth
TOKEN   = ''

class Activity(object):
    def __init__(self, activity_data={}):
        # prepare activity data
        self._parse_activity_data(activity_data)
        # GPS data
        self._way_points = None

    def __str__(self):
        return '%s(%s)' % (self.__class__, self.id)

    def _parse_activity_data(self, data):
        self.id         = data.get('activityId', '')
        self.calories   = data.get('calories', 0)
        self.distance   = data.get('distance', 0)
        self.duration   = data.get('duration', '')
        self.start_time = data.get('startTime', '')

    @property
    def way_points(self):
        if self._way_points is None:
            self._way_points = self._get_gps_data()
        return self._way_points

    def _get_gps_data(self):
        url = API_URL + '/activities/%s/gps' % self.id
        response = _send_request(url)
        return response.get('waypoints', [])

def get_activity_list():
    activities = []

    # TODO: params (offset, count, startDate, endDate)
    url = API_URL + '/activities'
    response = _send_request(url)

    # create activity objects
    # TODO: next
    for item in response['data']:
        obj = Activity(item)
        activities.append(obj)

    return activities

def _send_request(url, params={}):
    params['access_token'] = TOKEN
    url += '?' + urllib.urlencode(params)

    try:
        data = None
        headers = {
            'appid': 'fuelband',
            'Accept': 'application/json'}

        request = urllib2.Request(url, data, headers)
        file    = urllib2.urlopen(request)

        response = json.load(file)
    except urllib2.HTTPError as err:
        print 'Error: _send_request(%s) = %s' % (url, err.read())
        response = {}

    return response
