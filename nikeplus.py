import urllib
import urllib2
import json

from os.path import join
import gpx
import time
import datetime

import logging
logger = logging.getLogger(__name__)

SRV_URL = 'https://api.nike.com'
API_URL = SRV_URL + '/me/sport'

UTC_DATE_FMT = '%Y-%m-%dT%H:%M:%SZ'

# TODO: OAuth
TOKEN   = ''

class Activity(object):
    def __init__(self, activity_data={}):
        # prepare activity data
        self._parse_activity_data(activity_data)
        # GPS data
        self._gps = None

    def _parse_activity_data(self, data):
        self.activityId         = data.get('activityId', '')
        self.activityType       = data.get('activityType', '')
        self.activityTimeZone   = data.get('activityTimeZone', '')
        self.startTime          = data.get('startTime', '')
        self.deviceType         = data.get('deviceType', '')

        # metricSummary
        metricSummary   = data.get('metricSummary')
        self.distance   = metricSummary.get('distance', 0)
        self.duration   = metricSummary.get('duration', '')
        self.calories   = metricSummary.get('calories', 0)
        self.fuel       = metricSummary.get('fuel', 0)
        self.steps      = metricSummary.get('steps', 0)

    @property
    def gps(self):
        if self._gps is None:
            self._gps = GPSData(self.activityId)
        return self._gps

class GPSData(object):
    def __init__(self, activityId):
        self.activityId = activityId
        self._get_gps_data()

    def _get_gps_data(self):
        url = API_URL + '/activities/%s/gps' % self.activityId
        response = _send_request(url)
        self._parse_gps_data(response)

    def _parse_gps_data(self, data):
        self.elevationLoss  = data.get('elevationLoss', 0)
        self.elevationGain  = data.get('elevationGain', 0)
        self.elevationMin   = data.get('elevationMin', 0)
        self.elevationMax   = data.get('elevationMax', 0)
        self.intervalMetric = data.get('intervalMetric', 0)
        self.intervalUnit   = data.get('intervalUnit', '')
        self.wayPoints      = data.get('waypoints', [])

def get_activity_list(startDate='', endDate=''):
    # Date format: yyyy-mm-dd
    activities = []

    # TODO: params (offset, count, startDate, endDate)
    url = API_URL + '/activities'

    tm_start = None
    while url:
        # Init the params
        params = {}

        if startDate and endDate:
            params['startDate'] = startDate
            params['endDate']   = endDate

        # Get the activities from host
        response = _send_request(url, params)
        data_list = response.get('data')
        if not data_list:
            break

        # TODO: response['paging']['next'] will not be None if we add startDate/endDate into query parameters.
        # Workaround: Check the start time of the first activity. Break while loop if we have handled it before.
        tm_current = time.strptime(data_list[0]['startTime'], UTC_DATE_FMT)
        if not tm_start:
            tm_start = tm_current
        elif tm_current >= tm_start:
            break

        # Create Activity objects
        for item in data_list:
            obj = Activity(item)
            activities.append(obj)

        # Prepare the url for next query
        next = response['paging'].get('next')
        url = SRV_URL + next if next else ''

    return activities

def export_activities_to_gpx(target_folder, start_date='', end_date='', pretty_print=False):
    activity_list = get_activity_list(start_date, end_date)
    for activity in activity_list:
        start_time = datetime.datetime.strptime(activity.startTime, UTC_DATE_FMT)
        logger.info('Parsing NIKE+ activity: %s' % start_time.strftime('%Y-%m-%d_%H%M'))

        way_points = activity.gps.wayPoints
        numof_way_points = len(way_points)
        if numof_way_points <= 0:
            continue

        # Set the time delta
        try:
            # tm_delta = total_duration / number_of_way_points
            duration = time.strptime(activity.duration.split('.')[0], '%H:%M:%S')
            tm_delta = datetime.timedelta(hours=duration.tm_hour, minutes=duration.tm_min, seconds=duration.tm_sec) / numof_way_points
        except:
            tm_delta = datetime.timedelta(seconds=activity.gps.intervalMetric)

        current_time = start_time

        # Create Root element
        root = gpx.GPX()

        # Add Track into Root
        trk = gpx.Track()
        root.append(trk)

        # Add TrackSegment into Track
        trkseg = gpx.TrackSegment()
        trk.append(trkseg)

        # Add TrackPoints into TrackSegment
        for item in way_points:
            pt = gpx.TrackPoint()
            pt.lat = item['latitude']
            pt.lon = item['longitude']
            pt.ele = item['elevation']
            pt.time = current_time.strftime(UTC_DATE_FMT)
            trkseg.append(pt)

            current_time += tm_delta

        filename = 'NIKE+_gpx_%s.gpx' % start_time.strftime('%Y-%m-%d_%H%M')
        filepath = join(target_folder, filename)

        logger.info('Export NIKE+ activity to: %s' % filepath)
        root.write(filepath, pretty_print)

def _send_request(url, params={}):
    if url.find('?') < 0:
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
        logger.error('Error: _send_request(%s) = %s' % (url, err.read()))
        response = {}

    return response
