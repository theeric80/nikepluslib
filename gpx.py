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
