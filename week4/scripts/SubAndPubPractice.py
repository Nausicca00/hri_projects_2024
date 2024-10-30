#!/usr/bin/python3

import rospy
from sensor_msgs.msg import JointState

class SubandPub:
    def __init__(self):
        rospy.init_node('repub_joint_states', anonymous=True)
        self.pub = rospy.Publisher('joint_states', JointState, queue_size=10)

    def callback(self, data):
        # Publish the received data to 'joint_states'
        self.pub.publish(data)
        rospy.loginfo(f"Republished joint state: {data}")

    def repub_joint_states(self):
        rospy.Subscriber('joint_states_input', JointState, self.callback)
        rospy.spin()

if __name__ == '__main__':
    test = SubandPub()
    test.repub_joint_states()
