# -*- encoding: utf-8 -*-
import cv2
import time
from threading import Thread

def update_check(detections):
	labels = [det[0] for det in detections]
	labels = set(labels)
	if len(labels) == 1:
		return list(labels)[0]
	else:
		return 'false'

def yolov4_tiny_cv2(model, cap, second, return_check):
	color_dic = {
			'pet':(255,0,0),
			'pp':(0,255,0),
			'ps':(0,0,255)
	}

	if cap.isOpened():
		ret_val, img = cap.read()
		cv2.resize(img,
				   (640,640),
				   interpolation=cv2.INTER_LINEAR)
		video_shower = VideoShow(img).start()
		window_handle = cv2.namedWindow("CSI Camera", cv2.WINDOW_AUTOSIZE)

		end = time.time() + second

		while cap.isOpened() and time.time() < end:
			ret_val, img = cap.read()
			if not ret_val:
				break

			if video_shower.stopped:
				break

			img = cv2.resize(img,
					         (640,640),
							 interpolation=cv2.INTER_LINEAR)
			detections = model.detect(img, need_resize=False)

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
			
			result = update_check(detections)
			if result and return_check:
				return result 

		cv2.destroyAllWindows()
		return 'false'
	else:
		print("Unable to open camera")
		return 'false'

def yolov4_tiny_log(model, cap, second):
	color_dic = {
			'pet':(255,0,0),
			'pp':(0,255,0),
			'ps':(0,0,255)
	}

	if cap.isOpened():
		end = time.time() + second
		while cap.isOpened() and time.time() < end:
			ret_val, img = cap.read()
			if not ret_val:
				break

			img = cv2.resize(img,
					         (640,640),
							 interpolation=cv2.INTER_LINEAR)
			detections = model.detect(img, need_resize=False)

			for det in detections:
				det_class = det[0]
				prob = str(format(det[1],".2f"))
				print(det_class+" : "+prob)

			result = update_check(detections)
			if result != 'false':
				return result 
		return 'false'
	else:
		print("Unable to open camera")
		return 'false'

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
