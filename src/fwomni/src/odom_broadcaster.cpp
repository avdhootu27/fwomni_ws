#include <ros/ros.h>
#include <tf/transform_broadcaster.h>
#include <nav_msgs/Odometry.h>
#include <geometry_msgs/TransformStamped.h>

// this code doesn't work

void onOdom(const nav_msgs::Odometry::ConstPtr& msg){

  tf::TransformBroadcaster odom_broadcaster;
  geometry_msgs::TransformStamped odom_trans;

  odom_trans.header.stamp=msg->header.stamp;
  odom_trans.header.frame_id="base_footprint";
  odom_trans.child_frame_id="odom";

  odom_trans.transform.translation.x = msg->pose.pose.position.x;
  odom_trans.transform.translation.y = msg->pose.pose.position.y;
  odom_trans.transform.translation.z = msg->pose.pose.position.z;
  odom_trans.transform.rotation.x = msg->pose.pose.orientation.x;
  odom_trans.transform.rotation.y = msg->pose.pose.orientation.y;
  odom_trans.transform.rotation.z = msg->pose.pose.orientation.z;
  odom_trans.transform.rotation.w = msg->pose.pose.orientation.w;

  odom_broadcaster.sendTransform(odom_trans);

}

int main(int argc, char **argv) {
  
  ros::init(argc, argv, "odom_broadcaster");

  ros::NodeHandle n;

  ros::Subscriber odom_sub = n.subscribe("odom", 1, onOdom);

  ros::Rate loop_rate(5);

  ROS_INFO("Odom broadcaster initialised"); 
  
  ros::spin();

  return 0;
}