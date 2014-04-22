#SnapGcode by rcpedersen
import SimpleHTTPServer
import serial
from gcode_turtle import GcodeTurtle
from send_gcode import send_gcode


class CORSHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def send_head(self):
        path = self.path
        print path
        ospath = os.path.abspath('')
        if 'setxy' in path:
            regex = re.compile("/setxy([0-9]+)a([0-9]+)")
            m = regex.match(path)
            x = int(m.group(1))
            y = int(m.group(2))
            t.setxy(x, y)
        elif 'setz' in path:
            regex = re.compile("/setz([0-9]+)")
            m = regex.match(path)
            z = int(m.group(1))
            t.setz(z)
        elif 'forward' in path:
            regex = re.compile("/forward([0-9]+)")
            m = regex.match(path)
            distance = int(m.group(1))
            t.forward(distance)
        elif 'turn' in path:
            regex = re.compile("/turn([0-9]+)")
            m = regex.match(path)
            angle = int(m.group(1))
            t.right(angle)
        elif 'penup' in path:
            t.pen_up()
        elif 'pendown' in path:
            t.pen_down()
        elif 'layerup' in path:
            t.up()
        elif path == '/snapgcode':
            f = open(ospath + '/snapgcode.xml', 'rb')
            ctype = self.guess_type(ospath + '/nxreturn')
            self.send_response(200)
            self.send_header("Content-type", ctype)
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs[6]))
            self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            return f


if __name__ == "__main__":
    import os
    import re
    import SocketServer

    PORT = 1234
    Handler = CORSHTTPRequestHandler
    ser = serial.Serial(
        port='/dev/ttyACM0',
        baudrate=115200,
        timeout=1,
    )

    ser.open()
    if ser.isOpen():
        print "connected to 3d printer"
        print "3d printer says:"
        line = ser.readline()
        while line != "" and line[-1] == '\n':
            line += ser.readline()
        print line
        t = GcodeTurtle(fd=send_gcode(ser), bed_temp=20)

        httpd = SocketServer.TCPServer(("", PORT), Handler)

        print "serving at port", PORT
        print "Go ahead and launch Snap!."
        print "<a>http://snap.berkeley.edu/snapsource/snap.html#open:http://localhost:1234/snapgcode</a>"

        httpd.serve_forever()