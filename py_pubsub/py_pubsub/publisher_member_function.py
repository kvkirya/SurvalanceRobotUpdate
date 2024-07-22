import rclpy
from rclpy.node import Node #imported so we can use nodes
import serial
from std_msgs.msg import Int32 #this is the data structure the node passes to the topic
#!Ros2 dependencies need to be added to package.xml!

class MinimalPublisher(Node):
    #subclass of node
    def __init__(self):
        super().__init__('minimal_publisher')#calls node's class's constructure and give it your node name
        self.publisher_ = self.create_publisher(Int32, 'sensor_data', 10)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.read_serial)
        self.serial_port = serial.Serial('//dev/ttyACM0', 9600)
        self.i = 0

    def read_serial(self):
        if serial.serial_port.in_waiting > 0:
            try:
                line = self.serial_port.readline().decode('utf-8').strip()
                sensor_value = int(line)
                if sensor_value < 500: #threshold value
                    msg = Int32()
                    msg.data = sensor_value
                    self.publisher_.publish(msg)
                    self.get_logger().info(f'Publishing: {msg.data}')
            except ValueError:
                self.get_logger().info('Error reading serial data')


def main(args=None):
    rclpy.init(args=args)
    node = MinimalPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
