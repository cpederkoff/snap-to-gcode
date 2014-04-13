import math
import sys


class GcodeTurtle():
    def __init__(self, filename=None, bed_temp=57, ext_temp=185, filament_diameter=1.75, extrusion_width=.7, layer_height=.35, speed=60):
        #Borrowed from http://code.google.com/p/gcodegen
        self.filename = filename
        # set up the gcode file:
        if not filename:
          self.fd = sys.stdout
        else:
          self.fd = open(filename, "w")
        self.layer_height = layer_height

        #0 is north, 90 is east, 180 is south, and 270 is west
        self.heading = 0
        self.is_pen_down = True
        self.filament_width = filament_diameter
        self.extrusion_width = extrusion_width
        #should be 0.092, turns out to be 0.1018621678
        self.extrusion_rate = .092
        #speed is given in mm/s but gcode uses mm/s * 100
        self.gcode_speed = speed * 100

        self.fd.write("; bed_temp = %d\n"%bed_temp)
        self.fd.write("; extruder_temp = %d\n"%ext_temp)
        self.fd.write("; filament_diameter = %f\n"%filament_diameter)
        self.fd.write("; extrusion_width = %f\n"%extrusion_width)
        self.fd.write("; layer_height = %f\n"%layer_height)
        self.fd.write("; speed = %f\n"%speed)
        self.fd.write("G21 ; set units to millimeters\n")
        self.fd.write("M107\n")
        self.fd.write("M190 S%d ; wait for bed temperature to be reached\n"%bed_temp)
        self.fd.write("M104 S%d ; set temperature\n"%ext_temp)
        self.fd.write("G28 ; home all axes\n")
        self.fd.write("M109 S%d ; wait for temperature to be reached\n"%ext_temp)
        self.fd.write("G90 ; use absolute coordinates\n")
        self.fd.write("G92 E0\n")
        self.fd.write("M82 ; use absolute distances for extrusion\n")
        self.fd.write("G1 F%f.3 E-1.00000\n"%self.gcode_speed)
        self.fd.write("G92 E0\n")
        self.fd.write("G1 Z%f.3 F%f.3\n"%(self.layer_height,self.gcode_speed))
        self.z = self.layer_height
        self.fd.write("G1 X0.000 Y0.000 F%f.3\n"%self.gcode_speed)
        self.x = 0.0
        self.y = 0.0
        self.fd.write("G1 E1.00000 F720.000\n")
        self.e = 1.000

    def set_extrusion_rate(self, extrusion_width):
        self.extrusion_width = extrusion_width
        filament_cross_sectional_area = (self.filament_width/2)**2 * 3.1415
        extrusion_cross_sectional_area = self.layer_height*self.extrusion_width
        self.extrusion_rate = extrusion_cross_sectional_area/filament_cross_sectional_area

    def setx(self,x):
        self.setxy(x,self.y)

    def sety(self,y):
        self.setxy(self.x, y)

    def setxy(self,x,y):
        dist = ((float(x)-self.x)**2 + (float(y)-self.y)**2)**.5
        self.x = x
        self.y = y
        if self.is_pen_down:
            self.e += dist * self.extrusion_rate
            self.fd.write("G1 X%.3f Y%.3f E%.5f\n"%(self.x, self.y, self.e ))
        else:
            self.fd.write("G1 X%.3f Y%.3f\n"%(self.x, self.y))

    def up(self):
        upcode = \
'''G1 F1800.000 E%.5f
G92 E0
G1 Z%.3f F6000.000
;G1 X54.278 Y54.137 F6000.000
G1 E1.00000 F1800.000\n'''%(self.e - 1,self.z+self.layer_height)

        self.z += self.layer_height
        self.fd.write(upcode)

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


t = GcodeTurtle()

for i in range(180):
    t.forward(1)
    t.right(1)
    t.up()


