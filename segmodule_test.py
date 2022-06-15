from segmodule import segmodule
import cv2

SegModel = segmodule.SegModule()

# segmap = segmentation info, res = segmap + orginal img
segmap, res = SegModel.predict("segmodule/test_image.jpg")
# im = cv2.imread("segmodule/test_image.jpg")
# segmap, res = SegModel.predict(im)

class_seg_map = segmodule.convert(segmap)  # (720, 1280) 각 픽셀별 클래스 값

print(res)
print(class_seg_map)