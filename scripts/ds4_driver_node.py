#!/usr/bin/env python3
from logger import Logger
from controller_ros import ControllerRos
from ds4drv.backends import BluetoothBackend, HidrawBackend
from ds4drv.exceptions import BackendError
from std_msgs.msg import Int32
import rclpy
import signal
import sys


class SignalHandler(object):
    def __init__(self, controller):
        self.controller = controller

    def __call__(self, signum, frame):
        rospy.loginfo('Shutting down...')
        self.controller.exit()
        sys.exit(0)


class ds4_driver_BLE(ControllerRos):
    def __init__(self,ros2_node):
        super(ds4_driver_BLE, self).__init__(ros2_node)
        self.ros2_node = ros2_node
        # Publish Connect Status
        self.DS4_Connect_Status = self.ros2_node.create_publisher(Int32,"ds4_connect_status")
        # 
        # self.device_addr = rospy.get_param('~device_addr', None)
        self.device_addr = None
        backend_type = 'bluetooth'
        #backend_type = rospy.get_param('~backend', 'hidraw')
        # Connect Status 
        self.Status = Int32()
        self.Status.data = 0
        # backend_type
        if backend_type == 'bluetooth':
            self.backend = BluetoothBackend(Logger('backend'))
        else:
            self.backend = HidrawBackend(Logger('backend'))
        self.ds4_connect()

    def ds4_connect(self):
        try:
            self.backend.setup()
        except BackendError as err:
            #rospy.logerr(err)
            ros2_node.get_logger().info('Error')
            sys.exit(1)
        # 
        print('Wait....')
        for device in self.backend.devices:
            self.ros2_node.get_logger().info('I heard: "%s"' % format(device.name))
            #rospy.loginfo('Connected to {0}'.format(device.name))
            if self.device_addr in (None, '', device.device_addr):
                self.setup_device(device)
                break
            #rospy.loginfo('Waiting for specified controller')
            self.ros2_node.get_logger().info('Waiting for specified controller')
        # DS4 Connect Status
        # Status = Int32()
        self.Status.data = 1
        self.DS4_Connect_Status.publish(self.Status)
        # Status
        # self.DS4_Connect_Status.publish(Status)

    def ds4_Not_connect(self):
        # DS4 Connect Status
        # Status = Int32()
        self.Status.data = 0
        self.DS4_Connect_Status.publish(self.Status)
        # Status
        # self.DS4_Connect_Status.publish(Status)
        #
        self.ros2_node.get_logger().info('Disconnected...')
        # self.exit()
        self.loop.stop()
        self.ds4_connect()
        # Run
        self.loop.register_event('device-report', self.cb_report)
        self.loop.register_event('device-cleanup', self.ds4_Not_connect)
        self.run()
        '''
        if self.is_alive():
            self.join()
        '''

    def ds4_Start(self):
        if not self.is_alive():
            self.start()
            self.loop.register_event('device-report', self.cb_report)
            self.loop.register_event('device-cleanup', self.ds4_Not_connect)
        
    def Send_Connect_Status(self):
        self.DS4_Connect_Status.publish(self.Status)

def main(args=None):
    # rospy.init_node('ds4_driver_node')
    rclpy.init(args=args)
    ros2_node = rclpy.create_node('ds4_driver_node')
    DS4_BLE = ds4_driver_BLE(ros2_node)
    DS4_BLE.ds4_Start()
    try:
        rclpy.spin(ros2_node)
    except KeyboardInterrupt:
        print("ShutDown") 
    ros2_node.destroy_node()
    rclpy.shutdown()
    '''
    rospy.init_node('ds4_driver_node')
    DS4_BLE = ds4_driver_BLE()
    DS4_BLE.ds4_Start()
    try:
        rospy.spin()
        rospy.sleep(1)
    except KeyboardInterrupt:
        print("ShutDown")
    '''

if __name__ == '__main__':
    main(sys.argv)
