#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 YA-androidapp(https://github.com/YA-androidapp) All rights reserved.

# Required: python -m pip install opencv-python


import cv2
import glob
import os
import time


def get_devices():
    index = 0
    devices_available = []
    devices_unavailable = []
    devices_working = []
    while len(devices_unavailable) < 6:
        camera = cv2.VideoCapture(index)
        if not camera.isOpened():
            devices_unavailable.append(index)
        else:
            is_reading, img = camera.read()
            w = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
            h = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
            # fps = camera.get(cv2.CAP_PROP_FPS)
            if is_reading:
                devices_working.append({"index": index, "width": w, "height": h})
                cv2.imwrite('{}.png'.format(index), img)
            else:
                devices_available.append(index)
        index += 1
    return devices_available, devices_working, devices_unavailable


def capture(src, width, height):
    # capture = cv2.VideoCapture(0)
    capture = cv2.VideoCapture(src)

    # capture = cv2.VideoCapture('src/110879.mp4')

    capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT,height)

    if capture.isOpened():
        print('Press Q to quit.')
        while(True):
            ret, frame = capture.read()

            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # グレースケール
            # frame = cv2.GaussianBlur(frame, (0, 0), 5) # ぼかし
            # frame = cv2.bitwise_not(frame) # 色の反転
            # frame = frame[0 : 500, 0: 500] # トリミング [top : bottom, left : right]

            cv2.imshow('Frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        capture.release()
        cv2.destroyAllWindows()
    else:
        sys.exit()


def capture_trimmed(src, width, height, time_out=120):
    capture = cv2.VideoCapture(src)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT,height)

    if capture.isOpened():
        print('Press Q to quit.')

        _, img = capture.read()

        start = time.time()

        x1 = -1
        x2 = -1
        y1 = -1
        y2 = -1

        def printCoor(event,x,y,flags,param):
            nonlocal x1
            nonlocal y1
            nonlocal x2
            nonlocal y2

            if event == cv2.EVENT_LBUTTONDOWN:
                x1 = x
                y1 = y
                img_tmp = img_mes.copy()
                cv2.putText(img_tmp, text=f'(x,y):({x1},{y1})',org=(x1, y1-10), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=0.5, color=(255,255,255),thickness=1,lineType=cv2.LINE_4)
                cv2.imshow('image',img_tmp)

            elif event == cv2.EVENT_RBUTTONDOWN:
                x2 = x
                y2 = y

                img_tmp = img_mes.copy()
                cv2.rectangle(img_tmp,(x1,y1),(x2,y2),(255,255,255), thickness=1)
                cv2.putText(img_tmp, text=f'(x,y):({x1},{y1})',org=(x1, y1-10), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=0.5, color=(255,255,255),thickness=1,lineType=cv2.LINE_4)
                cv2.putText(img_tmp, text=f'(x,y):({x2},{y2})',org=(x2, y2-10), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=0.5, color=(255,255,255),thickness=1,lineType=cv2.LINE_4)
                cv2.imshow('image',img_tmp)

        cv2.namedWindow('image', cv2.WINDOW_AUTOSIZE)
        cv2.setMouseCallback('image',printCoor)
        cv2.moveWindow('image', 0, 0)

        img_mes = img.copy()
        cv2.imshow('image',img_mes)

        isSelected = False
        while True:
            elasped_time = time.time() - start

            print(elasped_time, start, time_out)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            if elasped_time > time_out:
                print('time out')
                break

            if x2 > -1 and y2 > -1:
                if isSelected == False:
                    start = time.time() - time_out + 3
                    isSelected = True

        cv2.destroyWindow('image')

        print(x1, y1, x2, y2)

        while(True):
            ret, frame = capture.read()
            frame = frame[y1 : y2, x1: x2]
            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        capture.release()
        cv2.destroyAllWindows()
    else:
        sys.exit()


def remove_glob(filepath):
    # for p in glob.glob(filepath, recursive=recursive):
    for p in glob.glob(filepath):
        if os.path.isfile(p):
            os.remove(p)


if __name__ == "__main__":
    _, devices_working, _ = get_devices()
    for device in devices_working:
        print(device)

    param_str = input('Enter a device index or "trim": ')
    remove_glob('./*.png')

    if param_str.isnumeric():
        device_index = int(param_str)
        capture(
            device_index,
            1920,
            1080
        )
    elif param_str == 'trim':
        param_str = input('Enter a device index: ')
        device_index = int(param_str)
        capture_trimmed(
            device_index,
            1920,
            1080
        )
