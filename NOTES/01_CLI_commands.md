# ROS 2 commands

---

## Basic CLI :

- `ros2 node list`
- `ros2 topic list`
- `ros2 service list`
- `ros2 action list`

---

## Nodes

- `ros2 run <package_name> <exactable_name>`
    - to run a specific node
    - EXAMPLE : 
        - `ros2 run turtlesim turtlesim_node`
        - `ros2 run turtlesim turtle_teleop_key`

- `ros2 node list`
    - gives the list of running nodes in the system

### Remapping

- assigning the default node properties(node name, topic, services) to a custom value.
- EXAMPLE : 
    - `ros2 run turtlesim turtlesim_node --ros-args --remap __node:=my_turtle`
    - now if we try `ros2 node list` we will see a new node appear with the name /my_turtle

### info

- `ros2 node info <node_name>
- EXAMPLE : 
    - `ros2 node info /my_turtle`

- this gives a list of subscribers ,publishers ,services and actions about the node

---

### rqt_graph

we use `rqt_graph` to visualize data sharing between diff nodes

- `ros2 run rqt_graph rqt_graph`

---

## Topics

- `ros2 topic list`
    - returns the topics currently active in the system

- `ros2 topic list -t` 
    - returns the topics running with their message type in "[]"

- `ros2 topic echo <topic_name>`
    - we just created a node that will be receiving the inputs from the topic (the messages given to the topic from the publisher)
    - EXAMPLE : 
        - `ros2 topic echo /turtle1/cmd_vel`

- `ros2 topic info <topic_name>`
    - getting clean info about the topic 
    - EXAMPLE :
    - `ros2 topic info /turtle1/cmd_vel`

- `ros2 topic info <topic_name> --verbose`
    - gives detailed and additional info about the topic

- `ros2 interface show <msg_type>`
    - we cna use this to know what structure of input the topic expects 
    - EXAMPLE :
    - `ros2 interface show geometry_msgs/msg/Twist`   (msg type from the /turtle1/cmd_vel topic)

### Publishing manually from the terminal

As now we have the message structure a topic need we can directly give inputs from the terminal    
- `ros2 topic pub <topic_name> <msg_type> '<args>'`

- EXAMPLE :
    - Structure used here : 
    ```
    Vector3  linear
        float64 x
        float64 y
        float64 z
    Vector3  angular
        float64 x
        float64 y
        float64 z
    ```
    (only the linear: {x} and angular: {z} works because the turtlesim is in 2d)
    - `ros2 topic pub /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"` --> does nothing forever

    - `ros2 topic pub /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 4.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"` --> moves 4 units forward forever 
    - `ros2 topic pub /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: -4.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"` --> moves 4 units backward forever
    - `ros2 topic pub /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 2.0}}"` --> rotates +2 radians forever
    - `ros2 topic pub /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: -2.0}}"` --> rotates -2 radians forever

    - we can also publish the input only once: (using `--once` optional arg)
    - `ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"` --> does nothing once and exits

- hz : frequency of the arriving messages

    - `ros2 topic hz <topic_name>`
    - EXAMPLE : 
        - `ros2 topic hz /turtle1/pose`

- bw : bandwidth of the arriving messages (network usage)

    - `ros2 topic bw <topic_name>`
    - EXAMPLE :
        - `ros2 topic bw /turtle1/pose`

### find a topic

- `ros2 topic find <topic_type>`
    - EXAMPLE :
        - `ros2 topic find geometry_msgs/msg/Twist` (gives out : /turtle1/cmd_vel)

---

## Service

(make sure turtlesim_node and turtle_teleop_key is running)

- `ros2 service list`
    - this returns all the services available for the currently running system

- `ros2 service list -t`
    - shows the type of each service

- `ros2 service type <service_name>`
    - EXAMPLE :
        - `ros2 service type /clear`
        - *in output* `EMPTY` means the service call sends no data nor receive any data (default)

- `ros2 service info /clear`
    - gives the count of the clients and services

- **FIND** : `ros2 interface find <type_name>`
    - EXAMPLE :
        - `ros2 interface find std_srvs/srv/Empty` --> (/clear and /reset)

- **show** : `ros2 interface show <service_name>

tells us the data we need to send to the service in order to us it
    
- `rso2 interface show std_srvs/srv/Empty` 
    - gives out nothing as we need nothing to use the service

- `ros2 interface show turtlesim/srv/Spawn`
    - gives out rq args to use the service

### Service call

- `ros2 service call <service_name> <service_type> <arguments>

