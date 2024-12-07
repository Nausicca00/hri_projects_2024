# THIS CODE IS AI GENERATED AND I AM USING IT AS A REFERENCE TO HELP ME FIGURE THINGS OUT
# I DO NOT EXPECT THIS CODE TO WORK BUT IF IT DOES COOL!

#!/usr/bin/python3

import rospy
import math
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import tf2_ros
import tf2_geometry_msgs

class PersonFollower:
    def __init__(self):
        self.scan_data = LaserScan()
        self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
        self.sub_scan = rospy.Subscriber("/scan", LaserScan, self.scan_callback)
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer)
        rospy.sleep(rospy.Duration.from_sec(0.5))

    def scan_callback(self, msg):
        self.scan_data = msg

    def get_scan(self):
        return self.scan_data

    def get_person_position(self):
        try:
            trans = self.tf_buffer.lookup_transform('base_link', 'person', rospy.Time(0))
            return trans.transform.translation.x, trans.transform.translation.y
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            return None, None

if __name__ == '__main__':
    rospy.init_node('person_follower')
    n = PersonFollower()
    rate = rospy.Rate(10.0)

    t = Twist()

    while not rospy.is_shutdown():
        scan = n.get_scan()
        if not scan.ranges:
            continue

        person_x, person_y = n.get_person_position()
        if person_x is None or person_y is None:
            rospy.loginfo("Person not detected.")
            t.linear.x = 0.0
            t.angular.z = 0.0
            n.pub.publish(t)
            rate.sleep()
            continue

        # Goal 3: Stop if an obstacle is close
        min_distance = min(scan.ranges)
        if min_distance < 0.5:  # Threshold distance to stop
            t.linear.x = 0.0
            t.angular.z = 0.0
            n.pub.publish(t)
            rospy.loginfo("Obstacle detected! Stopping.")
            continue

        # Goal 4: Move toward the person while avoiding obstacles
        angle_to_person = math.atan2(person_y, person_x)
        front_ranges = scan.ranges[len(scan.ranges)//3:2*len(scan.ranges)//3]
        if min(front_ranges) < 0.5:  # Threshold distance to turn
            left_ranges = scan.ranges[:len(scan.ranges)//3]
            right_ranges = scan.ranges[2*len(scan.ranges)//3:]
            if min(left_ranges) < min(right_ranges):
                t.angular.z = -0.5  # Turn right
                rospy.loginfo("Turning right to avoid obstacle.")
            else:
                t.angular.z = 0.5  # Turn left
                rospy.loginfo("Turning left to avoid obstacle.")
            t.linear.x = 0.0
        else:
            t.linear.x = 0.5  # Move forward
            t.angular.z = angle_to_person  # Turn towards the person

        n.pub.publish(t)
        rate.sleep()
