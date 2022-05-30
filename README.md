# fwomni_ws

The workspace is created in ros-noetic. The purpose of creatng this workspace is to test navigation parameters for 4 wheel omni bot (holonomic/non-holonomic).
The controller for the navigation is not working as expected due to unknown reasons so I have used a planar plugin to move the bot according to the velocities published on cmd_vel topic.

This workspace have the URDF of 4 omni-wheeled bot, partially created using Autodesk Fusion360 & partially created/modified by me.

### To run the bot using teleop_twist_keyboard:
```
$ roslaunch fwomni gazebo.launch
```

### To start slam-gmapping:
```
$ roslaunch fwomni gmapping.launch
```

### To run AMCL:
```
$ roslaunch fwomni amcl.launch
```

### To start autonomous navigation:
```
$ roslaunch fwomni navigation.launch
```
