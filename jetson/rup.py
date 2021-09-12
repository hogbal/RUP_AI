# -*- encoding: utf-8 -*-
from ctypes import *
import cv2
import time
import argparse
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import auth
from pyzbar import pyzbar
from threading import Thread

class IMAGE(Structure):
	_fields_ = [("w", c_int),
			    ("h", c_int),
			    ("c", c_int),
			    ("data", POINTER(c_float))]

class BOX(Structure):
	_fields_ = [("x", c_float),
			    ("y", c_float),
				("w", c_float),
				("h", c_float)]

class DETECTION(Structure):
	_fields_ = [("cl", c_int),
			    ("bbox", BOX),
				("prob", c_float),
				("name", c_char*20)]

def str2bool(v):
	if isinstance(v, bool):
		return v
	if v.lower() in ('yes', 'true', 't', 'y', '1'):
		return True
	elif v.lower() in ('no', 'false', 'f', 'n', '0'):
		return False
	else:
		raise argparse.ArgumentTypeError('Boolean value expected.')

lib = CDLL("libary/librup_libary.so", RTLD_GLOBAL)

load_network = lib.load_network
load_network.argtypes = [c_char_p, c_int, c_int]
load_network.restype = c_void_p

copy_image_from_bytes = lib.copy_image_from_bytes
copy_image_from_bytes.argtypes = [IMAGE, c_char_p]

make_image = lib.make_image
make_image.argtypes = [c_int, c_int, c_int]
make_image.restype = IMAGE

do_inference = lib.do_inference
do_inference.argtypes = [c_void_p, IMAGE]

get_network_boxes = lib.get_network_boxes
get_network_boxes.argtypes = [c_void_p, c_float, c_int, POINTER(c_int)]
get_network_boxes.restype = POINTER(DETECTION)

parser = argparse.ArgumentParser(description='tkDNN detect')
parser.add_argument('--debug', type=str2bool ,default=True)
args = parser.parse_args()

def gstreamer_pipeline(
		capture_width=640,
		capture_height=640,
		display_width=640,
		display_height=640,
		framerate=60,
		flip_method=0,
		):
	return ("nvarguscamerasrc ! "
			"video/x-raw(memory:NVMM), "
			"width=(int)%d, height=(int)%d, "
			"format=(string)NV12, framerate=(fraction)%d/1 ! "
			"nvvidconv flip-method=%d ! "
			"video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
			"videoconvert ! "
			"video/x-raw, format=(string)BGR ! appsink"
			% (
				capture_width,
				capture_height,
				framerate,
				flip_method,
				display_width,
				display_height
				)
			)

def detect_image(net, darknet_image, thresh=0.5):
	num = c_int(0)

	pnum = pointer(num)
	do_inference(net, darknet_image)
	dets = get_network_boxes(net, thresh, 0, pnum)
	res = []
	for i in range(pnum[0]):
		b = dets[i].bbox
		res.append((dets[i].name.decode("ascii"), dets[i].prob, (b.x,b.y,b.w,b.h)))
	return res

class YOLOv4Tiny(object):
	def __init__(self,
			     input_size=640,
				 weight_file='model/yolov4-tiny_fp32.rt',
				 conf_thresh=0.5):
		self.input_size = input_size
		self.model = load_network(weight_file.encode("ascii"), 3, 1)
		self.darknet_image = make_image(input_size, input_size, 3)
		self.thresh = conf_thresh

	def detect(self, img, need_resize=True):
		try:
			if need_resize:
				frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
				img = cv2.resize(frame_rgb,
						         (self.input_size, self.input_size),
								 interpolation=cv2.INTER_LINEAR)
			frame_data = img.ctypes.data_as(c_char_p)
			copy_image_from_bytes(self.darknet_image,frame_data)
			detections = detect_image(self.model, self.darknet_image, thresh=self.thresh)
			return detections
		except Exception as e_s:
			print(e_s)

def firebase_update(detections):
	labels = [det[0] for det in detections]
	labels = set(labels)
	if len(labels) == 1:
		#uid = QRcode user data
		"""
		cap = cv2.VideoCapture(0)
		if cap.isOpened():
			if args.debug:
				ret_val, img = cap.read()
				video_shower = VideoShow(img).start()
				window_handle = cv2.namedWindow("Web Cam", cv2.WINDOW_AUTOSIZE)
			
			target_tick = time.time()+10
			uid = None 
			while cap.isOpened() and time.time() < target_tick:
				ret_val, img = cap.read()
				if not ret_val:
					break

				if args.debug:
					if video_shower.stopped:
						break
				barcodes = pyzbar.decode(img)

				if args.debug:
					video_shower.frame = img

				for barcode in barcodes:
					uid = barcode.data.decode()

				if uid:
					if args.debug:
						video_shower.stopped
					break
			cap.release()
			cv2.destoryAllWindows()
		else:
			print("Unable to open camera")
			return
		"""
		uid = "5aefF22EfVdWslKaWQ7CSZecUjW2"

		if db.reference('Users2').get().get(uid):
			user = db.reference('Users2/'+uid)
			point = str(int(user.get()['point'])+1)
			user.update({'point':point})
		else:
			print('error')

def loop_detect(model):
	cred = credentials.Certificate("firebase/reduce-the-use-of-plastic-firebase-adminsdk-7r0al-d13b6f66fe.json")
	default_app = firebase_admin.initialize_app(cred,{
		'databaseURL' : 'https://reduce-the-use-of-plastic-default-rtdb.firebaseio.com/'
	})
	cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=2), cv2.CAP_GSTREAMER)

	color_dic = {
			'pet':(255,0,0),
			'pp':(0,255,0),
			'ps':(0,0,255)
	}

	if cap.isOpened():
		if args.debug:
			ret_val, img = cap.read()
			cv2.resize(img,
					   (640,640),
					   interpolation=cv2.INTER_LINEAR)
			video_shower = VideoShow(img).start()
			window_handle = cv2.namedWindow("CSI Camera", cv2.WINDOW_AUTOSIZE)

		while cap.isOpened():
			ret_val, img = cap.read()
			if not ret_val:
				break

			if args.debug:
				if video_shower.stopped:
					break

			img = cv2.resize(img,
					         (640,640),
							 interpolation=cv2.INTER_LINEAR)
			detections = model.detect(img, need_resize=False)

			if args.debug:
				for det in detections:
					print(det)
					prob = str(format(det[1],".2f"))
					x0 = int(det[2][0])
					x1 = int(det[2][0]) + int(det[2][2])
					y0 = int(det[2][1])
					y1 = int(det[2][1]) + int(det[2][3])
					det_class = det[0]
					img = cv2.rectangle(img, (x0, y0), (x1, y1), color_dic[det_class], 2)
					img = cv2.putText(img, det_class+" "+prob, (x0, (y0-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color_dic[det_class], 2)
				video_shower.frame = img
			firebase_update(detections)
		cap.release()
		cv2.destroyAllWindows()
	else:
		print("Unable to open camera")

class VideoShow:
	def __init__(self, frame=None):
		self.frame = frame
		self.stopped = False
	
	def start(self):
		Thread(target=self.show, args=()).start()
		return self

	def show(self):
		while not self.stopped:
			cv2.imshow("CSI Camera", self.frame)
			if cv2.waitKey(1) == ord("q"):
				self.stopped = True

	def stop(self):
		self.stopped = True

if __name__ == '__main__':
	model = YOLOv4Tiny(weight_file='model/yolov4-tiny_fp32.rt')

	loop_detect(model)
