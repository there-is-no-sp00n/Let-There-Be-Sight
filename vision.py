'''

Copyright 2021, Aninda Zaman, All rights reserved.

'''


import cv2
from darkflow.net.build import TFNet
import numpy as np
import time
import pyrealsense2 as rs
from real_sense import realsense
from yolov2 import yolo

def manager():
    options = {
        'model': 'cfg/yolo.cfg',
        'load': 'bin/yolo.weights',
        'threshold': 0.5,
        'gpu': 0.5
    }

    tfnet = TFNet(options)    

    pipe_mngr = rs.pipeline()
    config = rs.config()
    profile = pipe_mngr.start(config)   

    frames_mngr = pipe_mngr.wait_for_frames()
    color_mngr = frames_mngr.get_color_frame()
    depth_mngr = frames_mngr.get_depth_frame()

    capture_mngr = cv2.VideoCapture(0)
    capture_mngr.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
    capture_mngr.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)
    
    for p in range(0, 5):
        time.sleep(1)
        print(p+1)

    i = 0
    iteration = 0

    align_to = rs.stream.color
    align = rs.align(align_to)

    while True:
        print("\nMODE IS: ", i)
        iteration += 1

        if i == 1:
            #time.sleep(0.25)
            if not depth_mngr: continue

            frames_mngr = pipe_mngr.wait_for_frames()
            depth_mngr = frames_mngr.get_depth_frame()
            align_to = rs.stream.color
            align = rs.align(align_to)

            color_f = frames_mngr.get_color_frame()
            colorr = np.asanyarray(color_f.get_data())


            i = realsense(depth_mngr, profile, frames_mngr, align)
            print("Iterations ", iteration);
        
        elif i == 0:
            #refresh depth output
        ########
            color_image = np.asanyarray(color_mngr.get_data())
            depth_image = np.asanyarray(depth_mngr.get_data())

            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.05), cv2.COLORMAP_JET)

            images = depth_colormap


            cv2.namedWindow('Manager', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('Depth_RealSense', images)
            cv2.waitKey(1)
        ########

            i = yolo(capture_mngr, tfnet)
            print("Iterations ", iteration);
        
        elif i == 2:
            print("PRESSED 'Q'");
            print("Iterations ", iteration);
            break       
        
    





manager()


'''

Copyright 2021, Aninda Zaman, All rights reserved.

'''
