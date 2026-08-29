# the imports

from launch import LaunchDescription
# the main container

from launch_ros.actions import Node
# needed to run nodes from the launch file

# the function
def generate_launch_description():
    return LaunchDescription(
        [
        # running the node
            Node(
            # package that contains the executable name
                package='turtlesim',
            # executable name
                # BY DEFAULT this node subscribe to : /input/pose
                # whenever it receives a pose, it computes the velocity commands and publishes them to the topic : /output/cmd_vel
                executable='mimic',
            # giving it a name
                name='mimic',

            # remapping caz we are changing the defaults of the node without changing the code
                remappings=[
                    ('/input/pose', '/turtle2/pose'),
                    # instead of LISTENING to -> /input/pose , listen to -> /turtle2/pose
                    ('/output/cmd_vel', '/turtlesim2/turtle1/cmd_vel'),
                    # instead of PUBLISHING to -> /output/cmd_vel , listen to -> /turtlesim2/turtle1/cmd_vel
                ]
            )
        ]
    )