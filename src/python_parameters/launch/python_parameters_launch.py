# needed to write a launch file ig? (not much info in ths tutorial)
from launch import LaunchDescription
from launch_ros.actions import Node

"""
we are doing nothing much but giving the parameter a set value
in that case (launch file) that set value is : earth
"""
def generate_launch_description():
    return LaunchDescription([
        Node(
            package='python_parameters',
            executable='minimal_param_node',
            name='custom_minimal_param_node',
            output='screen',
            emulate_tty=True,
            parameters=[
                {'my_parameter': 'earth'}
            ]
        )
    ])
# this is the syntax ....i cant do anything