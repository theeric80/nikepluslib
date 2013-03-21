
# TODO: Unittest

if __name__ == '__main__':
    from os.path import split
    import nikeplus

    target = split(__file__)[0]
    nikeplus.export_activities_to_gpx(target, pretty_print=True)
