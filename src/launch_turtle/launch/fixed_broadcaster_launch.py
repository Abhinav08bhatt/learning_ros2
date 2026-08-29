# the imports

from launch import LaunchDescription
# the main container

from launch.actions import DeclareLaunchArgument
# to make default values for this file (creating cli launch arguments)

from launch.substitutions import EnvironmentVariable,LaunchConfiguration
# EnvironmentVariable : Reads the env variables that are in the system (example : $HOME , $USER)
# LaunchConfiguration : a placeholder until we get values at runtime (here we are getting values from the args we declared in the file)

from launch_ros.actions import Node
# needed to run the node from the launch file

# the main function
def generate_launch_description():
    return LaunchDescription(
        [
        # declare an argument : node_prefix
        # default value : the user of the system + "_" at the end(example in my case : avi_ )
            DeclareLaunchArgument(
                'node_prefix',
                default_value=[EnvironmentVariable('USER'),'_'],
                description='prefix for the node name'
            ),

        # running the node
            Node(
            # package containing the executable
                package='turtle_tf2_py',
            # name of the executable
                executable='fixed_frame_tf2_broadcaster',
            # alright this is imp...
            # in my case it gives name = avi_fixed_broadcaster
                name=[LaunchConfiguration('node_prefix'), 'fixed_broadcaster']
            )
        ]
    )