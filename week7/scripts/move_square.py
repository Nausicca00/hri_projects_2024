#!/usr/bin/python3
import rospy
from geometry_msgs.msg import Twist
import time
from nav_msgs.msg import Odometry
import math
from tf.transformations import euler_from_quaternion, quaternion_from_euler

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
        
    def get_yaw (self, msg):
        orientation_q = msg.pose.pose.orientation
        orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
        (roll, pitch, yaw) = euler_from_quaternion (orientation_list)
        return yaw

    def move_square(self):
        rospy.init_node('move_square', anonymous=True)
        self.rate = rospy.Rate(10)  # 10 Hz
        
        self.t = Twist()
        
        for i in range(4):
            self.start = self.get_odom()
            #self.current_yaw = self.get_yaw(self.get_odom())
            #self.target_yaw = self.current_yaw + math.radians(90)
            #self.turn = self.target_yaw - self.current_yaw
            
            while not rospy.is_shutdown():
                self.t.linear.x = 1.0
                self.t.angular.z = 0.0
                #self.pub.publish(self.t)
            
                self.cur = self.get_odom()
                
                self.dx = self.cur.pose.pose.position.x - self.start.pose.pose.position.x
                self.dy = self.cur.pose.pose.position.y - self.start.pose.pose.position.y

                # distance
                self.dist = math.sqrt(self.dx*self.dx + self.dy*self.dy)
                print(self.dist)

                if self.dist > 1.0:
                    self.t.linear.x = 0.0
                    #self.pub.publish(self.t)

                    # Turn 90 degrees
                    self.current_yaw = self.get_yaw(self.get_odom())
                    self.target_yaw = self.current_yaw + math.radians(90)
                    self.turn = self.target_yaw - self.current_yaw
                    print("Difference: ", self.turn, "\n")
                    self.turn = (self.turn + math.pi) % (2 * math.pi) - math.pi
                    print("Current:", self.current_yaw, "\n")
                    print("Target: ", self.target_yaw)
                    
                    if self.turn > 1.0:
                        self.t.angular.z = -1.0
                        self.t.linear.x = 0.0
                        self.cur = self.get_odom()
                    elif self.turn < -1.0:
                        self.t.angular.z = 1.0
                        self.t.linear.x = 0.0
                        self.cur = self.get_odom()
                    else:
                        self.t.angular.z = 0.0
                        self.t.linear.x = 0.0
                        self.cur = self.get_odom()
                
                    #self.t.linear.x = 1.0
                    #self.t.angular.z = 0.0
                self.pub.publish(self.t)

if __name__ == '__main__':
    try:
        test = MoveSquare()
        test.move_square()
    except rospy.ROSInterruptException:
        pass
