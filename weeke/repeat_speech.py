#!/usr/bin/python3
import rospy
from std_msgs.msg import String

class SpeechRepeater:
    def __init__(self):
        rospy.init_node('speech_repeater', anonymous=True)
        self.pub = rospy.Publisher('tts/phrase', String, queue_size=10)
        rospy.Subscriber('speech_recognition', String, self.callback)
        rospy.spin()

    def callback(self, data):
        rospy.loginfo(f"I heard: {data.data}")
        self.pub.publish(data.data)

if __name__ == '__main__':
    SpeechRepeater()
