import numpy as np
from enum import Enum


class Road(Enum):
    background = 0
    bike_lane = 1  # 자전거 도로
    caution_zone = 2  # 주의 구역
    crosswalk = 3  # 횡단 보도
    guide_block = 4  # 점자 블록
    roadway = 5  # 차도
    sidewalk = 6  # 인도


def count_roads(arr):  # 도로 카테고리 별 픽셀 수
    # 입력
    # arr : numpy array
    # return : 인덱스 별 픽셀 수 ex list[6] = sidewalk 픽셀 수
    roads = []
    for r in Road:
        roads += (arr == r.value).sum()
    return roads


def reduce_arr(arr: np.ndarray, n: int) -> np.ndarray:
    # 입력
    # arr : 2차원 numpy array
    # n : int
    # return : n 행 및 열 마다 1개씩 축소된 arr
    if arr.ndim !=2:
      print("2차원 배열만 처리 가능합니다.")
      return
    
    if n==0:
        return arr

    column, row = arr.shape
    for i in range(column-1, -1, -n):
      arr = np.delete(arr, i, axis=0)

    for i in range(row-1, -1, -n):
      arr = np.delete(arr, i, axis = 1)
    
    return arr

class MergeModule:
    def __init__(self):
        self.now_road = 0  # 현재도로 초기값 background

    def current_road(self, class_segmap, distance):  # 현재 나의 도로 enum 값
        # 입력
        # class_segmap : 인식된 도로의 class로 segmentation된 numpy array(img size)
        y, x = class_segmap.shape
        # y 축의 하단 20%, x축의 중앙 30%로 Indexing
        roads = count_roads(class_segmap[int(y*0.75):, int(x*0.3):int(x*0.65)])
        new_road = roads.index(max(roads))  # 현재 나의 도로 enum 값
        self.now_road = new_road  # 현재 나의 도로 update

    def dep_road(self, class_segmap, distance, reduce = 4):  # 도로 별 거리
        # 입력
        # class_segmap : 인식된 도로의 class로 segmentation된 1 channel numpy array(img size)
        # distance : 픽셀 별 상대적 거리, 1 channel numpy array(img size)
        # reduce : 축소할 비율, n 행 및 열 마다 1개씩 축소되어 처리됨
        # 출력
        # Road에 저장된 도로 클래스 별로 거리가 존재하는 경우 0~1 사이의 실수로, 아닌 경우, 100.0을 출력 
        # 배열 크기는 Road에 저장된 도로 클래스의 수와 같다.
        # ex) [0.1, 0.4, 0.3, 0.1, 100.0, 0.3, 0.12]

        res = [100.0 for r in Road] # 도로 수만큼 100.0을 원소로 가지는 배열 생성

        reduced_segmap = reduce_arr(class_segmap, reduce) # 1/reduce로 축소
        reduced_distance = reduce_arr(distance, reduce)

        reduced_segmap = np.reshape(reduced_segmap, (-1)) # 1차원으로 차원 축소
        reduced_distance = np.reshape(reduced_distance, (-1))

        for class_seg, distance in zip(reduced_segmap, reduced_distance):
          if res[class_seg] > distance:
            res[class_seg] = distance # 저장된 최소 거리보다 작은 값이 입력으로 들어오면, 클래스의 최소 거리를 업데이트

        return res

    def dep_objects(self, object_class, objcet_location, distance):  # 장애물 별 거리
        # 입력
        # objcet_class : 인식된 장애물의 class, [장애물, 장애물, 장애물, ...] ex)[1, 2, 3,...]
        # objcet_location : 인식된 장애물의 위치, [좌상 픽셀, 우하 픽셀], [[x1, y1, x2, y2], ...]
        # distance : 픽셀 별 상대적 거리, 1 channel numpy array
        # 출력
        # tuple(인식된 장애물의 class: list, 장애물 별 거리: list)
        # ex) [1, 2, 3,...], [0.1, 0.4, 0.12, ...]
        res = []
        for loc in objcet_location:
            x1, y1, x2, y2 = loc
            # distance를 장애물의 범위 내로 슬라이싱
            cut_distance = distance[y1:y2+1, x1:x2+1]
            res.append(np.min(cut_distance))  # 최솟값 추가
        return object_class, res

    def loc_object(self, size, objcet_location):  # 장애물 위치(좌측, 중앙, 우측)
        # 입력
        # size : 가로 x 세로, ex) (width, height)
        # objcet_location : 인식된 장애물의 위치, [좌상 픽셀, 우하 픽셀], [[x1, y1, x2, y2], ...]
        # 출력
        # 좌측, 중앙, 우측 해당 여부, [[bool, bool, bool], ...]
        res = []
        for loc in objcet_location:
            temp = [False, False, False]
            width, height = size
            left, right = loc[0], loc[2]
            if width/3 > left:
                temp[0] = True  # 좌측 True로
            elif width*2/3 > left:
                temp[1] = True  # 중앙을 True로
            else:
                temp[2] = True  # 우측을 True로
                res.append(temp)
                continue

            if width/3 > right:
                pass  # 좌측 이미 True일 것이므로 pass
            elif width*2/3 > right:
                temp[1] = True  # 중앙 True로
            else:
                temp[2] = True  # 우측을 True로
            res.append(temp)

        return res  # 함수 종료
