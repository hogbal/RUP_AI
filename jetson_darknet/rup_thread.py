from ctypes import *
import random
import cv2
import time
import darknet
import serial
import os
from threading import Thread, enumerate
from queue import Queue
from object_detection import load_camera

config_file = 'model/yolov7-tiny/yolov7-tiny.cfg'
data_file = 'model/yolov7-tiny/obj.data'
weights = 'model/yolov7-tiny/yolov7-tiny_best.weights'

'''
config_file = 'model/yolov4-tiny/yolov4-tiny.cfg'
data_file = 'model/yolov4-tiny/obj.data'
weights = 'model/yolov4-tiny/yolov4-tiny_best.weights'
'''

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


def drawing(frame_queue, detections_queue, fps_queue):
    random.seed(3)  # deterministic bbox colors
    while cap.isOpened():
        frame = frame_queue.get()
        detections = detections_queue.get()
        fps = fps_queue.get()
        detections_adjusted = []
        if frame is not None:
            for label, confidence, bbox in detections:
                bbox_adjusted = convert2original(frame, bbox)
                detections_adjusted.append((str(label), confidence, bbox_adjusted))
            image = darknet.draw_boxes(detections_adjusted, frame, class_colors)
            cv2.imshow('Inference', image)
            if cv2.waitKey(fps) == 27:
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
                    label = '0'
                    
                ser_main.write(label.encode("utf-8"))
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
    Thread(target=drawing, args=(frame_queue, detections_queue, fps_queue)).start()
    arduino(label_queue)
