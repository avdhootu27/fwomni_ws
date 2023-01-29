#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64
from nav_msgs.msg import Odometry
import math

max_trans_vel = 5
max_angular_vel = 2
wheel_radius = 0.0198
diagonal_dist = 0.125
sqrt_2 = 1.41421356237
PI = math.pi

x = 0
y = 0
z = 0
omegaFR = 0.0
omegaFL = 0.0
omegaRR = 0.0
omegaRL = 0.0

def onOdom(data):
    pass

def callback(vel):

    # velocities are divided by 6 because original velocities are too high for this small robot
    x = vel.linear.x/6
    y = vel.linear.y/6
    z = vel.angular.z/6

    omegaFR = (-math.sin(7 * PI / 4) * x + math.cos(7 * PI / 4) * y + diagonal_dist * z) / wheel_radius
    omegaFL = (-math.sin(1 * PI / 4) * x + math.cos(1 * PI / 4) * y + diagonal_dist * z) / wheel_radius
    omegaRL = (-math.sin(3 * PI / 4) * x + math.cos(3 * PI / 4) * y + diagonal_dist * z) / wheel_radius
    omegaRR = (-math.sin(5 * PI / 4) * x + math.cos(5 * PI / 4) * y + diagonal_dist * z) / wheel_radius

    front_right.publish(omegaFR)
    front_left.publish(omegaFL)
    rear_right.publish(omegaRR)
    rear_left.publish(omegaRL)

    # front_right.publish(2)
    # front_left.publish(2)
    # rear_right.publish(2)
    # rear_left.publish(2)

    rospy.loginfo(str(omegaFR) + " | " + str(omegaFL) + " | " + str(omegaRR) + " | " + str(omegaRL))
    
def listener():
    rospy.init_node('omni_control')
    rospy.loginfo("------------------------------------------------------")
    rospy.loginfo("                Controller Initialized                ")
    rospy.loginfo("------------------------------------------------------")
    rospy.Subscriber("cmd_vel", Twist, callback)
    rospy.Subscriber("odom", Odometry, onOdom)
    rospy.spin()

if __name__ == '__main__':
    x=0
    y=0
    z=0
    omegaFR = 0.0
    omegaFL = 0.0
    omegaRR = 0.0
    omegaRL = 0.0

    front_right = rospy.Publisher('Cont1_velocity_controller/command', Float64, queue_size=1)
    front_left = rospy.Publisher('Cont2_velocity_controller/command', Float64, queue_size=1)
    rear_left = rospy.Publisher('Cont3_velocity_controller/command', Float64, queue_size=1)
    rear_right = rospy.Publisher('Cont4_velocity_controller/command', Float64, queue_size=1)
    listener()