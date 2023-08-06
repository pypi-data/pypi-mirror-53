### North Robots

The `north_robots` library provides a high-level API for interacting with North Robotics robots and components.

## Installation

Install the `north_robots` library
```bash
pip install git+https://gitlab.com/north-robotics/north_robots
```

Import the `C9Controller` and `N9Robot` classes
```python
from north_c9.controller import C9Controller
from north_robots.n9 import N9Robot
```

Now create instances of the controller and robot
```python
controller = C9Controller()
robot = N9Robot(controller)
```

Now you can home and move the N9 robot arm around
```python
robot.home()
robot.move(0, 150)
robot.move(0, 150, 200)
robot.move(gripper=90)
robot.elbow.move_degrees(-90)
```