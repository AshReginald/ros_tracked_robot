# ros_tracked_robot
Mô phỏng robot: 
- 2 bánh xích, tay máy 2 khớp xoay; 
- Cảm biến IMU, Camera, Encoder.

1. Cấp quyền thực thi:
source devel/setup.bash
chmod +x control_by_keyboard.py
chmod +x encoders_display.py
  
2. Khởi động:
Có 2 cách khởi động:
- Cách 1: Mở 1 terminal: Nhanh hơn.
roslaunch ros_tracked_robot start.launch
- Cách 2: Mở 3 terminal: Cách này sử dụng để nhìn rõ log gửi về với twnfg file.
    - Terminal 1 (Mở gazebo): roslaunch ros_tracked_robot gazebo.launch
    - Terminal 2 (Mở RVIZ): roslaunch ros_tracked_robot display.launch 
    - Terminal 3 (Điều khiển Robot bằng bàn phím): rosrun ros_tracked_robot control_by_keyboard.py

 3. Điều khiển:
- Nếu đã chạy chương trình bằng cách 1 thì có thể điều khiển trực tiếp bằng bàn phím luôn (lưu ý là nhập kí tự sau đó bấm ENTER để truyền lệnh).
- Trong một terminal mới chạy lệnh: "rosrun ros_tracked_robot encoders_display.py" để xem các encoder trả về giá trị. 
