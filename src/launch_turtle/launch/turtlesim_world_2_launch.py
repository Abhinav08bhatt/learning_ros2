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
                # namespace='turtlesim2',   # <-- they told to remove it caz we are writing directly in main launch
            # renaming the node from /turtlesim/ to /sim/
                name='sim',
            # passing parameters to the node
                parameters=[
                # this time we are passing it from a yaml file that is meant for this specific file with name /turtlesim2/sim/
                    PathJoinSubstitution(
                        [
                            FindPackageShare('launch_turtle'),
                            'config',
                            'turtlesim.yaml'
                    # /turtlesim2/sim:
                    # ros__parameters:
                        # background_b: 255
                        # background_g: 255
                        # background_r: 255
                        ]
                    )
                ]
            )
        ]
    )