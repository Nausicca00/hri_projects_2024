#!/usr/bin/python3

import rospy
import math
import tf2_ros
import geometry_msgs.msg
from sensor_msgs.msg import JointState

def initialize(js):
    js.header.stamp = rospy.get_rostime()
    js.header.frame_id = "Torso"
    js.name = ["HeadYaw", "HeadPitch"]
    js.position = [0, 0]

def head(pub, js, pitch, yaw):
    js.position[js.name.index("HeadPitch")] = math.radians(pitch)
    js.position[js.name.index("HeadYaw")] = math.radians(yaw)
    pub.publish(js)
    initialize(js)

def gesture_toward_hand():
    try:
        trans = tfBuffer.lookup_transform('Head', 'LFinger23_link', rospy.Time())
        direction_vector = geometry_msgs.msg.Vector3(
            x = trans.transform.translation.x,
            y = trans.transform.translation.y,
            z = trans.transform.translation.z
        )
        rospy.loginfo(f"Gesture direction: x: {direction_vector.x}, y: {direction_vector.y}, z: {direction_vector.z}")
        
        # Calculate pitch and yaw from direction vector
        pitch = math.degrees(math.atan2(direction_vector.z, math.sqrt(direction_vector.x**2 + direction_vector.y**2)))
        yaw = math.degrees(math.atan2(direction_vector.y, direction_vector.x))
        
        # Move head to gesture toward the hand
        head(pub, js, pitch, yaw)
        rate.sleep()
    except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
        rospy.logwarn("Failed to get transformation")

def keep_head_pointed():
    while not rospy.is_shutdown():
        try:
            trans = tfBuffer.lookup_transform('Head', 'LFinger23_link', rospy.Time())
            direction_vector = geometry_msgs.msg.Vector3(
                x = trans.transform.translation.x,
                y = trans.transform.translation.y,
                z = trans.transform.translation.z
            )
            rospy.loginfo(f"Keep pointed direction: x: {direction_vector.x}, y: {direction_vector.y}, z: {direction_vector.z}")
            
            # Calculate pitch and yaw from direction vector
            pitch = math.degrees(math.atan2(direction_vector.z, math.sqrt(direction_vector.x**2 + direction_vector.y**2)))
            yaw = math.degrees(math.atan2(direction_vector.y, direction_vector.x))
            
            # Move head to keep pointed at the hand
            head(pub, js, pitch, yaw)
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            rate.sleep()
            continue
        rate.sleep()

def look_in_direction_hand_pointing():
    while not rospy.is_shutdown():
        try:
            trans = tfBuffer.lookup_transform('Head', 'LFinger23_link', rospy.Time())
            direction_vector = geometry_msgs.msg.Vector3(
                x = trans.transform.translation.x,
                y = trans.transform.translation.y,
                z = trans.transform.translation.z
            )
            rospy.loginfo(f"Look direction: x: {direction_vector.x}, y: {direction_vector.y}, z: {direction_vector.z}")
            
            # Calculate direction from hand position
            pitch = math.degrees(math.atan2(direction_vector.z, math.sqrt(direction_vector.x**2 + direction_vector.y**2)))
            yaw = math.degrees(math.atan2(direction_vector.y, direction_vector.x))
            
            # Move head to look in direction the hand is pointing
            head(pub, js, pitch, yaw)
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            rate.sleep()
            continue
        rate.sleep()

if __name__ == '__main__':
    rospy.init_node('robot_head_control', anonymous=True)
    tfBuffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfBuffer)
    pub = rospy.Publisher('joint_states_input', JointState, queue_size=10)
    js = JointState()
    rate = rospy.Rate(10.0)

    initialize(js)
    
    try:
        gesture_toward_hand()
        keep_head_pointed()
        look_in_direction_hand_pointing()
    except rospy.ROSInterruptException:
        pass

