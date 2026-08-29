import math
import sys

from geometry_msgs.msg import TransformStamped

import numpy as np

import rclpy
from rclpy.node import Node

from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster

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

# the init thingy
    def __init__(self,transformation):
        super().__init__('static_frame_tf2_broadcaster')
        self.tf_static_broadcaster = StaticTransformBroadcaster(self)
        self.make_transform(transformation)

    def make_transform(self, transformation):
        t = TransformStamped()

        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = "world"
        t.child_frame_id = transformation[1]

        t.transform.translation.x = float(transformation[2])
        t.transform.translation.y = float(transformation[3])
        t.transform.translation.z = float(transformation[4])

        q = quaternion_from_euler(
            float(transformation[5]),
            float(transformation[6]),
            float(transformation[7]),
        )

        t.transform.rotation.x = q[0]
        t.transform.rotation.y = q[1]
        t.transform.rotation.z = q[2]
        t.transform.rotation.w = q[3]

        self.tf_static_broadcaster.sendTransform(t) 

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

    rclpy.shutdown()