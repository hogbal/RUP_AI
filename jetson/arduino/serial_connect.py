import serial
import time
import json
 
"""
port_main = '/dev/ttyACM0' # 시리얼 포트
baud_main = 9600 # 시리얼 보드레이트(통신속도)

port_sub = '/dev/ttyUSB0'
baud_sub = 9600
"""
port_main = '/dev/ttyUSB0' # 시리얼 포트
baud_main = 9600 # 시리얼 보드레이트(통신속도)

#port_sub = '/dev/ttyACM0'
#baud_sub = 9600


ser_main = serial.Serial(port_main,baud_main)
#ser_sub = serial.Serial(port_sub,baud_sub)
 
 
'''
while True:
	msg['test'] = input('value : ')
	json_msg = json.dumps(msg)
	ser.write(json_msg.encode())
	ser.write(end_str.encode())
'''
while True:
	if ser_main.readable():
		res = ser_main.readline()
		read_data = res.decode()[:len(res)-1]
		print(read_data)
		if read_data == 'Detection\r':
			print("RUP START")
			send_data = "1"
			ser_main.write(send_data.encode("utf-8"))
