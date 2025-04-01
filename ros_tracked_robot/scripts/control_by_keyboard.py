#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64
import sys, tty, termios

class KeyboardControl:
    def __init__(self):
        # Khởi tạo node ROS
        rospy.init_node('keyboard_control')
        
        # Publisher cho base (xe tăng)
        self.pub_base = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        # Publisher cho tay máy
        self.pub_joint1 = rospy.Publisher('/arm_1_joint_controller/command', Float64, queue_size=10)
        self.pub_joint2 = rospy.Publisher('/arm_2_joint_controller/command', Float64, queue_size=10)
        
        # Khởi tạo thông điệp Twist cho base
        self.twist = Twist()
        self.linear_speed = 0.1   # Tốc độ tuyến tính (m/s)
        self.angular_speed = 0.1  # Tốc độ góc (rad/s)
        
        # Khởi tạo vị trí ban đầu và bước điều chỉnh cho các khớp
        self.joint1_pos = 0.0     # Vị trí arm_1
        self.joint2_pos = 0.0     # Vị trí arm_2
        self.step = 0.5           # Bước điều chỉnh (theo code mới)

    def get_key(self):
        """Lấy phím nhấn từ bàn phím"""
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return key

    def run(self):
        # Hiển thị hướng dẫn điều khiển
        rospy.loginfo("Điều khiển xe tăng: w: tiến, s: lùi, a: trái, d: phải, x: dừng")
        rospy.loginfo("Điều khiển tay máy: 1: tăng arm_1, 2: giảm arm_1, 3: tăng arm_2, 4: giảm arm_2")
        rospy.loginfo("Nhấn 'q' để thoát")
        
        rate = rospy.Rate(10)  # Tần suất 10 Hz
        while not rospy.is_shutdown():
            key = self.get_key()
            
            # Điều khiển base (xe tăng)
            if key == 'w':
                self.twist.linear.x = self.linear_speed
                self.twist.angular.z = 0.0
            elif key == 's':
                self.twist.linear.x = -self.linear_speed
                self.twist.angular.z = 0.0
            elif key == 'a':
                self.twist.linear.x = 0.0
                self.twist.angular.z = self.angular_speed
            elif key == 'd':
                self.twist.linear.x = 0.0
                self.twist.angular.z = -self.angular_speed
            elif key == 'x':
                self.twist.linear.x = 0.0
                self.twist.angular.z = 0.0

            # Điều khiển tay máy 
            if key == '1':
                self.joint1_pos += self.step
                if self.joint1_pos > 1.57:
                    self.joint1_pos = 1.57
            elif key == '2':
                self.joint1_pos -= self.step
                if self.joint1_pos < -1.57:
                    self.joint1_pos = -1.57
            elif key == '3':
                self.joint2_pos += self.step
                if self.joint2_pos > 1.57:
                    self.joint2_pos = 1.57
            elif key == '4':
                self.joint2_pos -= self.step
                if self.joint2_pos < -1.57:
                    self.joint2_pos = -1.57
            elif key == 'q':
                self.twist.linear.x = 0.0
                self.twist.angular.z = 0.0
                self.pub_base.publish(self.twist)
                break
            
            # Publish thông điệp
            self.pub_base.publish(self.twist)
            self.pub_joint1.publish(self.joint1_pos)
            self.pub_joint2.publish(self.joint2_pos)
            
            # In ra vị trí hiện tại của các khớp
            rospy.loginfo("Vi tri Arm_1: %.2f rad, Vi tri Arm_2: %.2f rad", self.joint1_pos, self.joint2_pos)
            
            rate.sleep()

if __name__ == "__main__":
    try:
        KeyboardControl().run()
    except rospy.ROSInterruptException:
        pass