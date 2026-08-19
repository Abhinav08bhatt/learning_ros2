from example_interfaces.srv import AddTwoInts
# holds the structure of the service
""" 
Request : 
    a
    b

Response :
    sum
"""

import rclpy
from rclpy.node import Node

class MinimalServices(Node):
# creating a node for the service

    def __init__(self):
        super().__init__('minimal_services')
        # node name given

        self.srv = self.create_service(
            AddTwoInts, 
            'add_two_ints',
            self.add_two_ints_callback
        )
        """
        "srv" now says :
            i provide a service called : "add_two_ints"
            it uses "AddTwoInts" type (from the imported example_interface.srv)
            when request arrive call the function : "add_two_ints_callback"
        """

    # setting the function that handles the sum and stuff

    # this function is called whenever the service receive a request (the request was given from a potential client)
    # the request was then formatted and given to this service and service sends that formatted data to this function
    def add_two_ints_callback(self,request,response):
        # response.sum = request.a + request.b
        response.sum = request.a + request.b
        self.get_logger().info('Incoming request\na: %d, b: %d'%(request.a,request.b))

        return response
    
def main():

    rclpy.init()

    minimal_service = MinimalServices()
    rclpy.spin(minimal_service)

    minimal_service.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()