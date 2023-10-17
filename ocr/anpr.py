import cv2
import numpy as np
import imutils
import easyocr
# from cv2 import dnn_superres


# load video
cap = cv2.VideoCapture('./sample.mp4')
sr = cv2.dnn_superres.DnnSuperResImpl_create()
# sr.readModel("EDSR_x4.pb")
# sr.setModel('edsr',4)

sr.readModel("EDSR_x4.pb")
sr.setModel('edsr',4)
# sr.setPreferableBackend(cv2.dnn.DNN_BACKEND_CANN)
# sr.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
# read frames
ret = True
while ret:
    ret, frame = cap.read()
    # print(frame)
    # print(frame.shape)
    
    if ret:
        
        try:
            # gray = frame
            # (h, w) = frame.shape[:2]
            # print(h,w)
            frame = frame[600:800, 500:]
            (h, w) = frame.shape[:2]
            (cX, cY) = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D((cX, cY), -25, 1.0)
            frame = cv2.warpAffine(frame, M, (w, h))

            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            # gray = gray[600:800, 500:]
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
            # new_image = cv2.bitwise_and(frame, frame, mask=mask)

            (x,y) = np.where(mask==255)
            (x1, y1) = (np.min(x), np.min(y))
            (x2, y2) = (np.max(x), np.max(y))
            cropped_image = frame[x1:x2+20, y1:y2+20]
            # cropped_image = cv2.resize(cropped_image, None, fx=5, fy=5)

            
            upscalled = sr.upsample(cropped_image)
            # adjusted_image = cv2.adjustContrast(rotated, 2.0, 0.0)

            cv2.imshow('graycsale image',upscalled)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            # reader = easyocr.Reader([ 'en' ] )
            # result = reader.readtext(upscalled)
            # if len(result) != 0:
            #     print(result[0][1])
        except Exception as e: 
            pass
