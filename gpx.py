from xml.etree import ElementTree

class GPX(ElementTree.Element):
    def __init__(self):
        # Required Attributes
        attrib = {
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

    def write(self, filename):
        f = open(filename, 'w')
        ElementTree.ElementTree(self).write(f, encoding='utf-8')
        f.close()

class WayPoint(ElementTree.Element):
    def __init__(self):
        # Required Attributes
        attrib = {
            'lat': '0',
            'lon': '0'}
        ElementTree.Element.__init__(self, 'wpt', attrib)

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
