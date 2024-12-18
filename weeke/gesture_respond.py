#!/usr/bin/python3
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import JointState
import math

class GestureResponder:
    def __init__(self):
        rospy.init_node('gesture_responder', anonymous=True)
        self.pub = rospy.Publisher('joint_states', JointState, queue_size=10)
        rospy.Subscriber('speech_recognition', String, self.gesture_callback)
        self.js = JointState()
        self.rate = rospy.Rate(1)
        rospy.spin()

    def gesture_callback(self, data):
        command = data.data.lower()
        if command in ['hi', 'hello']:
            self.wave()
        elif command == 'yes':
            self.nod()
        elif command == 'no':
            self.shake_head()

    def initialize(self):
        self.js.header.stamp = rospy.get_rostime()
        self.js.header.frame_id = "Torso"
        self.js.name = ["HeadYaw", "HeadPitch", "LHipYawPitch", "LHipRoll", "LHipPitch", "LKneePitch", "LAnklePitch", "LAnkleRoll", "RHipRoll", "RHipPitch", "RKneePitch", "RAnklePitch", "RAnkleRoll", "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw", "LHand", "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand"]
        self.js.position = [0] * len(self.js.name)

    def head(self, pitch, yaw):
        self.js.position[self.js.name.index("HeadPitch")] = math.radians(pitch)
        self.js.position[self.js.name.index("HeadYaw")] = math.radians(yaw)
        self.rate.sleep()
        self.pub.publish(self.js)
        self.initialize()

    def rArm(self, pitch, roll):
        self.js.position[self.js.name.index("RShoulderPitch")] = math.radians(pitch)
        self.js.position[self.js.name.index("RShoulderRoll")] = math.radians(roll)
        self.rate.sleep()
        self.pub.publish(self.js)
        self.initialize()

    def wave(self):
        self.initialize()
        self.rArm(0, 0)
        self.rArm(85, 0)
        self.rArm(-85, -85)
        self.rArm(-45, -45)
        self.rArm(-85, -85)
        self.rArm(-45, -45)
        self.rArm(0, 0)

    def nod(self):
        self.initialize()
        self.head(0, 0)
        self.head(-10, 0)
        self.head(-30, 0)
        self.head(-60, 0)
        self.head(-90, 0)
        self.head(-60, 0)
        self.head(-30, 0)
        self.head(-10, 0)
        self.head(0, 0)

    def shake_head(self):
        self.initialize()
        self.head(0, -45)
        self.head(0, 45)
        self.head(0, -45)
        self.head(0, 45)
        self.head(0, 0)

if __name__ == '__main__':
    GestureResponder()
