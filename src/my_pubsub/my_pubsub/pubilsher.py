import rclpy
from rclpy.node import Node

from tutorial_interfaces.msg import Num
""" 
msg Num : int64 num
"""

class Publisher(Node):

    def __init__(self):

        super().__init__('num_publisher')
        self.publisher_ = self.create_publisher(
            Num,
            'num_topic',
            10
        )
        self.timer = self.create_timer(0.5, self.callback_function)
        self.i = 0

    def callback_function(self):
        msg = Num()
        msg.num = self.i
        self.publisher_.publish(msg)
        self.get_logger().info("Screaming : %d"%self.i)
        self.i += 1

def main(args=None):

    rclpy.init(args=args)

    num_publisher= Publisher()
    rclpy.spin(num_publisher)

    num_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()