# Some basic setup:
# Setup detectron2 logger
import cv2
import json
import os
import detectron2
import numpy as np
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.utils.logger import setup_logger
from detectron2.utils.visualizer import Visualizer
import torch
import torchvision


# import some common libraries
# import some common detectron2 utilities

class OdModel():

    def __init__(self):
        setup_logger()
        cfg = get_cfg()
        cfg.merge_from_file("Base-RetinaNet.yaml")
        # cfg.merge_from_file(
        #     "/content/drive/MyDrive/Base-RetinaNet.yaml")  # Ver.Colab
        cfg.MODEL.WEIGHTS = "retinanet_r_50_fpn_3x_aihub_final.pth"  # model path
        # cfg.MODEL.WEIGHTS = "/content/drive/MyDrive/retinanet_r_50_fpn_3x_aihub_final.pth"  # Ver.Colab
        cfg.MODEL.RETINANET.SCORE_THRESH_TEST = 0.5

        if not torch.cuda.is_available():
            cfg.MODEL.DEVICE = 'cpu'

        self.predictor = DefaultPredictor(cfg)

    def predict(self, data):
        if type(data) != np.ndarray:
            im = cv2.imread(data)
        else:
            im = data

        outputs = self.predictor(im)
        v = Visualizer(im[:, :, ::-1], scale=1)
        v = v.draw_instance_predictions(outputs["instances"].to("cpu"))

        return outputs, v.get_image()[:, :, ::-1]
