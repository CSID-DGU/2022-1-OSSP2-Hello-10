# 임계값 설정 임계값을 넘는 장애물만 장애물 배열 넣는다.
# 도로 이탈은 높은 위험도로 설정한다.
# 횡단보도 일정거리 이하로 들어오면 장애물에 넣는다.
import numpy as np

class Data:
    def calculate_danger(Road_kind, Objkind, distance) -> danger:
        
        
    def __init__(self, Road_kind, Obj_kind, distance, danger) -> None:
        self.Obj_kind = Obj_kind
        self.distance = distance
        self.danger = calculate_danger(Road_kind, Obj_kind, distance)
        
    def __lt__(self, other):
        return self.danger < other.danger