from io import StringIO
from unittest import TestCase
from io import StringIO
from gcode_turtle import GcodeTurtle

__author__ = 'christian'


class TestGcodeTurtle(TestCase):
    from_slic3r=\
"""G21 ; set units to millimeters
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
;G1 X59.310 Y59.310 F6000.000
G1 E1.00000 F1800.000
"""
    def test_init(self):
        output = StringIO()
        t = GcodeTurtle(fd=output)
        slic3r_lines = self.from_slic3r.split("\n")
        slic3r_lines = map(lambda line:line.split(";")[0],slic3r_lines)
        slic3r_lines = filter(None, slic3r_lines)

        output_lines = output.getvalue().split("\n")
        output_lines = map(lambda line:line.split(";")[0],output_lines)
        output_lines = filter(None, output_lines) # fastest
        for slic3r_line, output_line in zip(slic3r_lines, output_lines):
            slic3r_line = slic3r_line.split(";")[0]
            slic3r_line = slic3r_line.strip()
            output_line = output_line.split(";")[0]
            output_line = output_line.strip()
            self.assertEqual(slic3r_line, output_line, "Expected line:\n %s\n did not match actual line:\n %s\n"%(slic3r_line,output_line))

    def test_setxy(self):
        output = StringIO()
        t = GcodeTurtle(fd=output)
        prelude = output.getvalue()
        t.setxy(20,30)
        output_line = output.getvalue()
        output_line = output_line.replace(prelude, "")
        output_line_parts = output_line.split(" ")
        self.assertEqual(len(output_line_parts),4)
        self.assertEqual(output_line_parts[0], "G1")
        self.assertEqual(output_line_parts[1], "X20.000")
        self.assertEqual(output_line_parts[2], "Y30.000")
        self.assertEqual(output_line_parts[3][0], "E")
