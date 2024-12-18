#!/usr/bin/python3
import rospy
from std_msgs.msg import String
import math

class TTSListener:
    def __init__(self):
        rospy.init_node('tts_listener', anonymous=True)
        self.pub = rospy.Publisher('tts/phrase', String, queue_size=10)
        self.gesture_pub = rospy.Publisher('joint_states', JointState, queue_size=10)
        rospy.Subscriber('tts_input', String, self.tts_callback)
        self.js = JointState()
        self.rate = rospy.Rate(1)
        rospy.spin()

    def tts_callback(self, data):
        phrase = data.data.lower()
        if 'hello' in phrase:
            self.wave()
            self.nod_or_shake(phrase)
        
        self.pub.publish(data.data)

    def initialize(self):
        self.js.header.stamp = rospy.get_rostime()
        self.js.header.frame_id = "Torso"
        self.js.name = ["HeadYaw", "HeadPitch", "LHipYawPitch", "LHipRoll", "LHipPitch", "LKneePitch", "LAnklePitch", "LAnkleRoll", "RHipRoll", "RHipPitch", "RKneePitch", "RAnklePitch", "RAnkleRoll", "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw", "LHand", "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand"]
        self.js.position = [0] * len(self.js.name)

    def head(self, pitch, yaw):
        self.js.position[self.js.name.index("HeadPitch")] = math.radians(pitch)
        self.js.position[self.js.name.index("HeadYaw")] = math.radians(yaw)
        self.rate.sleep()
        self.gesture_pub.publish(self.js)
        self.initialize()

    def rArm(self, pitch, roll):
        self.js.position[self.js.name.index("RShoulderPitch")] = math.radians(pitch)
        self.js.position[self.js.name.index("RShoulderRoll")] = math.radians(roll)
        self.rate.sleep()
        self.gesture_pub.publish(self.js)
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

    def nod_or_shake(self, phrase):
        if 'yes' in phrase:
            self.nod()
        elif 'no' in phrase:
            self.shake_head()

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
    TTSListener()
