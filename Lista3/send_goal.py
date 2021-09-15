#! /usr/bin/env python
import rospy
import sys

from geometry_msgs.msg import Pose2D
from rospy.core import is_shutdown

def SendGoal(x,y):
    pub = rospy.Publisher('goal',Pose2D, queue_size=10)
    rospy.init_node('send_goal',anonymous=True)
    rate = rospy.Rate(10)
    while (not rospy.is_shutdown()):
        sent_msg = Pose2D()
        sent_msg.x = x
        sent_msg.y = y
        pub.publish(sent_msg)
        rate.sleep


if __name__ == "__main__":
    if len(sys.argv) == 3:
        x = float(sys.argv[1])
        y = float(sys.argv[2])
    else:
        print('falha na entrada')
        sys.exit(1)
    try:
        SendGoal(x,y)
    except rospy.ROSInterruptException:
        pass