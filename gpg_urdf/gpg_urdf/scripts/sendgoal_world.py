#!/usr/bin/env python

#imports necessários
import rospy

from math import sqrt
from random import seed,random
from geometry_msgs.msg import Pose2D, PoseStamped
from turtlesim.msg import Pose

#inicialização do nó e parâmetros gerais
rospy.init_node('sendgoal', anonymous=True)
rate = rospy.Rate(50)
seed()

def getposecallback(msg):
    global myflag, cur_pose
    cur_pose = (msg.pose.position.x,msg.pose.position.y)
    myflag = False
    #print('getpose done')
  
def getpose():
    global myflag
    #rospy.Subscriber('turtle1/pose', Pose , getposecallback)
    myflag = True
    while myflag and not rospy.is_shutdown():
        rate.sleep()
    #print('getpose')
    return cur_pose

def sendgoal(xgoal,ygoal,pub):
    #pub = rospy.Publisher('turtlecontrol/goal', Pose2D , queue_size=1)
    goal = Pose2D()

    goal.x = xgoal
    goal.y = ygoal
    goal.theta = 0

    count = 1
    while count >= 1:
        pub.publish(goal)
        rate.sleep()
        count = count - 1

if __name__ == '__main__':
    try:
        rospy.Subscriber('/gopigo_pose', PoseStamped , getposecallback)
        pub = rospy.Publisher('/gopigo_goal', Pose2D , queue_size=10)
        distance = 0
        while not rospy.is_shutdown():
            
            if distance <= 0.1:
                currentgoal = (4*random()-2,4*random()-2)
                #print('sending new goal')
                rospy.logwarn('sending new goal') 
            #else:
                #print('waiting for turtle arrival')
                #rospy.logwarn('waiting for gopigo arrival') 
            
            sendgoal(currentgoal[0],currentgoal[1],pub)
            currentpos=getpose()
            distance = sqrt((currentgoal[0]-currentpos[0])**2+(currentgoal[1]-currentpos[1])**2)
            rate.sleep()

        rospy.logwarn('sendgoal encerrando')        
        print('Done')
    except rospy.ROSInterruptException:
        pass
