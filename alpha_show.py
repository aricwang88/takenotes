import cv2

x_offset=5
y_offset=5

def load_alpha_PNG(fn):
    img = cv2.imread(fn, cv2.IMREAD_UNCHANGED)
    channels = cv2.split(img)
    mask = channels[3]
    res = cv2.bitwise_and(img, img, mask=mask)
    return res


def load_png(x_offset, y_offset, s_img, l_img):
    y1,y2=y_offset, y_offset+s_img.shape[0]
    x1,x2=x_offset, x_offset+s_img.shape[1]

    alpha_s = s_img[:,:,3]/255.0
    alpha_l = 1.0 - alpha_s

    for c in range(0, 3):
        l_img[y1:y2, x1:x2, c] = (alpha_s * s_img[:,:,c] + alpha_l * l_img[y1:y2, x1:x2,c]) 
    return l_img
    pass

#cap = cv2.VideoCapture("rtsp://192.168.1.3:8554/live") #http://172.16.1.89:8080/?action=stream") #0)
cap = cv2.VideoCapture(1)
#cap.set(cv2.CAP_PROP_BUFFERSIZE,1)
cap.set(3, 1280)
cap.set(4, 720)

png_alpha = load_alpha_PNG("football01.png")
pa = png_alpha
while True:
    ret,big_frame = cap.read()
    #big_frame = cv2.resize(frame, (1280,720))
    #big_frame = cv2.cvtColor(big_frame, cv2.COLOR_RGB2RGBA)
    #big_frame[y_offset:y_offset+png_alpha.shape[0], x_offset:x_offset+png_alpha.shape[1]]=png_alpha

    big_frame = load_png(5,5,png_alpha,big_frame)
    cv2.imshow("frame", big_frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

cap.release()
cv2.destroyAllWindows()

