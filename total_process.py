import cv2
import numpy as np
from odmodule.odmodule import OdModel
from depmodule.depmodule import DepModel
from segmodule import segmodule
from mergemodule.mergemodule import MergeModule
from alarmmodule.alarmmodule import Alarm
from calculate.calculate import Data
import time

OdModule = OdModel()
print("장애물 인식 모듈 Loaded")
SegModule = segmodule.SegModule()
print("도로 인식 모듈 Loaded")
DepModule = DepModel()
DepModule.load_model(model_name="mono_640x192")
print("거리 예측 모듈 Loaded")
MgModule = MergeModule()
print("정보 종합 모듈 Loaded")
CacModule = Data()
print("위험도 계산 모듈 Loaded")
ArModule = Alarm()
print("알람 모듈 Loaded")

cap = cv2.VideoCapture("street3.avi")

while(True):
    ret, image = cap.read()

    od_outputs, od_res = OdModule.predict(image)
    object_class = od_outputs['instances'].pred_classes.numpy()
    size = od_outputs['instances'].image_size
    object_location = od_outputs['instances'].pred_boxes.tensor.numpy()
    object_location = object_location.astype(int)
    print("장애물 인식 모듈 Finished")

    segmap, seg_res = SegModule.predict(image)
    class_seg_map = segmodule.convert(segmap)
    print("도로 인식 모듈 Finished")

    pre_image = DepModule.preprocess_image(image)
    distance = DepModule.predict(pre_image)
    print("거리 예측 모듈 Finished")

    MgModule.current_road(class_seg_map)
    cur_road = MgModule.now_road
    dep_road_res = MgModule.dep_road(class_seg_map, distance)
    od_classes, res = MgModule.dep_objects(object_class, object_location, distance)
    od_location = MgModule.loc_object(size, object_location)
    print("정보 종합 모듈 Finished")

    num_detect = int(input('한 프레임당 탐색 개체 수 : '))

    calculated_danger = np.array(CacModule.return_highest_danger(od_classes, od_location, res, dep_road_res, cur_road, num_detect))
    classes, direction, order = calculated_danger[:, 0], calculated_danger[:, 1], calculated_danger[:, 2]
    print("위험도 계산 모듈 Finished")

    org_image = image.copy()
    num = classes.size
    for i in range(num):
        if classes[i] == -1 or classes[i] == -2:
            ArModule.runmodule(classes[i], direction[i])
            # 도로 시각화
        else:
            res_image = cv2.rectangle(image, (object_location[order[i]][0], object_location[order[i]][1]),
                                    (object_location[order[i]][2], object_location[order[i]][3]), (0, 0, 255), 2)
            ArModule.runmodule(classes[i], direction[i])
            cv2.imshow("result", image)
            cv2.waitKey(1000)
            cv2.destroyAllWindows()
            image = org_image.copy()
    print("알람 모듈 Finished")
