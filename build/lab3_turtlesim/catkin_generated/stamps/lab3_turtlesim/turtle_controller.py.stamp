#!/usr/bin/env python3

import rospy
import sys
import termios
import tty
from geometry_msgs.msg import Twist

# Key bindings
move_bindings = {
    'w': (1.0, 0.0),
    's': (-1.0, 0.0),
    'a': (0.0, 1.0),
    'd': (0.0, -1.0),
    'q': (1.0, 1.0),
    'e': (1.0, -1.0),
    'z': (-1.0, 1.0),
    'c': (-1.0, -1.0),
}

def get_key():
    """Read a single keypress from terminal"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd) #Switching the terminal to raw mode to immediately move on the keypress without having to press "enter key"
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def main():
    if len(sys.argv) < 2:
        print("Usage: rosrun lab3_turtlesim turtle_controller.py turtle_name")
        sys.exit(1)

    turtle_name = sys.argv[1]
    topic = f"/{turtle_name}/cmd_vel" 

    rospy.init_node("turtle_controller", anonymous=True) #Registers this script as a node with the ROS master. "True" Allows multiple terminals.
    pub = rospy.Publisher(topic, Twist, queue_size=10) #publish data to the topic in linear and angualar format with buffer to store 10 msgs in line.

    print(f"Controlling turtle: {turtle_name}")
    print("Use w/a/s/d to move, q/e/z/c for curves, Ctrl+C to quit")

    twist = Twist()

    try:
        while not rospy.is_shutdown(): 
            key = get_key()

            if key in move_bindings:
                linear, angular = move_bindings[key]
                twist.linear.x = linear * 2.0
                twist.angular.z = angular * 2.0
            else:
                twist.linear.x = 0.0
                twist.angular.z = 0.0

            pub.publish(twist)

    except KeyboardInterrupt:
        pass
    finally:
        twist.linear.x = 0.0
        twist.angular.z = 0.0
        pub.publish(twist)

if __name__ == "__main__":
    main()

#I have used Chat GPT for reference and understanding the code.

