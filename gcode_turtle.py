class GcodeTurtle():
    header = \
'''; layer_height = 0.3
; perimeters = 1
; top_solid_layers = 3
; bottom_solid_layers = 3
; fill_density = .2
; perimeter_speed = 40
; infill_speed = 60
; travel_speed = 100
; nozzle_diameter = 0.4
; filament_diameter = 1.75
; extrusion_multiplier = 1
; perimeters extrusion width = 0.40mm
; infill extrusion width = 0.42mm
; solid infill extrusion width = 0.42mm
; top infill extrusion width = 0.42mm
; first layer extrusion width = 0.70mm

G21 ; set units to millimeters
M107
M190 S57 ; wait for bed temperature to be reached
M104 S185 ; set temperature
G28 ; home all axes
M109 S185 ; wait for temperature to be reached
G90 ; use absolute coordinates
G92 E0
M82 ; use absolute distances for extrusion
G1 F1800.000 E-1.00000
G92 E0
G1 Z0.350 F6000.000
G1 X49.500 Y49.350 F6000.000
G1 E1.00000 F720.000'''

    def __init__(self):
        self.output = self.header.split("\n")

        #if changing need to update self.header
        self.layer_height = .35
        self.x = 0.0
        self.y = 0.0
        self.z = self.layer_height
        self.e = 1.000
        self.filament_width = 1.75
        self.extrusion_width = .7
        #should be 0.092, turns out to be 0.1018621678
        self.extrusion_rate = 0

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
        self.e = self.e + dist*self.extursion_rate
        self.x = x
        self.y = y
        self.output.append("G1 X%.3f Y%.3f E%.5f"%(self.x, self.y, self.e ))

    def up(self):
        upcode = \
'''G1 F1800.000 E%.5f
G92 E0
G1 Z%.3f F6000.000
;G1 X54.278 Y54.137 F6000.000
G1 E1.00000 F1800.000'''%(self.e - 1,self.z+self.layer_height)

        self.z += self.layer_height
        self.output.extend(upcode.split("\n"))


t = GcodeTurtle()
for i in range(20):
    t.setxy(0,0)
    t.setx(5)
    t.sety(5)
    t.setx(0)
    t.sety(0)
    t.up()

for line in t.output:
    print (line)