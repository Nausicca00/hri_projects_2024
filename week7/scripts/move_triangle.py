# THIS CODE IS AI GENERATED AND I AM USING IT AS A REFERENCE TO HELP ME FIGURE THINGS OUT
# I DO NOT EXPECT THIS CODE TO WORK BUT IF IT DOES COOL!

import rospy
import math
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion

class TriangleOdom:
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
    rospy.init_node('triangle')
    n = TriangleOdom()
    rate = rospy.Rate(15.0)

    # Define the twist message
    t = Twist()

    # Function to move forward
    def move_forward(distance, speed):
        t.linear.x = speed
        start_odom = n.get_odom()
        start_x = start_odom.pose.pose.position.x
        start_y = start_odom.pose.pose.position.y
        while not rospy.is_shutdown():
            n.pub.publish(t)
            cur_odom = n.get_odom()
            cur_x = cur_odom.pose.pose.position.x
            cur_y = cur_odom.pose.pose.position.y
            dist = math.sqrt((cur_x - start_x)**2 + (cur_y - start_y)**2)
            if dist >= distance:
                break
            rate.sleep()
        t.linear.x = 0.0
        n.pub.publish(t)
        rospy.sleep(rospy.Duration.from_sec(1.0))

    # Function to turn
    def turn(angle, speed):
        t.angular.z = speed
        start_yaw = n.get_yaw(n.get_odom())
        while not rospy.is_shutdown():
            n.pub.publish(t)
            cur_yaw = n.get_yaw(n.get_odom())
            yaw_diff = abs(cur_yaw - start_yaw)
            if yaw_diff >= angle:
                break
            rate.sleep()
        t.angular.z = 0.0
        n.pub.publish(t)
        rospy.sleep(rospy.Duration.from_sec(1.0))

    # Move in a triangle
    for _ in range(3):
        move_forward(distance=1.0, speed=0.5)
        turn(angle=2*math.pi/3, speed=0.5)

    rospy.spin()
