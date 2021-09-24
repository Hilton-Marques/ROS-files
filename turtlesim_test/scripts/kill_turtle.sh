#!/bin/bash
turtle_name=$(rostopic list | grep turtle | uniq -f2 |cut -d/ -f3)
rosservice call  /myturtle/kill $turtle_name

