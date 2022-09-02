import os
import re
import zipfile
from glob import glob

import cv2
import natsort
from flask import Flask, redirect, render_template, request, send_file
from werkzeug.utils import secure_filename

from object_detection import darknet, darknet_images

app = Flask(__name__)

# network, class_names, class_colors = darknet.load_network(
# 	'model/yolov4-tiny/yolov4-tiny.cfg',
# 	'model/yolov4-tiny/obj.data',
# 	'model/yolov4-tiny/yolov4-tiny_best.weights',
# 	batch_size=1
# )

network, class_names, class_colors = darknet.load_network(
	'model/yolov7-tiny/yolov7-tiny.cfg',
	'model/yolov7-tiny/obj.data',
	'model/yolov7-tiny/yolov7-tiny_3000.weights',
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

		met = request.form['met']
		if filename:
			f.save('temp/'+filename)
			vidcap = cv2.VideoCapture('temp/'+filename)
			
			num = request.form['num']
			count = int(num)
			frame_count = 10
			while vidcap.isOpened():
				success, frame = vidcap.read()
				if(frame_count != 10):
					frame_count += 1
				elif success:
					frame_count = 1
					image_resized, image_draw, detections = darknet_images.image_detection(
							frame, network, class_names, class_colors,.25, met
					)

					yolo_path = 'static/yolo/'
					img_name = 'original/'+met+str(count)+'.png'
					dis_img_name = 'detection/dis'+str(count)+'.png'
					label_name = 'yolo_txt/'+met+str(count)+'.png'

					cv2.imwrite(yolo_path+dis_img_name, image_draw)
					cv2.imwrite(yolo_path+img_name, image_resized)
					darknet_images.save_annotations(yolo_path+label_name, image_draw, detections, class_names)
					count += 1
				else:
					break
			os.remove('temp/'+filename)
			vidcap.release()
		else:
			return 'upload error'
		return redirect('/')


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
			filelist = glob('static/yolo/original/*.png')
			filelist += glob('static/yolo/yolo_txt/p*.txt')
			filelist += glob('static/yolo/detection/*.png')

			for filename in filelist:
				os.remove(filename)
			return redirect('/')

@app.route('/download')
def download():
    download_zip = zipfile.ZipFile('temp/download.zip','w')
    
    filelist_img = glob('static/yolo/original/*.png')
    filelist_txt = glob('static/yolo/yolo_txt/*.txt')
    
    for filename in filelist_img:
        download_zip.write(filename,'img/'+os.path.basename(filename))
    
    for filename in filelist_txt:
        download_zip.write(filename,'txt/'+os.path.basename(filename))
    
    download_zip.close()
    
    return send_file('temp/download.zip',
			mimetype='application/zip',
			attachment_filename='download.zip',
			as_attachment=True
			)


@app.route('/')
def home():
	filepaths = glob('static/yolo/detection/dis*.png')
	filepaths = natsort.natsorted(filepaths)
	filenames = []
	for i in range(len(filepaths)):
		filenames.append([os.path.basename(filepaths[i]),i+1])
	return render_template("index.html", filenames=filenames, filelen=len(filenames))

if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True)
