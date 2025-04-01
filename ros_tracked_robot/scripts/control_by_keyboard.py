#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
import sys
import tty
import termios
import tty

# Các tốc độ mặc định
MAX_LIN_VEL = 0.5    # m/s
MAX_ANG_VEL = 1.5    # rad/s
LIN_VEL_STEP = 0.1
ANG_VEL_STEP = 0.1

msg = """
Control Your Robot!
---------------------------
Moving around:
        W
   A    S    D
        X

Q/E : Tăng/Giảm tốc độ

Space/S : Dừng

ESC : Thoát
"""

def getKey():
    tty.setraw(sys.stdin.fileno())
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def vels(target_linear_vel, target_angular_vel):
    return "Tốc độ hiện tại:\tlinear vel %s\t angular vel %s " % (target_linear_vel, target_angular_vel)

def makeSimpleProfile(output, input, slop):
    if input > output:
        output = min(input, output + slop)
    elif input < output:
        output = max(input, output - slop)
    else:
        output = input
    return output

def constrain(input, low, high):
    if input < low:
        input = low
    elif input > high:
        input = high
    else:
        input = input
    return input

if __name__=="__main__":
    settings = termios.tcgetattr(sys.stdin)
    
    rospy.init_node('robot_teleop')
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    
    status = 0
    target_linear_vel = 0.0
    target_angular_vel = 0.0
    control_linear_vel = 0.0
    control_angular_vel = 0.0
    
    try:
        print(msg)
        while not rospy.is_shutdown():
            key = getKey()
            if key == '\x1b':  # ESC
                break
            elif key == 'w' or key == 'W':
                target_linear_vel = constrain(target_linear_vel + LIN_VEL_STEP, -MAX_LIN_VEL, MAX_LIN_VEL)
                status = status + 1
                print(vels(target_linear_vel, target_angular_vel))
            elif key == 'x' or key == 'X':
                target_linear_vel = constrain(target_linear_vel - LIN_VEL_STEP, -MAX_LIN_VEL, MAX_LIN_VEL)
                status = status + 1
                print(vels(target_linear_vel, target_angular_vel))
            elif key == 'a' or key == 'A':
                target_angular_vel = constrain(target_angular_vel + ANG_VEL_STEP, -MAX_ANG_VEL, MAX_ANG_VEL)
                status = status + 1
                print(vels(target_linear_vel, target_angular_vel))
            elif key == 'd' or key == 'D':
                target_angular_vel = constrain(target_angular_vel - ANG_VEL_STEP, -MAX_ANG_VEL, MAX_ANG_VEL)
                status = status + 1
                print(vels(target_linear_vel, target_angular_vel))
            elif key == ' ' or key == 's' or key == 'S':
                target_linear_vel = 0.0
                target_angular_vel = 0.0
                control_linear_vel = 0.0
                control_angular_vel = 0.0
                print(vels(target_linear_vel, target_angular_vel))
            elif key == 'q' or key == 'Q':
                MAX_LIN_VEL = MAX_LIN_VEL + 0.1
                MAX_ANG_VEL = MAX_ANG_VEL + 0.1
                print("Tăng tốc độ:\tlinear %s\t angular %s " % (MAX_LIN_VEL, MAX_ANG_VEL))
            elif key == 'e' or key == 'E':
                MAX_LIN_VEL = MAX_LIN_VEL - 0.1
                MAX_ANG_VEL = MAX_ANG_VEL - 0.1
                print("Giảm tốc độ:\tlinear %s\t angular %s " % (MAX_LIN_VEL, MAX_ANG_VEL))
            else:
                if (key == '\x03'):
                    break
            
            if status == 20:
                print(msg)
                status = 0

            twist = Twist()

            control_linear_vel = makeSimpleProfile(control_linear_vel, target_linear_vel, (LIN_VEL_STEP/2.0))
            twist.linear.x = control_linear_vel
            twist.linear.y = 0.0
            twist.linear.z = 0.0

            control_angular_vel = makeSimpleProfile(control_angular_vel, target_angular_vel, (ANG_VEL_STEP/2.0))
            twist.angular.x = 0.0
            twist.angular.y = 0.0
            twist.angular.z = control_angular_vel

            pub.publish(twist)

    except Exception as e:
        print(e)

    finally:
        twist = Twist()
        twist.linear.x = 0.0
        twist.linear.y = 0.0
        twist.linear.z = 0.0
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = 0.0
        pub.publish(twist)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)