from mergemodule.mergemodule import MergeModule
import numpy as np


mm = MergeModule()

class_segmap = np.array([[1, 0],[1, 0]]) 
distance = np.array([[0.23, 0.1],[0.32, 0.14]]) 

# 현재 나의 도로 test
# cr = mm.current_road(class_segmap, []) # 오류
# print(cr)


# 도로 별 거리 test
dr = mm.dep_road(class_segmap, distance, reduce=2)
print(dr)

