import cv2
import os
from glob import glob
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from object_detection import darknet, darknet_images

app = Flask(__name__)
network, class_names, class_colors = darknet.load_network(
	'model/yolov4-csp/yolov4-csp.cfg',
	'model/yolov4-csp/obj.data',
	'model/yolov4-csp/yolov4-csp_best.weights',
	batch_size=1
)


@app.route('/upload', methods = ['GET', 'POST'])
def render_file():
	if request.method == 'GET':	
		return render_template('upload.html')
	else:
		f = request.files['file']
		filename = secure_filename(f.filename)
		if filename:
			f.save('temp/'+filename)
			vidcap = cv2.VideoCapture('temp/'+filename)
			
			count = 0
			while vidcap.isOpened():
				success, frame = vidcap.read()
				if success:
					image_resized, image_draw, detections = darknet_images.image_detection(
							frame, network, class_names, class_colors,.25
					)
					yolo_path = 'static/yolo/'
					img_name = 'frame'+str(count)+'.png'
					dis_img_name = 'dis'+str(count)+'.png'
					cv2.imwrite(yolo_path+dis_img_name, image_draw)
					cv2.imwrite(yolo_path+img_name, image_resized)
					darknet_images.save_annotations(yolo_path+img_name, image_draw, detections, class_names)
				else:
					break
				count += 1
			os.remove('temp/'+filename)
			vidcap.release()
		else:
			return 'upload error'

		return  'detections success'

@app.route('/view')
def view():
	filepaths = glob('static/yolo/dis*.png')
	filename = []
	for filepath in filepaths:
		filename.append(os.path.basename(filepath))
	return render_template("view.html", pics=filename)

@app.route('/')
def home():
	return 'rup web server!'

if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True)
