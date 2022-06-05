import cv2
from odmodule.odmodule import odmodule
from depmodule.depmodule import DepModel
from segmodule.segmodule import segmodule
from mergemodule.mergemodule import MergeModule
from alarmmodule.alarmmodule import Alarm
from calculate.calculate import Data
from threading import Thread


def od_pred(id, img):
    global object_class, object_location, size, OdModel
    od_outputs, _ = OdModel.predict(img)
    object_class = od_outputs['instances'].pred_classes.numpy()
    size = od_outputs['instances'].image_size
    object_location = od_outputs['instances'].pred_boxes.tensor.numpy()
    object_location = object_location.astype(int)


def seg_pred(id, img):
    global class_segmap, SegModel
    segmap, _ = SegModel.predict(img)
    class_segmap = segmodule.convert(segmap)


def dep_pred(id, img):
    global distance, depmodel
    image = depmodel.preprocess_image(img)
    distance = depmodel.predict(img)


OdModel = odmodule.OdModel()
SegModel = segmodule.SegModule()
depmodel = DepModel()
depmodel.load_model(model_name="mono_640x192")
mgmodule = MergeModule()
cacmodule = Data()
armodule = Alarm()

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

    mgmodule.current_road(class_segmap)
    cur_road = mgmodule.now_road
    dep_road_res = mgmodule.dep_road(class_segmap, distance)
    od_classes, res = mgmodule.dep_objects(
        object_class, object_location, distance)
    od_location = mgmodule.loc_object(size, object_location)

    classes, direction = cacmodule.return_highest_danger(
        od_classes, od_location, res, dep_road_res, cur_road)

    armodule.runmodule(classes, direction)
