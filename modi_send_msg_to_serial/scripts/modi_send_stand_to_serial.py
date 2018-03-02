#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String

def talker():
	pub = rospy.Publisher('write', String, queue_size=10)
	rospy.init_node('talker', anonymous=True)
	rate = rospy.Rate(10) # 10hz
	if not rospy.is_shutdown():
	#while not rospy.is_shutdown():
		for l in range(4):
			RS_str = "RS "+"\r\n"
			rospy.loginfo(RS_str)
			pub.publish(RS_str)
			rospy.sleep(3)

		OG_str = "OG "+"\r\n"
		rospy.loginfo(OG_str)
		pub.publish(OG_str)
		rospy.sleep(3)
		stand_str = "MJ 0,0,-90,0,0 "+"\r\n"
		rospy.loginfo(stand_str)
		pub.publish(stand_str)
		rospy.sleep(4)
		# stand_str = "DJ 4,30 "+"\r\n"
		# rospy.loginfo(stand_str)
		# pub.publish(stand_str)
		# rospy.sleep(4)


		#hello_str = "hello world %s" % rospy.get_time()
		#rospy.loginfo(hello_str)
		#pub.publish(hello_str)
		rate.sleep()

if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass
