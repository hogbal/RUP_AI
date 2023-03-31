from ctypes import *
import numpy as np
import random
import cv2
import json
import time
import darknet
import serial
import os
import requests
import Adafruit_PCA9685
import time
from threading import Thread, enumerate
from queue import Queue
from object_detection import load_camera
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

config_file = 'model/aihub/aihub_yolov7-tiny.cfg'
data_file = 'model/aihub/obj.data'
weights = 'model/aihub/aihub_yolov7-tiny_last.weights'

thresh = 0.3
ext_output = False

network, class_names, class_colors = darknet.load_network(
            config_file,
            data_file,
            weights,
            batch_size=1
        )

darknet_width = darknet.network_width(network)
darknet_height = darknet.network_height(network)

#servo setting
pwm = Adafruit_PCA9685.PCA9685(address = 0x40, busnum = 1)

servo_min    = 150 # min. pulse length
servo_max    = 600 # max. pulse length
servo_offset = 50

servo_open = 350
servo_close = 100
open_time = 5

servo_pet = 0
servo_pp = 1
servo_ps = 2

pwm.set_pwm_freq(60)

pwm.set_pwm(servo_pet, 0, servo_close)
pwm.set_pwm(servo_pp, 0, servo_close)
pwm.set_pwm(servo_ps, 0, servo_close)


#csi camera setting
cap = load_camera.csi_camera()

os.system("clear")
print("setting success")

def convert2relative(bbox):
    """
    YOLO format use relative coordinates for annotation
    """
    x, y, w, h  = bbox
    _height     = darknet_height
    _width      = darknet_width
    return x/_width, y/_height, w/_width, h/_height


def convert2original(image, bbox):
    x, y, w, h = convert2relative(bbox)

    image_h, image_w, __ = image.shape

    orig_x       = int(x * image_w)
    orig_y       = int(y * image_h)
    orig_width   = int(w * image_w)
    orig_height  = int(h * image_h)

    bbox_converted = (orig_x, orig_y, orig_width, orig_height)

    return bbox_converted


def convert4cropping(image, bbox):
    x, y, w, h = convert2relative(bbox)

    image_h, image_w, __ = image.shape

    orig_left    = int((x - w / 2.) * image_w)
    orig_right   = int((x + w / 2.) * image_w)
    orig_top     = int((y - h / 2.) * image_h)
    orig_bottom  = int((y + h / 2.) * image_h)

    if (orig_left < 0): orig_left = 0
    if (orig_right > image_w - 1): orig_right = image_w - 1
    if (orig_top < 0): orig_top = 0
    if (orig_bottom > image_h - 1): orig_bottom = image_h - 1

    bbox_cropping = (orig_left, orig_top, orig_right, orig_bottom)

    return bbox_cropping

def servo_controller(pin):
	pwm.set_pwm(pin, 0, servo_open)
	time.sleep(open_time)
	pwm.set_pwm(pin, 0, servo_close)


def video_capture(frame_queue, darknet_image_queue):
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (darknet_width, darknet_height),
                                   interpolation=cv2.INTER_LINEAR)
        
        frame_queue.put(frame)
        img_for_detect = darknet.make_image(darknet_width, darknet_height, 3)
        darknet.copy_image_from_bytes(img_for_detect, frame_resized.tobytes())
        darknet_image_queue.put(img_for_detect)
    cap.release()


def inference(darknet_image_queue, detections_queue, fps_queue, label_queue):
    while cap.isOpened():
        darknet_image = darknet_image_queue.get()
        prev_time = time.time()
        detections = darknet.detect_image(network, class_names, darknet_image, thresh=thresh)
        labels = [detection[0] for detection in detections]
        if(label_queue.full()):
            label_queue.get()
        label_queue.put(labels)
        detections_queue.put(detections)
        fps = int(1/(time.time() - prev_time))
        fps_queue.put(fps)
        darknet.free_image(darknet_image)
    cap.release()


def drawing(frame_queue, detections_queue, label_queue, fps_queue):
    random.seed(3)  # deterministic bbox colors
    cv2.namedWindow('Inference', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('Inference',cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while cap.isOpened():
        frame = frame_queue.get()
        detections = detections_queue.get()
        fps = fps_queue.get()
        if(fps == 0):
            fps = 1
        detections_adjusted = []
        if frame is not None:
            for label, confidence, bbox in detections:
                bbox_adjusted = convert2original(frame, bbox)
                detections_adjusted.append((str(label), confidence, bbox_adjusted))
            image = darknet.draw_boxes(detections_adjusted, frame, class_colors)
            cv2.imshow('Inference', image)
            
            input = cv2.waitKey(fps)
            if input == 27:
                break
    cap.release()
    cv2.destroyAllWindows()

def label_check(label_queue):
    end = time.time() + 20
    
    while time.time() < end:
        labels = label_queue.get()
        
        if(len(labels)== 1):
            return labels[0]
    return None

def flow(label_queue):
    while(True):
        label = label_check(label_queue)

        if(label == "plastic"):
            servo_controller(servo_pet)
        elif(label == "can"):
            servo_controller(servo_pp)
        elif(label == "glass"):
            servo_controller(servo_ps)


    cap.release()

if __name__ == '__main__':
    frame_queue = Queue()
    darknet_image_queue = Queue(maxsize=1)
    detections_queue = Queue(maxsize=1)
    fps_queue = Queue(maxsize=1)
    label_queue = Queue(maxsize=1)

    video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    Thread(target=video_capture, args=(frame_queue, darknet_image_queue)).start()
    Thread(target=inference, args=(darknet_image_queue, detections_queue, fps_queue, label_queue)).start()
    Thread(target=drawing, args=(frame_queue, detections_queue, label_queue, fps_queue)).start()
    flow(label_queue)
