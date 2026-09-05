# the imports

# for the math use obviously
import math

# core ros2 python lib
import rclpy
from rclpy.node import Node

# message, forum
from geometry_msgs.msg import Twist

# a service from turtlesim : spawn
from turtlesim.srv import Spawn

# tf2 stuff i have no clue about

# to raise error : i am not using it (using it caz its a good practice)
from tf2_ros import TransformException

# a subscriber that auto subscribe to /tf where all nodes are broadcasting, and dumps that info into the buffer
from tf2_ros.transform_listener import TransformListener

# to create buffer aka our empty room where we stores data from the TransformListener : by default it stores values for 10sec
from tf2_ros.buffer import Buffer

# the node
'''
The job : 

'''
class FrameListener(Node):

# the init thingy
    def __init__(self):

    # giving node a name : turtle_tf2_frame_listener
        super().__init__("turtle_tf2_frame_listener")

    # setting a parameter to reuse the node and setting a default value : turtle1
        self.target_frame = self.declare_parameter(
            "target_frame" , "turtle1"
        ).get_parameter_value().string_value

    # creating an empty room where TransformListener can dump info it gets from /tf hoping we get some info from our own broadcaster "Frame broadcaster node : turtle_tf2_frame_publisher"
        self.tf_buffer = Buffer()

    # once the empty room is created we launch TransformListener attached to this node (self) to subscribe to /tf and dump all the broadcasting it is receiving into the buffer
    # stores for 10 sec for default
        self.tf_listener = TransformListener(self.tf_buffer,self)

    # creating a client to spawn a turtle
    #   client for service : /spawn provided by the turtlesim node  
        self.spawner = self.create_client(
            Spawn , 
            'spawn'
        )

    # flags for tracking turtle2's creation

    #   have we called the spawn request
        self.turtle_spawning_service_ready = False
    #   has spawn service finished creating turtle2
        self.turtle_spawned = False

    # creating a publisher to send velocity commands (Twist message) to turtle2/cmd_vel
        self.publisher = self.create_publisher(
            Twist , 
            'turtle2/cmd_vel' , 
            1
        )

    # a timer to call function on a period
        self.timer = self.create_timer(

        # after every period of 1 sec
            1.0,

        # call this function
            self.on_timer
        )

# the function that does two jobs:
# 1) makes sure turtle2 is alive and healthy
# 2) does the math to chase turtle1 and sends the details to turtle2
    def on_timer(self):

    # the leader turtle : turtle1 (we defined it as by default...parameter) : <- we follow this
        leader = self.target_frame

    # the follower turtle :turtle2: <- we sends him the info to follow the leader
        follower = 'turtle2'

    # ! go inside out here
        """
        [ on_timer() called every second ]
            │
            │
            +--------- Is service request sent? (self.turtle_spawning_service_ready)
                        |
                        |---- [YES] ----> Has turtle2 finished spawning? (self.turtle_spawned)
                        |                   |
                        |                   |----- [YES] ---> STAGE 3: (TF Math)
                        |                   |                   |---------> Drive turtle2
                        |                   |
                        |                   |----- [NO] ----> STAGE 2: 
                        |                                       |---------> Check If Spawn Finished
                        |                   
                        |---- [NO] -----> STAGE 1: 
                                            |---------> Send Spawn Request
        """

        if self.turtle_spawning_service_ready:

            if self.turtle_spawned:

            # trying caz we are scared for : lookup_transform
            # at the birth of node turtle1 and turtle2 might not have received yet (it will give error for first few iterations in that case)
                try:
                # we are asking where is the latest position of source frame from the perspective of target_frame 
                    t = self.tf_buffer.lookup_transform(
                        target_frame = follower, # turtle2 (defined above)
                        source_frame = leader, # turtle1 by default (parameter)
                        time = rclpy.time.Time() # Time() = 0 : we are saying we need the latest available info in the buffer
                    )
                # we just created a variable "t" that will store info in : t.transform.translation.x , t.transform.translation.y
                
                except TransformException as ex:
                    self.get_logger().info(
                        f'Could not transform {follower} to {leader} : \n--------------------------------------------\n{ex}'
                    )
                    return

# ! STAGE 3
    # at this point the service req is accepted and the turtle 2 is in the simulation with turtle 1 in the coordinates we gave when we called client

            # creating a empty message forum that we can send to the turtle2
                msg = Twist()
                """
                the goal of this message is to give turtle2 the velocity it needs to reach to the turtle1 (velocity = speed with direction)
                
                +X (Forward direction of turtle2)
                                │
                                │
                                │        @ turtle1 (Leader)
                                │       /
                                │      /  Distance (Hypotenuse)
                                │     /
                                │    / 
                                │   / ) θ (Angle: atan2(y, x))
                                │  /
                                │ /
                +Y <------------@ (turtle2's nose/center)
                (Left)
                """
            # defining the speed of change
                scale_rotation_rate = 1.0
                scale_forward_speed = 0.5
            
            # direction : theta = tan(x/y)
                msg.angular.z = scale_rotation_rate * math.atan2(
                    t.transform.translation.y , t.transform.translation.x
                )

            # direction : h = sqrt(x^2 +y^2)
                msg.linear.x = scale_forward_speed * math.sqrt(
                    (t.transform.translation.x)**2 + (t.transform.translation.y)**2
                )

            # once the forum is filled with correct details we send it to the turtle2 
                self.publisher.publish(msg)


# ! STAGE 2
    # this gets triggered when we sent the service the req and got a promise variable that our req will either be completed or not 
        # the result is the future variable that holds the ans from the service
            else:
            # if the service sent us the message saying its "done" : turtle has spawned
                if self.result.done():
                    self.get_logger().info(
                        f"successfully spawned {self.result.result().name}"
                    )
                # we make the flag TRUE as turtle is spawned
                    self.turtle_spawned = True

            # if the service is not done yet then we try it in another iteration
                else:
                    self.get_logger().info(
                        "Spawn is not finished yet"
                    )

# ! STAGE 1
    # at the start of the node the flags are false so our code will end up here [STAGE 1]
        else:
        # checking if the service is online or not
            if self.spawner.service_is_ready(): # once the service is active :

            # we create a empty structure/forum in the same structure the service needs : Spawn
                req = Spawn.Request()

            # we fill the forum with the info in structure it needs
                req.name = 'turtle2'
                req.x = float(4)
                req.y = float(2)
                req.theta = float(0)

            # making a future obj : a promise that service will accept our req
                self.result = self.spawner.call_async(req)

            # making the flag TRUE as we just sent the req to spawn the turtle
                self.turtle_spawning_service_ready = True

        # if service is not online (could be reasons but most probably the node as not started up yet)
            else:
            # we keeps sending this message until the service is online
                self.get_logger().info(
                    "service not ready"
                )

def main():

    rclpy.init()
    node = FrameListener()
    try :
        rclpy.spin(node)
    except:
        pass

    rclpy.try_shutdown()