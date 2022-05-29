import numpy as np

class MergeModule:
  def __init__(self):
    pass

  def current_road(self): # 현재 나의 도로
    pass

  def dep_road(self): # 거리 별 거리
    pass
  
  def dep_objects(self, object_class, objcet_location, distance): # 장애물 별 거리
    # 입력
    # objcet_class : 인식된 장애물의 class, [장애물, 장애물, 장애물, ...] ex)[1, 2, 3,...] 
    # objcet_location : 인식된 장애물의 위치, [[[왼쪽 위 점], [오른쪽 위 점], [왼쪽 아래 점], [오른쪽 아래 점]], ...] ex) [[[x1,y1], [x2,y1], [x1,y2], [x2,y2]], ...]
    # distance : 픽셀 별 상대적 거리, 1 channel numpy array 
    res = []
    for loc in objcet_location:
      y1, y2, x1, x2 = map(int, [loc[0][1], loc[3][1], loc[0][0], loc[1][0]])# 값 수정해야함
      # distance를 장애물의 범위 내로 슬라이싱
      cut_distance = distance[y1:y2,x1:x2]
      res.append(np.min(cut_distance))# 최솟값 추가
    return object_class, res


