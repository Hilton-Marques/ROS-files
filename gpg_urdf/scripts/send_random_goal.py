#! /usr/bin/env python
import rospy
import sys

from random import seed
from random import random
import math
from geometry_msgs.msg import Pose2D
from rospy.core import is_shutdown
from geometry_msgs.msg import PoseStamped

dist = None
goal_pose = None
current_pose = None
def GetDist2Goal():
    #global current_pose
    global dist, goal_pose
    dir_vector = [(goal_pose.x - current_pose[0]),(goal_pose.y - current_pose[1])]
    dist = math.sqrt(dir_vector[1]*dir_vector[1] + dir_vector[0]*dir_vector[0])
    return dist
def GetCurrentPose(msg):
    #global current_pose
    global current_pose
    current_pose = [msg.pose.position.x ,msg.pose.position.y]
def GenerateRandomPose():
    seed(1)  
    global goal_pose
    goal_pose = Pose2D()
    #goal_pose.x = 11*random()
    goal_pose.x = 2
    #goal_pose.y = 11*random()
    goal_pose.y = 2
def SendGoal():
    rospy.init_node('send_goal',anonymous=True)
    pub = rospy.Publisher('/gpg_goal',Pose2D, queue_size=10)
    state_subscriber = rospy.Subscriber('/robot_pose', PoseStamped, GetCurrentPose)
    rate = rospy.Rate(10)
    while (not rospy.is_shutdown()): 
        GenerateRandomPose()  
        pub.publish(goal_pose)
        if current_pose == None:
            continue
        diff = GetDist2Goal()
        if (diff < 0.01):
            GenerateRandomPose()  
        rate.sleep()


if __name__ == "__main__":
    try:
        SendGoal()
    except rospy.ROSInterruptException:
        pass
