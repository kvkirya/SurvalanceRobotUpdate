import rclpy
from rclpy.node import Node
import RPi.GPIO as GPIO

from std_msgs.msg import Int32

#define variables


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(Int32, "minimal_publisher",  self.listener_callback, 10)
        self.subscription
        GPIO.setmode(GPIO.BCM)
        self.input1 = 17
        self.input2 = 18
        self.input3 = 4
        self.input4 = 14
        self.enable1 = 21

        GPIO.setup(self.input1, GPIO.OUT)
        GPIO.setup(self.input2, GPIO.OUT)
        GPIO.setup(self.input3, GPIO.OUT)
        GPIO.setup(self.input4, GPIO.OUT)
        GPIO.setup(self.enable1, GPIO.OUT)

        self.motorInput1 = GPIO.PWM(self.input1, 100)
        self.motorInput2 = GPIO.PWM(self.input2, 100)

        self.motorInput3 = GPIO.PWM(self.input3, 100)
        self.motorInput4 = GPIO.PWM(self.input4, 100)

        self.motorEnable = GPIO.PWM(self.enable1, 100)

        self.motorInput1.start(0)
        self.motorInput2.start(0)

        self.motorInput3.start(0)
        self.motorInput4.start(0)

    
    def listener_callback(self, msg):
        self.get_logger().info(f'Received: {msg.data}')
        self.control_motor(msg.data)

    def control_motor(self,sensor_value):
        if sensor_value < 500:
            self.motorInput1.ChangeDutyCycle(100)
            self.motorInput2.ChangeDutyCycle(0)
        else:
            self.motorInput1.ChangeDutyCycle(0)
            self.motorInput2.ChangeDutyCycle(0)
        
def main(args=None):
    rclpy.init(args=args)

    node = MinimalSubscriber()

    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

