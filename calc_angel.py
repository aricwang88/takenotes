import os,sys
import time,cv2,math

##############################################################
#Fun: get_point_angle
#Args: pt_0 the start point. pt_1 the end point.
##############################################################
def get_point_angle(pt_0, pt_1):
    angle = 0
    
    point = (pt_1[0]-pt_0[0], pt_1[1]-pt_0[1])
    #print(point)
    if 0 == point[0] and 0 == point[1]:
        return 0
    if 0 == point[0]:
        angle = 90
        return angle
    if 0 == point[1]:
        angle = 0
        return angle
    temp = math.fabs(1.0*point[1]/point[0])
    temp = math.atan(temp)
    temp = temp*180.0/math.pi
    
    if point[0] > 0 and point[1] > 0:
        angle = 360 - temp
        return angle
    if point[0] < 0 and point[1] > 0:
        angle = 360 - (180-temp)
        return angle
    if point[0] > 0 and point[1] < 0:
        angle = temp
        return angle
    if point[0] < 0 and point[1] < 0:
        angle = 180 - temp
        return angle
    pass


print(get_point_angle((100,100),(20,20)))

print(get_point_angle((100,100),(20,120)))


