#! /usr/bin/env python
import rospy
import sys

from random import seed
from random import random
import math
from geometry_msgs.msg import Pose2D
from rospy.core import is_shutdown
from turtlesim.msg import Pose

def GetDist2Goal():
    #global current_pose
    current_pose = rospy.wait_for_message("/turtle1/pose", Pose) 
    dir_vector = [(goal_pose.x - current_pose.x),(goal_pose.y - current_pose.y)]
    dist = math.sqrt(dir_vector[1]*dir_vector[1] + dir_vector[0]*dir_vector[0])
    return dist
def SendGoal():
    global goal_pose
    seed(1)  
    pub = rospy.Publisher('goal',Pose2D, queue_size=10)
    rospy.init_node('send_goal',anonymous=True)
    rate = rospy.Rate(10)
    while (not rospy.is_shutdown()):   
        goal_pose = Pose2D()
        goal_pose.x = 11*random()
        goal_pose.y = 11*random()
        print("Posicao objetivo:")
        print(goal_pose)
        diff = GetDist2Goal()
        
        while (diff > 0.01):
            pub.publish(goal_pose)
            diff = GetDist2Goal()
            rate.sleep()


if __name__ == "__main__":
    try:
        SendGoal()
    except rospy.ROSInterruptException:
        pass
