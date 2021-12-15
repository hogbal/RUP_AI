# -*- encoding: utf-8 -*-
import cv2

def detect_save(model, cap, img):
	img = cv2.resize(img,
			         (640,640),
					 interpolation=cv2.INTER_LINEAR)
	detections = model.detect(img, need_resize=False)

	for det in detections:
		det_class = det[0]
		prob = str(format(det[1],".2f"))
		print(det_class+" : "+prob)

	return detections
