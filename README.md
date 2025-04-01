# ros_tracked_robot
Mô phỏng robot: 
- 2 bánh xích, tay máy 2 khớp xoay; 
- Cảm biến IMU, Camera, Encoder.

Khởi động:
Có 2 cách khởi động:
1. Mở 3 terminal: Cách này sử dụng để nhìn rõ log gửi về với twnfg file.
- Terminal 1 (Mở gazebo): roslaunch ros_tracked_robot gazebo.launch
- Terminal 2 (Mở RVIZ): roslaunch ros_tracked_robot display.launch 
- Terminal 3 (Điều khiển Robot bằng bàn phím): rosrun ros_tracked_robot control_by_keyboard.py

2. Mở 1 terminal: Nhanh hơn.
roslaunch ros_tracked_robot start.launch
