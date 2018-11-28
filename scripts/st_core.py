#!/usr/bin/env python

from geometry_msgs.msg import Transform
from ros_smart_template.srv import *
import rospy

class ActuatorPositions:
    def __init__(self, depth=0.0, front_x=0.0, front_y=0.0, rear_x=0.0, rear_y=0.0):
        self.depth = depth
        self.front_x = front_x
        self.front_y = front_y
        self.rear_x = rear_x
        self.rear_y = rear_y

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

    rospy.loginfo(rospy.get_caller_id() + ": Setting a new calibration matrix..")
    newTrans = req.transform
    set_param_transform('~CALIBRATION', newTrans)
    curTrans = get_param_transform('~CALIBRATION')
    
    return SetCalibrationResponse(True, curTrans)


def get_calibration(req):

    print "Get calibration matrix: "
    curTrans = get_param_transform('~CALIBRATION')
    
    return GetCalibrationResponse(True, curTrans)


def set_param_target(pos):

    rospy.set_param('~TARGET_depth',   pos.depth)
    rospy.set_param('~TARGET_front_x', pos.front_x)
    rospy.set_param('~TARGET_front_y', pos.front_y)
    rospy.set_param('~TARGET_rear_x',  pos.rear_x)
    rospy.set_param('~TARGET_rear_y',  pos.rear_y)

def get_param_target():

    pos = ActuatorPositions()
    pos.depth   = rospy.get_param('~TARGET_depth')
    pos.front_x = rospy.get_param('~TARGET_front_x')
    pos.front_y = rospy.get_param('~TARGET_front_y')
    pos.rear_x  = rospy.get_param('~TARGET_rear_x')
    pos.rear_y  = rospy.get_param('~TARGET_rear_y')

    return pos


def set_target(req):
    rospy.loginfo(rospy.get_caller_id() + ": Setting a new target..")
    rospy.wait_for_service('/st_kinematics_service/inverse_kinematics')
    res1 = None
    try:
        rospy.loginfo(rospy.get_caller_id() + ": Calling inverse kinematics")
        inverse_kinematics = rospy.ServiceProxy('/st_kinematics_service/inverse_kinematics', InverseKinematics)
        res1 = inverse_kinematics(req.transform)
        if res1.success:
            pos = ActuatorPositions()
            pos.depth   = res1.depth  
            pos.front_x = res1.front_x
            pos.front_y = res1.front_y
            pos.rear_x  = res1.rear_x 
            pos.rear_y  = res1.rear_y
            set_param_target(pos)
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

    if res1 == None or res1.success == False:
        return SetTargetResponse(False, None)

    rospy.loginfo(rospy.get_caller_id() + ": Checking the set target")

    res2 = None
    rospy.wait_for_service('/st_kinematics_service/forward_kinematics')
    try:
        forward_kinematics = rospy.ServiceProxy('/st_kinematics_service/forward_kinematics', ForwardKinematics)
        res2 = forward_kinematics(pos.depth, pos.front_x, pos.front_y, pos.rear_x, pos.rear_y)
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

    if res2 == None or res2.success == False:
        return SetTargetResponse(False, None)
    
    return SetTargetResponse(True, res2.transform)


def get_target(req):
    res = None
    rospy.wait_for_service('/st_kinematics_service/forward_kinematics')
    try:
        forward_kinematics = rospy.ServiceProxy('/st_kinematics_service/forward_kinematics', ForwardKinematics)
        res = forward_kinematics(pos.depth, pos.front_x, pos.front_y, pos.rear_x, pos.rear_y)
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

    if res == None or res.success == False:
        return GetTargetResponse(False, None)
    
    return GetTargetResponse(True, res.transform)


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
    set_param_transform('~CALIBRATION', calibration)

    # Actuator positions
    pos = ActuatorPositions()
    pos.depth = 0.0
    pos.front_x = 0.0
    pos.front_y = 0.0
    pos.rear_x = 0.0
    pos.rear_y = 0.0
    set_param_target(pos)

def start_st_core_service():
    rospy.init_node('st_core_service')

    init_parameters()

    print "Starting Core Service for Smart Template.."
    s = rospy.Service('~set_calibration', SetCalibration, set_calibration)
    s = rospy.Service('~get_calibration', GetCalibration, get_calibration)
    s = rospy.Service('~set_target', SetTarget, set_target)
    s = rospy.Service('~get_target', GetTarget, get_target)
    
    rospy.spin()

if __name__ == "__main__":
    start_st_core_service()
    


