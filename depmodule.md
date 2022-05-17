# DepModule 거리 인식 모듈

- 실행에 필요한 파일 및 폴더
depmodule.py, util.py, network 폴더

- 사용법 : 모듈을 import한 파이썬 파일을 만든다. 아래와 같이 사용할 수 있다.
```python3
from depmodule import DepModel
import cv2

# 아래는 사용법 실행 코드

# 1. 모델 객체 생성
depmodel = DepModel()

# 2. 모델 불러오기
depmodel.load_model(model_name  = "mono_640x192")

# 3-1. 이미지 경로로 이미지 불러오기 + 전처리
image = depmodel.load_image("assets/test_image.jpg")

# 3-2. 다른 경로에서 불러온 이미지를 전처리 하기
image = cv2.imread("assets/test_image.jpg") # 다른 곳에서 불러온 이미지
image = depmodel.preprocess_image(image)

# 4. 전처리된 이미지로 예측 진행
res = depmodel.predict(image)

# 5. 결과 시각화(디버깅용)
depmodel.show(vmax_percentage = 99)
```