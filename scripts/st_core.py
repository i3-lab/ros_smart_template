#!/usr/bin/env python

from geometry_msgs.msg import Transform

from ros_smart_template.srv import *
import rospy

def set_param_transform(key, trans):

    rospy.set_param(key+'_translation_x', trans.translation.x)
    rospy.set_param(key+'_translation_y', trans.translation.y)
    rospy.set_param(key+'_translation_z', trans.translation.z)
    rospy.set_param(key+'_rotation_x', trans.rotation.x)
    rospy.set_param(key+'_rotation_y', trans.rotation.y)
    rospy.set_param(key+'_rotation_z', trans.rotation.z)
    rospy.set_param(key+'_rotation_w', trans.rotation.w)

    
def get_param_transform(key):
    
    trans = Transform()
    trans.translation.x = rospy.get_param(key+'_translation_x')
    trans.translation.y = rospy.get_param(key+'_translation_y')
    trans.translation.z = rospy.get_param(key+'_translation_z')
    trans.rotation.x = rospy.get_param(key+'_rotation_x')
    trans.rotation.y = rospy.get_param(key+'_rotation_y')
    trans.rotation.z = rospy.get_param(key+'_rotation_z')
    trans.rotation.w = rospy.get_param(key+'_rotation_w')
    
    return trans

def set_calibration(req):
    
    print "New calibration matrix."
    newTrans = req.transform
    set_param_transform('~CALIBRATION', newTrans)
    curTrans = get_param_transform('~CALIBRATION')
    
    return SetCalibrationResponse(True, curTrans)


def get_calibration(req):
    
    print "Get calibration matrix: " 
    return GetCalibrationResponse(True)


def init_parameters():
    # Calibration Transform
    calibration = Transform()
    calibration.translation.x = 0.0
    calibration.translation.y = 0.0
    calibration.translation.z = 0.0
    calibration.rotation.x = 0.0
    calibration.rotation.y = 0.0
    calibration.rotation.z = 0.0
    calibration.rotation.w = 1.0
    set_param_transform("~CALIBRATION", calibration)

def start_st_core_service():
    rospy.init_node('st_core_service')

    init_parameters()

    print "Starting Core Service for Smart Template.."
    s = rospy.Service('set_calibration', SetCalibration, set_calibration)
    s = rospy.Service('get_calibration', GetCalibration, get_calibration)
    
    rospy.spin()

if __name__ == "__main__":
    start_st_core_service()
    


