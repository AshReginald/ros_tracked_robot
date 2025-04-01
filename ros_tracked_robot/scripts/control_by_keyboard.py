#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64
import sys
import tty
import termios

# Default 
MAX_LIN_VEL = 0.5    # m/s
MAX_ANG_VEL = 1.5    # rad/s
LIN_VEL_STEP = 0.5
ANG_VEL_STEP = 0.5
ARM_STEP = 0.5  # Step for arrm
msg = """
Control Your Robot!
---------------------------
Moving around:
        W
   A    S    D
        X

Q/E : Raise/Decrease speed

Space/S : Stop

Arm Control:
R/F : Raise/Decrease arm_1
T/G : Raise/Decrease arm_2

ESC : Thoát
"""

def getKey():
    tty.setraw(sys.stdin.fileno())
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def vels(target_linear_vel, target_angular_vel):
    return "Current speed:\tlinear vel %s\t angular vel %s " % (target_linear_vel, target_angular_vel)

def makeSimpleProfile(output, input, slop):
    if input > output:
        output = min(input, output + slop)
    elif input < output:
        output = max(input, output - slop)
    else:
        output = input
    return output

def constrain(input, low, high):
    return max(min(input, high), low)

if __name__=="__main__":
    settings = termios.tcgetattr(sys.stdin)
    
    rospy.init_node('robot_teleop')
    # Publishers 
    cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    
    # Publishers for arm
    arm1_pub = rospy.Publisher('/arm_1_joint_controller/command', Float64, queue_size=10)
    arm2_pub = rospy.Publisher('/arm_2_joint_controller/command', Float64, queue_size=10)
    
    status = 0
    target_linear_vel = 0.0
    target_angular_vel = 0.0
    control_linear_vel = 0.0
    control_angular_vel = 0.0
    
    # Arm
    arm1_pos = 0.0
    arm2_pos = 0.0
    arm_limit = 1.57  # limit in URDF
    
    try:
        print(msg)
        while not rospy.is_shutdown():
            key = getKey()
            if key == '\x1b':  # ESC
                break
            # key
            elif key == 'w' or key == 'W':
                target_linear_vel = constrain(target_linear_vel + LIN_VEL_STEP, -MAX_LIN_VEL, MAX_LIN_VEL)
                print(vels(target_linear_vel, target_angular_vel))
            elif key == 'x' or key == 'X':
                target_linear_vel = constrain(target_linear_vel - LIN_VEL_STEP, -MAX_LIN_VEL, MAX_LIN_VEL)
                print(vels(target_linear_vel, target_angular_vel))
            elif key == 'a' or key == 'A':
                target_angular_vel = constrain(target_angular_vel + ANG_VEL_STEP, -MAX_ANG_VEL, MAX_ANG_VEL)
                print(vels(target_linear_vel, target_angular_vel))
            elif key == 'd' or key == 'D':
                target_angular_vel = constrain(target_angular_vel - ANG_VEL_STEP, -MAX_ANG_VEL, MAX_ANG_VEL)
                print(vels(target_linear_vel, target_angular_vel))
            elif key == ' ' or key == 's' or key == 'S':
                target_linear_vel = 0.0
                target_angular_vel = 0.0
                print(vels(target_linear_vel, target_angular_vel))
            elif key == 'q' or key == 'Q':
                MAX_LIN_VEL += 0.1
                MAX_ANG_VEL += 0.1
                print(f"Tăng tốc độ: linear {MAX_LIN_VEL}, angular {MAX_ANG_VEL}")
            elif key == 'e' or key == 'E':
                MAX_LIN_VEL = max(0.1, MAX_LIN_VEL - 0.1)
                MAX_ANG_VEL = max(0.1, MAX_ANG_VEL - 0.1)
                print(f"Giảm tốc độ: linear {MAX_LIN_VEL}, angular {MAX_ANG_VEL}")
            
            # arm_controller
            elif key == 'r' or key == 'R':
                arm1_pos = constrain(arm1_pos + ARM_STEP, -arm_limit, arm_limit)
                print(f"Arm1: {arm1_pos:.2f} rad")
            elif key == 'f' or key == 'F':
                arm1_pos = constrain(arm1_pos - ARM_STEP, -arm_limit, arm_limit)
                print(f"Arm1: {arm1_pos:.2f} rad")
            elif key == 't' or key == 'T':
                arm2_pos = constrain(arm2_pos + ARM_STEP, -arm_limit, arm_limit)
                print(f"Arm2: {arm2_pos:.2f} rad")
            elif key == 'g' or key == 'G':
                arm2_pos = constrain(arm2_pos - ARM_STEP, -arm_limit, arm_limit)
                print(f"Arm2: {arm2_pos:.2f} rad")
            
            if key in ['w', 'x', 'a', 'd', ' ', 's', 'r', 'f', 't', 'g', 'q', 'e']:
                status += 1
            
            if status == 20:
                print(msg)
                status = 0

            # Move
            twist = Twist()
            control_linear_vel = makeSimpleProfile(control_linear_vel, target_linear_vel, LIN_VEL_STEP/2.0)
            twist.linear.x = control_linear_vel
            control_angular_vel = makeSimpleProfile(control_angular_vel, target_angular_vel, ANG_VEL_STEP/2.0)
            twist.angular.z = control_angular_vel
            cmd_vel_pub.publish(twist)
            
            # Send cmd
            arm1_pub.publish(arm1_pos)
            arm2_pub.publish(arm2_pos)

    except Exception as e:
        print(e)

    finally:
        # Dừng robot
        twist = Twist()
        cmd_vel_pub.publish(twist)
        # Reset cánh tay
        arm1_pub.publish(0.0)
        arm2_pub.publish(0.0)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
