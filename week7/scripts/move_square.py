#!/usr/bin/python3
import rospy
from geometry_msgs.msg import Twist
import time
from nav_msgs.msg import Odometry
import math

class MoveSquare:
    def __init__(self):
        self.odom = Odometry()
        
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.sub = rospy.Subscriber("/odom", Odometry, self.odom_callback)
        rospy.sleep(rospy.Duration.from_sec(0.5))
        
    def odom_callback(self, msg):
        self.odom = msg

    def get_odom(self):
        return self.odom

    def move_square(self):
        rospy.init_node('move_square', anonymous=True)
        self.rate = rospy.Rate(10)  # 10 Hz
        self.start = self.get_odom()
        
        
        self.t = Twist()
        
        while not rospy.is_shutdown():
        
            for i in range(4):
                self.t.linear.x = 1.0
                self.pub.publish(self.t)
            
                self.cur = self.get_odom()
            
                self.dx = self.cur.pose.pose.position.x - self.start.pose.pose.position.x
                self.dy = self.cur.pose.pose.position.y - self.start.pose.pose.position.y

                # distance
                self.dist = math.sqrt( self.dx*self.dx + self.dy*self.dy )
                print(self.dist)

                if self.dist > 0.1:
                    self.t.linear.x = 0.0
                    self.pub.publish(self.t)
                    break

            # Turn 90 degrees

if __name__ == '__main__':
    try:
        test = MoveSquare()
        test.move_square()
    except rospy.ROSInterruptException:
        pass
