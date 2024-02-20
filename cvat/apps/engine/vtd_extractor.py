# Copyright (C) 2024 CVAT.ai Corporation
#
# SPDX-License-Identifier: MIT

import os
import png
import cv2
import numpy as np

def extract_vtd(source_file, extract_path):
    # https://stackoverflow.com/a/55715162
    with open(source_file, 'rb') as file:
        # print('vtd:', source_file)
        # print('vtd:', extract_path)

        waste = int.from_bytes(file.read(84), byteorder='little', signed=True)

        width = int.from_bytes(file.read(4), byteorder='little', signed=True)
        height = int.from_bytes(file.read(4), byteorder='little', signed=True)
        # print("size:", width, "x", height)

        frame =  int.from_bytes(file.read(4), byteorder='little', signed=True)
        # print("frames:", frame)

        for i in range(frame):
            points_x = file.read(width * height * 4)
            points_y = file.read(width * height * 4)
            points_z = file.read(width * height * 4)
            intensity = file.read(width * height * 2)

            depth_array = (np.frombuffer(points_z, dtype=np.float32) * 1000 * 255.0 / 4095).astype(np.uint8)
            depth_array = depth_array.reshape(height, width)

            depth_array[depth_array != 0] = 1
            depth_array[depth_array == 0] = 255
            depth_array[depth_array == 1] = 0

            ir_array = np.frombuffer(intensity, dtype=np.uint16).astype(np.uint8)
            ir_image = cv2.cvtColor(ir_array.reshape((height, width)), cv2.COLOR_GRAY2BGR)

            b, g, r = cv2.split(ir_image)
            b[depth_array == 255] = [255]
            ir_image = cv2.merge((b, g, r))

            cv2.imwrite(extract_path + '/{:04d}'.format(i) + '.png', ir_image)

