import segmodule
import cv2

SegModel = segmodule.SegModel()

# segmap = segmentation info, res = segmap + orginal img
segmap, res = SegModel.predict("file_path")
# im = cv2.imread("img_file")
# segmap, res = SegModel.predict(im)
