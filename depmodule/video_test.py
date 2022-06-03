from depmodule import DepModel
import cv2
import numpy as np
# import matplotlib.pyplot as plt


cap = cv2.VideoCapture('./street3.avi')

width = int(cap.get(3)) # 가로 길이 가져오기 
height = int(cap.get(4)) # 세로 길이 가져오기
fps = 20

depmodel = DepModel()
depmodel.load_model(model_name  = "mono_640x192")

fcc = cv2.VideoWriter_fourcc(*'MJPG')
# fcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
# out = cv2.VideoWriter('output.avi', fcc, fps, (width, height))

# img2 = np.zeros_like(640, 192)
# img2[:,:,0] = gray
# img2[:,:,1] = gray
# img2[:,:,2] = gray

while (cap.isOpened()) :
    ret, frame = cap.read()
    if ret :
        image = depmodel.preprocess_image(frame)
        res = depmodel.predict(image)
        # depmodel.show(vmax_percentage = 99)
        # img2[:,:,0] = res
        # cv2.imshow('res', img2)
        # out.write(res)

        depmodel.show(99)

        if cv2.waitKey(1) & 0xFF == ord('q') : break
    else :
        print("Fail to read frame!")
        break

cap.release()
# out.release()
cv2.destroyAllWindows()
