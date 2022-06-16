from __future__ import absolute_import, division, print_function

import os
import numpy as np
# import PIL.Image as pil
import matplotlib.pyplot as plt
import cv2

import torch
from torchvision import transforms

from . import networks
from .utils import download_model_if_doesnt_exist

class DepModel :
    def __init__(self) -> None:
        self.i = 0
        pass

    def load_model(self, model_name  = "mono_640x192") -> None:
        download_model_if_doesnt_exist(model_name)
        self.encoder_path = os.path.join("models", model_name, "encoder.pth")
        self.depth_decoder_path = os.path.join("models", model_name, "depth.pth")

        # LOADING PRETRAINED MODEL
        self.encoder = networks.ResnetEncoder(18, False)
        self.depth_decoder = networks.DepthDecoder(num_ch_enc=self.encoder.num_ch_enc, scales=range(4))

        self.loaded_dict_enc = torch.load(self.encoder_path, map_location='cpu')
        self.filtered_dict_enc = {k: v for k, v in self.loaded_dict_enc.items() if k in self.encoder.state_dict()}
        self.encoder.load_state_dict(self.filtered_dict_enc)

        self.loaded_dict = torch.load(self.depth_decoder_path, map_location='cpu')
        self.depth_decoder.load_state_dict(self.loaded_dict)

        self.encoder.eval()
        self.depth_decoder.eval()


    # def pil_load_image(self, image_path = "assets/human_road_image.jpg") -> np.ndarray:
    #     self.input_image = pil.open(image_path).convert('RGB')
    #     self.original_width, self.original_height = self.input_image.size

    #     feed_height = self.loaded_dict_enc['height']
    #     feed_width = self.loaded_dict_enc['width']
    #     input_image_resized = self.input_image.resize((feed_width, feed_height), pil.LANCZOS)
    #     return input_image_resized

    def load_image(self, image_path = "assets/test_image.jpg") -> np.ndarray:
        self.input_image = cv2.imread(image_path)
        return self.preprocess_image(self.input_image)

    def preprocess_image(self, image : np.ndarray) -> np.ndarray:
        self.input_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.original_height = self.input_image.shape[0]
        self.original_width = self.input_image.shape[1]

        feed_height = self.loaded_dict_enc['height']
        feed_width = self.loaded_dict_enc['width']
        input_image_resized = cv2.resize(self.input_image, dsize=(feed_width, feed_height), interpolation=cv2.INTER_LANCZOS4)
        return input_image_resized


    def predict(self, input_image_resized:np.ndarray) -> np.ndarray:
        input_image_pytorch = transforms.ToTensor()(input_image_resized).unsqueeze(0)

        with torch.no_grad():
            features = self.encoder(input_image_pytorch)
            outputs = self.depth_decoder(features)

        disp = outputs[("disp", 0)]

        disp_resized = torch.nn.functional.interpolate(disp,
            (self.original_height, self.original_width), mode="bilinear", align_corners=False)

        # Saving colormapped depth image
        self.disp_resized_np = disp_resized.squeeze().cpu().numpy()
        # print("disp", self.disp_resized_np)
        # print(type(self.disp_resized_np))
        return self.disp_resized_np


    def show(self, vmax_percentage = 95) -> None: # vmax_percentage의 백분위만큼 거리 예측 결과를 시각적 출력
        vmax = np.percentile(self.disp_resized_np, vmax_percentage) # 백분위 percentage% 수

        plt.figure(figsize=(10, 10))
        plt.subplot(121)
        plt.imshow(self.input_image)
        plt.title("Input", fontsize=22)
        plt.axis('off')

        plt.subplot(122)
        plt.imshow(self.disp_resized_np, cmap='magma', vmax=vmax)
        plt.title("Depth prediction", fontsize=22)
        plt.axis('off')
        plt.show()

    def res_show(self, vmax_percentage = 95):
        vmax = np.percentile(self.disp_resized_np, vmax_percentage) # 백분위 percentage% 수

        plt.imshow(self.disp_resized_np, cmap='magma', vmax=vmax)
        # plt.title("Depth prediction", fontsize=22)
        plt.axis('off')

        plt.show()

    def save(self, vmax_percentage = 95)-> None:
        vmax = np.percentile(self.disp_resized_np, vmax_percentage) # 백분위 percentage% 수
        plt.imsave("res/%d.png"%self.i,self.disp_resized_np, cmap='magma', vmax=vmax)
        self.i += 1