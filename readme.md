# Learning ROS2 (JAZZY) from the official documentation

official doc : [link](https://docs.ros.org/en/jazzy/Tutorials.html) (its not easy but much cleaner then any youtube tutorial)

## NOTES

> this folder has the notes i though to note while going through the documentation

## Packages

> in the tutorial we created many packages (i choose python to continue to reduce the complexity)

### 1) [my_package](src/my_package)

- Learnt to create a python package using command :
```zsh
ros2 pkg create --build-type ament_python --license <Any_license> my_package
```
- Edited the entry points in [setup.py](src/my_package/setup.py) and edited [package.xml](src/my_package/package.xml)

### 2) [py_pubsub](src/py_pubsub)

- Created [publishe](src/py_pubsub/py_pubsub/publisher_member_function.py) and [subscribe](src/py_pubsub/py_pubsub/subscriber_member_function.py) node
    - Publisher : screams the "Hello world i"
    - Subscriber : listens to it and prints it in the terminal

- Edited entry points in setup.py
- Added the using dependencies in package.xml

- **How to use :**
    - Terminal 1 :
    ```zsh
        ros2 run py_pubsub talker
    ```
    - Terminal 2 :
    ```zsh
        ros2 run py_pubsub listener
    ```

### 3) [py_servli](src/py_servli)

- Created [service](src/py_servli/py_servli/service_member_function.py) and [client](src/py_servli/py_servli/client_member_function.py) node that uses the **built-in interface** : `example_interface` (AddTwoInts)

- **How to use:**
    - Terminal 1 :
    ```zsh
        ros2 run py_servli service
    ```
    - Terminal 2 :
    ```zsh
        ros2 run py_servli client 10 12
    ```

### 4) [tutorial_interfaces](src/tutorial_interfaces)

> interface packages are created in `ament_cmake` (not in strict python package)
```zsh
ros2 pkg create --build-type ament_cmake --license <Any_license> tutorial_interfaces
```

- Learned to create our own custom interfaces [msg](src/tutorial_interfaces/msg) and [srv](src/tutorial_interfaces/srv) and used them in pub-sub , ser-cli

- The `cmake` package structure is very diff from `python`
- Edited the [package.xml](src/tutorial_interfaces/package.xml)
    - buildtool_depend
    - test_depend
    - exec_depend
    > all needed to create interfaces out of the `msg/` and `srv/`


#### a) [my_pubsub](src/my_pubsub)

- used the `msg/` : [`Num.msg`](src/tutorial_interfaces/msg/Num.msg) as a interface in the publisher-subscriber
    - publisher screams the `num` and subscriber listens and displays in the terminal

- **How to use?**
    - Terminal 1 :
    ```zsh
        ros2 run my_pubsub speaker
    ```
    - Terminal 2 :
    ```zsh
        ros2 run my_pubsub listener
    ```

#### b) (my_servli)[src/my_servli]

- used the `srv/` : [`AddThreeInts.srv`](src/tutorial_interfaces/srv/AddThreeInts.srv) as a interface between client-service
    - we give client 3 integers
    - which are then shared with service which calculates sum of those 3 integers and give back to client
    - the client receive the response and tells us the output in the terminal

- **How to use?**
    - Terminal 1 :
    ```zsh
        ros2 run my_servli service
    ```
    - Terminal 2 :
    ```zsh
        ros2 run my_servli client 12 56 109
    ```


### 5) [custom_interfaces](https://github.com/Abhinav08bhatt/address_book_ros_ws)

> the official tutorial taught us to create : interface + nodes in one single package, but that method was strictly using `cmake` (and i don't work with it yet)

- I created 3 different `python` packages
    - interface
    - pub-sub
    - ser-cli

used the interface inside the pub-sub and ser-cli all by myself

> follow the link to view the package : https://github.com/Abhinav08bhatt/address_book_ros_ws

### 6) [python_parameters](src/python_parameters)

> no clue rn