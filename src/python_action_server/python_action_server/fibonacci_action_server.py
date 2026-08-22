import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node

# our action file
from custom_action_interface.action import Fibonacci

# just for the effect
import time 

# creating the node class
class FibonacciActionServer(Node):

# the __init__ thing
    def __init__(self):

    # naming the node
        super().__init__('fibonacci_action_server')

    # initiating a new action server :
        # 1. a ros2 node to add the action server to `self`
        # 2. type of action (the one we imported)
        # 3. action name
        # 4. a callback function to execute accepted goals
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            self.execute_callback
        )
    
# the callback function must **return** a message to the **action type**
    def execute_callback(self, goal_handle):

    # informing in the terminal that execution is in process
        self.get_logger().info('Executing ...')

    #! LOGIC for fibonacci (without feedback) : 
        # sequence = [0,1]
        # for i in range(1, goal_handle.request.order):
        #     # i      = 1           = 2           = 3             = ...
        #     # append = (s[1]+s[0]) = (s[2]+s[1]) = (s[3] + s[2]) = ...
        #     # append = (1 + 0)     = (1 + 1)     = (2 + 1)       = ...
        #     sequence.append(sequence[i] + sequence[i-1])

    #! LOGIC for fibonacci :
    # creating a FEEDBACK OBJECT that ros2 found in the fibonacci.action file
        feedback_msg = Fibonacci.Feedback()
        feedback_msg.partial_sequence = [0,1]

        for i in range(1, goal_handle.request.order):
            feedback_msg.partial_sequence.append(feedback_msg.partial_sequence[i] + feedback_msg.partial_sequence[i-1])
            self.get_logger().info(f'Feedback : {feedback_msg.partial_sequence}')
            goal_handle.publish_feedback(feedback_msg)
            time.sleep(1)

    # giving the action client the info about SUCCESS of process
        goal_handle.succeed()

    # informing in the terminal that execution is in completed
        self.get_logger().info('Goal completed !!!')

    # creating the RESULT OBJECT that ROS2 found in the Fibonacci.action file
        result = Fibonacci.Result()

    # passing values to the variable
        result.sequence = feedback_msg.partial_sequence

    # giving out the result (an obj of RESULT from Fibonacci.action file)
        return result


def main(args=None):
    rclpy.init(args=args)
    Fibonacci_action_server = FibonacciActionServer()
    rclpy.spin(Fibonacci_action_server)


if __name__ == "__main__":
    main()