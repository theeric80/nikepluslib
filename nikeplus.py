import urllib
import urllib2
import json

API_URL = 'https://api.nike.com/me/sport'

APPID   = 'fuelband'
ACCEPT  = 'application/json'

# TODO: OAuth
TOKEN   = ''

class Activity(object):
    def __init__(self, activity_data={}):
        # prepare activity data
        self._parse_activity_data(activity_data)

    def __str__(self):
        return '%s(%s)' % (self.__class__, self.id)

    def _parse_activity_data(self, data):
        self.id         = data.get('activityId', '')
        self.calories   = data.get('calories', 0)
        self.distance   = data.get('distance', 0)
        self.duration   = data.get('duration', '')
        self.start_time = data.get('startTime', '')

def get_activity_list():
    activities = []

    # TODO: offset, count, startDate, endDate
    params = {'access_token': TOKEN}
    url = API_URL + '/activities' + '?' + urllib.urlencode(params)

    data = None
    headers = {'appid': APPID,
               'Accept': ACCEPT}

    request = urllib2.Request(url, data, headers)
    file = urllib2.urlopen(request)

    # create activity objects
    # TODO: next
    response = json.load(file)
    for item in response['data']:
        obj = Activity(item)
        activities.append(obj)

    return activities
