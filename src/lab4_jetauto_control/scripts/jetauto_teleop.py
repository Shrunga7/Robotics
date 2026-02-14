#!/usr/bin/env python3

import rospy
import sys
import termios
import tty
import math
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
    except KeyboardInterrupt:
        # This handles Ctrl+C properly and stops the program
        print("\nExiting gracefully...")
        sys.exit(0)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def move_forward(pub, twist, duration=5.0, speed=0.2):
    """Move forward for a set duration."""
    twist.linear.x = speed         #This sets the speed at which the robot will move forward
    twist.angular.z = 0.0          # No turning, straight movement
    pub.publish(twist)		   # Send the velocity command
    rospy.sleep(duration)	   # Keep moving for the specific duration
    twist.linear.x = 0.0	   # Stop moving after duration
    pub.publish(twist)


def move_sideways(pub, twist, duration=5.0, speed=0.2):
    """Move sideways (left or right) for a set duration."""
    twist.linear.x = 0.0	   # No linear movement
    twist.linear.y = speed	   # Move sideways
    twist.angular.z = 0.0	   # No rotational movement
    pub.publish(twist)
    rospy.sleep(duration)
    twist.linear.y = 0.0	   # Stop moving sideways after duration
    pub.publish(twist)


def turn(pub, twist, angle, speed=0.2):
    """Turn the robot by a specified angle."""
    angle_rad = math.radians(angle) #1.57rad
    duration = abs(angle_rad) / speed
    twist.linear.x = 0.0
    twist.angular.z = speed if angle_rad > 0 else -speed
    pub.publish(twist)
    rospy.sleep(duration) #7.85s
    twist.angular.z = 0.0
    pub.publish(twist)

# I figured this part on my own by trying out differnt ways
def drift(pub, twist, angle, speed=0.2):
    """Move sideways (left or right) for a set duration."""

    duration = math.radians(angle)/(2*speed) # 3.925s
    twist.linear.x = speed	   # linear movement
    twist.linear.y = -speed
    twist.angular.z = 2*speed # R = v/w = 

    pub.publish(twist)
    rospy.sleep(duration)
    twist.linear.x = 0.0
    twist.linear.y = 0.0
    twist.angular.z = 0.0
    pub.publish(twist)


def main():

    rospy.init_node("jetauto_teleop") #Initializes the ROS node.
    pub = rospy.Publisher("jetauto_controller/cmd_vel", Twist, queue_size=10) #publish data to the topic in linear and angualar format with buffer to store 10 msgs in line.

    print(f"Controlling jetauto_controller")
    print("Press Enter to start the movement sequence...")
    
    # Wait for input before starting the sequence
    input("Press Enter to start...")

    twist = Twist()

    try:
        # Repeat the sequence twice
        for _ in range(2):
            # Step 1: Move forward from (0, 0, 0°) to (1, 0, 0°)
            print("Moving forward to (1, 0, 0°)...for roughly 1 meter")
            move_forward(pub, twist, duration=5.0)

            # Step 2: Move sideways to the left from (1, 0, 0°) to (1, 1, 0°)
            print("Moving sideways to the left to (1, 1, 0°)...for roughly 1 meter")
            move_sideways(pub, twist, duration=5.0, speed=0.2)

            # Step 3: Turn clockwise from (1, 1, 0°) to (1, 1, -90°)
            print("Turning clockwise to (1, 1, -90°)...for roughly 1 meter")
            turn(pub, twist, angle=-90, speed=0.2)

            # Step 4: Move sideways to the right from (1, 1, -90°) to (0, 1, -90°)
            print("Moving sideways to the right to (0, 1, -90°)..for roughly 1 meter")
            move_sideways(pub, twist, duration=5.0, speed=-0.2)

            # Step 5: Move forward and turn from (0, 1, -90°) to (0, 0, 0°)
            print("Moving forward and turning to (0, 0, 0°)...for roughly 1 meter")
            drift(pub, twist, angle=90, speed=0.4)
            # turn(pub, twist, angle=90, speed=0.8)

    except KeyboardInterrupt:
        pass
    finally:
        twist.linear.x = 0.0
        twist.linear.y = 0.0
        twist.angular.z = 0.0
        pub.publish(twist)

if __name__ == "__main__":
    main()

#I have used Chat GPT for reference and understanding the code.

