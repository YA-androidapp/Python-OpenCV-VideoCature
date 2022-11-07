#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 YA-androidapp(https://github.com/YA-androidapp) All rights reserved.

# Required: python -m pip install opencv-python


import cv2


# capture = cv2.VideoCapture(0)
capture = cv2.VideoCapture(1)

# capture = cv2.VideoCapture('src/110879.mp4')

capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)

if capture.isOpened():
    while(True):
        ret, frame = capture.read()
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()
else:
    sys.exit()
