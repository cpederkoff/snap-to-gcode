# configure the serial connections (the parameters differs on the device you are connecting to)
import serial


class send_gcode():
    def __init__(self, ser):
        self.ser = ser

    def write(self, msg):
        print "writing:" + str(msg)
        self.ser.write(msg)
        response = self.ser.readline()
        while response != 'ok\n':
            print "recieved:" + str(response)
            response = self.ser.readline()
        print "recieved:" + str(response)


    def readline(self):
        return self.ser.readline()
