# THIS CODE IS AI GENERATED AND I AM USING IT AS A REFERENCE TO HELP ME FIGURE THINGS OUT
# I DO NOT EXPECT THIS CODE TO WORK BUT IF IT DOES COOL!

#!/usr/bin/python3

import rospy
from people_msgs.msg import People, Person
from geometry_msgs.msg import Point
import math

class GroupDetector:
    def __init__(self):
        self.pub = rospy.Publisher("/robot_0/detected_groups", People, queue_size=10)
        self.sub = rospy.Subscriber("/people", People, self.people_callback)
        rospy.sleep(rospy.Duration.from_sec(0.5))

    def people_callback(self, msg):
        people = msg.people
        if len(people) < 3:
            return

        # Check if people are in a line
        if self.are_people_in_line(people):
            group_name = "line"
        elif self.are_people_in_circle(people):
            group_name = "circle"
        else:
            group_name = "group"

        # Update names and publish
        for i, person in enumerate(people):
            person.name = f"{group_name}_{i+1}_{person.name}"
        msg.people = people
        self.pub.publish(msg)

    def are_people_in_line(self, people):
        if len(people) < 3:
            return False
        p1 = people[0].position
        p2 = people[1].position
        for person in people[2:]:
            p = person.position
            if not self.is_point_on_line(p1, p2, p):
                return False
        return True

    def is_point_on_line(self, p1, p2, p):
        # Check if point p is on the line defined by points p1 and p2
        return abs((p.y - p1.y) * (p2.x - p1.x) - (p2.y - p1.y) * (p.x - p1.x)) < 0.1

    def are_people_in_circle(self, people):
        if len(people) < 3:
            return False
        center = self.calculate_circle_center(people)
        radius = self.calculate_distance(center, people[0].position)
        for person in people:
            if abs(self.calculate_distance(center, person.position) - radius) > 0.1:
                return False
        return True

    def calculate_circle_center(self, people):
        # Simple average of positions as an approximation
        x = sum(person.position.x for person in people) / len(people)
        y = sum(person.position.y for person in people) / len(people)
        return Point(x, y, 0)

    def calculate_distance(self, p1, p2):
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

if __name__ == '__main__':
    rospy.init_node('group_detector')
    gd = GroupDetector()
    rospy.spin()
