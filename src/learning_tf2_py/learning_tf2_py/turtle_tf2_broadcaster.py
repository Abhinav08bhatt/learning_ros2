# import stuff

# needed to read the arguments passed in command line
import sys

# for the math obviously
import math
import numpy as np

# the code rclpy library
import rclpy
from rclpy.node import Node

# the speaker
from tf2_ros import TransformBroadcaster
# TransformBroadcaster is needed for frames that changes continuously like position of robot in the world

# the empty forums we use as a message blueprint
from turtlesim.msg import Pose  # Pose : x , y , theta
from geometry_msgs.msg import TransformStamped

# the function to convert human 3d space to ros2 computer needed 4d space
def quaternion_from_euler(ai, aj, ak):
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

# the node
class FramePublisher(Node):

# the init thingy
    def __init__(self):

    # giving node a name
        super().__init__('turtle_tf2_frame_publisher')

    # declaring a parameter
    # these parameter act as a user tag ....we can use them to create multiple instance of this same node using launch file
    # here we are setting the turtlename as turtle <-default value given here
    # in launch file we can create a node with turtlename as turtle1 and another as turtle2 (makes code very reusable)
        self.turtlename = self.declare_parameter(
            'turtlename' , 'turtle'
        ).get_parameter_value().string_value

    # initializing transformer broadcaster <- for object that move (robot in world)
        self.tf_broadcaster = TransformBroadcaster(self)

    # subscribing to nodes screaming in the system
    # here we subscribe to the node we care about...nodes that are 
    # talking through topic : turtlename/pose (ex : turtle1/pose or turtle2/pose)
    # in the format of Pose (x,y,theta)
    # when we get someone screaming in this same format we need, we call our function : handle_turtle_pose
        self.subscription = self.create_subscription(
            Pose,
            # Pose : x , y , theta
            f"/{self.turtlename}/pose",
            self.handle_turtle_pose,
            1
        )

    # just to handle empty variable error if we get one
        self.subscription

# the callback function
    def handle_turtle_pose(self,msg):

    # creating the blueprint object of TransformStamped -> its like a forum needed by the frames that are always moving
        t = TransformStamped()

    # the forum shape :

    # header : 
        # time at the top :
        t.header.stamp = self.get_clock().now().to_msg()

        # then the name of parent : world here (the place where it moves)
        t.header.frame_id = 'world'

    # child frame : our turtle here (the one that moves)
        t.child_frame_id = self.turtlename

    # transform data : translation <- it tells us the distance, vector distance of our turtle from the origin at the time being (x,y,z)

        # x : extracted from the scream we heard using our subscriber
        t.transform.translation.x = msg.x

        # y : extracted from the scream we heard using our subscriber
        t.transform.translation.y = msg.y

        # z is 0 because turtlesim operate in a 2d env , no point of being in air
        t.transform.translation.z = 0.0


    # converting the human given 3d space into the quaternion space needed by ros2 computer
        q = quaternion_from_euler(
            0,
            0,
            msg.theta
        )

    # transform data : rotation (quaternion) <- it tells us where the robot is facing right now
        t.transform.rotation.x = q[0]
        t.transform.rotation.y = q[1]
        t.transform.rotation.z = q[2]
        t.transform.rotation.w = q[3]


    # now we have the 6d space, we know where the robot is respective to the origin : x,y,z and we know where the robot is facing using : quaternion (representing 3d x,y,z)
        self.tf_broadcaster.sendTransform(t)


def main():

    rclpy.init()
    node = FramePublisher()
    try : 
        rclpy.spin(node)
    except :
        pass

    rclpy.try_shutdown()