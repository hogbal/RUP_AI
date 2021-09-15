import cv2

def web_cam():
	cap = cv2.VideoCapture(0)
	cap.set(cv2.CAP_PROP_BUFFERSIZE, 0)
	return cap
