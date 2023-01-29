#include "ros/ros.h"
#include "std_msgs/Float64.h"
#include "nav_msgs/Odometry.h"
#include "geometry_msgs/Twist.h"
#include "tf/tf.h"
#include "geometry_msgs/Pose2D.h"
#include <cmath>

#define PI 3.14159265358979323846
#define WHEEL_RADIUS 0.0198
#define BOT_RADIUS 0.125

float alpha,beta,gama;
float error=0,prev_error=0,correction=0,curr_angle=0,set_angle=0;
float kp=0.01;
float kd=0.05;
float ki=0;

float q0,q1,q2,q3,cb;
float arr[3][3];

float x=0,y=0,z=0;
std_msgs::Float64 omegaFR,omegaFL,omegaRL,omegaRR;

void onOdom(const nav_msgs::Odometry::ConstPtr& msg){

  q0=msg->pose.pose.orientation.x;
  q1=msg->pose.pose.orientation.y;
  q2=msg->pose.pose.orientation.z;
  q3=msg->pose.pose.orientation.w;

  arr[0][0]=2 * (q0 * q0 + q1 * q1) - 1;
  arr[0][1]=2 * (q1 * q2 - q0 * q3);
  arr[0][2]=2 * (q1 * q3 + q0 * q2);
  arr[1][0]=2 * (q1 * q2 + q0 * q3);
  arr[1][1]=2 * (q0 * q0 + q2 * q2) - 1;
  arr[1][2]=2 * (q2 * q3 - q0 * q1);
  arr[2][0]=2 * (q1 * q3 - q0 * q2);
  arr[2][1]=2 * (q2 * q3 + q0 * q1);
  arr[2][2]=2 * (q0 * q0 + q3 * q3) - 1;

  cb=sqrt(arr[0][0]*arr[0][0]+arr[1][0]*arr[1][0]);
  // beta = atan2(-arr[2][0],cb);
  // alpha = atan2(arr[1][0]/cb,arr[0][0]/cb);
  
  gama = atan2(arr[2][1]/cb,arr[2][2]/cb) * 180/PI;

}

void onTwist(const geometry_msgs::Twist::ConstPtr& msg){
// velocities are divided by 6 because original velocities are too high for this small robot
  x = msg->linear.x/6;
  y = msg->linear.y/6;
  z = msg->angular.z/6;

}

int main(int argc, char **argv) {
  
  ros::init(argc, argv, "omni_control");

  ros::NodeHandle n;

  ros::Subscriber odom_sub = n.subscribe("odom", 1, onOdom);
  ros::Subscriber cmd_vel_sub = n.subscribe("cmd_vel", 1, onTwist);
  ros::Publisher front_right = n.advertise<std_msgs::Float64>("/Cont1_velocity_controller/command", 1);
  ros::Publisher front_left = n.advertise<std_msgs::Float64>("/Cont2_velocity_controller/command", 1);
  ros::Publisher rear_left = n.advertise<std_msgs::Float64>("/Cont3_velocity_controller/command", 1);
  ros::Publisher rear_right = n.advertise<std_msgs::Float64>("/Cont4_velocity_controller/command", 1);

  ros::Rate loop_rate(5);

  ROS_INFO("Controller initialised"); 
  
  while (ros::ok()){

    omegaFR.data = (sin(7 * PI / 4) * x + cos(7 * PI / 4) * y + BOT_RADIUS * z - correction) / WHEEL_RADIUS;    //assuming u1 as front-right
    omegaFL.data = (sin(1 * PI / 4) * x + cos(1 * PI / 4) * y + BOT_RADIUS * z - correction) / WHEEL_RADIUS;    //assuming u2 as front-left
    omegaRL.data = (sin(3 * PI / 4) * x + cos(3 * PI / 4) * y + BOT_RADIUS * z - correction) / WHEEL_RADIUS;    //assuming u3 as rear-left 
    omegaRR.data = (sin(5 * PI / 4) * x + cos(5 * PI / 4) * y + BOT_RADIUS * z - correction) / WHEEL_RADIUS;    //assuming u4 as rear-right

    front_right.publish(omegaFR);
    front_left.publish(omegaFL);
    rear_left.publish(omegaRL);
    rear_right.publish(omegaRR);

    curr_angle = gama;
    if(z!=0){
      set_angle = gama;
    }
    error = curr_angle - set_angle;
    correction = kp*(error) + kd*(error-prev_error) + ki*(error+prev_error);
    prev_error = error;

    ros::spinOnce();
    loop_rate.sleep();
  }

  return 0;
}


// https://automaticaddison.com/how-to-convert-a-quaternion-to-a-rotation-matrix/
// https://stackoverflow.com/questions/11514063/extract-yaw-pitch-and-roll-from-a-rotationmatrix