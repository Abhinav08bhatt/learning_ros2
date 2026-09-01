# needed by the calculation function
import math
import numpy as np

# needed to read arguments
import sys

# the python ros module
import rclpy
from rclpy.node import Node

# a message type (think of it as empty structure that we fill with our values)
from geometry_msgs.msg import TransformStamped

# a speaker
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster
# StaticTransformBroadcaster is used for frames that will forever remain static like position of camera in robot and stuff

# forget what this is
def quaternion_from_euler(ai, aj, ak):
    '''
    it takes parameters from the human mental model of  3d space aka : roll , pitch , yawn
    IN RADIANS
    and gives out a list with 4 values (index 0-3)
    which tells motion to the computer in : x , y , z , w
    '''
    ai /= 2.0
    aj /= 2.0
    ak /= 2.0
    ci = math.cos(ai)
    si = math.sin(ai)
    cj = math.cos(aj)
    sj = math.sin(aj)
    ck = math.cos(ak)
    sk = math.sin(ak)
    cc = ci*ck
    cs = ci*sk
    sc = si*ck
    ss = si*sk

    q = np.empty((4, ))
    q[0] = cj*sc - sj*cs
    q[1] = cj*ss + sj*cc
    q[2] = cj*cs - sj*sc
    q[3] = cj*cc + sj*ss

    return q


# creating the node
class StaticFramePublisher(Node):
    '''
    Broadcast transform that never change.

    This example publishes transform from 'world' to a static turtle frame
    The transformer are only published once at startup, and are constant for all time
    '''

# the init thingy but this time it takes a input LIST at initialization of the class
    def __init__(self,transformation):

    # giving node a name : static_frame_tf2_broadcaster <- not the executable name -> executable name is present in the setup.py
        super().__init__('static_frame_tf2_broadcaster')

    # a speaker that screams a static transformation at the startup of the Node
        self.tf_static_broadcaster = StaticTransformBroadcaster(self)

    # calling our function
        self.make_transform(transformation)


# the function that does the job....it takes the argument that were passed to the class on the instant of initialization of the node
    def make_transform(self, transformation):

    # a message type : think of empty forum where we fill the details in blanks 
        t = TransformStamped()

    # at the top we need the following info : 

        # the current time
        t.header.stamp = self.get_clock().now().to_msg()
        
        # name of the world
        t.header.frame_id = "world"

        # child id : first argument in the list of input
        t.child_frame_id = transformation[1]

    # in the main message content we need 6d pose : translation and rotation

        # translation
        t.transform.translation.x = float(transformation[2])
        t.transform.translation.y = float(transformation[3])
        t.transform.translation.z = float(transformation[4])

        # converting human radian 3d rotation -> computer needed quaternion rotation
        q = quaternion_from_euler(
            float(transformation[5]),
            float(transformation[6]),
            float(transformation[7]),
        )

        # rotation
        t.transform.rotation.x = q[0]
        t.transform.rotation.y = q[1]
        t.transform.rotation.z = q[2]
        t.transform.rotation.w = q[3]


    # sending the message we filled with our info
        self.tf_static_broadcaster.sendTransform(t) 


# the main function
def main():


    logger = rclpy.logging.get_logger('world')

    if len(sys.argv) != 8:
        logger.info("bhai fuck up kr diya aapne tho, fir se try karo")
        sys.exit(1)

    if sys.argv[1] == 'world':
        logger.info("ye world name nhi likh sakte")
        sys.exit(2)

    rclpy.init()
    node = StaticFramePublisher(sys.argv)
    try :
        rclpy.spin(node)
    except :
        pass

    rclpy.try_shutdown()