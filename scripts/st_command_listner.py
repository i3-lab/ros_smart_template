#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from ROS_IGTL_Bridge.msg import igtlstring
from ROS_IGTL_Bridge.msg import igtltransform

def cb_transform(data):
    rospy.loginfo(rospy.get_caller_id() + "Tranform %s has been received.", data.name)

def cb_string(data):
    rospy.loginfo(rospy.get_caller_id() + "String %s has been received.", data.name)
    
def st_command_listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('st_command_listener', anonymous=True)
    rospy.Subscriber("IGTL_TRANSFORM_IN", igtlstring, callback_transform)
    rospy.Subscriber("IGTL_STRING_IN", igtlstring, callback_string)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    st_command_listner()

