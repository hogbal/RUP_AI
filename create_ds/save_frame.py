import cv2
import os

def video_to_frames(video, met, output_dir):
	vidcap = cv2.VideoCapture(video)

	count = 0
	while vidcap.isOpened():
		success, img = vidcap.read()
		if success:
			cv2.imwrite(os.path.join(output_dir, met+'%d.png') % count, img)
			count += 1
		else:
			break
	cv2.destroyAllWindows()
	vidcap.release()

print("start")
video_to_frames('/server/test.mp4','pet','/server/save')
print("end")
