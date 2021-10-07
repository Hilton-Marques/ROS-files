#!/usr/bin/env python  
from sys import flags
import rospy

from math import atan2, hypot
import tf2_ros
from geometry_msgs.msg import Twist,Pose2D
from tf2_geometry_msgs import PointStamped
import turtlesim.srv

goal = None

def GetGoal(msg):
    global goal
    #goal_pose = rospy.wait_for_message("/goal", Pose2D)
    goal = PointStamped()
    goal.header.stamp = rospy.Time()
    goal.header.frame_id = "world" #turtle1
    goal.point.x = msg.x
    goal.point.y = msg.y
    goal.point.z = 0.0    #return goal_stamped
    
    #goal = tfBuffer.transform(goal, 'world')
    #goal.header.stamp = rospy.Time()
if __name__ == '__main__':
    rospy.init_node('move2goal')
    rospy.Subscriber('/goal',Pose2D, GetGoal)
    tfBuffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfBuffer)
    rate = rospy.Rate(10.0)
    pub = rospy.Publisher('/turtle1/cmd_vel' ,Twist, queue_size=100)  
    while (not rospy.is_shutdown()):
        #print('try1')
        if (goal == None):
            rate.sleep()
            continue
        try:
	    if (goal == None):
            	print('entrei')
            trans = tfBuffer.transform(goal, 'turtle1')
            #print(trans)
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            rate.sleep()
            continue
        rate.sleep()
        sent_msg = Twist()
        norm = hypot(trans.point.x, trans.point.y)
        angle = atan2(trans.point.y, trans.point.x)   
        sent_msg.linear.x = 0.5*norm
        sent_msg.linear.y = 0
        sent_msg.linear.z = 0

        sent_msg.angular.z = 1.5*angle
        sent_msg.angular.x = 0
        sent_msg.angular.y = 0

        pub.publish(sent_msg)
        if (norm < 0.01):
            goal = None
            rospy.logwarn("objetivo atingido")


