from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, PythonExpression
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    sim_rviz = PythonExpression([
        "'false' if '", LaunchConfiguration('mode'), "' == 'mppi' else 'true'"
    ])

    nav_rviz = PythonExpression([
        "'true' if '", LaunchConfiguration('headless'), "' != 'true' else 'false'"
    ])

    simulation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('simulation'),
                'launch',
                'simulation.launch.py',
            ])
        ),
        launch_arguments={
            'world': LaunchConfiguration('world'),
            'headless': LaunchConfiguration('headless'),
            'use_rviz': sim_rviz,
        }.items(),
    )

    base = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('bringup'),
                'launch',
                'bringup_base.launch.py',
            ])
        ),
        launch_arguments={
            'use_sim_time': 'true',
            'use_rviz': nav_rviz,
            'mode': LaunchConfiguration('mode'),
            'train': LaunchConfiguration('train'),
            'policy': LaunchConfiguration('policy'),
        }.items(),
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'world',
            default_value='tekno_world',
            description='World name without .sdf (tekno_world or mppi_test_world).',
        ),
        DeclareLaunchArgument(
            'mode',
            default_value='mppi',
            description='Controller selection: mppi, rl, or mppi_rl.',
        ),
        DeclareLaunchArgument(
            'train',
            default_value='false',
            description='Enable RL training.',
        ),
        DeclareLaunchArgument(
            'policy',
            default_value='',
            description='Saved policy file for RL evaluation.',
        ),
        DeclareLaunchArgument(
            'headless',
            default_value='false',
            description='Run Gazebo in headless mode.',
        ),
        simulation,
        base,
    ])
