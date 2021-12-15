import cv2
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from object_detection import load_model, darknet

app = Flask(__name__)
model = load_model.YOLOv4CSP(weight_file='model/yolov4-csp_fp32.rt')

@app.route('/upload', methods = ['GET', 'POST'])
def render_file():
	if request.method == 'GET':	
		return render_template('upload.html')
	else:
		f = request.files['file']
		filename = secure_filename(f.filename)
		if filename:
			vidcap = cv2.VideoCapture(video)
			while cap.isOpened():
				success, img = cap.read()
				if success:
					darknet.detect_save(model, vidcap, img)
				break
			else:
				return 'cap error'
		else:
			return 'upload error'

		return  'uploads success'

@app.route('/')
def home():
	return 'rup web server!'

if __name__ == '__main__':
	app.run(debug=True)
