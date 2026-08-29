# the imports

from launch import LaunchDescription
# every launch file needs this

from launch.actions import DeclareLaunchArgument
# defines the input parameter for the launch file (something like setting up default values for a file)
# ros2 launch launch_turtle turtlesim_world_1_launch.py background_r:=255 -> this will accept the background_r as input

from launch.substitutions import LaunchConfiguration
# a placeholder until we get values at runtime (here we are getting values from the args we declared in the file)

from launch_ros.actions import Node
# needed to run a specific node in the launch file

# the function
def generate_launch_description():

# execution starts here
    return LaunchDescription(
        [
    # the turtlesim as 3 parameters that lets us config the value of the background color of the sim
    # setting the default value we need from this file

        # VALUES ARE GIVEN IN STRING

            DeclareLaunchArgument(
                'background_r',
                default_value='0'
            ),
            DeclareLaunchArgument(
                'background_g',
                default_value='0'
            ),
            DeclareLaunchArgument(
                'background_b',
                default_value='0'
            ),

        # running the node 
            Node(

            # the ros2 package where the executable is located
                package='turtlesim',

            # executable name
                executable='turtlesim_node',

            # RENAME the node name from /turtlesim to /sim
                name = 'sim',

            # we can pass parameters for a file as list containing dict
                parameters=[
                    {
                    # this uses the value declared above or uses the values given while calling the file
                        'background_r': LaunchConfiguration('background_r'),
                        'background_g': LaunchConfiguration('background_g'),
                        'background_b': LaunchConfiguration('background_b'),
                    }
                ]
            )
        ]
    )