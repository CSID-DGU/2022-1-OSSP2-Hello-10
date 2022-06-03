import cv2
import odmodule
from depmodule import DepModel
import segmodule
import MergeModule
from alarm import Alarm

OdModel = odmodule.OdModel()
SegModel = segmodule.SegModule()
depmodel = DepModel()
depmodel.load_model(model_name  = "mono_640x192")
mgmodule = MergeModule.MergeModule()
armodule = Alarm()

image = cv2.imread("test_img.jpg")

od_outputs, res = OdModel.predict(image)

segmap, res = SegModel.predict(image)
class_seg_map = segmodule.convert(segmap)

image = depmodel.preprocess_image(image)
distance = depmodel.predict(image)

mgmodule.current_road(class_seg_map, distance)
rdist = mgmodule.dep_road(class_seg_map, distance)

object_class = od_outputs['instances'].pred_classes.numpy()
size = od_outputs['instances'].image_size
objcet_location = od_outputs['instances'].pred_boxes.tensor.numpy()

od_classes, res = mgmodule.dep_objects(object_class, objcet_location, distance)
od_location = mgmodule.loc_object(size, objcet_location)

#armodule.runmodule(classes, distance)
