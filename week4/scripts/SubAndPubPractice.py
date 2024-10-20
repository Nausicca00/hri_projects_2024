#!/usr/bin/python3

import rospy
from sensor_msgs.msg import JointState

def callback(data):
    # Initialize publisher inside the callback to avoid repetitive initialization
    pub = rospy.Publisher('joint_states', JointState, queue_size=10)
    # Publish the received data to 'joint_states'
    pub.publish(data)
    rospy.loginfo(f"Republished joint state: {data}")

def repub_joint_states():
    rospy.init_node('repub_joint_states', anonymous=True)
    rospy.Subscriber('joint_state_input', JointState, callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        repub_joint_states()
    except rospy.ROSInterruptException:
        pass
