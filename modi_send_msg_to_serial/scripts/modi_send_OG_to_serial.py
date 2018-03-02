#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String

def send_OG():
	pub = rospy.Publisher('write', String, queue_size=10)
	#rospy.init_node('send_OG', anonymous=True)
	rate = rospy.Rate(10) # 10hz
	if not rospy.is_shutdown():
	#while not rospy.is_shutdown():
		for l in range(4):
			RS_str = "RS "+"\r\n"
			rospy.loginfo(RS_str)
			pub.publish(RS_str)
			rospy.sleep(1)
		OG_str = "OG "+"\r\n"
		rospy.loginfo(OG_str)
		pub.publish(OG_str)
		rospy.sleep(1)
		rate.sleep()

if __name__ == '__main__':
	try:
		send_OG()
	except rospy.ROSInterruptException:
		pass
