#! /usr/bin/env python
import rospy
import math
from geometry_msgs.msg import Twist,Pose2D
from turtlesim.msg import Pose

def GetGoal():   
    global goal_pose, init_pose, max_dist
    goal_pose = rospy.wait_for_message("/goal", Pose2D)
    init_pose = rospy.wait_for_message("/turtle1/pose", Pose) 
    max_dist = GetDist2Goal()
def GetDist2Goal():
    #global current_pose
    current_pose = rospy.wait_for_message("/turtle1/pose", Pose)   
    dir_vector = [(goal_pose.x - current_pose.x),(goal_pose.y - current_pose.y)]
    dist = math.sqrt(dir_vector[1]*dir_vector[1] + dir_vector[0]*dir_vector[0])
    return dist
def GetAngle2Goal():
    ###global current_pose
    current_pose = rospy.wait_for_message("/turtle1/pose", Pose)   
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
    current_pose = rospy.wait_for_message("/turtle1/pose", Pose)  
    dir_vector = [(current_pose.x - init_pose.x),(current_pose.y - init_pose.y)]
    dist = math.sqrt(dir_vector[1]*dir_vector[1] + dir_vector[0]*dir_vector[0])
    return max_dist - dist
def Move2Goal():
    rospy.init_node('move2goal',anonymous=True) 
    global pub
    pub = rospy.Publisher('/turtle1/cmd_vel',Twist, queue_size=100) 
    while (not rospy.is_shutdown()):
        GetGoal()
        signedDist = GetSignedDist()
        dist = GetDist2Goal()        
        angle_dif = GetAngle2Goal()
        while (abs(angle_dif) > 0.001):
            SendVel(0,angle_dif,0.5)
            angle_dif = GetAngle2Goal()   
            print("Diferenca angular ate o objetivo:", angle_dif) 
            #rospy.loginfo("Diferenca angular ate o objetivo:%s" % angle_dif)

        while (dist > 0.01):
            #pub.publish(sent_msg)
            SendVel(signedDist,0,0.5)
            signedDist = GetSignedDist() 
            dist = GetDist2Goal()
            print("Diferenca linear ate o objetivo:",dist)   
        rospy.sleep(1)        
        print("Novo objetivo adicionado")


if __name__ == "__main__":    
    try:
        Move2Goal()
    except rospy.ROSInterruptException:
        pass
    
	


