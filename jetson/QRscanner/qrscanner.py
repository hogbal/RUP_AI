import cv2
import pyzbar.pyzbar as pyzbar

def scan(cap):
	if cap.isOpened():
		end = time.time() + 10
		while cap.isOpened() and time.time() < end:
			ret_val, img = cap.read()
			if not ret_val:
				break
			
			qrcodes = pyzbar.decode(img)	

			if(len(qrcodes) == 1):
				return qrcodes[0].data.decode()

def scan_img(path):
	img = cv2.imread(path)
	qrcodes = pyzbar.decode(img)
	
	return qrcodes[0].data.decode()
