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

# the start of chain
    def send_goal(self, order):
        """
        this function returns a FUTURE OBJECT (empty right now)
        - it represent a promise that someday the server will tell us : GOAL ACCEPTED (or not)
        """
    # making a FEEDBACK OBJECT from the Feedback.action file
        goal_msg = Fibonacci.Goal()
    # giving it the argument of the function
        goal_msg.order = order

    # waiting for the server to be available
        self.action_client.wait_for_server()

    # making the future object (empty rn but with promise) (when we dont have to see the feedback)
        # self.send_goal_future = self.action_client.send_goal_async(goal_msg) 

    # making the future object (empty rn but with promise) but also telling that if we get ANY FEEDBACK we will callback the function
        self.send_goal_future = self.action_client.send_goal_async(goal_msg, feedback_callback = self.feedback_callback)

    # add_done_callback tells ROS : the moment the future gets a value -> jump to callback function
        self.send_goal_future.add_done_callback(self.goal_response_callback)

# once the send_goal function got the future value meaning : SERVER GOT THE JOB LETTER AND IT REPLIED : accepted or rejected
    def goal_response_callback(self,future):

    # looking the response of the server
        goal_handle = future.result()

    # if the server said rejected we display it else we continue
        if not goal_handle.accepted:
            self.get_logger().info("Goal rejected :(")

    # if we get here our request was accepted from the server
        self.get_logger().info("Goal accepted :)")
        """
        the server has accepted the request but have'nt produced an output yet...
        so we make another FUTURE OBJECT (empty right now)
        - it represent a promise that someday the server will tell us : JOB COMPLETED (or failed)
        """

    # making the FUTURE OBJECT (empty rn)
        self.get_result_future = goal_handle.get_result_async()

    # using add_done_callback so that once server tells us i completed the job we can continue to next callback
        self.get_result_future.add_done_callback(self.get_result_callback)

# when the server tells us i am done with the job here is the result , we call this function (it got result info in it)
    def get_result_callback(self,future):

    # looking at the result the server sent
        # result = future.result().result   <- tutorial line (but we can simply)
    # the server sent the result in a truck... the FUTURE OBJECT is the truck (we open it)
    # inside that truck is the result wrapped in a box... the `result()` is that box (we open it)
        result_in_box = future.result()
    # when we open the wrapped box...inside we find our RESULT that the server sent for us
        result = result_in_box.result

    # we log the result
        self.get_logger().info(f"Result {result.sequence}")

    # we terminate everything once work is done
        rclpy.shutdown()

# in-case we get any feedback from the server we trigger this function :
    def feedback_callback(self, feedback_msg):

    # we open the feedback message
        feedback = feedback_msg.feedback

    # we display the feedback the server sent us
        self.get_logger().info(f'Received feedback: {feedback.partial_sequence}')

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