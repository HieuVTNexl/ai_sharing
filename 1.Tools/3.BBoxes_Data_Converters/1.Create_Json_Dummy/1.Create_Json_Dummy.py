#!/usr/bin/env python

from __future__ import print_function

import os.path as osp

import numpy as np
import PIL.Image
from scipy import misc
import glob
import cv2
import json
import argparse

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('in_dir1', help='input dir with Image files')
    args = parser.parse_args()
    print ("Input of Image: ", args.in_dir1)
    for label_file_1 in glob.glob(osp.join(args.in_dir1, '*.png')):
        file_name_base = osp.splitext(osp.basename(label_file_1))[0]
        label_file_Output = osp.join(args.in_dir1, file_name_base + '.json')
        data_1 = {"version": "3.16.1", "flags": {}, "shapes": [], "lineColor": [0,    255,    0,    128  ],"fillColor": [    255,    0,    0,    128  ],"imagePath": None,"imageData": None}
        data_1['imagePath'] = file_name_base + ".png"
        with open(label_file_Output, "w") as jsonFile:
            json.dump(data_1, jsonFile, cls=NumpyEncoder, indent=4)
if __name__ == '__main__':
    main()