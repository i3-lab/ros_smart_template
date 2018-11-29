Installation of Smart Template Controller Node
==============================================

Prerequisite
------------
- Control computer (single-board computer (SBC))
  - 16GB SD card
  - [Ubuntu 18.04 LTS](https://www.ubuntu.com/download/desktop/thank-you?country=US&version=18.04.1&architecture=amd64)
  - [ROS Melodic Morenia](http://wiki.ros.org/melodic/Installation)
  
- Host computer
  - 3D Slicer 4.8 or later

In the following instruction, BeagleBone Black (BBB) and MacBook Pro are used as control and host computers.


Set up ROS on Single-Board Computer (SBC)
-----------------------------------------
Please follow [Tutorial on ROS-IGTL-Bridge for Single-Board Computer](http://openigtlink.org/tutorials/sbc-igtl) to install
the following software on the SBC.

- Ubuntu 18.04 LTS
- ROS Melodic
- OpenIGTLink
- ROS-IGTL-Bridge

If you are using BeagleBone Black Wireless and having a trouble in connecting to your local WiFi, please follow [the memo](bbb-wifi.md)

Set up Smart Template Controller Node
-------------------------------------
In the console on the SBC, first make sure that the system is connected to the internet, and the environmental variables are all set:

    cd catkin_ws
    ubuntu@beaglebone:~/catkin_ws$ source devel/setup.bash

Then download the source code for Smart Template Controller node from GitHub to ~/catkin_ws/src

    ubuntu@beaglebone:~/catkin_ws$ cd src
    ubuntu@beaglebone:~/catkin_ws/src$ git clone https://github.com/i3-lab/ros_smart_template
    Cloning into 'ros_smart_template'...
    remote: Enumerating objects: 47, done.
    remote: Counting objects: 100% (47/47), done.
    remote: Compressing objects: 100% (34/34), done.
    remote: Total 47 (delta 15), reused 40 (delta 11), pack-reused 0
    Unpacking objects: 100% (47/47), done.
    ubuntu@beaglebone:~/catkin_ws/src$ cd ..
    ubuntu@beaglebone:~/catkin_ws$

Run cmake using `catkin_make` command
  
    $ ubuntu@beaglebone:~/catkin_ws# catkin_make
    Base path: /root/catkin_ws
    Source space: /root/catkin_ws/src
    Build space: /root/catkin_ws/build
    Devel space: /root/catkin_ws/devel
    Install space: /root/catkin_ws/install
    ####
    #### Running command: "make cmake_check_build_system" in "/root/catkin_ws/build"
    ####
    ####
    #### Running command: "make -j4 -l4" in "/root/catkin_ws/build"
    ####
    [  0%] Built target std_msgs_generate_messages_eus
    [  0%] Built target geometry_msgs_generate_messages_eus
    
      ...
        
    [100%] Built target ros_igtl_bridge_node
    $ ubuntu@beaglebone:~/catkin_ws# 

