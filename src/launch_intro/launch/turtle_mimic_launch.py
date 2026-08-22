# importing the stuff needed to make a lunch file
from launch import LaunchDescription
from launch_ros.actions import Node


# the wrapper function aka launch description begins
def generate_launch_description():
    return LaunchDescription([

    # action 1 : launch turtlesim with arguments
        Node(
            package= 'turtlesim',
            namespace= 'turtlesim1',
            executable= 'turtlesim_node',
            name= 'sim',
            arguments=['--ros-args','--log-level','info']
        ),
    # action 2 : launch turtlesim with arguments diff then action 1
        Node(
            package= 'turtlesim',
            namespace= 'turtlesim2',
            executable= 'turtlesim_node',
            name= 'sim',
            ros_arguments=['--log-level','warn']
        ),
    # action 3 : launch turtlesim with some remaps (idk)
        Node(
            package= 'turtlesim',
            executable= 'mimic',
            name= 'sim',
            remappings = [
                ('/input/pose', '/turtlesim1/turtle1/pose'),
                ('/output/cmd_vel', '/turtlesim2/turtle1/cmd_vel'),
            ] 
        ),
    ])

"""
so what happen is :

launch file looks at action 1 and fires it
we get a turtlesim screen

then launch file looks at action 2 and fires it
we get another turtlesim screen

then launch file looks at action 3 and it creates a underlying hidden mimicking engine
HOW?
when we run our code we plan to give commands to the turtle1 so we make it the LEADER and turtle2 becomes the follower
- remapping lines :
    ('/input/pose', '/turtlesim1/turtle1/pose')         ----> position of the leader
    ('/output/cmd_vel', '/turtlesim2/turtle1/cmd_vel'), ----> velocity of the follower

when we give command what the mimic gets a earphone connected to turtle1 and a microphone for turtle2 is doing:
it keeps listening to the position of the turtle 1 and keep shouting the position/velocity to the turtle2

so when turtle 1 moves
mimic notice it and screams at turtle2 to immediately move to that position
"""