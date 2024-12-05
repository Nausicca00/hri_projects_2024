#!/usr/bin/python3
import rospy
import time
import math
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

class MoveTriangle():

    def __init__(self):
        self.odom = Odometry()
        
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.sub = rospy.Subscriber("/odom", Odometry, self.odom_callback)
        rospy.sleep(rospy.Duration.from_sec(0.5))
        
    def odom_callback(self, msg):
        self.odom = msg

    def get_odom(self):
        return self.odom
        
    def get_yaw (self, msg):
        orientation_q = msg.pose.pose.orientation
        orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
        (roll, pitch, yaw) = euler_from_quaternion (orientation_list)
        return yaw
        
    def move_triangle(self):
        rospy.init_node('move_triangle', anonymous=True)
        self.rate = rospy.Rate(10)
        self.t = Twist()
        
        for i in range(3):
            self.start = self.get_odom()
            self.current_yaw = self.get_yaw(self.get_odom())
            self.target_yaw = self.current_yaw + math.radians(120)
            self.turn = self.target_yaw - self.current_yaw
            self.turn = (self.turn + math.pi) % (2 * math.pi) - math.pi
            
            while not rospy.is_shutdown():
                
            
        
if __name__ == '__main__':
    try:
        test = MoveTriangle()
        test.move_triangle()
    except rospy.ROSInterruptException:
        pass
