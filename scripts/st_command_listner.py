#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from ROS_IGTL_Bridge.msg import igtlstring
from ROS_IGTL_Bridge.msg import igtltransform
from ros_smart_template.srv import *

def cb_transform(data):
    
    global pub_igtl_transform_out
    
    rospy.loginfo(rospy.get_caller_id() + ": Tranform %s has been received.", data.name)

    if data.name == 'SET_CALIBRATION':
        rospy.loginfo(rospy.get_caller_id() + ": Waiting for Core Service.")
        rospy.wait_for_service('/st_core_service/set_calibration')
        try:
            rospy.loginfo(rospy.get_caller_id() + ": Calling SetCalibration Service.")
            set_calibration = rospy.ServiceProxy('/st_core_service/set_calibration', SetCalibration)
            res = set_calibration('CALIBRATION', data.transform)
            transmsg = igtltransform()
            transmsg.name = 'CALIBRATION'
            transmsg.transform = res.transform
            pub_igtl_transform_out.publish(transmsg)
            
        except rospy.ServiceException, e:
            print "Service call failed: %s"%e

    if data.name == 'SET_TARGET':
        rospy.loginfo(rospy.get_caller_id() + ": Waiting for Core Service.")
        rospy.wait_for_service('/st_core_service/set_target')
        try:
            rospy.loginfo(rospy.get_caller_id() + ": Calling SetTarget Service.")
            set_target = rospy.ServiceProxy('/st_core_service/set_target', SetTarget)
            res = set_target(data.transform)
            transmsg = igtltransform()
            transmsg.name = 'TARGET'
            transmsg.transform = res.transform
            pub_igtl_transform_out.publish(transmsg)
            
        except rospy.ServiceException, e:
            print "Service call failed: %s"%e
        
        

def cb_string(data):
    
    global pub_igtl_transform_out
    
    rospy.loginfo(rospy.get_caller_id() + "String %s has been received.", data.name)

    if data.name == 'GET_CALIBRATION':
        rospy.loginfo(rospy.get_caller_id() + ": Waiting for Core Service.")
        rospy.wait_for_service('/st_core_service/get_calibration')
        try:
            rospy.loginfo(rospy.get_caller_id() + ": Calling GetCalibration Service.")
            get_calibration = rospy.ServiceProxy('/st_core_service/get_calibration', GetCalibration)
            res = get_calibration('CALIBRATION')
            transmsg = igtltransform()
            transmsg.name = 'CALIBRATION'
            transmsg.transform = res.transform
            pub_igtl_transform_out.publish(transmsg)

        except rospy.ServiceException, e:
            print "Service call failed: %s"%e
            
        
    
def st_command_listener():

    global pub_igtl_transform_out
    
    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    pub_igtl_transform_out = rospy.Publisher('IGTL_TRANSFORM_OUT', igtltransform, queue_size=10)
    
    rospy.init_node('st_command_listener', anonymous=True)
    rospy.Subscriber("IGTL_TRANSFORM_IN", igtltransform, cb_transform)
    rospy.Subscriber("IGTL_STRING_IN", igtlstring, cb_string)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    st_command_listener()

