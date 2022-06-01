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
		# mark goal as reached if timestamp of reached goal is equal to timestamp of current goal
		if msg.status.goal_id.stamp==currentGoalHeader.stamp:
			currentGoalReached = true
			rospy.loginfo("Path in progress, goal "+str(currentGoalHeader.seq)+ "reached")

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
	# wait till start command is not received
	while(!keepGoing):
		pass

	l = len(path)
	for i in range(l):
		# send one goal
		sendGoal(i)
		# wait till current goal is not reached
		while(!currentGoalReached):
			# stop the path if stop command is received
			if keepGoing==false:
				return
			pass
	rospy.loginfo("Path complete")


if __name__ == '__main__':
	# initialize the node
	rospy.init_node('automate')

	to_move_base = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=1)
	rospy.Subscriber("/move_base/result", MoveBaseActionResult, onGoalReached)
	rospy.Subscriber("/automate/command", String, onCommand)
	# start the path
	startPath()
	rospy.loginfo("Path automation stopped")
	rospy.spin()