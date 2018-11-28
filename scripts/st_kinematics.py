#!/usr/bin/env python

from geometry_msgs.msg import Transform

from ros_smart_template.srv import *
import rospy

def forward_kinematics(req):

    trans = Transform()
    #req.depth
    #req.front_x
    #req.front_y
    #req.rear_x
    #req.rear_y
    trans.translation.x = req.front_x
    trans.translation.y = req.front_y
    trans.translation.z = - req.depth
    return ForwardKinematicsResponse(True, trans)


def inverse_kinematics(req):

    trans = req.transform
    depth = -trans.translation.z
    front_x = trans.translation.x
    front_y = trans.translation.y
    rear_x = 0.0
    rear_y = 0.0
    return InverseKinematicsResponse(True, depth, front_x, front_y, rear_x, rear_y)


def init_parameters():

    pass
    ## Calibration Transform
    #calibration = Transform()
    #calibration.translation.x = 0.0
    #calibration.translation.y = 0.0
    #calibration.translation.z = 0.0
    #calibration.rotation.x = 0.0
    #calibration.rotation.y = 0.0
    #calibration.rotation.z = 0.0
    #calibration.rotation.w = 1.0
    #set_param_transform("~CALIBRATION", calibration)

def start_st_kinematics_service():
    rospy.init_node('st_kinematics_service')

    init_parameters()

    print "Starting Kinematics Service for Smart Template.."
    s = rospy.Service('~forward_kinematics', ForwardKinematics, forward_kinematics)
    s = rospy.Service('~inverse_kinematics', InverseKinematics, inverse_kinematics)
    
    rospy.spin()

if __name__ == "__main__":
    start_st_kinematics_service()


