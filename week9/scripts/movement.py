# THIS CODE IS AI GENERATED AND I AM USING IT AS A REFERENCE TO HELP ME FIGURE THINGS OUT
# I DO NOT EXPECT THIS CODE TO WORK BUT IF IT DOES COOL!

#!/usr/bin/python3

import rospy
import math
from people_msgs.msg import People
from geometry_msgs.msg import Twist, Point
import tf2_ros
import tf2_geometry_msgs

class GroupFollower:
    def __init__(self):
        self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
        self.sub = rospy.Subscriber("/robot_0/detected_groups", People, self.people_callback)
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer)
        self.target_position = None
        rospy.sleep(rospy.Duration.from_sec(0.5))

    def people_callback(self, msg):
        people = msg.people
        if not people:
            return

        group_type = people[0].name.split('_')[0]
        if group_type == "circle":
            self.target_position = self.calculate_circle_center(people)
        elif group_type == "line":
            self.target_position = self.calculate_line_end(people)

    def calculate_circle_center(self, people):
        x = sum(person.position.x for person in people) / len(people)
        y = sum(person.position.y for person in people) / len(people)
        return Point(x, y, 0)

    def calculate_line_end(self, people):
        return people[-1].position

    def move_to_target(self):
        if self.target_position is None:
            return

        t = Twist()
        try:
            trans = self.tf_buffer.lookup_transform('base_link', 'map', rospy.Time(0))
            target_transformed = tf2_geometry_msgs.do_transform_point(self.target_position, trans)
            distance = math.sqrt(target_transformed.point.x**2 + target_transformed.point.y**2)
            angle = math.atan2(target_transformed.point.y, target_transformed.point.x)

            if distance > 0.1:
                t.linear.x = 0.5 * distance
                t.angular.z = 0.5 * angle
            else:
                t.linear.x = 0.0
                t.angular.z = 0.0

            self.pub.publish(t)
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            pass

if __name__ == '__main__':
    rospy.init_node('group_follower')
    gf = GroupFollower()
    rate = rospy.Rate(10.0)

    while not rospy.is_shutdown():
        gf.move_to_target()
        rate.sleep()
