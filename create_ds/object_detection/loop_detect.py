# -*- encoding: utf-8 -*-
import cv2
import time
from threading import Thread

def yolov4_tiny(model, cap, second):
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
