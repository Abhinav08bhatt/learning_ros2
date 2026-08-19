import rclpy
from rclpy.node import Node

from tutorial_interfaces.srv import AddThreeInts

class MinimalService(Node):

    def __init__(self):
        super().__init__("minimal_service")
        self.srv = self.create_service(
            AddThreeInts,
            "add_three_ints",
            self.add_three_ints_callback
        )

    def add_three_ints_callback(self,Request,Response):
        Response.sum = Request.a + Request.b + Request.c
        self.get_logger().info('Incoming request :\na : %d\nb : %d\nc : %d '%(Request.a, Request.b, Request.c))

        return Response

def main():

    rclpy.init()

    minimal_service = MinimalService()
    rclpy.spin(minimal_service)

    minimal_service.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()