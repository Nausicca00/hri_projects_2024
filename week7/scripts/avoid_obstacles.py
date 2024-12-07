# THIS CODE IS AI GENERATED AND I AM USING IT AS A REFERENCE TO HELP ME FIGURE THINGS OUT
# I DO NOT EXPECT THIS CODE TO WORK BUT IF IT DOES COOL!

#!/usr/bin/python3

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class ObstacleAvoidance:
    def __init__(self):
        self.scan_data = LaserScan()
        self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
        self.sub = rospy.Subscriber("/scan", LaserScan, self.scan_callback)
        rospy.sleep(rospy.Duration.from_sec(0.5))

    def scan_callback(self, msg):
        self.scan_data = msg

    def get_scan(self):
        return self.scan_data

if __name__ == '__main__':
    rospy.init_node('obstacle_avoidance')
    n = ObstacleAvoidance()
    rate = rospy.Rate(10.0)

    t = Twist()

    while not rospy.is_shutdown():
        scan = n.get_scan()
        if not scan.ranges:
            continue

        # Goal 3: Stop if an obstacle is close
        min_distance = min(scan.ranges)
        if min_distance < 0.5:  # Threshold distance to stop
            t.linear.x = 0.0
            t.angular.z = 0.0
            n.pub.publish(t)
            rospy.loginfo("Obstacle detected! Stopping.")
            continue

        # Goal 4: Turn if an obstacle is in front
        front_ranges = scan.ranges[len(scan.ranges)//3:2*len(scan.ranges)//3]
        if min(front_ranges) < 0.5:  # Threshold distance to turn
            left_ranges = scan.ranges[:len(scan.ranges)//3]
            right_ranges = scan.ranges[2*len(scan.ranges)//3:]
            if min(left_ranges) < min(right_ranges):
                t.angular.z = -0.5  # Turn right
                rospy.loginfo("Turning right.")
            else:
                t.angular.z = 0.5  # Turn left
                rospy.loginfo("Turning left.")
            t.linear.x = 0.0
        else:
            t.linear.x = 0.5  # Move forward
            t.angular.z = 0.0

        n.pub.publish(t)
        rate.sleep()
