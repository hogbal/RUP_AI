import cv2
import time

from object_detection import load_camera, load_detect, load_model

cap = load_camera.csi_camera()
model = load_model.YOLOv4Tiny(weight_file='model/yolov4-tiny_fp32.rt')

time.sleep(3)

print("Start")

count = 0
while True:
	ret, frame = cap.read()

	frame = cv2.resize(frame,(640,640,interpolation=cv2.INTER_LINEAR)
	detections = model.detect(frame, need_resize=False) 

	for det in detections:
		'''
		format
		'''

	img_name = "save/frame%d.jpg"%count

	cv2.imwrite(img_name, frame)
	count += 1
