# importing the lib we know we have done it before
import rclpy
from rclpy.node import Node

# creating a node 
class MinimalParam(Node):

# init thing
    def __init__(self):
    # giving the node a name : minimal_param_node (executable_name they call it)
        super().__init__('minimal_param_node')

    # this is optional but we are giving out parameter a description that we can look using the command :
        """
        ros2 param describe /minimal_param_node my_parameter
        """
        from rcl_interfaces.msg import ParameterDescriptor
        my_parameter_description = ParameterDescriptor(description='idk what this is yet but tutorial said its my parameter???Is it?')

    # we are DECLARING a PARAMETER :
    # NAMED : my_parameter
    # DEFAULT VALUE : world 
        self.declare_parameter('my_parameter','world',my_parameter_description)

        """the parameter type is the same as the type of the default value : in this case -> STRING"""

    # every 1 sec the node runs we calls function : timer_callback()
        self.timer = self.create_timer(
            1,
            self.timer_callback
        )

# THE function
    def timer_callback(self):

    # with this line we are getting the parameter "my_parameter" and storing it in "my_param" with its type (STRING)
        my_param = self.get_parameter("my_parameter").get_parameter_value().string_value

    # logging in the terminal to view the ..uk whatever is going on
        self.get_logger().info('Hello %s'%my_param)

    # this is some BS idk
        my_new_param = rclpy.parameter.Parameter(
            'my_parameter',
            rclpy.Parameter.Type.STRING,
            'world'
        )
        all_new_parameters = [my_new_param]
        self.set_parameters(all_new_parameters)
    # the documentation says it makes sure that the parameters sets to the default even if the user ties to change it from the terminal

# the main and stuff uk
def main():
    rclpy.init()
    node = MinimalParam()
    rclpy.spin(node)

if __name__=="__main__":
    main()