
# TODO: Unittest

if __name__ == '__main__':
    import nikeplus
    activity_list = nikeplus.get_activity_list()
    for activity in activity_list:
        print '--------------------'
        print 'Activity Id: %s' % activity.id
        print 'Number of GPS data:  %d' % len(activity.way_points)
        print '--------------------'
