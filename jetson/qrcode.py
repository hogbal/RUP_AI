from pyzbar import pyzbar
import cv2

cap = cv2.VideoCapture(1)

if cap.isOpened():
	window_handle = cv2.namedWindow("test",cv2.WINDOW_AUTOSIZE)
	while cv2.getWindowProperty("test",0) >= 0:
		ret_val, img = cap.read()
		"""
		barcodes = pyzbar.decode(img)
		
		for barcode in barcodes:
			print(barcode.data.decode())
		"""
		cv2.imshow("test", img)
		if cv2.waitKey(1) == 27:
			break
