
#!/usr/bin/env python
import rospy
from nav_msgs.msg import Path
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3
import tf



class ODOM:
    def __init__(self):
        
        rospy.init_node('odometry_calculation_node', anonymous=True)

        self.x = None
        self.y = None
        self.yaw = None
        self.odom_pub = rospy.Publisher(name="/measured_odom", data_class=Odometry, queue_size=50)
        self.odom_broadcaster = tf.TransformBroadcaster()
        rospy.Subscriber(name='/odom', data_class=Odometry, callback=self._sub_callback)
        

    def _sub_callback(self, msg):
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y

    def publish_odom(self):
        current_time = rospy.Time.now()
        odom = Odometry()
        odom.header.stamp = current_time
        odom.header.frame_id = "solamr_1/odom"
        odom.child_frame_id = "solamr_1/base_footprint"
        odom.twist.twist = Twist(Vector3(0, 0, 0), Vector3(0, 0, 0))

        odom_quat = tf.transformations.quaternion_from_euler(0, 0, self.yaw)
        odom.pose.pose = Pose(Point(self.x, self.y, 0.), Quaternion(*odom_quat))

        self.odom_pub.publish(odom)


if __name__ == '__main__':
    
    a = ODOM()

    try:
        rospy.spin()

    except KeyboardInterrupt:
        pass

    finally:
        pass
        