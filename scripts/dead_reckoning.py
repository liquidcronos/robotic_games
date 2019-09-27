'''
Code performs dead reckoning using wheel encoders which values  are read in in Form of a Float32.
it is asumed that the encoder counts upward when driving forward and downward when drving backwards.

vector3.x =left wheel,
vector3.y=right wheel
'''

import rospy 
import numpy as np
import robot_dimensions as robo
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Vector3
class deadreckoning:
    def __init__(self):
        rospy.subscriber("wheel",Vector3,self.encoder_callback)
        pub=rospy.Publisher("dead_reckoning",Odometry,queue_size=10)

        encoder_counter=np.array([0,0])
        #                  x y phi
        current_position= [0,0, 0 ]

    def encoder_callback(self,data):
        new_encoder_counter=np.array([data.x,data.y])
        dist    = (new_encoder_counter-self.encoder_counter)/robo.encoder_increments*2*np.pi*robo.wheel_radius
        del_s   = 0.5*(dist[0]+dist[1])
        del_phi = 0.5*(dist[0]-dist[1])/robo.axis_length

        movement=np.array([-1*del_s*np.sin(self.current_position[2]+del_phi/2),
                              del_s*np.cos(self.current_position[2]+del_phi/2),
                              del_phi])
        self.current_position=self.current_position+movement

        output=Odometry()
        output.pose.pose.position.x   = self.current_position[0]
        output.pose.pose.position.y   = self.current_position[1]
        output.pose.pose.orientation.z= self.current_position[2]

        output.twist.twist.linear.x  = np.sqrt(movement[0]**2+movement[1]**2)
        output.twist.twist.angular.z = movement[2]
        self.pub.publish(output)
        encoder_counter=new_encoder_counter
        

if __name__ == "__main__":
    try:
        rospy.init_node("dead_reckoning")
        reck=deadreckoning()
    except rospy.ROSInterrupt:
        rospy.loginfo(" dead reckoning error")

 