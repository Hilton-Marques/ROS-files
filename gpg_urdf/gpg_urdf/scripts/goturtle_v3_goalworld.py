#!/usr/bin/env python

import rospy, tf2_ros

from math import atan2, hypot
from geometry_msgs.msg import Pose2D,Twist
from tf2_geometry_msgs import PointStamped

def goalcallback(msg):
    global goalstamped

    goalstamped = PointStamped()
    goalstamped.header.stamp = rospy.Time.now()
    goalstamped.header.frame_id = "world"
    goalstamped.point.x = msg.x
    goalstamped.point.y = msg.y
    goalstamped.point.z = 0.0

#def goalfromturtleframe(msg):
#    global goalturtle
#    goalturtle = PointStamped()
#    goalturtle.header.stamp = rospy.Time.now()
#    goalturtle.header.frame_id = "turtle1"
#    goalturtle.point.x = msg.x
#    goalturtle.point.y = msg.y
#    goalturtle.point.z = 0.0
    
if __name__ == '__main__':
    try:
        rospy.init_node('movegopigo', anonymous=True)
        rospy.Subscriber('/gopigo_goal', Pose2D , goalcallback)
        #rospy.Subscriber('turtlecontrol/goal', Pose2D , goalfromturtleframe)
        rospy.wait_for_message('/gopigo_goal', Pose2D)
        turtle_vel = rospy.Publisher('/gpg/mobile_base_controller/cmd_vel', Twist , queue_size=2)

        rate = rospy.Rate(50)

        tfBuffer = tf2_ros.Buffer()
        listener = tf2_ros.TransformListener(tfBuffer)

        while not rospy.is_shutdown():

            try:
                #goalstamped = tfBuffer.transform(goalturtle,'world')
                trans = tfBuffer.transform(goalstamped,'gopigo')
            except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
                rate.sleep()
                continue
            
            rate.sleep()

            lvelocity=0.8*hypot(trans.point.x,trans.point.y)
            avelocity=1.5*atan2(trans.point.y,trans.point.x)

            velmsg = Twist()
            velmsg.linear.x = lvelocity
            velmsg.linear.y = 0
            velmsg.linear.z = 0
            velmsg.angular.x = 0
            velmsg.angular.y = 0
            velmsg.angular.z = avelocity

            turtle_vel.publish(velmsg)

        rospy.logwarn('goturtle encerrando')         
        print('Done')
    except rospy.ROSInterruptException:
        pass
