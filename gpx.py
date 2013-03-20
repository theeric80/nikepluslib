from xml.etree import ElementTree
from xml.dom import minidom

class GPX(ElementTree.Element):
    def __init__(self):
        # Required Attributes
        attrib = {
            'xmlns': 'http://www.topografix.com/GPX/1/1',
            'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
            'xsi:schemaLocation': 'http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd',
            'version': '1.1',
            'creator': ''}
        ElementTree.Element.__init__(self, 'gpx', attrib)

    @property
    def version(self):
        return self.get('version', '1.1')

    @version.setter
    def version(self, value):
        self.set('version', value)

    @property
    def creator(self):
        return self.get('creator', '')

    @creator.setter
    def creator(self, value):
        self.set('creator', value)

    def write(self, filename, pretty_print=False):
        f = open(filename, 'w')
        if pretty_print:
            text = ElementTree.tostring(self, encoding='UTF-8')
            f.write( minidom.parseString(text).toprettyxml(encoding='UTF-8') )
        else:
            ElementTree.ElementTree(self).write(f, encoding='UTF-8')
        f.close()

class WayPoint(ElementTree.Element):
    def __init__(self):
        # Required Attributes
        attrib = {
            'lat': '0',
            'lon': '0'}
        ElementTree.Element.__init__(self, 'wpt', attrib)

    # Attributes
    @property
    def lat(self):
        return float( self.get('lat', 0) )

    @lat.setter
    def lat(self, value):
        assert(value <= 90)
        assert(value >= -90)
        self.set('lat', str(value))

    @property
    def lon(self):
        return float( self.get('lon', 0) )

    @lon.setter
    def lon(self, value):
        assert(value <= 180)
        assert(value >= -180)
        self.set('lon', str(value))

    # Elements
    @property
    def ele(self):
        value = _getSubElement(self, 'ele').text
        return float(value) if value else 0

    @ele.setter
    def ele(self, value):
        _getSubElement(self, 'ele').text = str(value)

    @property
    def time(self):
        return _getSubElement(self, 'time').text

    @time.setter
    def time(self, value):
        _getSubElement(self, 'time').text = value

class Track(ElementTree.Element):
    def __init__(self):
        ElementTree.Element.__init__(self, 'trk')

class TrackSegment(ElementTree.Element):
    def __init__(self):
        ElementTree.Element.__init__(self, 'trkseg')

class TrackPoint(WayPoint):
    def __init__(self):
        WayPoint.__init__(self)
        self.tag = 'trkpt'

# Utils
def _getSubElement(parent, tag):
    element = parent.find(tag)
    if not element:
        element = ElementTree.Element(tag)
        parent.append(element)
    return element
