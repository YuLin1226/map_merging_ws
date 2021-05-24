#! /usr/bin/env python
import rospy
import math
from sensor_msgs.msg import LaserScan
import numpy as np
from rospy.numpy_msg import numpy_msg
from rospy_tutorials.msg import Floats
import matplotlib.pyplot as plt
import csv



class readLaserscan:
    def __init__(self):
        rospy.init_node('read_laserscan')
        self.data_list =[]
        # get angle deviation
        # self.angle_deviation = rospy.get_param('~angle_deviation')
        # self.x_deviation = rospy.get_param('~x_deviation')
        # self.y_deviation = rospy.get_param('~y_deviation')
        # define publisher and subscriber
        # self.pub = rospy.Publisher('/laser_xy', numpy_msg(Floats), queue_size=10)
        self.rate = rospy.Rate(10)
        self.sub = rospy.Subscriber('/front/scan', LaserScan, self.callback)

        while not rospy.is_shutdown():
            
            print(len(self.data_list))
            if len(self.data_list) > 500:
                self.sub.unregister()
                print("stop now")
        rospy.spin()

    def callback(self, msg):
        # Lidar data array : msg.ranges
        # i : point radius
        # [i]*0.352 : point angle
        self.data = msg.ranges
        self.data_list.append(self.data[341])
        # for i in range( len(self.data) ): 
        #     self.angle = ((i-341)*0.352)*math.pi/180 + self.angle_deviation
        #     self.radius = self.data[i]
        #     if self.radius < 5:
        #         self.y = math.sin(self.angle) * self.radius + self.y_deviation
        #         self.x = math.cos(self.angle) * self.radius + self.x_deviation
        #         # print([self.x, self.y])
        #         self.xy = numpy.array([self.x, self.y], dtype = numpy.float32)
        #         self.pub.publish(self.xy)


if __name__ == "__main__":
    try:
        RLS = readLaserscan() 

        print("============= 統計資料 ============\n")

        print("平均：%f" %(np.mean(RLS.data_list)))
        print("標準差：%f" %(np.std(RLS.data_list)))

        print("\n===================================")

        plt.rcParams['font.sans-serif'] = ['DFKai-SB'] 
        plt.rcParams['axes.unicode_minus'] = False
        plt.hist(RLS.data_list)
        # plt.text(4.02,140,"平均：%f\n標準差：%f" %(np.mean(RLS.data_list),np.std(RLS.data_list)))
        plt.xlabel("感測距離（公尺）")
        plt.ylabel("資料數量")
        # plt.title("光達感測誤差模擬測試（標準差：0.005）")
        plt.title("平均：%f\n標準差：%f" %(np.mean(RLS.data_list),np.std(RLS.data_list)))
        plt.show()


        with open('sigma0_05.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # 寫入二維表格
            for data in RLS.data_list:
                writer.writerow([data])
            # writer.writerow(RLS.data_list)



    except rospy.ROSInterruptException:
        pass

    # finally:
        


