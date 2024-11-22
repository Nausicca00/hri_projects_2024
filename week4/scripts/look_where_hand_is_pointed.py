#!/usr/bin/python3
import rospy

import math
import tf2_ros
from sensor_msgs.msg import JointState
import geometry_msgs.msg

class motion:
    def __init__(self):
        rospy.init_node('look_where_hand_is_pointed', anonymous=True)
        self.js = JointState()
        self.pub = rospy.Publisher('joint_states', JointState, queue_size=10)
        self.sub = rospy.Subscriber('joint_states_input', JointState, self.callback)
        self.tfBuffer = tf2_ros.Buffer()
        self.listener = tf2_ros.TransformListener(self.tfBuffer)
        self.br = tf2_ros.TransformBroadcaster()
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
        
    def lookWhereHandIsPointed(self):
        pitch = 0
        yaw = 0
        while not rospy.is_shutdown():
            try:
                trans = self.tfBuffer.lookup_transform('Head', 'l_gripper', rospy.Time())
                self.broadcast_pointing_frame(trans)
                
                direction_vector = geometry_msgs.msg.Vector3(
                    x = trans.transform.translation.x,
                    y = trans.transform.translation.y,
                    z = trans.transform.translation.z
                )
                
                pitch -= math.atan2(direction_vector.z, direction_vector.x)
                yaw += math.atan2(direction_vector.y, direction_vector.x) - 0.25
                self.head(pitch, yaw)
                
            except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
                rospy.logwarn("Failed to get transformation")
                self.pub.publish(self.js)
            self.rate.sleep()
    
    def broadcast_pointing_frame(self, trans):
        t = geometry_msgs.msg.TransformStamped()
        t.header.stamp = rospy.Time.now()
        t.header.frame_id = "l_gripper"
        t.child_frame_id = "pointing_frame"
        
        t.transform.translation.x = trans.transform.translation.x + 1.0
        t.transform.translation.y = trans.transform.translation.y
        t.transform.translation.z = trans.transform.translation.z
        
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = 0.0
        t.transform.rotation.w = 1.0
    
        self.br.sendTransform(t)
      
if __name__ == '__main__':
    try: 
        test = motion() 
        test.lookWhereHandIsPointed()
        
    except rospy.ROSInterruptException: 
        pass
