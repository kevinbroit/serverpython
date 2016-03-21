from bluetooth import *
import RPi.GPIO as GPIO
import time

## function to make it blink
def Blink182(numTimes,speed):
	for i in range(0,numTimes):
		print str(i+1)
		GPIO.output(11,True)
		time.sleep(speed)
		GPIO.output(11,False)
		time.sleep(speed)
	print "Done"
	GPIO.cleanup()


GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
GPIO.setup(11,GPIO.OUT) ## Mark pin from Rasp to use

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "00001101-0000-1000-8000-00805f9b34fb"

advertise_service( server_sock, "SampleServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ], 
#                   protocols = [ OBEX_UUID ] 
                    )

print("Waiting for connection on RFCOMM channel %d" % port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)

try:
    while True:
        data = client_sock.recv(1024)
        if len(data) == 0: break
	
	if data.strip()  == 'on':
		Blink182(int(1),float(1))
	else:
	        print("received [%s]" % data.strip())
except IOError:
    pass

print("disconnected")

client_sock.close()
server_sock.close()
print("all done")


