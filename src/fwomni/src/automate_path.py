#!/usr/bin/env python3

import roslib
import rospy
from std_msgs import String
from geometry_msgs.msg import PoseStamped
from move_base_msgs.msg import MoveBaseActionResult

path = [
	[(1, 1, 0), (0,0,0,0)],
	[(1, 2, 0), (0,0,0,0)],
	[(1, 3, 0), (0,0,0,0)],
	[(2, 3, 0), (0,0,0,0)],
]

keepGoing = false
currentGoalReached = false
currentGoalHeader = Header()

def onCommand(msg):
	if msg.data=="start":
		keepGoing = true
	elif msg.data=="stop":
		keepGoing = false
		rospy.loginfo("Stopping path automation")
		exit()

def onGoalReached(msg):
	if msg.status.text=="Goal reached.":
		if msg.status.goal_id.stamp==currentGoalHeader.stamp:
			currentGoalReached = true
			rospy.loginfo("Path in progress, reached goal "+str(currentGoalHeader.seq))

def sendGoal(seq_):
	poseStamp_ = PoseStamped()
	header_ = Header()
	pose_ = Pose()

	header_.seq = seq_
	header_.stamp = rospy.Time.now()
	header_.frame_id = "map"

	pose_.position = path[seq_][0]
	pose_.orientation = path[seq_][1]

	poseStamp_.header = header_
	poseStamp_.pose = pose_

	currentGoalReached = false
	currentGoalHeader = header_
	to_move_base.publish(poseStamp_)
	rospy.loginfo("Path in progress, reaching goal " + str(seq_))

def startPath():
	l = len(path)
	for i in range(l):
		sendGoal(i)
		while(!currentGoalReached):
			if keepGoing==false:
				return
			pass
	rospy.loginfo("Path complete")


if __name__ == '__main__':
	rospy.init_node('automate')
	to_move_base = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=1)
	rospy.Subscriber("/move_base/result", MoveBaseActionResult, onGoalReached)
	rospy.Subscriber("/automate/command", String, onCommand)

	startPath()

	rospy.loginfo("Path automation stopped")
	rospy.spin()