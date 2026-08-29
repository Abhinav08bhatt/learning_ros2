# the imports

from launch import LaunchDescription
# the main container object, every launch file mst return this

from launch.actions import IncludeLaunchDescription
# lets us call and run another launch file from this file

from launch.actions import GroupAction
from launch_ros.actions import PushROSNamespace
# using this we can wrap a node or group of nodes to have same namespace instead of writing in every child file

from launch.substitutions import PathJoinSubstitution
# finds and join the paths of folder/files

from launch_ros.substitutions import FindPackageShare
# substitution that finds installed directory of package

# the main function
def generate_launch_description():

# creating a usable path that points to folder containing all the launch files
    launch_dir = PathJoinSubstitution(
        [
            FindPackageShare(
                'launch_turtle'
            ),'launch'
        ]
    )

# running the stuff starts here
    return LaunchDescription(
        [

        # includes and execute the file
            IncludeLaunchDescription(
                PathJoinSubstitution(
                    [
                        launch_dir,
                        'turtlesim_world_1_launch.py'
                    ]
                )
            ),
        # edited -----------------------------------------
        # includes and execute the file
            # IncludeLaunchDescription(
            #     PathJoinSubstitution(
            #         [
            #             launch_dir,
            #             'turtlesim_world_2_launch.py'
            #         ]
            #     )
            # ),

        # groups everything that is inside the actions list
            GroupAction(
                actions=[

                # PREPENDS /turtlesim2/ to every node,topic and service that starts after this line 
                    PushROSNamespace('turtlesim2'),

                # includes and executes the file - with /turtlesim2/ prepended
                    IncludeLaunchDescription(
                        PathJoinSubstitution(
                            [
                                launch_dir,
                                'turtlesim_world_2_launch.py'
                            ]
                        )
                    ),
                ]
            ),
        # ------------------------------------------------

        # added later ------------------------------------
        # includes and executes the file
            IncludeLaunchDescription(
                PathJoinSubstitution(
                    [
                        launch_dir,
                        'turtlesim_world_3_launch.py'
                    ]
                )
            ),
        # ------------------------------------------------

        # includes and executes the file
            IncludeLaunchDescription(
                PathJoinSubstitution(
                    [
                        launch_dir,
                        'broadcast_listener_launch.py'
                    ]
                ),
            # overrides the default arguments
                launch_arguments={
                    'target_frame': 'carrot1'
                }.items()
                #  use carrot1 instead
            ),

        # includes and executes the file
            IncludeLaunchDescription(
                PathJoinSubstitution(
                    [
                        launch_dir,
                        'mimic_launch.py'
                    ]
                )
            ),

        # includes and executes the file
            IncludeLaunchDescription(
                PathJoinSubstitution(
                    [
                        launch_dir,
                        'fixed_broadcaster_launch.py'
                    ]
                )
            ),

        # includes and executes the file
            IncludeLaunchDescription(
                PathJoinSubstitution(
                    [
                        launch_dir,
                        'turtlesim_rviz_launch.py'
                    ]
                )
            ),
        ]
    )


"""
-----------------------------------------------------------------------------------
NAMESPACE / TOPIC NAMES

full topic name = / namespace / turtle_name / topic_name

-----------------------------------------------------------------------------------
THE WORLDS CREATED

WORLD    -    NAMESPACE   -   TURTLE INSIDE
-----------------------------------------------------------------------------------
world1   -      none      -   turtle1 , turtle2(spawns)
world2   -   /turtlesim2  -   turtle1
world3   -   /turtlesim3  -   turtle1
-----------------------------------------------------------------------------------

WORLD 1 
    - namespace                 :   default/root(/)
    - Node name                 :   /sim (or /turtlesim)
    - /turtle1                  <-   the leader, created by default
        - pose topic            :   /turtle1/pose
        - commanded velocity    :   /turtle1/cmd_vel
    - /turtle2                  <-   the follower, spawned auto by listener (in broadcaster file)
        - pose topic            :   /turtle2/pose
        - commanded velocity    :   /turtle2/cmd_vel

WORLD 2 : 
    - namespace                 :   /turtlesim2
    - Node name                 :   /turtlesim2/sim
    - /turtle1                  <-  created by default
        - pose topic            :   /turtlesim2/turtle1/pose
        - commanded velocity    :   /turtlesim2/turtle1/cmd_vel

WORLD 3 :  
    - namespace                 :   /turtlesim3
    - Node name                 :   /turtlesim3/sim
    - /turtle1                  <-  created by default
        - pose topic            :   /turtlesim3/turtle1/pose
        - commanded velocity    :   /turtlesim3/turtle1/cmd_vel

-----------------------------------------------------------------------------------

1. YOU DRIVE TURTLE 1 (via teleop / topic pub)
    └── You publish to: /turtle1/cmd_vel
            │
            ▼
2. TURTLE 1 MOVES in Window 1
    └── /broadcaster1 reads /turtle1/pose ────> Broadcasts turtle1 frame to /tf
                                                         │
3. LISTENER NODE DOES TF MATH                            ▼
    └── /broadcaster2 reads /turtle2/pose ────> Broadcasts turtle2 frame to /tf
    └── /listener calculates distance/angle between turtle1 & turtle2
    └── /listener publishes to: /turtle2/cmd_vel
            │
            ▼
4. TURTLE 2 CHASES TURTLE 1 in Window 1
            │
            ├── (turtle2 moves, emitting /turtle2/pose)
            │
            ▼
5. MIMIC NODE COPIES TURTLE 2
    └── /mimic reads: /turtle2/pose (via remapping)
    └── /mimic publishes to: /turtlesim2/turtle1/cmd_vel (via remapping)
            │
            ▼
6. TURTLE 1 IN WINDOW 2 MOVES
    └── The turtle in Window 2 mimics whatever turtle2 in Window 1 is doing
"""