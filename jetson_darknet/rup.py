from ctypes import *
import cv2
import os
import time
import darknet
import serial
from object_detection import load_camera

#Darknet Yolo setting
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

def video_capture():
    end = time.time() + 20
    
    while cap.isOpened() and time.time() < end:
        ret, frame = cap.read()
        if not ret:
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (darknet_width, darknet_height),
                                   interpolation=cv2.INTER_LINEAR)
        img_for_detect = darknet.make_image(darknet_width, darknet_height, 3)
        darknet.copy_image_from_bytes(img_for_detect, frame_resized.tobytes())
        result, label = inference(img_for_detect)
        if(result):
            return label

    return False
        
def inference(darknet_image):
    prev_time = time.time()
    detections = darknet.detect_image(network, class_names, darknet_image, thresh=thresh)
    print('detections : ',end='')
    print(detections)
    darknet.free_image(darknet_image)
    labels = [detection[0] for detection in detections]
    print('labels : ',end='')
    print(labels)
    if(len(labels) == 1):
        return True, labels[0]
    else:
        return False, None

if __name__ == '__main__':
    while(True):
        if(ser_main.readable()):
            main_res = ser_main.readline()
            read_data = main_res.decode()[:len(main_res)-1]
            if(read_data == 'Detection\r'):
                print("Detection start")
                label = video_capture()
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
