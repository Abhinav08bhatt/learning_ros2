from launch import LaunchDescription
# the launch file blueprint every python launch file needs

from launch.actions import IncludeLaunchDescription
# used to run another launch file from current launch file

from launch.substitutions import PathJoinSubstitution
# used to write the path of a file or folder

from launch_ros.substitutions import FindPackageShare
# helps ros2 finds automatically where a package's /share folder is located

# the container/blueprint
def generate_launch_description():

# just a python dict
    colors = {
        'background_r' : '255'
    }

# packs it the way ros2 needs
    return LaunchDescription(
    # wraps everything into the list the ros2 needs
        [

        # helps us run the substitution launch file from this file
            IncludeLaunchDescription(

            # sp that we dont have to hardcode the file path (varies system to system)
                PathJoinSubstitution(
                    [
                    # the package name
                        FindPackageShare("launch_substitution"),
                    # launch folder name
                        'launch',
                    # the file we needs to spot (here: the substitution launch file)
                        'example_substitution_launch.py'
                    ]
                ),
            # while starting the node we want these arguments to be passed to the substitution launch file
                launch_arguments = {
                    'turtlesim_ns' : 'turtlesim2',
                    'use_provided_red' : 'True',
                    'new_background_r' : colors['background_r']
                }.items()
                # .item() converts it into the key-value pair
            )
        ]
    )


'''
[ This Launch File ]
        │
        ├─ 1. Finds path to example_substitution_launch.py
        │
        ├─ 2. Packages arguments:
        │     - turtlesim_ns = "turtlesim2"
        │     - use_provided_red = "True"
        │     - new_background_r = "200"
        │
        ▼
[ Runs example_substitution_launch.py with those values ]
        │
        ▼
[ Spawns Turtlesim Node with Red Background = 200 inside /turtlesim2 ]
'''