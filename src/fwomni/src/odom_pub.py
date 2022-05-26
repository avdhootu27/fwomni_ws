#!/usr/bin/env python3

import roslib
import rospy
from nav_msgs.msg import Odometry
import tf

odom_broadcaster = tf.TransformBroadcaster()

def callback(msg):
    pos = msg.pose.pose.position
    orient = msg.pose.pose.orientation
    odom_broadcaster.sendTransform(
        (pos.x, pos.y, 0),
        (orient.x, orient.y, orient.z, orient.w),
        msg.header.stamp,
        "base_footprint",
        "odom"
    )

if __name__ == '__main__':
    rospy.init_node('odom_broadcaster')
    rospy.Subscriber("odom", Odometry, callback)
    rospy.spin()