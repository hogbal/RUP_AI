import os
import cv2
import time
import serial
import firebase_admin
import Jetson.GPIO as GPIO
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import auth

from object_detection import load_model, load_camera, loop_detect
from firebase_rup import firebase_rup
#from arduino import serial_connect

ser_main = serial.Serial(
		port = '/dev/ttyACM0',
		baudrate=9600)


model = load_model.YOLOv4Tiny(weight_file='model/yolov4-tiny_fp32.rt')
cap_object_detection = load_camera.csi_camera()

cred = credentials.Certificate("firebase_sdk/rup-ver2-81b50-firebase-adminsdk-tuwg4-592225897b.json")
default_app = firebase_admin.initialize_app(cred,{
	'databaseURL' : 'https://rup-ver2-81b50-default-rtdb.firebaseio.com/'
})

print('Setting success!')
time.sleep(0.5)
os.system('clear')

while(True):
	if(ser_main.readable()):
		main_res = ser_main.readline()
		read_data = main_res.decode()[:len(main_res)-1]
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
				
				print("QR scanner start")
				while(True):
					qr_data = input()
					print("qrcode : "+qr_data)

					firebase_rup.firebase_update(qr_data)
					break
				print("QR scanner end")



