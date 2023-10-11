import cv2
from matplotlib import pyplot as plt
import numpy as np
import imutils
import easyocr


# load video
cap = cv2.VideoCapture('./sample.mp4')


# read frames
ret = True
while ret:
    ret, frame = cap.read()
    # print(frame)
    # print(frame.shape)
    
    if ret:
        
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            bfilter = cv2.bilateralFilter(gray, 11, 17, 17) #Noise reduction
            edged = cv2.Canny(bfilter, 30, 200) #Edge detection
            keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours = imutils.grab_contours(keypoints)
            contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
            location = None
            for contour in contours:
                approx = cv2.approxPolyDP(contour, 10, True)
                if len(approx) == 4:
                    location = approx
                    break

            mask = np.zeros(gray.shape, np.uint8)
            new_image = cv2.drawContours(mask, [location], 0,255, -1)
            new_image = cv2.bitwise_and(frame, frame, mask=mask)
            (x,y) = np.where(mask==255)
            (x1, y1) = (np.min(x), np.min(y))
            (x2, y2) = (np.max(x), np.max(y))
            cropped_image = gray[x1:x2+1, y1:y2+1]

            cv2.imshow('graycsale image',cropped_image)
            cv2.destroyAllWindows()

            # reader = easyocr.Reader([ 'en' ] )
            # result = reader.readtext(cropped_image)
            # print(result)
        except:
            pass