- EXAMPLE :
    - `ros2 service call /clear std_srvs/srv/Empty`
        - clears the path yet without affecting the turtle position

    - `ros2 service call /spawn turtlesim/srv/Spawn "{x: 2, y: 2, theta: 0.2, name: 'turtle2'}"`
        - a new turtle spawns that can be controlled by the `ros2 topic pub` command

---

## Parameters

(make sure turtlesim and turtle_teleop_key is running)

Parameters are config value or settings of the given node, each node has its own parameters that can be float, integer, boolean, string, list.

- `ros2 param list`
    - gives out the list of the parameters for each active node in the system.

### `get`

We can get the value of a parameter from a node.

- `ros2 param get <node_name> <parameter_name>`
    - EXAMPLE :
        - `ros2 param get /turtlesim background_r`
        - `ros2 param get /turtlesim background_g`
        - `ros2 param get /turtlesim background_b`

### `set`

We can also set the value of a parameter of a known node at the runtime for the current session

- `ros2 param set <node_name> <parameter_name> <new_value>`
    - EXAMPLE :
        - `ros2 param get /turtlesim background_r 0`

### `dump`

The values set by the `set` variable are just for the current session, in order to save them for future use we need to `dump` those configs. into a .yaml file

- `ros2 param dump <node_name> > <file_name>.yaml`
    - EXAMPLE : 
        - `ros2 param dump /turtlesim > turtlesim.yaml`
        - `ros2 param dump /teleop_turtle > teleop_turtle.yaml`
    - Saves the file in current location of the terminal

### `load`

We can load a .yaml dump file we created to get the parameters we created in current session.

- `ros2 param load <node_name> <file_name>.yaml`
    - EXAMPLE : 
        - `ros2 param load /turtlesim turtlesim.yaml`
        - `ros2 param load /teleop_turtle teleop_turtle.yaml`
    - changes the current session state to the state in the file

(read only parameters can we edited and loaded)

- **LOADING THE CONFIG FILE AT THE NODE STARTUP**
    
    -  `ros2 run <package_name> <executable_name --ros-args --params-file <file_name>.yaml`
        - EXAMPLE : 
            - `ros2 run turtlesim turtlesim_node --ros-args --params-file turtlesim.yaml`
            - `ros2 run turtlesim turtle_teleop_key --ros-args --params-file teleop_turtle.yaml`

---

## Actions

- `ros2 run turtlesim turtlesim_node` -> this opens a turtlesim with turtle in it

- `ros2 run turtlesim turtle_teleop_key` 
    - this returns :
    - `Use g|b|v|c|d|e|r|t keys to rotate to absolute orientations. 'f' to cancel a rotation.'q' to quit.`
    - these are the **actions** that can be used to control the orientation of the turtle in the sim....these can be aborted mid task and they report the task status (complete, failed, etc...)

- actions are a form for long-running task, it consist of three parts:
    - **Goal :**  the initial request sent to the robot
        - EXAMPLE : when we press `E` in the turtle_teleop_key we give turtle the goat to rotate in the top left direction
    - **Feedback :** continuous updates given by the robot
        - *rotated 10 degree, 20 degree, 30 degree etc...*
    - **Result :**  informing about the success or the failure of the task
        - EXAMPLE :
            - when we press `E` in turtle_teleop_key : once the motion is completed we get a message :
                - `[INFO] [1784866647.562063209] [turtlesim]: Rotation goal completed successfully`
            - when we press `E` and press `V` before the completion of the action we get a message of abortion of the goal to turn to `E` :
                - `[WARN] [1784866938.505536597] [turtlesim]: Rotation goal received before a previous goal finished. Aborting previous goal`

- **NODE INFO**
    - `ros2 node info /turtlesim`
        - in the bottom we can see the actions sections : 
            - `Action Servers : /turtle1/rotate_absolute: turtlesim/action/RotateAbsolute`
            - `Action Clients : - `

    - `ros2 node info /turtle_teleop_key`
        - in the bottom we can see the action sections :
            - `Action Servers : -`
            - `Action Clients : /turtle1/rotate_absolute: turtlesim/action/RotateAbsolute`

### action commands

- `ros2 action list`
    - this tells us all the actions available in the current running system

- to know all the actions available in the current running system **alongside its type**
    - `ros2 action list -t`
    
- to know the type of a specific actions
    - `ros2 action type /turtle1/rotate_absolute`

- `ros2 action info <action>`
    - EXAMPLE : `ros2 action info /turtle1/rotate_absolute`

