# the imports

from launch import LaunchDescription
# every launch file needs this

from launch.substitutions import PathJoinSubstitution
# finds and join the paths of folder/files

from launch_ros.actions import Node
# needed to run a specific node in the launch file

from launch_ros.substitutions import FindPackageShare
# substitution that finds installed directory of package

# the function
def generate_launch_description():

    return LaunchDescription(
        [
        # running the node
            Node(
            # ros2 package that contains the executable
                package='turtlesim',
            # executable name
                executable='turtlesim_node',
            # writing the hardcoded namespace
                namespace='turtlesim3',
            # renaming the node
                name='sim',
            # passing parameters to the node
                parameters=[
                # giving a WILDCARD yaml file...meaning that file will work with any node regardless of the namespace
                    PathJoinSubstitution(
                        [
                            FindPackageShare('launch_turtle'),
                            'config',
                            'wildcard_turtlesim.yaml'
                        # /**:
                        #     ros__parameters:
                        #         background_b: 205
                        #         background_g: 155
                        #         background_r: 55
                        ]
                    )
                ]
            )
        ]
    )