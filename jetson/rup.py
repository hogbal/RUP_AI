import os
import cv2
import time
import argparse
import firebase_admin
import Jetson.GPIO as GPIO
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import auth

from QRscanner import qrscanner
from object_detection import load_model, load_camera, loop_detect
from firebase_rup import firebase_rup


def str2bool(v):
	if isinstance(v, bool):
		return v
	if v.lower() in ('yes', 'true', 't', 'y', '1'):
		return True
	elif v.lower() in ('no', 'false', 'f', 'n', '0'):
		return False
	else:
		raise argparse.ArgumentTypeError('Boolean value expected.')

parser = argparse.ArgumentParser(description='RUP jetson nano')
parser.add_argument('--debug', type=str2bool ,default=True)
args = parser.parse_args()

model = load_model.YOLOv4Tiny(weight_file='model/yolov4-tiny_fp32.rt')
cap_object_detection = load_camera.csi_camera()

cred = credentials.Certificate("firebase_sdk/reduce-the-use-of-plastic-firebase-adminsdk-7r0al-d13b6f66fe.json")
default_app = firebase_admin.initialize_app(cred,{
	'databaseURL' : 'https://reduce-the-use-of-plastic-default-rtdb.firebaseio.com/'
})

print('Setting success!')
time.sleep(0.5)
os.system('clear')

def menu():
	print('F : Full Flow')
	print('S : Starting Object Detection')
	print('F : Firebase Update')
	print('Q : QRcode')
	print('E : Exit')

while(True):
	menu()
	cup_check = input('select : ')

	if(cup_check == 'F'):
		print('[DEBUG] Find Cup')
		print('[DEBUG] Starting Object Detection...')
		if(args.debug):
			detect = loop_detect.yolov4_tiny_cv2(model, cap_object_detection)
		else:
			detect = loop_detect.yolov4_tiny_log(model, cap_object_detection)

		if(detect):
			print('[DEBUG] Find recycling code')
			user_email = qrscanner.scan_img('QRscanner/qrcode.png')
			if(user_email):
				print('[DEBUG] User Email QRcode scan success')
				print('[DEBUG] Update Firebase')
				firebase_rup.firebase_update(user_email)

	elif(cup_check == 'S'):
		if(args.debug):
			firebase_update = loop_detect.yolov4_tiny_cv2(model, cap_object_detection)
		else:
			firebase_update = loop_detect.yolov4_tiny_log(model, cap_object_detection)
	elif(cup_check == 'F'):
		firebase_rup.firebase_update()
	elif(cup_check == 'Q'):
		qrscanner.scan_img('QRscanner/qrcode.png')
	elif(cup_check == 'E'):
		break
	else:
		print('Error!')
	time.sleep(0.5)
	os.system("clear")	

cap_object_detection.release()
