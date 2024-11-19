#!/usr/bin/python3
import rospy

import math
import tf2_ros
from sensor_msgs.msg import JointState
import geometry_msgs.msg

# this is based on the ROS tf2 tutorial: http://wiki.ros.org/tf2/Tutorials/Writing%20a%20tf2%20listener%20%28Python%29

class lookAtHand:
    def __init__(self):
        rospy.init_node('tf2_look_at_hand', anonymous=True)
        self.js = JointState()
        self.pub = rospy.Publisher('joint_states', JointState, queue_size=10)
        self.sub = rospy.Subscriber('joint_states_input', JointState, self.callback)
        self.tfBuffer = tf2_ros.Buffer()
        self.listener = tf2_ros.TransformListener(self.tfBuffer)
        self.rate = rospy.Rate(10.0)
        self.js.name.append("HeadYaw")
        self.js.name.append("HeadPitch")
        self.js.position.append(0)
        self.js.position.append(0)
        self.initialize()
        
    def callback(self, data):
        self.js = data
        
    def initialize(self):
        self.js.header.frame_id = "Torso"
        
        
    def head(self, pitch, yaw):
        self.js.header.stamp = rospy.get_rostime()
        pos = list(self.js.position)
        pos[1] = pitch
        pos[0] = yaw
        self.js.position = tuple(pos)
        self.pub.publish(self.js)
        
    def LookAtHand(self):
        pitch = 0
        yaw = 0
        while not rospy.is_shutdown():
            try:
                trans = self.tfBuffer.lookup_transform('Head', 'l_gripper', rospy.Time())
                direction_vector = geometry_msgs.msg.Vector3(
                    x = trans.transform.translation.x,
                    y = trans.transform.translation.y,
                    z = trans.transform.translation.z
                )
                
                pitch -= math.atan2(direction_vector.z, direction_vector.x)
                yaw += math.atan2(direction_vector.y, direction_vector.x)
                self.head(pitch, yaw)
                
            except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
                rospy.logwarn("Failed to get transformation")
                self.pub.publish(self.js)
            self.rate.sleep()
            
if __name__ == '__main__':
    try: 
        look_at_hand = lookAtHand() 
        look_at_hand.LookAtHand()
        
    except rospy.ROSInterruptException: 
        pass
