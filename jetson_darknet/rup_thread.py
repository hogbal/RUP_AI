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
from threading import Thread, enumerate
from queue import Queue
from object_detection import load_camera
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

config_file = 'model/yolov7-tiny/yolov7-tiny.cfg'
data_file = 'model/yolov7-tiny/obj.data'
weights = 'model/yolov7-tiny/yolov7-tiny_2000.weights'

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

#Arduino setting
ser_main = serial.Serial(
		port = '/dev/ttyACM0',
		baudrate=9600)

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


def video_capture(frame_queue, darknet_image_queue):
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (darknet_width, darknet_height),
                                   interpolation=cv2.INTER_LINEAR)
        
		#val = 50
        #BGR
		#array = np.full(frame_resized.shape, (0, 0, val), dtype=np.uint8)
		#frame_resized = cv2.add(frame_resized, array)

		#frame_queue.put(frame_resized)
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
            elif input == 113:
                label_queue.get()
                label_queue.put(['pet'])
            elif input == 119:
                label_queue.get()
                label_queue.put(['pp'])
            elif input == 101:
                label_queue.get()
                label_queue.put(['ps'])
    cap.release()
    cv2.destroyAllWindows()

def label_check(label_queue):
    end = time.time() + 20
    
    while time.time() < end:
        labels = label_queue.get()
        
        if(len(labels)== 1):
            return labels[0]
    return None

def arduino(label_queue):
    while(True):
        if(ser_main.readable()):
            main_res = ser_main.readline()
            read_data = main_res.decode()[:len(main_res)-1]
            if(read_data == 'Detection\r'):
                print("Detection start")
                label = label_check(label_queue)
                print("Detection end")
                
                if(label == "pet"):
                    label = '1'
                elif(label == "pp"):
                    label = '2'
                elif(label == "ps"):
                    label = '3'
                else:
                    ser_main.write(label.encode("utf-8"))
                    label = '0'
                    continue
                    
                ser_main.write(label.encode("utf-8"))
                
                while(True):
                    if(ser_main.readable()):
                        main_res = ser_main.readline()
                        read_data = main_res.decode()[:len(main_res)-1]
                        if(read_data == 'End\r'):
                            print('Point update start')
                            # uid = input()
                            uid = "d334cc4w"
                            url="http://13.124.80.15/home/get-point-record"
                            res = requests.post(url, json={'uid': uid, 'point': 1})
                            result = json.loads(res.text)
                            if(result):
                                print('Point update success')
                            else:
                                print('Point update error')
                            break
                
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
    arduino(label_queue)
