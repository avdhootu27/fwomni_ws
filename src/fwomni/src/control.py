#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64
import math

max_trans_vel = 5
max_angular_vel = 2
wheel_radius = 0.01
diagonal_dist = 0.247345/2
sqrt_2 = 1.41421356237
PI = math.pi

x = 0
y = 0
z = 0
omegaFR = 0.0
omegaFL = 0.0
omegaRR = 0.0
omegaRL = 0.0

def callback(vel):
    if(vel.linear.x > max_trans_vel):
        x = max_trans_vel
    elif(vel.linear.x < -max_trans_vel):
        x = -max_trans_vel
    else:
        x = vel.linear.x

    if(vel.linear.y > max_trans_vel):
        y = max_trans_vel
    elif(vel.linear.y < -max_trans_vel):
        y = -max_trans_vel
    else:
        y = vel.linear.y

    if(vel.angular.z > max_angular_vel):
        z = max_angular_vel
    elif(vel.angular.z < -max_angular_vel):
        z = -max_angular_vel
    else:
        z = vel.angular.z

    # omegaFR = sqrt_2 * (x + y) + 2 * z * diagonal_dist
    # omegaFL = sqrt_2 * (-x + y) + 2 * z * diagonal_dist
    # omegaRR = sqrt_2 * (x - y) + 2 * z * diagonal_dist
    # omegaRL = sqrt_2 * (-x - y) + 2 * z * diagonal_dist

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
    rospy.init_node('controller')
    rospy.loginfo("------------------------------------------------------")
    rospy.loginfo("                Controller Initialized                ")
    rospy.loginfo("------------------------------------------------------")
    rospy.Subscriber("cmd_vel", Twist, callback)
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
    rear_right = rospy.Publisher('Cont3_velocity_controller/command', Float64, queue_size=1)
    rear_left = rospy.Publisher('Cont4_velocity_controller/command', Float64, queue_size=1)
    listener()