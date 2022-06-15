from segmodule import segmodule
import cv2
import numpy as np

SegModel = segmodule.SegModule()

# segmap = segmentation info, res = image + segmap
# segmap, res = SegModel.predict("segmodule/test_image.jpg")
image = cv2.imread("segmodule/docs/imgs/MP_SEL_SUR_001457.jpg")
segmap, res = SegModel.predict(image)

class_seg_map = segmodule.convert(segmap)  # (720, 1280) 각 픽셀별 클래스 값

print(res)
print(class_seg_map)

h, w, _ = np.array(image).shape
res_resized = cv2.resize(res, (w, h))
res_image = res_resized # (image * 1.0 + res_resized * 100).astype(np.uint8)

cv2.imshow("result", res_image)
cv2.waitKey(6000)
cv2.destroyAllWindows()