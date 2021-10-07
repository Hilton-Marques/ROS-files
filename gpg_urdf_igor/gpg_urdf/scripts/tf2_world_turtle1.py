#!/usr/bin/env python  
import rospy

# Because of transformations
import tf_conversions

import tf2_ros
import geometry_msgs.msg
from turtlesim.msg import Pose

def handle_pose(msg):
    br = tf2_ros.TransformBroadcaster()
    t = geometry_msgs.msg.TransformStamped()

    t.header.stamp = rospy.Time.now()
    t.header.frame_id = "world"
    t.child_frame_id = "gopigo"
    t.transform.translation.x = msg.pose.position.x
    t.transform.translation.y = msg.pose.position.y
    t.transform.translation.z = msg.pose.position.z
    t.transform.rotation.x = msg.pose.orientation.x
    t.transform.rotation.y = msg.pose.orientation.y
    t.transform.rotation.z = msg.pose.orientation.z
    t.transform.rotation.w = msg.pose.orientation.w

    br.sendTransform(t)

if __name__ == '__main__':
    rospy.init_node('tf2_turtle_broadcaster')
    rospy.Subscriber('/gopigo_pose', geometry_msgs.msg.PoseStamped , handle_pose)
    rate = rospy.Rate(50)
    while not rospy.is_shutdown():
        rate.sleep()
        #print('test')
    