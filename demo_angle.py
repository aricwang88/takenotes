#!/usr/bin/env python

import os,sys,time
import cv2
import numpy as np
import math


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


def nothing(x):
    pass
 

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    cv2.namedWindow("Trackbars")
    
    cv2.createTrackbar("L - H", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("U - H", "Trackbars", 255, 255, nothing)
    cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
    cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)

    #cap.set(cv2.CAP_PROP_FRAME_WIDTH,800)
    #cap.set(cv2.CAP_PROP_FRAME_HEIGHT,600)
    cap.set(3, 1280)
    cap.set(4, 720)
    frame_num = 0
    while True:
        ret, frame = cap.read()
        #cv2.imshow("Capture", frame)
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        frame_num = frame_num + 1
        #if frame_num > 300:
        #    cap.release()
        #    frame_num = 0
        #    cap = cv2.VideoCapture("mb.mp4")

        l_h = cv2.getTrackbarPos("L - H", "Trackbars")
        l_s = cv2.getTrackbarPos("L - S", "Trackbars")
        l_v = cv2.getTrackbarPos("L - V", "Trackbars")
        u_h = cv2.getTrackbarPos("U - H", "Trackbars")
        u_s = cv2.getTrackbarPos("U - S", "Trackbars")
        u_v = cv2.getTrackbarPos("U - V", "Trackbars")

        #cv2.imshow("HSV", hsv_frame)
        #Filter color
        lower_red = np.array([l_h,l_s,l_v])
        upper_red = np.array([u_h,u_s,u_v])
        #mask
        #f_frame = cv2.inRange(hsv_frame, lower_red, upper_red)
        f_frame = cv2.inRange(hsv_frame, np.array([0,187,100]), np.array([21,255,255]))
        #cv2.imshow("Masked", f_frame)
        #erode twice
        element = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
        element2 = cv2.getStructuringElement(cv2.MORPH_RECT,(8,8))
        
        erode_frame = cv2.erode(f_frame, element)
        erode_frame = cv2.erode(erode_frame, element)

        dilate_frame = cv2.dilate(erode_frame, element2)
        dilate_frame = cv2.dilate(dilate_frame, element2)
        dilate_frame = cv2.dilate(dilate_frame, element2)
        
        #cv2.imshow("MORPH", dilate_frame)
        x,y,w,h = cv2.boundingRect(dilate_frame)
        cv2.rectangle(frame, (x,y), (x+w, y+h) , (0,255,0),3)
########################################################################
        #sec_frame = cv2.inRange(hsv_frame, lower_red, upper_red)
        sec_frame = cv2.inRange(hsv_frame, np.array([23,125,142]), np.array([63,220,214]))

        element = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
        element2 = cv2.getStructuringElement(cv2.MORPH_RECT,(8,8))
        
        erode_frame2 = cv2.erode(sec_frame, element)
        erode_frame2 = cv2.erode(erode_frame2, element)

        dilate_frame2 = cv2.dilate(erode_frame2, element2)
        dilate_frame2 = cv2.dilate(dilate_frame2, element2)
        dilate_frame2 = cv2.dilate(dilate_frame2, element2)
        
        #cv2.imshow("MORPH", dilate_frame)
        x2,y2,w2,h2 = cv2.boundingRect(dilate_frame2)
        cv2.rectangle(frame, (x2,y2), (x2+w2, y2+h2) , (0,255,0),3)

        
        #Find contours
        #contours, hierarchy = cv2.findContours(dilate_frame, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        #for cnt in contours:
        #    rect = cv2.minAreaRect(cnt)
        #    #box = cv2.cv.BoxPoints(rect)
        #    box = cv2.boxPoints(rect)
        #    box = np.int0(box)
        #    cv2.drawContours(frame, [box], 0, (0,0,255), 2)
        #    #print("Angle:%d" % rect[2])
        
        #print("Angle:%3.2f" % (get_point_angle((x2,y2),(x,y))))
        cv2.putText(frame, "ANGLE:%4.2f"%(get_point_angle((x2,y2),(x,y))), (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,255,0), 2);

        cv2.imshow("MORPH", dilate_frame2)
        cv2.imshow("Capture", frame)
 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite("test.jpeg", frame)
            break
    cap.release()
    cv2.destroyAllWindows()

