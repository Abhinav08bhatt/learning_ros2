# Client Libraries

---

## Creating a workspace

> the workspace follows proper naming of the folders and files

- creating the folder that will hold our files and folder related to the particular example
```bash
mkdir ros2_ws
cd ros2_ws
```

- `src` folder is where we do everything
```bash
mkdir src
```

---

## Using `colcon` to build packages

- colcon perform out of source builds. By default it will create teh following directories as peers of `src` directory
    - `build`
    - `install`
    - `log`

- **Cloning example repo to the `/src`**

(run inside the `/ros2_ws` location)

    - `git clone https://github.com/ros2/examples src/examples -b jazzy`

- **Build the workspace**

(we run this command in the `root folder of ros workspace`, and it installs and builds the req stuff for the things present inside the `/src`)
    - `colcon build`
> use --executor sequential if CPU is a limit

### Trying the demo

- Terminal 1 :
    - `ros2 run examples_rclcpp_minimal_subscriber subscriber_member_function`

- Terminal 2 :
    - `ros2 run examples_rclcpp_minimal_publisher publisher_member_function`


---

## ROS2 package

> ROS 2 python and cmake packages have their own minimum req contents

- Python :
    - `package.xml` : file containing meta information about the package
    - `resource/<package_name>` : marker file for the package
    - `setup.cfg` : is required when a package has executables, so `ros2 run` can file them
    - `<package_name>` : a directory with the same name as your package used by ros2 tools to find your package contains `__init__.py`
```txt
my_package/
      package.xml
      resource/my_package
      setup.cfg
      setup.py
      my_package/
```

- CMake :
    - `CMakeLists.txt` : file that describe how to build the code within the package
    - `include/<package_name>` : directory containing the public headers for the package
    - `package.xml` : file containing meta information about the package
    - `src` : directory containing the source code for the package
```txt
my_package/
     CMakeLists.txt
     include/my_package/
     package.xml
     src/
```

> in a single workspace there can be as many packages as we want but each in their own folder inside the `/src`

### Creating a new python package

> inside the /ros2_ws/src

- `ros2 pkg create --build-type ament_python --license Apache-2.0 <package_name>`
    - EXAMPLE (here) :
        - `ros2 pkg create --build-type ament_python --license Apache-2.0 --node-name my_node my_package`

- **BUILD the package** (inside the `/ros2_ws`)

    - `colcon build`

    - To build a specific package : 
        - `colcon build --package-select my_package`

- **SOURCE the setup** (or create a new terminal instance)

    - `source install/setup.zsh`

- **USE the package**

    - `ros2 run my_package my_node`

- **Contents inside the package**

    - `ls src/my_package`

- **Editing the package.xml** (putting intentional info into the auto generated file)

    - editing the maintainer email, license, description

```xml
 ❯ cat src/my_package/package.xml 
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>my_package</name>
  <version>0.0.0</version>
  <description>beginner client lib tutorials practice</description>
  <maintainer email="random@gmail.com">avi</maintainer>
  <license>Apache-2.0</license>

  <test_depend>ament_copyright</test_depend>
  <test_depend>ament_flake8</test_depend>
  <test_depend>ament_pep257</test_depend>
  <test_depend>python3-pytest</test_depend>

  <export>
    <build_type>ament_python</build_type>
  </export>
</package>
```

- **Editing the setup.py**

    - editing the maintainer, email, description to match `package.xml`

```py
from setuptools import find_packages, setup

package_name = 'my_package'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='avi',
    maintainer_email='random@gmail.com',
    description='beginner client lib tutorials practice',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'my_node = my_package.my_node:main'
        ],
    },
)
```

---

## Writing a simple publisher and subscriber (python)

> Node are executable processes that communicate over the ros graph. in this example we create one node that publishes data and the other subscriber to the topic so it can receive that data

- **Create a new package** (in the ros2_ws/src)

    - `ros2 pkg create --build-type ament_python --license Apache-2.0 py_pubsub
    
    - rest in the ros2_ws

---

## Writing a simple service and client