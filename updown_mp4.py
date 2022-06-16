# 원본 영상, 실행 결과 위아래 동영상으로 합치는 코드

import numpy as np
import cv2

cap1 = cv2.VideoCapture("street_cut.mp4")
if not cap1.isOpened():
    print("Error opening video")
    exit(0)

# cap2 = cv2.VideoCapture("res.mp4")
# if not cap2.isOpened():
#     print("Error opening video")
#     cap1.release()
#     exit(0)

w = round(640)
h = round(480)
fps = cap1.get(cv2.CAP_PROP_FPS) # 카메라에 따라 값이 정상적, 비정상적

# fourcc 값 받아오기, *는 문자를 풀어쓰는 방식, *'DIVX' == 'D', 'I', 'V', 'X'
fourcc = cv2.VideoWriter_fourcc(*'DIVX')

# 1프레임과 다음 프레임 사이의 간격 설정
delay = round(fps)

# 웹캠으로 찰영한 영상을 저장하기
# cv2.VideoWriter 객체 생성, 기존에 받아온 속성값 입력
out = cv2.VideoWriter('demo.avi', fourcc, fps, (w, h))


# 제대로 열렸는지 확인
if not out.isOpened():
    print('File open failed!')
    cap1.release()
    # cap2.release()
    exit(0)

image_path = "D:/DGU/3-1/OpenSWProject/git/out/res/"
i = 0

while cap1.isOpened(): #and cap2.isOpened():
    
    ret1, image = cap1.read()
    # ret2, dep = cap2.read()
    dep = cv2.imread(image_path+"%d.png"%i)
    if ret1: #and ret2:
        
        img_resized = cv2.resize(image, (w, round(h/2)))
        dep_resized = cv2.resize(dep, (w, round(h/2)))

        res_image = cv2.vconcat([img_resized, dep_resized])

        out.write(res_image) # 영상 데이터만 저장. 소리는 X
    else:
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        exit(0)
    i+=1

cv2.destroyAllWindows()
cap1.release()
# cap2.release()
out.release()