from alarm import Alarm


classes, distance = [['사람', '전봇대', '자전거', '차도', '횡단보도'], [10, 2, 5, 7, 15]]
a = Alarm()
a.runmodule(classes, distance)
