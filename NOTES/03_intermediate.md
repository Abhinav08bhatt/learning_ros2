# Intermediate

---

## `rosdep`

> helps us download metadata packages for ros. (usually this is the thing that downloads stuff in package.xml)

- **package.xml** tags :

    - `<depend>`
        - built time and run time dependencies for package
        - generally `cpp` packages needs this, pure `python` packages does not need

    - `<build-depend>`
        - if dependency is only needed to build the code and not at execution time

    - `<build_export_depend>`
        - if our package exports a package that includes header a dependency, we will need to us this with our dependency

    - `<exec_depend>`
        - Declares dependencies for shared lib, executable, python module, launch file while **running** the package
    
    - `<test_depend>`
        - dependencies needed by test

---

## Creating an action 

> (created in same package as other interfaces : msg, srv)

- structure of .action : 

```action
# Request
---
# Result
---
# Feedback
```

- .action here : `Fibonacci.action`
    ```action
    int32 order
    ---
    int32[] sequence
    ---
    int32[] partial_sequence
    ```
    - The goal request is the `order` of the Fibonacci sequence
    - The result is the `sequence`
    - The feedback is `partial_sequence` computed so far

### Building the action

- CMakeList : 
    ```txt
    find_package(rosidl_default_generators REQUIRED)

    rosidl_generate_interfaces(${PROJECT_NAME}
        "action/Fibonacci.action"
    )
    ```

- package.xml :
    ```xml
    <buildtool_depend>rosidl_default_generators</buildtool_depend>
    <member_of_group>rosidl_interface_packages</member_of_group>
    ```

### Checking the interface :

```zsh
ros2 interface show custom_action_interface/action/Fibonacci
```