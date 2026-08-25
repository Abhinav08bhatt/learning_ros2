from launch import LaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    return LaunchDescription(
        [
            Node(
                package='turtlesim',
                executable='turtlesim_node',
                namespace='turtlesim_3',
                name='sim',
                parameters=[
                    PathJoinSubstitution(
                        [
                            FindPackageShare('launch_turtle'),
                            'config',
                            'wildcard_turtlesim.yaml'
                        ]
                    )
                ]
            )
    ]
    )