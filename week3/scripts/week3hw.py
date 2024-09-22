#!/usr/bin/python3
# license removed for brevity
import rospy
import math

from sensor_msgs.msg import JointState

def initialize(js):
    js.header.stamp = rospy.get_rostime()
    js.header.frame_id = "Torso"
    
    js.name.append("HeadYaw")
    js.name.append("HeadPitch")
    js.name.append("LHipYawPitch")
    js.name.append("LHipRoll")
    js.name.append("LHipPitch")
    js.name.append("LKneePitch")
    js.name.append("LAnklePitch")
    js.name.append("LAnkleRoll")
    js.name.append("RHipRoll")
    js.name.append("RHipPitch")
    js.name.append("RKneePitch")
    js.name.append("RAnklePitch")
    js.name.append("RAnkleRoll")
    js.name.append("LShoulderPitch")
    js.name.append("LShoulderRoll")
    js.name.append("LElbowYaw")
    js.name.append("LElbowRoll")
    js.name.append("LWristYaw")
    js.name.append("LHand")
    js.name.append("RShoulderPitch")
    js.name.append("RShoulderRoll")
    js.name.append("RElbowYaw")
    js.name.append("RElbowRoll")
    js.name.append("RWristYaw")
    js.name.append("RHand")
    
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    js.position.append(0)
    
def head(pub, js, rate, pitch, yaw):
    js.position[js.name.index("HeadPitch")] = math.radians(pitch)
    js.position[js.name.index("HeadYaw")] = math.radians(yaw)
    rate.sleep()
    pub.publish(js)
    initialize(js)
    
def rArm(pub, js, rate, pitch, roll):
    js.position[js.name.index("RShoulderPitch")] = math.radians(pitch)
    js.position[js.name.index("RShoulderRoll")] = math.radians(roll)
    rate.sleep()
    pub.publish(js)
    initialize(js)
    
def moveHead(pub, js, rate):
    initialize(js)
    head(pub, js, rate, 0, 0)
    head(pub, js, rate, -10, 0)
    head(pub, js, rate, -30, 0)
    head(pub, js, rate, -60, 0)
    head(pub, js, rate, -90, 0)
    head(pub, js, rate, -60, 0)
    head(pub, js, rate, -30, 0)
    head(pub, js, rate, -10, 0)
    head(pub, js, rate, 0, 0)
    head(pub, js, rate, 10, 0)
    head(pub, js, rate, 30, 0)
    head(pub, js, rate, 60, 0)
    head(pub, js, rate, 90, 0)
    head(pub, js, rate, 60, 0)
    head(pub, js, rate, 30, 0)
    head(pub, js, rate, 10, 0)
    head(pub, js, rate, 0, 0)
    
    head(pub, js, rate, 0, -45)
    head(pub, js, rate, 0, 45)
    head(pub, js, rate, 0, -45)
    head(pub, js, rate, 0, 45)
    head(pub, js, rate, 0, 0)
    
def moveRArm(pub, js, rate):
    initialize(js)
    rArm(pub, js, rate, 0, 0)
    rArm(pub, js, rate, 85, 0)
    rArm(pub, js, rate, -85, -85)
    rArm(pub, js, rate, -45, -45)
    rArm(pub, js, rate, -85, -85)
    rArm(pub, js, rate, -45, -45)
    rArm(pub, js, rate, 0, 0)
    
def talker(pub, js, rate):
    rate.sleep()
    rospy.loginfo(js)
    pub.publish(js)

if __name__ == '__main__':
    pub = rospy.Publisher('joint_states', JointState, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(1) # 10hz
    #hello_str = "hello world %s" % rospy.get_time()
    js = JointState()

    try:
        moveRArm(pub, js, rate)
        moveHead(pub, js, rate)
    except rospy.ROSInterruptException:
        pass
