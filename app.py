from os.path import split
import sys
import logging
import time
import nikeplus

def main():
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)

    if nikeplus.TOKEN == '':
        logger.warning('Invalid NIKE+ access token.')
        logger.warning('Please get your access token from https://developer.nike.com/console')
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
            logger.warning('The startDate/endDate does not match format: yyyy-mm-dd')
            sys.exit(1)

        logger.info('Export NIKE+ activities from %s to %s' % (start_date, end_date))

    target = split(__file__)[0]
    nikeplus.export_activities_to_gpx(target, start_date, end_date, pretty_print=False)


if __name__ == '__main__':
    main()
