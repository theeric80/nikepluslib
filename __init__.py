
# TODO: Unittest

if __name__ == '__main__':
    start_date  = raw_input('startDate (yyyy-mm-dd): ')
    end_date    = raw_input('endDate (yyyy-mm-dd): ')
    print 'Get NIKE+ activities from %s to %s' % (start_date, end_date)

    from os.path import split
    import nikeplus

    target = split(__file__)[0]
    nikeplus.export_activities_to_gpx(target, start_date, end_date, pretty_print=False)
