#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan

def callback(data):
    # Find the closest reading
    closest_distance = min(data.ranges)
    rospy.loginfo('Closest distance: %f', closest_distance)

def listener():
    rospy.init_node('base_scan_listener', anonymous=True)
    rospy.Subscriber('/base_scan', LaserScan, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
