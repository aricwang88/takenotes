#!/usr/bin/env python

import os,sys,time
import cv2
import numpy as np

def nothing(x):
    pass
 

if __name__ == '__main__':
    cap = cv2.VideoCapture("mb.mp4") #1)
    cv2.namedWindow("Trackbars")
    
    cv2.createTrackbar("L - H", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("L - S", "Trackbars", 41, 255, nothing)
    cv2.createTrackbar("L - V", "Trackbars", 68, 255, nothing)
    cv2.createTrackbar("U - H", "Trackbars", 7, 255, nothing)
    cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
    cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)

    #cap.set(cv2.CAP_PROP_FRAME_WIDTH,800)
    #cap.set(cv2.CAP_PROP_FRAME_HEIGHT,600)
    cap.set(3, 1280)
    cap.set(4, 720)

    frame_num = 0
    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (1280,720))
        frame_num = frame_num + 1
        if frame_num > 300:
            cap.release()
            frame_num = 0
            cap = cv2.VideoCapture("mb.mp4")

        #cv2.imshow("Capture", frame)
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

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
        f_frame = cv2.inRange(hsv_frame, np.array([0,0,0]), np.array([255,255,17]))
        #cv2.imshow("Masked", f_frame)
        #erode twice
        element = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
        element2 = cv2.getStructuringElement(cv2.MORPH_RECT,(8,8))
        
        erode_frame = cv2.erode(f_frame, element)
        erode_frame = cv2.erode(erode_frame, element)

        dilate_frame = cv2.dilate(erode_frame, element2)
        dilate_frame = cv2.dilate(dilate_frame, element2)
        
        #cv2.imshow("MORPH", dilate_frame)
        x,y,w,h = cv2.boundingRect(dilate_frame)
        cv2.rectangle(frame, (x-20,y-20), (x+w+30, y+h+40) , (0,255,0),3)
        cv2.putText(frame, "USV(%d,%d)"%(x,y), (x,y-37), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,255,0), 2);
        
        contours, hierarchy = cv2.findContours(dilate_frame, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        black_idx=0
        for cnt in contours:
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            if rect[1][0] > 8:
                cv2.drawContours(frame, [box], 0, (0,250,250), 2)
                cv2.putText(frame, "Angle:"+"%3.2f ID:%d" % (rect[2],black_idx), (box[0][0],box[0][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (15,170,50), 2);
                black_idx=black_idx+1
       
        #enlarge the picture
        y0 = y-20
        x0 = x-30
        img = frame[y0:y0+h+40, x0:x0+w+40]

        hsv_boat = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        #boat_frame = cv2.inRange(hsv_boat, np.array([0,0,0]), np.array([255,108,255]))
        boat_frame = cv2.inRange(hsv_boat, lower_red, upper_red)
        
        #Find contours
        contours, hierarchy = cv2.findContours(boat_frame, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        black_idx=0
        for cnt in contours:
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            if rect[1][0] > 98:
                cv2.drawContours(frame, [box], 0, (0,0,255), 2)
                #print("Angle:%d" % rect[2])
                cv2.putText(frame, "Angle:"+"%3.2f ID:%d" % (rect[2],black_idx), (box[0][0],box[0][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (150,17,50), 1);
                cv2.rectangle(frame,(0,0),(169,39),(100,100,100),-1)
                cv2.putText(frame, "Angle:"+"%3.2f" % rect[2], (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (150,17,15), 2);
                black_idx=black_idx+1

        cv2.imshow("MORPH", dilate_frame)
        cv2.imshow("Capture", frame)
        cv2.imshow("Boat",boat_frame)
        #time.sleep(0.1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite("test.jpeg", frame)
            break
    cap.release()
    cv2.destroyAllWindows()

