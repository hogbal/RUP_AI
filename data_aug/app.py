import cv2
import os
import zipfile
from glob import glob
from flask import Flask, render_template, request, redirect, send_file
from werkzeug.utils import secure_filename
from object_detection import darknet, darknet_images

app = Flask(__name__)
network, class_names, class_colors = darknet.load_network(
	'model/yolov4-csp/yolov4-csp.cfg',
	'model/yolov4-csp/obj.data',
	'model/yolov4-csp/yolov4-csp_best.weights',
	batch_size=1
)
admin_email = 'rup@talk'
admin_passwd = 'rup'


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
		return redirect('https:/hogbal.co.kr:5000')


@app.route('/delete_dir', methods = ['GET', 'POST'])
def delete_dir():
	if request.method == 'GET':
		return_addr = 'delete_dir'
		return render_template('login.html', path=return_addr)
	else:
		email = request.form['email']
		passwd = request.form['password']
		if email != admin_email:
			return 'email error'
		elif passwd != admin_passwd:
			return 'passwd error'
		else:
			filelist = glob('static/yolo/*')
			for filename in filelist:
				os.remove(filename)
			return redirect('https:/hogbal.co.kr:5000')

@app.route('/download', methods = ['GET', 'POST'])
def download():
	if request.method == 'GET':
		return_addr = 'download'
		return render_template('login.html', path=return_addr)
	else:
		email = request.form['email']
		passwd = request.form['password']
		if email != admin_email:
			return 'email error'
		elif passwd != admin_passwd:
			return 'passwd error'
		else:
			download_zip = zipfile.ZipFile('temp/download.zip','w')

			filelist = glob('static/yolo/frame*')
			for filename in filelist:
				download_zip.write(filename)

			return send_file('temp/download.zip',
					mimetype='application/zip',
					attachment_filename='download.zip',
					as_attachment=True
					)


@app.route('/')
def home():
	filepaths = glob('static/yolo/dis*.png')
	filenames = []
	for i in range(len(filepaths)):
		filenames.append([os.path.basename(filepaths[i]),i+1])
	return render_template("index.html", filenames=filenames, filelen=len(filenames))

if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True)
