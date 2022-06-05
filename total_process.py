import cv2
from odmodule.odmodule import OdModel
from depmodule.depmodule import DepModel
from segmodule import segmodule
from mergemodule.mergemodule import MergeModule
from alarmmodule.alarmmodule import Alarm
from calculate.calculate import Data
import time

OdModule = OdModel()
SegModule = segmodule.SegModule()
DepModule = DepModel()
DepModule.load_model(model_name  = "mono_640x192")
MgModule = MergeModule()
CacModule = Data()
ArModule = Alarm()

cap = cv2.VideoCapture('street3.avi')

while(True):
    ret, image = cap.read()

    od_outputs, od_res = OdModule.predict(image)
    object_class = od_outputs['instances'].pred_classes.numpy()
    size = od_outputs['instances'].image_size
    objcet_location = od_outputs['instances'].pred_boxes.tensor.numpy()
    objcet_location = objcet_location.astype(int)

    segmap, seg_res = SegModule.predict(image)
    class_seg_map = segmodule.convert(segmap)

    pre_image = DepModule.preprocess_image(image)
    distance = DepModule.predict(pre_image)

    MgModule.current_road(class_seg_map)
    cur_road = MgModule.now_road
    dep_road_res = MgModule.dep_road(class_seg_map, distance)
    od_classes, dep_obj_res = MgModule.dep_objects(object_class, objcet_location, distance)
    od_location = MgModule.loc_object(size, objcet_location)

    classes, direction = CacModule.return_highest_danger(od_classes, od_location, dep_obj_res, dep_road_res, cur_road)

    ArModule.runmodule(classes, direction)
