#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import JointState

def joint_state_callback(msg):
    # Danh sách các khớp cần hiển thị, khớp với tên trong URDF
    joints_to_display = ['arm_1_joint', 'arm_2_joint', 'wheel1_joint', 'wheel2_joint', 'wheel3_joint', 'wheel4_joint']
    
    # Duyệt qua danh sách khớp từ thông điệp JointState
    for i, joint_name in enumerate(msg.name):
        if joint_name in joints_to_display:
            position = msg.position[i]
            # Kiểm tra xem velocity có tồn tại không, nếu không thì gán 0.0
            velocity = msg.velocity[i] if i < len(msg.velocity) else 0.0
            rospy.loginfo("%s: Position = %.3f rad, Velocity = %.3f rad/s", joint_name, position, velocity)

def encoder_display():
    # Khởi tạo node ROS
    rospy.init_node('encoder_display', anonymous=True)
    
    # Đăng ký subscriber để đọc topic /joint_states
    rospy.Subscriber('/joint_states', JointState, joint_state_callback)
    
    # Thông báo node đang chạy và giữ nó hoạt động
    rospy.loginfo("Hiển thị giá trị encoder của các khớp...")
    rospy.spin()

if __name__ == '__main__':
    try:
        encoder_display()
    except rospy.ROSInterruptException:
        pass