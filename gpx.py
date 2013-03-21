from xml.etree import ElementTree
from xml.dom import minidom

# Complex Types
class ComplexType(ElementTree.Element):
    def __init__(self, tag, attributes=[], elements=[]):
        self._attributes = attributes   # attributes
        self._elements   = elements     # simple elements
        ElementTree.Element.__init__(self, tag)

    def _subElement(self, tag):
        element = self.find(tag)
        if element is None:
            element = ElementTree.Element(tag)
            self.append(element)
        return element

    def __setattr__(self, name, value):
        if name in ['_attributes', '_elements']:
            pass
        elif name in self._attributes:
            self.set(name, str(value))
        elif name in self._elements:
            self._subElement(name).text = str(value)
        super(ComplexType, self).__setattr__(name, value)

class GPXType(ComplexType):
    def __init__(self, tag):
        attributes  = ['version', 'creator']
        elements    = []
        # Complex Elements: [metadata, wpt, rte, trk, extensions]
        ComplexType.__init__(self, tag, attributes, elements)

        # Required Attributes
        self.version = '1.1'
        self.creator = ''

        # Hack: Namespace
        self.set('xmlns', 'http://www.topografix.com/GPX/1/1')
        self.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        self.set('xsi:schemaLocation', 'http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd')

class TrackType(ComplexType):
    def __init__(self, tag):
        attributes  = []
        elements    = ['name', 'cmt', 'desc', 'src', 'number', 'type']
        # Complex Elements: [link, extensions, trkseg]
        ComplexType.__init__(self, tag, attributes, elements)

class TrackSegmentType(ComplexType):
    def __init__(self, tag):
        attributes  = []
        elements    = []
        # Complex Elements: [trkpt, extensions]
        ComplexType.__init__(self, tag, attributes, elements)

class WayPointType(ComplexType):
    def __init__(self, tag):
        attributes  = ['lat', 'lon']
        elements    = ['ele', 'time', 'geoidheight', 'name', 'cmt', 'desc', 'src', 'sym', 'type', 'sat', 'hdop', 'vdop', 'pdop', 'ageofdgpsdata']
        # Complex Elements: [magvar, link, fix, dgpsid, extensions]
        ComplexType.__init__(self, tag, attributes, elements)

        # Required Attributes
        self.lat = 0
        self.lon = 0

# Complex Elements
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

