#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sys
import os
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from std_msgs.msg import String


sys.path.append("/home/cx/catkin_ws/src/modi_send_msg_to_serial/scripts")
from modi_send_msg_to_serial_xy import talker
from modi_send_OG_to_serial import send_OG
from geometry_msgs.msg import Pose, PoseStamped
sys.path.append("/opt/ros/kinetic/lib/python2.7/dist-packages/moveit_commander")
from planning_scene_interface import PlanningSceneInterface

maxnum = 1000
def move_group_python_interface_tutorial():
  ## First initialize moveit_commander and rospy.
  print "============ Starting tutorial setup"
  moveit_commander.roscpp_initialize(sys.argv)
  rospy.init_node('move_group_python_interface_tutorial',
                  anonymous=True)
  robot = moveit_commander.RobotCommander()
  scene = moveit_commander.PlanningSceneInterface()
  group = moveit_commander.MoveGroupCommander("arm")
  ## Wait for RVIZ to initialize. This sleep is ONLY to allow Rviz to come up.
  print "============ Waiting for RVIZ..."
  rospy.sleep(1)
  print "============ Starting tutorial "
  print "============ Reference frame: %s" % group.get_planning_frame()
  print "============ End effector: %s" % group.get_end_effector_link()
  print "============ Robot Groups:"
  print robot.get_group_names()
  print "============ Printing robot state"
  print robot.get_current_state()
  send_OG()
  print "add plane"
  pose = PoseStamped()
  pose.pose.position.x = 0
  pose.pose.position.y = 0
  # offset such that the box is 0.1 mm below ground (to prevent collision with the robot itself)
  pose.pose.position.z = 0.85
  pose.pose.orientation.x = 0
  pose.pose.orientation.y = 0
  pose.pose.orientation.z = 0
  pose.pose.orientation.w = 1
  pose.header.stamp = rospy.get_rostime()
  pose.header.frame_id = '/base_link'
  plane_plan=PlanningSceneInterface()
  plane_plan.add_box('modi_plane',pose,size = (3, 3, 0.001))

  print "============ Generating plan 1"

  filepos = r"/home/cx/catkin_ws/src/modi_send_msg_to_serial/scripts/txt/"
  for i in range(1,maxnum):
    print '----------------------this is %d.txt' % i
    name = str(i)+".txt"
    filename = filepos + name
    flag = 0
    while(flag == 0):
      try:
        fhand = open(filename)
      except:
        pass
      else:
        result=[]
        for lines in fhand:
        	result.append(map(float,lines.split()))
        for k in range(len(result)):
          pose_target = geometry_msgs.msg.Pose()
          pose_target.orientation.x = -0.707113964363
          pose_target.orientation.y = 1.62052989438e-05
          pose_target.orientation.z = -1.61064322027e-05
          pose_target.orientation.w = 0.707099597568
          pose_target.position.x = result[k][0]
          pose_target.position.y = result[k][1]
          pose_target.position.z = 0.71
          group.set_pose_target(pose_target)
          plan1 = group.plan()
          group.execute(plan1)
          #group.go(wait=True)
        fhand.close()
        os.remove(filename)
        flag = 1
        rospy.sleep(1)
        print "============ STOPPING"
        try:
          talker(i)
        except rospy.ROSInterruptException:
          pass
 


if __name__=='__main__':
  try:
    move_group_python_interface_tutorial()
  except rospy.ROSInterruptException:
  	pass