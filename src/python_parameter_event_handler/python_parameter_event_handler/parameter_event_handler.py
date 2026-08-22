# importing the normal stuff
import rclpy
from rclpy.node import Node

# importing idk what these are
import rclpy.parameter
from rclpy.parameter_event_handler import ParameterEventHandler

# creating the node
class SimpleNodeWithParameters(Node):

# init thingy
    def __init__(self):

    # giving node the name
        super().__init__("node_with_parameter")

    # declaring the parameter :
    # Name of the parameter 
    # default value 
        self.declare_parameter(
            'an_int_parameter',
            0
        )

    # idk what this is but it is used to monitor changes
    # ParameterEventHandler is a SUPER LISTENER it keeps an eye on changes or every single node in the system
        self.handler = ParameterEventHandler(self)

    # here we are setting a alarm based on the above variable which we use to monitor the changes
    # we say to ros (ParameterEventHandler) :
    #   here is the parameter name which i care about
    #   here is node where that parameter is located
    #   and if any change happen to it -> call this function
        self.callback_handle = self.handler.add_parameter_callback(
            parameter_name = "an_int_parameter",
            node_name = "node_with_parameter",
            callback = self.callback
        )

        self.callback_handle2 = self.handler.add_parameter_callback(
            parameter_name="a_double_param",
            node_name="parameter_blackboard",
            callback=self.callback,
        )

        
        self.callback_handle2 = self.handler.add_parameter_callback(
            parameter_name="my_parameter",
            node_name="minimal_param_node",
            callback=self.my_callback,
        )

# the function we want to get triggered when any change happen to the parameter
    def callback(self,p: rclpy.parameter.Parameter) -> None:

    # p is the new version of the parameter that just arrived
    # we convert ros2 data to the normal python int/string data (using parameter_value_to_python)
        self.get_logger().info(f"Received an update to parameter : {p.name} : {rclpy.parameter.parameter_value_to_python(p.value)}")

    def my_callback(self,p: rclpy.parameter.Parameter) -> None:
        self.get_logger().info(f"yooo wtf ...dont panic but this shit is changing : {p.name} : {rclpy.parameter.parameter_value_to_python(p.value)}")


def main():
    rclpy.init()
    node = SimpleNodeWithParameters()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()