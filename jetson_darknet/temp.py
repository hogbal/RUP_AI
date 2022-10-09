from asyncio.windows_events import NULL
from ctypes import *
import cv2
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

thresh = 0.5
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

def video_capture():
    end = time.time() + 10
    
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
        
def inference(darknet_image):
    prev_time = time.time()
    detections = darknet.detect_image(network, class_names, darknet_image, thresh=thresh)
    darknet.free_image(darknet_image)
    labels = [detection[0] for detection in detections]
    if(len(labels) == 1):
        return True, labels
    else:
        return False, labels

if __name__ == '__main__':
    while(True):
        if(ser_main.readable()):
            main_res = ser_main.readline()
            read_data = main_res.decode()[:len(main_res)-1]
            if(read_data == 'Detection\r'):
                print("Detection start")
                label = video_capture()
                
                if(detect == "pet"):
                    detect = '1'
                elif(detect == "pp"):
                    detect = '2'
                elif(detect == "ps"):
                    detect = '3'
                else:
                    detect = '0'
                    
                ser_main.write(detect.encode("utf-8"))