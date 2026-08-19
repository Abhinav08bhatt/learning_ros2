# importing the rclpy lib so we can use teh NODE class
import rclpy
from rclpy.node import Node

# importing the message type out node use
from std_msgs.msg import String

# creating a class that inherits from the main class Node
class MinimalPublisher(Node):

    # creating a constructor that will be called at the instance of the class
    def __init__(self):

        # giving a name to our node
        super().__init__('minimal_publisher')

        # declaring that the node publish :
            # message of type : std_msgs/msg/String
            # over a TOPIC
            # in the queue size of 10
        self.publisher_ = self.create_publisher(String, 'topic', 10)

        # creating a timer that creates a callback that execute every 0.5 sec (self.i) is a counter used for that
        timer_period = 0.5 # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    # creating a function : timer_callback that does job :
        # creates a message with the counter value appended
        # publishes it
        # prints it to the console (with the get_logger()'s info() function)
    def timer_callback(self):
        msg = String()

        # the content that we will be sending
        msg.data = "Hello World : %d " % self.i # (its the syntax for the String message)
        self.publisher_.publish(msg)

        # the content we will be showing in the terminal once we successfully send the message
        self.get_logger().info("Publishing : '%s' " % msg.data) 

        self.i += 1


# main function

def main(args=None):

    # Initializes the ROS 2 Python client library.
    # This must be called before creating any ROS 2 nodes.
    rclpy.init(args=args)

    # Creates an instance of the MinimalPublisher node.
    # The constructor (__init__) sets up the publisher and timer.
    minimal_publisher = MinimalPublisher()

    # Keeps the node running so it can process callbacks.
    # Here, it repeatedly executes timer_callback() every 0.5 seconds.
    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly (optional, otherwise it will be done automatically)
    minimal_publisher.destroy_node()

    # Shuts down the ROS 2 client library and cleans up resources.
    rclpy.shutdown()

if __name__ == '__main__':
    main()