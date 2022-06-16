import cv2
import numpy as np
from odmodule.odmodule import OdModel
from depmodule.depmodule import DepModel
from segmodule import segmodule
from mergemodule.mergemodule import MergeModule
from alarmmodule.alarmmodule import Alarm
from calculate.calculate import Data
from threading import Thread
import time
import copy

NUMBER_OUT_SPEACH = 1
VISUALIZE = True
WATCH_FRAMES = 64 # 몇 프레임마다 하나씩 읽어오는지, 주의!!! 카메라로 할때는 사용하지 않는다. 동영상 읽을 때 비슷한 프레임이 너무 많아서 건너뛰기 위함.

def od_pred(id, img):
    global object_class, object_location, size, OdModule
    od_outputs, _ = OdModule.predict(img)
    object_class = od_outputs['instances'].pred_classes.cpu().numpy()
    size = od_outputs['instances'].image_size
    object_location = od_outputs['instances'].pred_boxes.tensor.cpu().numpy()
    object_location = object_location.astype(int)
    print("장애물 인식 모듈 Finished")


def seg_pred(id, img):
    global class_segmap, SegModule, segmap
    segmap, color_segmap = SegModule.predict(img)
    class_segmap = segmodule.convert(copy.copy(segmap))

    print("도로 인식 모듈 Finished")


def dep_pred(id, img):
    global distance, DepModule
    image = DepModule.preprocess_image(img)
    distance = DepModule.predict(image)
    print("거리 예측 모듈 Finished")


def exe_alarm(id, image, classes, direction, order, danger, object_location, segmap):
    global ArModule

    if type(image) == np.ndarray:  # 값이 들어왔으면
        res_image = None
        org_image = image.copy()
        num = classes.size
        for i in range(num):
            if danger[i] != 0:
                if classes[i] == -1 or classes[i] == -2:
                    # ArModule.runmodule(classes[i], direction[i])
                    if VISUALIZE and classes[i] == -1:
                        res_image = image
                    # 도로 시각화
                    if VISUALIZE and classes[i] == -2:  # 횡단보도 시각화
                        seg_out = copy.copy(segmap)
                        for c in segmodule.CUSTOM_COLOR_MAP:
                            if c != segmodule.CUSTOM_COLOR_MAP[3]:
                                seg_out[(seg_out == c).all(axis=2)] = [0, 0, 0]

                            h, w, _ = np.array(seg_out).shape
                            img_resized = cv2.resize(image, (w, h))
                            res_image = (img_resized * 0.5 +
                                         seg_out * 0.5).astype(np.uint8)

                else:
                    # 장애물 시각화
                    if VISUALIZE:
                        res_image = cv2.rectangle(image, (object_location[order[i]][0], object_location[order[i]][1]),
                                                  (object_location[order[i]][2], object_location[order[i]][3]),
                                                  (0, 0, 255), 2)
                        seg_out = copy.copy(segmap)
                        for c in segmodule.CUSTOM_COLOR_MAP:
                            if c != segmodule.CUSTOM_COLOR_MAP[3]:
                                seg_out[(seg_out == c).all(axis=2)] = [0, 0, 0]

                        # h, w, _ = np.array(seg_out).shape
                        # img_resized = cv2.resize(res_image, (w, h))
                        # res_image = (img_resized * 0.5 +
                        #              seg_out * 0.5).astype(np.uint8)
                        # cv2.imshow("result", res_image)
                        # cv2.waitKey(2000)
                        # cv2.destroyAllWindows()
                    # ArModule.runmodule(classes[i], direction[i])

                    image = org_image.copy()

                if VISUALIZE:

                    resize_result = cv2.resize(res_image, (1080, 720))
                    cv2.imshow("result", resize_result)
                    cv2.waitKey(500)
                    ArModule.runmodule(classes[i], direction[i])
                    cv2.destroyAllWindows()
                else:
                    ArModule.runmodule(classes[i], direction[i])

        print("알람 모듈 Finished")


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

cap = cv2.VideoCapture("street_cut.mp4")
# cap = cv2.VideoCapture(1)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

image, classes, direction, order, danger, object_location, segmap = None, None, None, None, None, None, None
while(True):

    th4 = Thread(target=exe_alarm, args=(
        4, image, classes, direction, order, danger, object_location, segmap))
    # if th4.is_alive():
    th4.start()

    start = time.time()
    for _ in range(WATCH_FRAMES):
        ret, image = cap.read()

    if not ret:
        break

    object_location, object_class, size = None, None, None
    th1 = Thread(
        target=od_pred, args=(1, image))
    th1.start()

    class_segmap, color_segmap, segmap = None, None, None
    th2 = Thread(target=seg_pred, args=(2, image))
    th2.start()

    distance = None
    th3 = Thread(target=dep_pred, args=(3, image))
    th3.start()

    th1.join()
    th2.join()
    th3.join()
    th4.join()

    MgModule.current_road(class_segmap)
    cur_road = MgModule.now_road
    dep_road_res = MgModule.dep_road(class_segmap, distance, 30)
    od_classes, res = MgModule.dep_objects(
        object_class, object_location, distance)
    od_location = MgModule.loc_object(size, object_location)
    print("정보 종합 모듈 Finished")

    num_detect = NUMBER_OUT_SPEACH  # int(input('한 프레임당 탐색 개체 수 : '))

    calculated_danger = np.array(CacModule.return_highest_danger(
        od_classes, od_location, res, dep_road_res, cur_road, num_detect))
    # if calculated_danger.size !=0:
    classes, direction, order, danger = calculated_danger[:,0], calculated_danger[:, 1], calculated_danger[:, 2], calculated_danger[:, 3]
    print("위험도 계산 모듈 Finished")

    end = time.time()
    print(f"{end - start:.5f} sec")
