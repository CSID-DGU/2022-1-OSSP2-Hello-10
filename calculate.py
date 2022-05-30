# 임계값 설정 임계값을 넘는 장애물만 장애물 배열 넣는다.
# 도로 이탈은 높은 위험도로 설정한다.
# 횡단보도 일정거리 이하로 들어오면 장애물에 넣는다.
import numpy as np
# 위험도의 초대값은 100으로 설정
# 거리는 대략적인 상대값이 나오고 이 상대적인 값도 정확하지 않기 때문에 소수점 첫째자리까지만 사용
# 도로이탈의 위험도는 특정 거리안에서 100 상수로 설정 같은 위험도가 있더라도 가장 우선순위로 한다.
# 같은 거리에서 위험도는 도로이탈 > 차량> 자전거 > 사람 > 소화전 > 가로수 > 전봇대으로 설정
class Data:
    def trans_distance(distance):
        if distance >= 0 and distance < 0.1:
            return 0
        elif distance >= 0.1 and distance < 0.2:
            return 0.1
        elif distance >= 0.2 and distance < 0.3:
            return 0.2
        elif distance >= 0.3 and distance < 0.4:
            return 0.3
        elif distance >= 0.4 and distance < 0.5:
            return 0.4
        elif distance >= 0.5 and distance < 0.6:
            return 0.5
        elif distance >= 0.6 and distance < 0.7:
            return 0.6
        elif distance >= 0.7 and distance < 0.8:
            return 0.7
        elif distance >= 0.8 and distance < 0.9:
            return 0.8
        else:
            return 0.9
    def calculate_danger(Road_kind, Objkind, distance):
        danger = 1 / (int(distance) + 0.01)
        if Objkind == "people":
            danger *= 1
        elif Objkind == "bicycle":
            danger *= 1
        elif Objkind == "motorcycle":
            danger *= 1
        elif Objkind == "car":
            danger *= 1
        elif Objkind == "tree":
            danger *= 1
        elif Objkind == "powerpole":
            danger *= 1
        elif Objkind == "fireplug":
            danger *= 1 
        return danger
        
    def __init__(self, Road_kind, Obj_kind, distance, danger) -> None:
        self.Obj_kind = Obj_kind
        self.distance = distance
        self.danger = calculate_danger(Road_kind, Obj_kind, distance)
        
    def __lt__(self, other):
        return self.danger < other.danger