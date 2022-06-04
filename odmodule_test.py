from odmodule.odmodule import odmodule

OdModel = odmodule.OdModel()

# od_outputs = pred_boxex 등 Detectron2 ouputs, res = Detection된 이미지
od_outputs, res = OdModel.predict("filepath")
# im = cv2.imread("img_file")
# od_outputs, res = OdModel.predict(im)
