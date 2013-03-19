from xml.etree.ElementTree import Element, ElementTree

class GPX(Element):
    def __init__(self):
        # Required Attributes
        attrib = {
            'version': '1.1',
            'creator': ''}
        Element.__init__(self, 'gpx', attrib)

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

    def write(self, filename):
        f = open(filename, 'w')
        ElementTree(self).write(f)
        f.close()

class WayPoint(Element):
    def __init__(self):
        # Required Attributes
        attrib = {
            'lat': '0',
            'lon': '0'}
        Element.__init__(self, 'wpt', attrib)

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
