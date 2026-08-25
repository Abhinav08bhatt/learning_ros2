from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription,GroupAction
from launch_ros.actions import PushROSNamespace
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    launch_dir = PathJoinSubstitution(
        [
            FindPackageShare(
                'launch_turtle'
            ),'launch'
        ]
    )
    return LaunchDescription(
        [
            IncludeLaunchDescription(
                PathJoinSubstitution(
                    [
                        launch_dir,
                        'turtlesim_world_1_launch.py'
                    ]
                )
            ),
        # edited -----------------------------------------
            # IncludeLaunchDescription(
            #     PathJoinSubstitution(
            #         [
            #             launch_dir,
            #             'turtlesim_world_2_launch.py'
            #         ]
            #     )
            # ),
            GroupAction(
                actions=[
                    PushROSNamespace('turtlesim2'),
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
            IncludeLaunchDescription(
                PathJoinSubstitution(
                    [
                        launch_dir,
                        'turtlesim_world_3_launch.py'
                    ]
                )
            ),
        # ------------------------------------------------
            IncludeLaunchDescription(
                PathJoinSubstitution(
                    [
                        launch_dir,
                        'broadcast_listener_launch.py'
                    ]
                ),
                launch_arguments={
                    'target_frame': 'carrot1'
                }.items()
            ),
            IncludeLaunchDescription(
                PathJoinSubstitution(
                    [
                        launch_dir,
                        'mimic_launch.py'
                    ]
                )
            ),
            IncludeLaunchDescription(
                PathJoinSubstitution(
                    [
                        launch_dir,
                        'fixed_broadcaster_launch.py'
                    ]
                )
            ),
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
