import cv2
from odmodule.odmodule import OdModel
from depmodule.depmodule import DepModel
from segmodule import segmodule
from mergemodule.mergemodule import MergeModule
from alarmmodule.alarmmodule import Alarm
from calculate.calculate import Data
from threading import Thread


def od_pred(id, img):
    global object_class, object_location, size, OdModule
    od_outputs, _ = OdModule.predict(img)
    object_class = od_outputs['instances'].pred_classes.numpy()
    size = od_outputs['instances'].image_size
    object_location = od_outputs['instances'].pred_boxes.tensor.numpy()
    object_location = object_location.astype(int)


def seg_pred(id, img):
    global class_segmap, SegModule
    segmap, _ = SegModule.predict(img)
    class_segmap = segmodule.convert(segmap)


def dep_pred(id, img):
    global distance, DepModule
    image = DepModule.preprocess_image(img)
    distance = DepModule.predict(img)


OdModule = OdModel()
SegModule = segmodule.SegModule()
DepModule = DepModel()
DepModule.load_model(model_name  = "mono_640x192")
MgModule = MergeModule()
CacModule = Data()
ArModule = Alarm()

cap = cv2.VideoCapture(1)

while(True):

    ret, image = cap.read()

    object_location, object_class, size = None, None, None
    th1 = Thread(
        target=od_pred, args=(1, image))
    th1.start()

    class_segmap = None
    th2 = Thread(target=seg_pred, args=(2, image))
    th2.start()

    distance = None
    th3 = Thread(target=dep_pred, args=(3, image))
    th3.start()

    th1.join()
    th2.join()
    th3.join()

    MgModule.current_road(class_segmap)
    cur_road = MgModule.now_road
    dep_road_res = MgModule.dep_road(class_segmap, distance)
    od_classes, res = MgModule.dep_objects(
        object_class, object_location, distance)
    od_location = MgModule.loc_object(size, object_location)

    classes, direction = CacModule.return_highest_danger(
        od_classes, od_location, res, dep_road_res, cur_road)

    ArModule.runmodule(classes, direction)