- `ros2 interface show turtlesim/action/RotateAbsolute`
    - output :
        - first section : the structure(datatype) the goal requests
        - second section : the structure of the result
        - last section : the structure of the feedback

### send goals

- `ros2 action send_goal <action_name> <action_type> <values>` (values need to be in yaml format)

- EXAMPLE : 
    - `ros2 action send_goal /turtle1/rotate_absolute turtlesim/action/RotateAbsolute`

- With value and to get **FEEDBACK**:
    - `ros2 action send_goal /turtle1/rotate_absolute turtlesim/action/RotateAbsolute "{theta : -2}" --feedback`

---

## rqt_console

> a gui tool to collect the log data for close examination

- `ros2 run rqt_console rqt_console`

- Message level : (assumption)
    - **Fatal** the system is going to terminate to try to protect itself from damage 
    - **Error** issue that are preventing system to function properly
    - **Warm** represent non-ideal results that represent deeper issue
    - **Info** event and status update , system running normally
    - **Debug** step by step process of the system execution

---

## Launching Nodes

> we can use a launch file to launch multiple nodes at onces

- `ros2 launch <package_name> <launch_file>`

- EXAMPLE :
    - `ros2 launch turtlesim multisim.launch.py`

> this launches the following launch file written in python (launch files will be discussed further)
```python
from launch import LaunchDescription
import launch_ros.actions


def generate_launch_description():
    return LaunchDescription([
        launch_ros.actions.Node(
            namespace='turtlesim1', package='turtlesim',
            executable='turtlesim_node', output='screen'),
        launch_ros.actions.Node(
            namespace='turtlesim2', package='turtlesim',
            executable='turtlesim_node', output='screen'),
    ])
```

- we can control each node by : `ros2 topic pub` for `turtle1` and `turtle2`

---

## Recording and playing back data

> so we could record the data published by the topic and a service to play it again anytime we want

### Recording topics

> keep the turtlesim_node and he turtle_teleop_key running in the background

> `ros2 bag...` is used to work with recording
- `ros2 bag record` makes recoding files and saves....it is better to make clean folders to manage the recordings
```bash
mkdir ros2_content
cd ros2_content
```

- Topics to record : 
    - `/turtle1/cmd_vel` <- the input topic
    - `/turtle1/pose` <- the output topic
    - To visualize the topics :
        - `ros2 topic echo /turtle1/cmd_vel` 
        - `ros2 topic echo /turtle1/pose` 

- `ros2 bag record <topic_name>
    - EXAMPLE :
        - `ros2 bag record /turtle1/cmd_vel`
        - `ros2 bag record /turtle1/pose`
    - OR record multiple nodes at once : 
        - `ros2 bag record /turtle1/cmd_vel /turtle1/pose`
    - TO SAVE THE RECORDING WITH INTENTIONAL NAME
        - `ros2 bac record -o recording_name /turtle1/cmd_vel /turtle1/pose`

- **Inspecting the topic**

> make sure you are in the folder where the recording was saved

- `ros2 bag info <recording_name>
    - EXAMPLE : (if file saved using `-o <name>`)
        - `ros2 bag info subset`

### Playing topics

> make sure you are in the same folder as recording or use the recording file path

- `ros2 bag play <recording_name>`
    - EXAMPLE : (if file saved using `-o <name>`)
        - `ros2 bag play subset`

### Recording a service

> we can not directly record services as they are continuously running between nodes only....we need to use the introspection client/server that shouts everything the services do so we could record them

- run these commands in two separate terminals
    - `ros2 run demo_node_cpp introspection_service --ros-args -p service_configure_introspection:=contents`
    - `ros2 run demo_node_cpp introspection_client --ros-args -p service_configure_introspection:=contents`

- **Checking service availability** as ros2 can only record data from the available services, and the services with service introspection **enabled**
    - `ros2 service list`
        - gives the list of services available in the system
    - `ros2 service echo <service_name>` or for clean info `ros2 service echo --flow-state <service_name>`
        - if we see the service communication this means we can use the introspection

- TO record : `ros2 bag record --service <service_name>`
    - EXAMPLE : 
        - `ros2 bag record --service /add_two_ints`
    - To record all services : `ros2 bag record --all-services`

- TO play : `ros2 bag play --publish-service-request <recording_name>`
    - EXAMPLE :
        - `ros2 bag play --publish-service-requests ros2_contents/rosbag2_2026_07_28-10_29_39/rosbag2_2026_07_28-10_29_39_0.mcap`
    - we will see changes in the terminal that is currently running : `ros2 run demo_nodes_cpp introspection_service --ros-args -p service_configure_introspection:=contents`