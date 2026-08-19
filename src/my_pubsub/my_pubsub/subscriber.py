import rclpy
from rclpy.node import Node

from tutorial_interfaces.msg import Num

class Subscriber(Node):

    def __init__(self):
        super().__init__('num_subscriber')
        self.subscriber_ = self.create_subscription(
            Num,
            'num_topic',
            self.function_callback,
            10
        )

    def function_callback(self,msg):
        self.get_logger().info("Received the msg : %d "%msg.num)

def main(args=None):

    rclpy.init(args=args)

    num_subscriber = Subscriber()
    rclpy.spin(num_subscriber)

    num_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()