
# TODO: Unittest

if __name__ == '__main__':
    import logging
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)

    from os.path import split
    import sys
    import time
    import nikeplus

    if nikeplus.TOKEN == '':
        print 'Invalid NIKE+ access token.'
        print 'Please get your access token from https://developer.nike.com/console'
        sys.exit(1)

    print 'Input the time period you want to export.'
    print 'Leave startDate/endDate empty if you want to export all activities.'

    start_date  = raw_input('startDate (yyyy-mm-dd): ')
    end_date    = raw_input('endDate (yyyy-mm-dd): ')

    if start_date or end_date:
        try:
            time.strptime(start_date, '%Y-%m-%d')
            time.strptime(end_date, '%Y-%m-%d')
        except:
            print 'The startDate/endDate does not match format: yyyy-mm-dd'
            sys.exit(1)

        print 'Export NIKE+ activities from %s to %s' % (start_date, end_date)

    target = split(__file__)[0]
    nikeplus.export_activities_to_gpx(target, start_date, end_date, pretty_print=False)
