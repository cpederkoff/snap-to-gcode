# configure the serial connections (the parameters differs on the device you are connecting to)
import serial

class send_gcode():
    def __init__(self,ser):
        self.ser = ser
    def write(self,msg):
        print "writing:" + str(msg)
        self.ser.write(msg)
        print "response:" + str(self.ser.readline())
    def readline(self):
        return self.ser.readline()
