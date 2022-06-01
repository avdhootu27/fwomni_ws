#!/usr/bin/env python3

import roslib
import rospy
from std_msgs.msg import String
from std_msgs.msg import Header
from geometry_msgs.msg import Pose
from geometry_msgs.msg import PoseStamped
from move_base_msgs.msg import MoveBaseActionResult

path = [
	[[1, 1, 0], [0,0,-0.00421336,0.9999911]],
	[[1, 2, 0], [0,0,-0.00421336,0.9999911]],
	[[1, 3, 0], [0,0,-0.00421336,0.9999911]],
	[[2, 3, 0], [0,0,-0.00421336,0.9999911]],
]

currentGoalStamp = 0

def onCommand(msg):
	if msg.data=="start":
		startPath()
	elif msg.data=="stop":
		rospy.loginfo("Stopping path automation")
		quit()

def onGoalReached(msg):
	global currentGoalStamp
	if msg.status.text=="Goal reached.":
		rospy.loginfo("Path in progress")
		currentGoalStamp += 1
		if currentGoalStamp>=len(path):
			rospy.loginfo("Path complete")
			quit()
		else:
			sendGoal(currentGoalStamp)

def sendGoal(seq_):
	poseStamp_ = PoseStamped()
	header_ = Header()
	pose_ = Pose()

	header_.seq = seq_
	header_.stamp = rospy.Time.now()
	header_.frame_id = "map"

	pose_.position.x = path[seq_][0][0]
	pose_.position.y = path[seq_][0][1]
	pose_.position.z = path[seq_][0][2]
	pose_.orientation.x = path[seq_][1][0]
	pose_.orientation.y = path[seq_][1][1]
	pose_.orientation.z = path[seq_][1][2]
	pose_.orientation.w = path[seq_][1][3]

	poseStamp_.header = header_
	poseStamp_.pose = pose_

	to_move_base.publish(poseStamp_)
	rospy.loginfo("Path in progress")

def startPath():
	rospy.loginfo("Start command received.")
	currentGoalStamp = 0
	sendGoal(0)

if __name__ == '__main__':
	rospy.init_node('automate')
	to_move_base = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=1)
	rospy.Subscriber("/move_base/result", MoveBaseActionResult, onGoalReached)
	rospy.Subscriber("/automate/command", String, onCommand)
	rospy.loginfo("Waiting for start command...")
	rospy.spin()

# rostopic pub /automate/command std_msgs/String "start"