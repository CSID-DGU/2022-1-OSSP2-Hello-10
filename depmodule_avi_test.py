from depmodule.depmodule import DepModel
import numpy as np
import cv2



# 1. 모델 객체 생성
depmodel = DepModel()

# 2. 모델 불러오기
depmodel.load_model(model_name  = "mono_640x192")

cap = cv2.VideoCapture("street_cut.mp4")
if not cap.isOpened():
    print("Error opening video")
    exit(0)

# 웹캠의 속성 값을 받아오기
# 정수 형태로 변환하기 위해 round
w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS) # 카메라에 따라 값이 정상적, 비정상적

# fourcc 값 받아오기, *는 문자를 풀어쓰는 방식, *'DIVX' == 'D', 'I', 'V', 'X'
fourcc = cv2.VideoWriter_fourcc(*'DIVX')

# 1프레임과 다음 프레임 사이의 간격 설정
delay = round(fps)

# 웹캠으로 찰영한 영상을 저장하기
# cv2.VideoWriter 객체 생성, 기존에 받아온 속성값 입력
out = cv2.VideoWriter('street_cut_out.avi', fourcc, fps, (w, h))

# 제대로 열렸는지 확인
if not out.isOpened():
    print('File open failed!')
    cap.release()
    exit(0)

while cap.isOpened():
    
    ret, frame = cap.read()

    if ret:
        # 3-2. 다른 경로에서 불러온 이미지를 전처리 하기
        image = depmodel.preprocess_image(frame)# cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # 4. 전처리된 이미지로 예측 진행
        res = depmodel.predict(image)

        # depmodel.save()

        res = (res * 255. ).astype(np.uint8)
        # cv2.imshow("show", res)
        # cv2.imshow("image", image)

        res_color = cv2.cvtColor(res, cv2.COLOR_GRAY2BGR)

        h, w, _ = np.array(res_color).shape
        img_resized = cv2.resize(image, (w, h))

        res_image = (img_resized * 0.05 + res_color * 0.95).astype(np.uint8)

        # cv2.imshow("res", res_image)
        out.write(res_image) # 영상 데이터만 저장. 소리는 X
    else:
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        exit(0)
    
cv2.destroyAllWindows()
cap.release()