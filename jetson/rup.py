import os
import cv2
import time
import serial
import firebase_admin
import Jetson.GPIO as GPIO
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import auth

from QRscanner import qrscanner
from object_detection import load_model, load_camera, loop_detect
from firebase_rup import firebase_rup
#from arduino import serial_connect

'''
ser_main = serial.Serial(
		port = '/dev/ttyACM0',
		baudrate=9600)

ser_sub = serial.Serial(
		port = '/dev/ttyUSB0',
		baudrate=9600)
'''
ser_main = serial.Serial(
		port = '/dev/ttyUSB0',
		baudrate = 9600)

model = load_model.YOLOv4Tiny(weight_file='model/yolov4-tiny_fp32.rt')
cap_object_detection = load_camera.csi_camera()

cred = credentials.Certificate("firebase_sdk/reduce-the-use-of-plastic-firebase-adminsdk-7r0al-d13b6f66fe.json")
default_app = firebase_admin.initialize_app(cred,{
	'databaseURL' : 'https://reduce-the-use-of-plastic-default-rtdb.firebaseio.com/'
})

print('Setting success!')
time.sleep(0.5)
os.system('clear')

while(True):
	if(ser_main.readable()):
		res = ser_main.readline()
		read_data = res.decode()[:len(res)-1]
		if(read_data == 'Detection\r'):
			print("Detection start")
			detect = loop_detect.yolov4_tiny_log(model, cap_object_detection)
			print("met : "+detect)

			if(detect == "pet"):
				detect = '1'
			elif(detect == "pp"):
				detect = '2'
			elif(detect == "ps"):
				detect = '3'
			else:
				detect = 0

			if(detect):
				ser_main.write(detect.encode("utf-8"))
