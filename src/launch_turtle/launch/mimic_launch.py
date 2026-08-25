from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription(
        [
            Node(
                package='turtlesim',
                executable='mimic',
                name='mimic',
                remappings=[
                    ('/input/pose','/turtle2/pose'),
                    ('/output/cmd_vel','/turtlesim2/turtle2/cmd_vel')
                ]
            )
        ]
    )