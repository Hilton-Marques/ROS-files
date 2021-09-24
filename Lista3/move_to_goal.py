#! /usr/bin/env python
import rospy
import math
from geometry_msgs.msg import Twist,Pose2D
from turtlesim.msg import Pose

def GetGoal():   
    global goal_pose, init_pose, max_dist
    goal_pose = rospy.wait_for_message("/goal", Pose2D)
    init_pose = rospy.wait_for_message("turtle1/pose", Pose) 
    max_dist = GetDist2Goal()
def GetDist2Goal():
    #global current_pose
    current_pose = rospy.wait_for_message("turtle1/pose", Pose)   
    dir_vector = [(goal_pose.x - current_pose.x),(goal_pose.y - current_pose.y)]
    dist = math.sqrt(dir_vector[1]*dir_vector[1] + dir_vector[0]*dir_vector[0])
    return dist
def GetAngle2Goal():
    ###global current_pose
    current_pose = rospy.wait_for_message("turtle1/pose", Pose)   
    dir_vector = [(goal_pose.x - current_pose.x),(goal_pose.y - current_pose.y)]
    angle = math.atan2(dir_vector[1],dir_vector[0])
    angle_dif = angle - current_pose.theta 
    return angle_dif
def SendVel(xlinear_vel, angular_vel,const ):
    sent_msg = Twist()
    sent_msg.linear.x = const*xlinear_vel
    sent_msg.linear.y = 0
    sent_msg.linear.z = 0
    sent_msg.angular.z = angular_vel
    sent_msg.angular.x = 0
    sent_msg.angular.y = 0
    pub.publish(sent_msg)
def GetSignedDist():
    current_pose = rospy.wait_for_message("turtle1/pose", Pose)  
    dir_vector = [(current_pose.x - init_pose.x),(current_pose.y - init_pose.y)]
    dist = math.sqrt(dir_vector[1]*dir_vector[1] + dir_vector[0]*dir_vector[0])
    return max_dist - dist
def Move2Goal():
    dist = GetDist2Goal()
    angle_dif = GetAngle2Goal()
    print(angle_dif)
    print(dist)
    rate = rospy.Rate(0.25)
    while ((dist) > 0.01):
        #pub.publish(sent_msg)
        SendVel(dist,angle_dif,0.5)         
        dist = GetDist2Goal()
        angle_dif = GetAngle2Goal()
        print(dist)
        rate.sleep()
def Move2Goal_2():
    dist = GetSignedDist()
    angle_dif = GetAngle2Goal()
    print(abs(angle_dif))
    print(dist)
    rate = rospy.Rate(2)
    while (abs(angle_dif) > 0.01):
        #pub.publish(sent_msg)
        print('hello')
        SendVel(0,angle_dif,0.5)
        print('world')
        angle_dif = GetAngle2Goal()   
        print(angle_dif)     
        #rospy.sleep(5)
        #rate.sleep()
    rate = rospy.Rate(2)
    while (abs(dist) > 0.01):
        #pub.publish(sent_msg)
        SendVel(dist,0,0.5)
        dist = GetSignedDist() 
        print(dist)      
        #rate.sleep()


if __name__ == "__main__":
    rospy.init_node('turtle_control',anonymous=True) 
    global pub
    pub = rospy.Publisher('/turtle1/cmd_vel',Twist, queue_size=100) 
    GetGoal()
    #Move2Goal()
    Move2Goal_2()