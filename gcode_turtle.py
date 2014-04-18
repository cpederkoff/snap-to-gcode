import math
import sys


class GcodeTurtle():
    def __init__(self, fd=sys.stdout, bed_temp=57, ext_temp=185, filament_diameter=1.75, extrusion_width=.7, layer_height=.35, speed=60, center_x=50, center_y=50):
        #be sure this is something like sys.stdout or open(filename, "w")
        self.fd = fd
        self.layer_height = layer_height

        #0 is north, 90 is east, 180 is south, and 270 is west
        self.heading = 90
        self.is_pen_down = True
        self.filament_width = filament_diameter
        self.extrusion_width = extrusion_width
        #should be 0.092, turns out to be 0.1018621678
        self.extrusion_rate = .092
        #speed is given in mm/s but gcode uses mm/s * 100
        self.gcode_speed = speed * 100

        # self.fd.write(u"; bed_temp = %d\r\n"%bed_temp)
        # self.fd.write(u"; extruder_temp = %d\r\n"%ext_temp)
        # self.fd.write(u"; filament_diameter = %f\r\n"%filament_diameter)
        # self.fd.write(u"; extrusion_width = %f\r\n"%extrusion_width)
        # self.fd.write(u"; layer_height = %f\r\n"%layer_height)
        # self.fd.write(u"; speed = %f\r\n"%speed)
        self.fd.write(u"G21\r\n")#set units to millimeters
        self.fd.write(u"M107\r\n")
        # self.fd.write(u";M190 S%d ; wait for bed temperature to be reached\r\n"%bed_temp)
        # self.fd.write(u";M104 S%d ; set temperature\r\n"%ext_temp)
        self.fd.write(u"G28\r\n")#home all axes
        # self.fd.write(u";M109 S%d ; wait for temperature to be reached\r\n"%ext_temp)
        self.fd.write(u"G90\r\n")#use absolute coordinates
        self.fd.write(u"G92 E0\r\n")
        self.fd.write(u"M82\r\n")#use absolute distances for extrusion
        self.x = 0
        self.y = 0
        self.z = 0
        self.e = 0.0
        self.up()
        self.pen_up()
        self.setxy(0,0)
        self.pen_down()

    def set_extrusion_rate(self, extrusion_width):
        self.extrusion_width = extrusion_width
        filament_cross_sectional_area = (self.filament_width/2)**2 * 3.1415
        extrusion_cross_sectional_area = self.layer_height*self.extrusion_width
        self.extrusion_rate = extrusion_cross_sectional_area/filament_cross_sectional_area

    def setx(self,x):
        self.setxyz(x, self.y, self.z)

    def changex(self,amt):
        self.setxyz(self.x + amt, self.y, self.z)

    def sety(self,y):
        self.setxyz(self.x, y, self.z)

    def changey(self, amt):
        self.setxyz(self.x, self.y + amt, self.z)

    def setz(self, z):
        self.setxyz(self.x, self.y, z)

    def setxy(self,x,y):
        self.setxyz(x, y, self.z)

    def setxyz(self, x, y, z):
        dist = ((float(x)-self.x)**2 + (float(y)-self.y)**2 + (float(z)-self.z)**2)**.5
        gcode = u"G1 "
        if self.x != x:
            gcode += "X%.3f " % x
            self.x = x
        if self.y != y:
            gcode += "Y%.3f " % y
            self.y = y
        if self.z != z:
            gcode += "Z%.3f " % z
            self.z = z
        if self.is_pen_down:
            self.e += dist * self.extrusion_rate
            gcode += "E%.5f"%self.e
        gcode+="\r\n"
        self.fd.write(gcode)



    def up(self):
        #Back the extruder up 1mm at 18mm/s
        self.fd.write(u"G1 F1800.000 E%.5f\r\n"%(self.e - 1))
        #Set the extruder counter to 0
        self.fd.write(u"G92 E0\r\n")
        self.e = 0
        #Move up one layer height
        self.fd.write(u"G1 Z%.3f F%.3f\r\n"%(self.z + self.layer_height,self.gcode_speed))
        self.z += self.layer_height
        #Move the extruder forward 1mm at 18mm/s
        self.fd.write(u"G1 E1.00000 F1800.000\r\n")
        self.e = 1
        #Set the default speed back to the gcode_speed
        self.fd.write(u"G1 F%.3f\r\n"%self.gcode_speed)

    def forward(self,distance):
        new_x = self.x + distance*math.sin(math.radians(self.heading))
        new_y = self.y + distance*math.cos(math.radians(self.heading))
        self.setxy(new_x, new_y)

    def right(self, angle):
        self.heading += angle
        self.heading %= 360

    def left(self, angle):
        self.right(-angle)

    def back(self, distance):
        self.forward(-distance)

    def pen_up(self):
        self.is_pen_down = False

    def pen_down(self):
        self.is_pen_down = True

    def set_heading(self, heading):
        self.heading = heading

if __name__ == '__main__':
    t = GcodeTurtle()

    for i in range(180):
        t.forward(1)
        t.right(1)
        t.up()


