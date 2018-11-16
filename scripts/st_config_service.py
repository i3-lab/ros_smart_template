#!/usr/bin/env python

from ros_smart_template.srv import *
import rospy

def set_calibration(req):
    print "New calibration: " 
    return SetCalibrationResponse(True)

def get_calibration(req):
    print "Get calibration matrix: " 
    return GetCalibrationResponse(True)

def start_config_service():
    rospy.init_node('st_config_service')

    print "Starting calibration service.."
    s = rospy.Service('set_calibration', SetCalibration, set_calibration)
    s = rospy.Service('get_calibration', SetCalibration, set_calibration)
    
    rospy.spin()

if __name__ == "__main__":
    start_config_service()
    
