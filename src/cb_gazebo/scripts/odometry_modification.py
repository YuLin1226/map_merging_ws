#!/usr/bin/env python
import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Pose, Twist, Transform, TransformStamped
from gazebo_msgs.msg import LinkStates
from std_msgs.msg import Header
import numpy as np
import math
import tf2_ros


class Odom:
    def __init__(self):
        self.pub_odom = rospy.Publisher('/odom', Odometry, queue_size=1)
        self.tf_pub = tf2_ros.TransformBroadcaster()
        rospy.Subscriber(name='/deprecated_odom', data_class=Odometry, callback=self.callback_function)


    def callback_function(self, msg):

        cmd = Odometry()
        cmd.header.stamp = rospy.Time.now()
        cmd.header.frame_id = 'odom'
        cmd.child_frame_id = 'base_footprint'
        cmd.pose.pose = msg.pose
        cmd.pose.pose.position.x = msg.pose.position.x
        cmd.pose.pose.position.y = msg.pose.position.y
        #cmd.pose.pose.position.z = 0  # odom z not equals to zero for no reason
        cmd.twist.twist = msg.twist
        self.pub_odom.publish(cmd)

        tf = TransformStamped(
            header=Header(
                frame_id=cmd.header.frame_id,
                stamp=cmd.header.stamp
            ),
            child_frame_id=cmd.child_frame_id,
            transform=Transform(
                translation=cmd.pose.pose.position,
                rotation=cmd.pose.pose.orientation
            )
        )
        self.tf_pub.sendTransform(tf)


# Start the node
if __name__ == '__main__':
    rospy.init_node("odometry_node")
    rospy.spin()
