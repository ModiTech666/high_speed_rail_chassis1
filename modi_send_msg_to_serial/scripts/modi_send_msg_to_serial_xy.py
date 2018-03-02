#!/usr/bin/env python
# license removed for brevity
import re
import rospy
from std_msgs.msg import String

def talker(n):
	pub = rospy.Publisher('write', String, queue_size=10)
	#rospy.init_node('talker', anonymous=True)
	rate = rospy.Rate(10) # 10hz
	if not rospy.is_shutdown():
	#while not rospy.is_shutdown():

		filename1 = r"/home/cx/catkin_ws/src/modi_send_msg_to_serial/scripts/output.txt"
		move_z1='DS 0,0,20\r\n'
		move_z2="DS 0,0,-20\r\n"
		rotate51="DJ 6,30\r\n"
		rotate50="DJ 6,-30\r\n"
		result=[]
		result_float=[]
		result_float2=[]
		result_str=[]
		fhand = open(filename1)
		startpos1 = 0
		stoppos1 = 0
		n = int(n)
		for lines in fhand:
			if lines.lstrip().startswith("model_id:"):
				startpos1 = startpos1 + 1
			if startpos1 == n:
				if lines.lstrip().startswith("positions:"):
				    result.append(re.findall(r"-?\d+\.?\d+e?-?\d*",lines))
			if lines.lstrip().startswith("is_diff:"):
				stoppos1 = stoppos1 + 1
			if stoppos1 == n:
				break
		fhand.close()
		print stoppos1
		#change to float
		for k in range(len(result)):
		    result_float.append(map(float,result[k]))		
		for l in range(2):
			RS_str = "RS"+"\r\n"
			rospy.loginfo(RS_str)
			pub.publish(RS_str)
			rospy.sleep(1)
		for k in range(len(result_float)-1):
			temp=[]
			for i in range(len(result_float[k])):
				temp.append(result_float[k+1][i]-result_float[k][i])
			result_float2.append(temp)
		for i in range(len(result_float2)):
		    temp=['MJ ']
		    for j in range(1,len(result_float2[i])-1):
		    	if j > 3:
		    		if j == 4:
		    			temp.append(str(round(-result_float2[i][j+1]*180/3.1415927,2)))
		    		else:
		        		temp.append(str(round(result_float2[i][j+1]*180/3.1415927,2)))
		        	temp.append(',')
		        else:
		        	temp.append(str(round(result_float2[i][j]*180/3.1415927,2)))
		        	temp.append(',')
		    temp.pop()  	
		    result_str.append(''.join(temp))
		for i in range(len(result_str)):
			rospy.loginfo(str(result_str[i])+"\r\n")
			pub.publish(str(result_str[i])+"\r\n")
			rospy.sleep(1)
		
		rospy.loginfo(move_z1)
		pub.publish(move_z1)

		rospy.sleep(1)
		rospy.loginfo(rotate51)
		pub.publish(rotate51)		

		rospy.sleep(1)
		rospy.loginfo(move_z2)
		pub.publish(move_z2)

		rospy.sleep(1)
		rospy.loginfo(rotate50)
		pub.publish(rotate50)

		rospy.sleep(1)

		rate.sleep()

if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass
