import rclpy
from rclpy.node import Node

import sys
from tutorial_interfaces.srv import AddThreeInts

class MinimalClient_Async(Node):

    def __init__(self):

        super().__init__("minimal_client_async")
        self.cli = self.create_client(
            AddThreeInts,
            "add_three_ints"
        )
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("no service available, waiting again1...")

        self.request = AddThreeInts.Request()

    def send_request(self,a,b,c):
        self.request.a = a
        self.request.b = b
        self.request.c = c

        return self.cli.call_async(self.request)

def main():
    rclpy.init()

    minimal_client = MinimalClient_Async()
    future = minimal_client.send_request(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]))
    rclpy.spin_until_future_complete(minimal_client, future)

    response = future.result()
    minimal_client.get_logger().info(
        "Outcome of the sum for : %d + %d + %d = %d"%(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),response.sum)
    )

    minimal_client.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()