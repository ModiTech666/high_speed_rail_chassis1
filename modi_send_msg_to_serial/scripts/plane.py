#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from std_msgs.msg import String
from geometry_msgs.msg import Pose, PoseStamped
sys.path.append("/opt/ros/kinetic/lib/python2.7/dist-packages/moveit_commander")
from planning_scene_interface import PlanningSceneInterface

print "============ Starting tutorial setup"
moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('plane',
              anonymous=True)
robot = moveit_commander.RobotCommander()
scene = moveit_commander.PlanningSceneInterface()
group = moveit_commander.MoveGroupCommander("arm")
## Wait for RVIZ to initialize. This sleep is ONLY to allow Rviz to come up.
rospy.sleep(1)
print "============ Reference frame: %s" % group.get_planning_frame()
print "============ End effector: %s" % group.get_end_effector_link()
print "============ Robot Groups:"
print robot.get_group_names()
print "============ Printing robot state"
print robot.get_current_state()
print "start"
pose = PoseStamped()
pose.pose.position.x = 0
pose.pose.position.y = 0
# offset such that the box is 0.1 mm below ground (to prevent collision with the robot itself)
pose.pose.position.z = 1
pose.pose.orientation.x = 0
pose.pose.orientation.y = 0
pose.pose.orientation.z = 0
pose.pose.orientation.w = 1
pose.header.stamp = rospy.get_rostime()
pose.header.frame_id = '/base_link'
plane_plan=PlanningSceneInterface()
plane_plan.add_box('modi_plane',pose,size = (3, 3, 0.01))add
print "end"