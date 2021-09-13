from ctypes import *

class IMAGE(Structure):
	_fields_ = [("w", c_int),
			    ("h", c_int),
			    ("c", c_int),
			    ("data", POINTER(c_float))]

class BOX(Structure):
	_fields_ = [("x", c_float),
			    ("y", c_float),
				("w", c_float),
				("h", c_float)]

class DETECTION(Structure):
	_fields_ = [("cl", c_int),
			    ("bbox", BOX),
				("prob", c_float),
				("name", c_char*20)]

try:
	lib = CDLL("cpp_libary/librup_libary.so", RTLD_GLOBAL)

	load_network = lib.load_network
	load_network.argtypes = [c_char_p, c_int, c_int]
	load_network.restype = c_void_p

	copy_image_from_bytes = lib.copy_image_from_bytes
	copy_image_from_bytes.argtypes = [IMAGE, c_char_p]

	make_image = lib.make_image
	make_image.argtypes = [c_int, c_int, c_int]
	make_image.restype = IMAGE

	do_inference = lib.do_inference
	do_inference.argtypes = [c_void_p, IMAGE]

	get_network_boxes = lib.get_network_boxes
	get_network_boxes.argtypes = [c_void_p, c_float, c_int, POINTER(c_int)]
	get_network_boxes.restype = POINTER(DETECTION)
except:
	print('tkdnn libary load error!!')
	print("Unexpected error:", sys.exc_info()[0])
	exit()


def detect_image(net, darknet_image, thresh=0.5):
	num = c_int(0)

	pnum = pointer(num)
	do_inference(net, darknet_image)
	dets = get_network_boxes(net, thresh, 0, pnum)
	res = []
	for i in range(pnum[0]):
		b = dets[i].bbox
		res.append((dets[i].name.decode("ascii"), dets[i].prob, (b.x,b.y,b.w,b.h)))
	return res

class YOLOv4Tiny(object):
	def __init__(self,
			     input_size=640,
				 weight_file='model/yolov4-tiny_fp32.rt',
				 conf_thresh=0.5):
		self.input_size = input_size
		self.model = load_network(weight_file.encode("ascii"), 3, 1)
		self.darknet_image = make_image(input_size, input_size, 3)
		self.thresh = conf_thresh

	def detect(self, img, need_resize=True):
		try:
			if need_resize:
				frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
				img = cv2.resize(frame_rgb,
						         (self.input_size, self.input_size),
								 interpolation=cv2.INTER_LINEAR)
			frame_data = img.ctypes.data_as(c_char_p)
			copy_image_from_bytes(self.darknet_image,frame_data)
			detections = detect_image(self.model, self.darknet_image, thresh=self.thresh)
			return detections
		except Exception as e_s:
			print(e_s)
