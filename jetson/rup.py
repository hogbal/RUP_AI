import os
import sys
import cv2
import time
import serial
import Jetson.GPIO as GPIO

from object_detection import load_model, load_camera, loop_detect
#from arduino import serial_connect

ser_main = serial.Serial(
		port = '/dev/ttyACM0',
		baudrate=9600)


model = load_model.YOLOv4Tiny(weight_file='model/yolov4-tiny_fp32.rt')
cap_object_detection = load_camera.csi_camera()

print('Setting success!')
time.sleep(0.5)
os.system('clear')

while(True):
	if(ser_main.readable()):
		main_res = ser_main.readline()
		read_data = main_res.decode()[:len(main_res)-1]
		if(read_data == 'Detection\r'):
			print("Detection start")
			detect = loop_detect.yolov4_tiny_log(model, cap_object_detection, 10)
			print("met : "+detect)

			if(detect == "pet"):
				detect = '1'
			elif(detect == "pp"):
				detect = '2'
			elif(detect == "ps"):
				detect = '3'
			else:
				detect = '0'

			ser_main.write(detect.encode("utf-8"))

			if(detect != '0'):
				print("QR scanner start")
				while(True):
					qr_data = input()
					print("qrcode : "+qr_data)
					break
				print("QR scanner end")

			time.sleep(1)
			end_signal = 'e'
			ser_main.write(end_signal.encode("utf-8"))
			print("end process")



