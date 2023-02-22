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

from scipy.interpolate import interp1d

here = osp.dirname(osp.abspath(__file__))
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('in_dir', help='input dir with annotated files')
    args = parser.parse_args()
    for label_file in glob.glob(osp.join(args.in_dir, '*.json')): 
        print('Arranging dataset from:', label_file)         
        with open(label_file, "r") as data_file:    
            data = json.load(data_file)
        shapes = data['shapes']
        new_shapes = []
        for shape in shapes:
            point = shape['points']
            x1 = point[0][0]
            y1 = point[0][1]
            x2 = point[1][0]
            y2 = point[1][1]
            xmin = x1
            if(xmin>x2):
                xmin = x2
            xmax = x2
            if(xmax<x1):
                xmax = x1
            
            ymin = y1
            if(ymin>y2):
                ymin = y2
            ymax = y2
            if(ymax<y1):
                ymax = y1
            #limit into border
            if (xmin<0):
                xmin = 0
                print("annotation point changed")
            if (xmax>data['imageWidth']):
                xmax = data['imageWidth']
                print("annotation point changed")
            if (ymin<0):
                ymin = 0
                print("annotation point changed")
            if (ymax>data['imageHeight']):
                ymax = data['imageHeight']
                print("annotation point changed")
           
            point[0][0] = xmin
            point[0][1] = ymin
            point[1][0] = xmax
            point[1][1] = ymax
            
            shape['points'] = point
            #if(shape['label'] == "face_other") or (shape['label'] == "face_driver"):
            #    shape['label'] = "face"
            new_shapes.append(shape)
        data['shapes'] = new_shapes

        with open(label_file, "w") as jsonFile:
            json.dump(data, jsonFile, cls=NumpyEncoder, indent=4)
if __name__ == '__main__':
    main()