from ctypes import *
import numpy as np
import re
import cv2
import json
import time
import darknet
import serial
import os
import requests
import Adafruit_PCA9685
import time
import pickle
from threading import Thread, enumerate
from queue import Queue
from object_detection import load_camera
from img.img import create_img, create_phone_img, create_info_img, create_result_img
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# AI setting
config_file = 'model/aihub/aihub_yolov7-tiny.cfg'
data_file = 'model/aihub/obj.data'
weights = 'model/aihub/aihub_yolov7-tiny_last.weights'

thresh = 0.65
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

# servo_open = 350
servo_open = 250
servo_close = 100
open_time = 5

servo_plastic = 1
servo_can = 0
servo_paper = 2
servo_glass = 2
servo_pet = 1

pwm.set_pwm_freq(60)

pwm.set_pwm(servo_plastic, 0, servo_close)
pwm.set_pwm(servo_can, 0, servo_close)
pwm.set_pwm(servo_paper, 0, servo_close)
pwm.set_pwm(servo_glass, 0, servo_close)
pwm.set_pwm(servo_pet, 0, servo_close)


#csi camera setting
cap = load_camera.csi_camera()

# pkl load and Img setting
pkl_name = "./data/dict.pkl"
number_data = dict()
if(os.path.isfile(pkl_name)):
    with open(pkl_name, "rb" ) as f:
        number_data = pickle.load(f)

base_font_size = 60
main_img = create_img("쓰레기를 카메라에 인식시켜주세요.", base_font_size, 0.7)
detection_img = create_img("쓰레기 식별 중입니다.", base_font_size, 0.7)
can_img = create_img("캔", base_font_size, 0.7)
plastic_img = create_img("플라스틱", base_font_size ,0.7)
pet_img = create_img("페트", base_font_size ,0.7)
paper_img = create_img("종이", base_font_size ,0.7)
glass_img = create_img("유리", base_font_size, 0.7)
input_img = create_img("번호를 입력해 주세요.", int(base_font_size*0.6), 0.65)

output_img = main_img
detection_check = False
input_phone_check = False

os.system("clear")
print("setting success")

def servo_controller(pin):
    pwm.set_pwm(pin, 0, servo_open)
    time.sleep(open_time)
    pwm.set_pwm(pin, 0, servo_close)
    # for i in range(servo_close, servo_open, -1):
    #     pwm.set_pwm(pin, 0, i)
    # time.sleep(open_time)
    # for i in range(servo_open, servo_close):
    #     pwm.set_pwm(pin, 0, i)

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

def input_phone():
    global output_img
    img = create_phone_img(input_img, "010-0000-0000", base_font_size, color=(204,204,204))
    phone_num = ""
            
    while(True):
        cv2.imshow("Inference", img)
        num = cv2.waitKey(0)
                
        if(num == ord('0')):
            phone_num += '0'
        elif(num == ord('1')):
            phone_num += '1'
        elif(num == ord('2')):
            phone_num += '2'
        elif(num == ord('3')):
            phone_num += '3'
        elif(num == ord('4')):
            phone_num += '4'
        elif(num == ord('5')):
            phone_num += '5'
        elif(num == ord('6')):
            phone_num += '6'
        elif(num == ord('7')):
            phone_num += '7'
        elif(num == ord('8')):
            phone_num += '8'
        elif(num == ord('9')):
            phone_num += '9'
        elif(num == 8):
            if(len(phone_num) != 0):
                phone_num = phone_num[:-1]
            if(len(phone_num) == 4 or len(phone_num) == 9):
                phone_num = phone_num[:-1]
        elif(num == 13):
            if(re.match('010-\d{3,4}-\d{4}', phone_num)):
                if(phone_num in number_data):
                    number_data[phone_num] += 1
                else:
                    number_data[phone_num] = 1
                            
                with open(pkl_name, 'wb') as f:
                    pickle.dump(number_data, f, pickle.HIGHEST_PROTOCOL)
                            
                img = create_info_img(f"{phone_num}님", f"적립현황 {number_data[phone_num]}p", base_font_size)
                cv2.imshow("Inference", img)
                cv2.waitKey(2000)
                        
                img = create_result_img(len(number_data), base_font_size)
                cv2.imshow("Inference", img)
                cv2.waitKey(2000)
                        
                img = main_img
                break
            else:
                img = create_phone_img(input_img, phone_num, base_font_size, notice=True)
                continue
                
        if(len(phone_num) == 4 or len(phone_num) == 9):
            phone_num = phone_num[:-1] + '-' + phone_num[-1]
                
        img = create_phone_img(input_img, phone_num, base_font_size)
    output_img = main_img

def label_check(label_queue):
    while(True):
        labels = label_queue.get()
        
        if(len(labels)== 1):
            return labels[0]

def drawing(frame_queue, detections_queue, label_queue, fps_queue):
    global detection_check
    global output_img
    global input_phone_check
    cv2.namedWindow('Inference', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('Inference',cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while cap.isOpened():
        frame = frame_queue.get()
        detections = detections_queue.get()
        fps = fps_queue.get()

        if(fps == 0):
            fps = 1
        
        cv2.imshow("Inference", output_img)
        
        input_key = cv2.waitKey(fps)
        
        if(input_key == 27):
            break
        elif(input_key == 13):
            detection_check = True
        elif(input_key == ord('q')):
            pwm.set_pwm(0, 0, servo_open)
        elif(input_key == ord('a')):
            pwm.set_pwm(0, 0, servo_close)
        elif(input_key == ord('w')):
            pwm.set_pwm(1, 0, servo_open)
        elif(input_key == ord('s')):
            pwm.set_pwm(1, 0, servo_close)
        elif(input_key == ord('e')):
            pwm.set_pwm(2, 0, servo_open)
        elif(input_key == ord('d')):
            pwm.set_pwm(2, 0, servo_close)
        
        if(input_phone_check):
            input_phone()
            input_phone_check = False

    cap.release()
    cv2.destroyAllWindows()

def flow(label_queue):
    global detection_check
    global output_img
    global input_phone_check
    
    while(cap.isOpened()):
        if(detection_check):
            output_img = detection_img
            label = label_check(label_queue)

            if(label == "plastic"):
                output_img = plastic_img
                servo_controller(servo_plastic)
            elif(label == "can"):
                output_img = can_img
                servo_controller(servo_can)
            elif(label == "paper"):
                output_img = paper_img
                servo_controller(servo_paper)
            elif(label == "glass"):
                output_img = glass_img
                servo_controller(servo_glass)
            elif(label == "pet"):
                output_img = pet_img
                servo_controller(servo_pet)
            
            input_phone_check = True
            detection_check = False

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
