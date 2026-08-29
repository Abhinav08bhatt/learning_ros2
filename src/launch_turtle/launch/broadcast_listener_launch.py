# the import

from launch import LaunchDescription
# the main container

from launch.actions import DeclareLaunchArgument
# to make default values for this file (creating cli launch arguments)

from launch.substitutions import LaunchConfiguration
# a placeholder until we get values at runtime (here we are getting values from the args we declared in the file)

from launch_ros.actions import Node
# needed to run a node from teh file

# the function
def generate_launch_description():
    return LaunchDescription(
        [

        # creating a variable named : target_frame
        # default value for variable : turtle1
        # while running the launch file we can override it in cli
            DeclareLaunchArgument(
                'target_frame',
                default_value='turtle1',
                description='target frame name'
            ),

        # running the nodes : 

            Node(
            # ros2 package that contains the executable
                package='turtle_tf2_py',
            # executable name
                executable='turtle_tf2_broadcaster',
            # idk why we care about name
                name='broadcaster1',
            # giving parameter to the node (this dose everything)
                parameters=[
                    {
                        'turtlename' : 'turtle1'
                    }
                # when the node gets the arguments the code inside the node runs :
                # ? [Launch File]
                # ?      │
                # ?      │  passes parameter: turtlename = 'turtle1'
                # ?      ▼
                # ?  [turtle_tf2_broadcaster executable (ALREADY WRITTEN)]
                # ?      │
                # ?      ├── Reads parameter -> knows its target is "turtle1"
                # ?      │
                # ?      ├── Subscribes to -> /turtle1/pose
                # ?      │
                # ?      └── Publishes to  -> /tf (broadcasts turtle1's frame relative to 'world')
                ]
            ),
            Node(
            # ros2 package that contains the executable
                package='turtle_tf2_py',
            # executable name
                executable='turtle_tf2_broadcaster',
            # idk why we care about name
                name='broadcaster2',
            # giving parameter to the node (this dose everything)
                parameters=[
                    {
                        'turtlename' : 'turtle2'
                    }
                # when the node gets the arguments the code inside the node runs :
                # ? [Launch File]
                # ?      │
                # ?      │  passes parameter: turtlename = 'turtle2'
                # ?      ▼
                # ?  [Another instance of turtle_tf2_broadcaster]
                # ?      │
                # ?      ├── Reads parameter -> knows its target is "turtle2"
                # ?      │
                # ?      ├── Subscribes to -> /turtle2/pose
                # ?      │
                # ?      └── Publishes to  -> /tf (broadcasts turtle2's frame relative to 'world')
                ]
            ),

        # THE NODE THAT DOES THE MATH JOB
        # ! it listens where the turtle1 is in relative to the turtle2 and gives out the speed and turning speed to turtle2
            Node(
            # package containing the executable
                package='turtle_tf2_py',
            # executable name
                executable='turtle_tf2_listener',
            # again idk why this matters
                name='listener',
            # giving the parameters needed by the node
                parameters=[
                    {
                        'target_frame' : LaunchConfiguration('target_frame')
                    }
                # ? [ turtlesim_node ] 
                # ?         │ 
                # ?         ├── (publishes /turtle1/pose) ──► [ broadcaster1 ] ──(publishes /tf)──┐
                # ?         │                                                                     │
                # ?         ├── (publishes /turtle2/pose) ──► [ broadcaster2 ] ──(publishes /tf)──┤
                # ?         │                                                                     │
                # ?         │                                                                     ▼
                # ?         │                                                            [ listener node ]
                # ?         │                                                            • Reads /tf
                # ?         │                                                            • Runs math
                # ?         │                                                            • Publishes speed
                # ?         │                                                                     │
                # ?         ▲                                                                     │
                # ?         └────────────────── (publishes to /turtle2/cmd_vel) ──────────────────┘
                ]
            ),
        ]
    )