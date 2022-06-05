import cv2
from odmodule.odmodule import odmodule
from depmodule.depmodule import DepModel
from segmodule.segmodule import segmodule
from mergemodule.mergemodule import MergeModule
from alarmmodule.alarmmodule import Alarm
from calculate.calculate import Data

OdModel = odmodule.OdModel()
SegModel = segmodule.SegModule()
depmodel = DepModel()
depmodel.load_model(model_name  = "mono_640x192")
mgmodule = MergeModule()
cacmodule = Data()
armodule = Alarm()

cap = cv2.VideoCapture('street3.avi')

while(cap.isOpened()):

    ret, image = cap.read()

    od_outputs, res = OdModel.predict(image)
    object_class = od_outputs['instances'].pred_classes.numpy()
    size = od_outputs['instances'].image_size
    objcet_location = od_outputs['instances'].pred_boxes.tensor.numpy()
    objcet_location = objcet_location.astype(int)

    segmap, res = SegModel.predict(image)
    class_seg_map = segmodule.convert(segmap)

    image = depmodel.preprocess_image(image)
    distance = depmodel.predict(image)

    mgmodule.current_road(class_seg_map)
    cur_road = mgmodule.now_road
    dep_road_res = mgmodule.dep_road(class_seg_map, distance)
    od_classes, res = mgmodule.dep_objects(object_class, objcet_location, distance)
    od_location = mgmodule.loc_object(size, objcet_location)

    classes, direction = cacmodule.return_highest_danger(od_classes, od_location, res, dep_road_res, cur_road)

    armodule.runmodule(classes, direction)
