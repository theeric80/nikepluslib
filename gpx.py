from xml.etree import ElementTree
from xml.dom import minidom

# Complex Types
class GPXType(ElementTree.Element):
    def __init__(self, tag):
        # Required Attributes
        attrib = {
            'version': '1.1',
            'creator': ''}
        # Namespace
        attrib['xmlns'] = 'http://www.topografix.com/GPX/1/1'
        attrib['xmlns:xsi'] = 'http://www.w3.org/2001/XMLSchema-instance'
        attrib['xsi:schemaLocation'] = 'http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd'
        ElementTree.Element.__init__(self, tag, attrib)

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

class TrackType(ElementTree.Element):
    def __init__(self, tag):
        ElementTree.Element.__init__(self, tag)

class TrackSegmentType(ElementTree.Element):
    def __init__(self, tag):
        ElementTree.Element.__init__(self, tag)

class WayPointType(ElementTree.Element):
    def __init__(self, tag):
        # Required Attributes
        attrib = {
            'lat': '0',
            'lon': '0'}
        ElementTree.Element.__init__(self, tag, attrib)

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

# Elements
class GPX(GPXType):
    def __init__(self):
        GPXType.__init__(self, 'gpx')

    def write(self, filename, pretty_print=False):
        f = open(filename, 'w')
        if pretty_print:
            text = ElementTree.tostring(self, encoding='UTF-8')
            f.write( minidom.parseString(text).toprettyxml(encoding='UTF-8') )
        else:
            ElementTree.ElementTree(self).write(f, encoding='UTF-8')
        f.close()

class Track(TrackType):
    def __init__(self):
        TrackType.__init__(self, 'trk')

class TrackSegment(TrackSegmentType):
    def __init__(self):
        TrackSegmentType.__init__(self, 'trkseg')

class TrackPoint(WayPointType):
    def __init__(self):
        WayPointType.__init__(self, 'trkpt')

class WayPoint(WayPointType):
    def __init__(self):
        WayPointType.__init__(self, 'wpt')

# Utils
def _getSubElement(parent, tag):
    element = parent.find(tag)
    if not element:
        element = ElementTree.Element(tag)
        parent.append(element)
    return element
