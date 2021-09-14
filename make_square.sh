#!/bin/bash

linear_velocity=$(rostopic echo -n 1 /myturtle/turtle1/speed | grep data| cut -d" " -f2)
echo $linear_velocity
rostopic pub -1 /myturtle/turtle1/cmd_vel geometry_msgs/Twist -- '['$linear_velocity', 0.0, 0.0]' '[0.0, 0.0, 0.0]'
rostopic pub -1 /myturtle/turtle1/cmd_vel geometry_msgs/Twist -- '[0.0, 0.0, 0.0]' '[0.0, 0.0, 1.55]'
rostopic pub -1 /myturtle/turtle1/cmd_vel geometry_msgs/Twist -- '['$linear_velocity', 0.0, 0.0]' '[0.0, 0.0, 0.0]'
rostopic pub -1 /myturtle/turtle1/cmd_vel geometry_msgs/Twist -- '[0.0, 0.0, 0.0]' '[0.0, 0.0, 1.55]'
rostopic pub -1 /myturtle/turtle1/cmd_vel geometry_msgs/Twist -- '['$linear_velocity', 0.0, 0.0]' '[0.0, 0.0, 0.0]'
rostopic pub -1 /myturtle/turtle1/cmd_vel geometry_msgs/Twist -- '[0.0, 0.0, 0.0]' '[0.0, 0.0, 1.55]'
rostopic pub -1 /myturtle/turtle1/cmd_vel geometry_msgs/Twist -- '['$linear_velocity', 0.0, 0.0]' '[0.0, 0.0, 0.0]'
rostopic pub -1 /myturtle/turtle1/cmd_vel geometry_msgs/Twist -- '[0.0, 0.0, 0.0]' '[0.0, 0.0, 1.55]'



