# importing stuff
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

# importing the action thing
from custom_action_interface.action import Fibonacci


# our node
class FibonacciActionClient(Node):

# init thingy
    def __init__(self):

    # giving node a name
        super().__init__("fibonacci_action_client")

    # creating action client :
        # 1. ros2 node to add action client on : self
        # 2. type of action : Fibonacci
        # 3. action name : 'fibonacci' (same as action server)
        self.action_client = ActionClient(
            self,
            Fibonacci,
            'fibonacci'
        )

# the function
    def send_goal(self, order):

    # making a FEEDBACK OBJECT from the Feedback.action file
        goal_msg = Fibonacci.Goal()
    # giving it the argument of the function
        goal_msg.order = order

    # waiting for the server to be available
        self.action_client.wait_for_server()

        self.send_goal_future = self.action_client.send_goal_async(goal_msg)
        self.send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self,future):

        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info("Goal rejected :(")

        self.get_logger().info("Goal accepted :)")

        self.get_result_future = goal_handle.get_result_async()
        self.get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self,future):

        result = future.result().result
        self.get_logger().info(f"Result {result.sequence}")
        rclpy.shutdown()


# code starts here
def main(args=None):

# we stats the rclpy engine
    rclpy.init(args=args)

# we initiate the class
    action_client = FibonacciActionClient()

    action_client.send_goal(10)

    rclpy.spin(action_client)

# code starts here actually
if __name__ == "__main__":
    main()



"""  
--------------------- it was this before i sold my soul -----------------------
"""

# # importing stuff
# import rclpy
# from rclpy.node import Node
# from rclpy.action import ActionClient

# # importing the action thing
# from custom_action_interface.action import Fibonacci


# # our node
# class FibonacciActionClient(Node):

# # init thingy
#     def __init__(self):

#     # giving node a name
#         super().__init__("fibonacci_action_client")

#     # creating action client :
#         # 1. ros2 node to add action client on : self
#         # 2. type of action : Fibonacci
#         # 3. action name : 'fibonacci' (same as action server)
#         self.action_client = ActionClient(
#             self,
#             Fibonacci,
#             'fibonacci'
#         )

# # the function
#     def send_goal(self, order):

#     # making a FEEDBACK OBJECT from the Feedback.action file
#         goal_msg = Fibonacci.Goal()
#     # giving it the argument of the function
#         goal_msg.order = order

#     # waiting for the server to be available
#         self.action_client.wait_for_server()

#     # sending the goal to the server
#         return self.action_client.send_goal_async(goal_msg)
#     # and returning a PROMISE to the main function



# # code starts here
# def main(args=None):

# # we stats the rclpy engine
#     rclpy.init(args=args)

# # we initiate the class
#     action_client = FibonacciActionClient()

# # we give the "send_goal" function from the class the value 10
# # in return we get a promise that it is going to send this 10 to the server
#     future = action_client.send_goal(10)

# # once the 10 reaches the server and server says, yea i can do it JOB ACCEPTED
# # we start the node AS LONG AS WE GET THE RESPONSE FROM SERVER : yo i am done, JOB FINISHED
#     rclpy.spin_until_future_complete(action_client, future)

# # code starts here actually
# if __name__ == "__main__":
#     main()