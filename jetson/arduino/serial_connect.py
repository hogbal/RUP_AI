import serial
import time
import json
 
msg = {'conveyor_step' : 0, 'sorting_step' : 0}
port = '/dev/ttyACM0' # 시리얼 포트
baud = 9600 # 시리얼 보드레이트(통신속도)
 
ser = serial.Serial(port,baud)
 
end_str = '\n'
 
while True:
	msg['test'] = input('value : ')
	json_msg = json.dumps(msg)
	ser.write(json_msg.encode())
	ser.write(end_str.encode())

