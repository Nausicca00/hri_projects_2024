# THIS CODE IS AI GENERATED AND I AM USING IT AS A REFERENCE TO HELP ME FIGURE THINGS OUT
# I DO NOT EXPECT THIS CODE TO WORK BUT IF IT DOES COOL!

#!/usr/bin/python3

import rospy
import math
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion

class FigureEightOdom:
    def __init__(self):
        self.odom = Odometry()
        self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
        self.sub = rospy.Subscriber("/odom", Odometry, self.odom_callback)
        rospy.sleep(rospy.Duration.from_sec(0.5))

    def odom_callback(self, msg):
        self.odom = msg

    def get_yaw(self, msg):
        orientation_q = msg.pose.pose.orientation
        orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
        (roll, pitch, yaw) = euler_from_quaternion(orientation_list)
        return yaw

    def get_odom(self):
        return self.odom

if __name__ == '__main__':
    rospy.init_node('figure_eight')
    n = FigureEightOdom()
    rate = rospy.Rate(15.0)

    # Define the twist message
    t = Twist()

    # Function to move in a circle
    def move_in_circle(radius, speed, duration):
        t.linear.x = speed
        t.angular.z = speed / radius
        start_time = rospy.Time.now()
        while rospy.Time.now() - start_time < rospy.Duration.from_sec(duration):
            n.pub.publish(t)
            rate.sleep()
        t.linear.x = 0.0
        t.angular.z = 0.0
        n.pub.publish(t)
        rospy.sleep(rospy.Duration.from_sec(1.0))

    # Move in the first circle (clockwise)
    move_in_circle(radius=1.0, speed=0.5, duration=6.28)  # 2*pi*radius/speed = duration

    # Move in the second circle (counter-clockwise)
    move_in_circle(radius=1.0, speed=-0.5, duration=6.28)

    rospy.spin()
