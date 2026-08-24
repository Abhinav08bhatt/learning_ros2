from launch import LaunchDescription
# the launch file blueprint every python launch file needs

from launch.actions import DeclareLaunchArgument, ExecuteProcess, TimerAction
# DeclareLaunchArgument : used to req the command line input that this file acn accept
# ExecuteProcess : Allows the file to run ROS2 commands from itself
# TimerAction : waits for given time before triggering other action

from launch.conditions import IfCondition
# checks if true or false (runs the command if true, if false it will be skipped)

from launch.substitutions import LaunchConfiguration, PythonExpression
# LaunchConfiguration : substitution placeholder that will get populated at the runtime (using user given argument)
# PythonEXpression : lets us write python logic (==,and.or,+)

from launch_ros.actions import Node
# needed to start a node from the file

# the container function
def generate_launch_description():

# making placeholder values that the substitution file will get from its user (who calls it)

    turtlesim_ns = LaunchConfiguration('turtlesim_ns')
    use_provided_red = LaunchConfiguration('use_provided_red')
    new_background_r = LaunchConfiguration('new_background_r')
         
    # example we manually can launch the sub file :
    '''ros2 launch launch_substitution example_substitution_launch.py use_provided_red:=True new_background_r:=0'''

    return LaunchDescription(
        [

    # defining the default values in-case the user/parent does not provide us with one
            DeclareLaunchArgument(
                'turtlesim_ns',
                default_value = 'turtlesim1'
            ),
            DeclareLaunchArgument(
                'use_provided_red',
                default_value = 'False'
            ),
            DeclareLaunchArgument(
                'new_background_r',
                default_value = '255'
            ),

    # launching the node
            Node(
                package='turtlesim',

            # here the turtlesim_ns will be the value provided by the user of the default value
                namespace=turtlesim_ns,

                executable='turtlesim_node',
                name='sim'
            ),

    # executing the process
    # ! PAY ATTENTION TO THE BLANK SPACE INSIDE THE '' OR ""
            ExecuteProcess(
                cmd = [
                    [
                        'ros2 service call ',
                    # either the user value or the default
                        turtlesim_ns,
                        '/spawn ',
                        'turtlesim/srv/Spawn ',
                        '"{x: 2, y:  2, theta: 0.2}"'
                    ]
                ],
                shell = True
            ),
            # this shit literally perform this command line in place of us
            '''ros2 service call turtlesim_ns /spawn turtlesim/srv/Spawn "{x: 2, y:  2, theta: 0.2}"'''

            ExecuteProcess(
                cmd = [
                    [
                        'ros2 param set ',
                    # either the user value or the default
                        turtlesim_ns,
                        '/sim background_r ',
                        '120 '
                    ]
                ],
                shell = True
            ),
            # this shit literally perform this command line in place of us
            '''ros2 param set turtlesim_ns /sim background_r 120'''

    # tells ros2 that this given section will wait for a set amount of time before execution
            TimerAction(

            # it will wait 2.0 seconds
                period=2.0,
            # and then perform these actions:
                actions=[

                # we are going to execute this process
                    ExecuteProcess(

                    # but before it we check a condition 
                    # if the condition is TRUE we perform the process
                    # if the condition is FALSE we do nothing and skip
                        condition = IfCondition(
                            PythonExpression(
                                [
                                    new_background_r,
                                    '== 255 ',
                                    ' and ', 
                                    use_provided_red
                                ]
                            )
                            # we did a simple if condition saying :
                            '''if new_background_r == 255 and use_provided_red'''
                            # new_background_r depends on the input the user/parent gave us....can be anything but we looking for 255
                            # use_provided_red depends on the input the user/parent gave us...can be True or False , we need True
                            # if both condition are True (needed by and) we execute the command below 
                        ),
                        cmd=[
                            [
                                'ros2 param set ',
                                turtlesim_ns,
                                '/sim background_r ',
                                new_background_r
                            ]
                        ],
                        shell = True
                        '''ros2 param set turtlesim_ns /sim background_r new_background_r(an int)'''
                    )
                ]
            )

        ]
    )

'''
Time 0.0s:
│
├─► 1. ROS 2 parses arguments:
│      turtlesim_ns     = "turtlesim2"
│      use_provided_red = "True"
│      new_background_r = "200"
│
├─► 2. Node started: /turtlesim2/sim (turtlesim window opens with turtle1)
│
├─► 3. ExecuteProcess 1 runs: Calls service /turtlesim2/spawn (spawns turtle2)
│
├─► 4. ExecuteProcess 2 runs: Calls ros2 param set /turtlesim2/sim background_r 120 (turns purple)
│
├─► 5. TimerAction timer starts ticking (2.0 seconds countdown)...
│
Time 2.0s:
│
└─► 6. Timer fires:
       - Evaluates condition: "200 == 200 and True" -> True
       - Runs: ros2 param set /turtlesim2/sim background_r 200
       - Screen background turns to pink/red!
'''