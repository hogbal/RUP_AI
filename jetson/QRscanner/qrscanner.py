import cv2
import pyzbar.pyzbar as pyzbar

def scan(cap):
	if cap.isOpened():
		end = time.time() + 10
		while cap.isOpened() and time.time() < end:
			ret_val, img = cap.read()
			if not ret_val:
				break

			qrcode = pyzbar.decode(img)	
			print(qrcode)

def scan_img(path):
	img = cv2.imread(path)
	qrcode = pyzbar.decode(img)

	print(qrcode)
