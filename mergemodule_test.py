from mergemodule.mergemodule import MergeModule
import numpy as np


mm = MergeModule()

class_segmap = np.array([[1, 0, 0, 2],
                          [1, 0, 0, 2], 
                          [1, 0, 0, 0]]) 
distance = np.array([[0.23, 0.1, 0.1, 0.1],
                      [0.32, 0.14, 0.2, 0.2], 
                      [0.01,0.02, 0.03, 0.04]]) 
object_class = np.array([0, 1])
objcet_location = np.array([[0,0,1,1],[1,1,2,2]])

# 현재 나의 도로 test
# cr = mm.current_road(class_segmap, []) # 오류
# print("현재 나의 도로:",cr)


# 도로 별 거리 test
dr = mm.dep_road(class_segmap, distance, reduce=2) # 정상 실행
print("도로 별 거리:", dr)
# 도로 별 거리: [0.2, 0.32, 100.0, 100.0, 100.0, 100.0, 100.0]

# 장애물 별 거리 test
do = mm.dep_objects(object_class, objcet_location, distance) # 정상 실행
print("장애물 클래스:",do[0],", 장애물 별 거리", do[1])
# 장애물 클래스: [0 1] , 장애물 별 거리 [0.1, 0.02]

# 장애물 위치(좌측, 중앙, 우측) test
lo = mm.loc_object(class_segmap.shape, objcet_location) # 정상 작동
print("장애물 위치[좌측, 중앙, 우측]:",lo)
# 장애물 위치[좌측, 중앙, 우측]: [[True, True, False], [False, True, True]]