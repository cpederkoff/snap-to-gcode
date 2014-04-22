from io import StringIO
from unittest import TestCase
from io import StringIO
from gcode_turtle import GcodeTurtle

__author__ = 'christian'


class TestGcodeTurtle(TestCase):
    from_slic3r = \
        u"""G21 ; set units to millimeters
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
        G1 E1.00000 F1800.000
        G1 F3000.000"""

    def test_init(self):
        output = StringIO()
        t = GcodeTurtle(fd=output)
        slic3r_lines = self.from_slic3r.split("\n")
        slic3r_lines = map(lambda line: line.split(";")[0], slic3r_lines)

        output_lines = output.getvalue().split("\r\n")
        self.assertEqual(output.getvalue()[-1], "\n")
        output_lines = map(lambda line: line.split(";")[0], output_lines)
        output_lines = filter(lambda line: len(line) > 0, output_lines)  # fastest

        slic3r_lines = map(lambda line: line.strip().split(";")[0], slic3r_lines)
        self.assertSequenceEqual(slic3r_lines, output_lines)

    def test_setxyz(self):
        output = StringIO()
        t = GcodeTurtle(fd=output)
        prelude = output.getvalue()
        t.setxyz(20, 30, 40)
        output_line = output.getvalue()
        output_line = output_line.replace(prelude, "")
        output_line_parts = output_line.split(" ")
        self.assertEqual(len(output_line_parts), 5)
        self.assertEqual(output_line[-1], "\n")
        self.assertEqual(output_line.count("\n"), 1)
        self.assertEqual(output_line_parts[0], "G1")
        self.assertEqual(output_line_parts[1], "X20.000")
        self.assertEqual(output_line_parts[2], "Y30.000")
        self.assertEqual(output_line_parts[3], "Z40.000")
        self.assertEqual(output_line_parts[4][0], "E")

    def test_setxyz_measures_distance(self):
        output = StringIO()
        t = GcodeTurtle(fd=output)
        prelude = output.getvalue()
        t.setxyz(20, 30, 40)
        start_e = t.e
        t.setxyz(30, 40, 50)
        stop_e = t.e
        distance = (stop_e - start_e) / t.extrusion_rate
        self.assertAlmostEqual(distance, 17.320508076)

    def test_setxy(self):
        output = StringIO()
        t = GcodeTurtle(fd=output)
        prelude = output.getvalue()
        t.setxy(20, 30)
        output_line = output.getvalue()
        output_line = output_line.replace(prelude, "")
        output_line_parts = output_line.split(" ")
        self.assertEqual(len(output_line_parts), 4)
        self.assertEqual(output_line[-1], "\n")
        self.assertEqual(output_line.count("\n"), 1)
        self.assertEqual(output_line_parts[0], "G1")
        self.assertEqual(output_line_parts[1], "X20.000")
        self.assertEqual(output_line_parts[2], "Y30.000")
        self.assertEqual(output_line_parts[3][0], "E")

    def test_setx(self):
        output = StringIO()
        t = GcodeTurtle(fd=output)
        prelude = output.getvalue()
        t.setx(20)
        output_line = output.getvalue()
        output_line = output_line.replace(prelude, "")
        output_line_parts = output_line.split(" ")
        self.assertEqual(len(output_line_parts), 3)
        self.assertEqual(output_line[-1], "\n")
        self.assertEqual(output_line.count("\n"), 1)
        self.assertEqual("G1", output_line_parts[0])
        self.assertEqual("X20.000", output_line_parts[1])
        self.assertEqual("E", output_line_parts[2][0])

    def test_changex(self):
        output = StringIO()
        t = GcodeTurtle(fd=output)
        t.setx(10)
        prelude = output.getvalue()
        t.changex(20)
        output_line = output.getvalue()
        output_line = output_line.replace(prelude, "")
        output_line_parts = output_line.split(" ")
        self.assertEqual(len(output_line_parts), 3)
        self.assertEqual(output_line[-1], "\n")
        self.assertEqual(output_line.count("\n"), 1)
        self.assertEqual("G1", output_line_parts[0])
        self.assertEqual("X30.000", output_line_parts[1])
        self.assertEqual("E", output_line_parts[2][0])

    def test_sety(self):
        output = StringIO()
        t = GcodeTurtle(fd=output)
        prelude = output.getvalue()
        t.sety(20)
        output_line = output.getvalue()
        output_line = output_line.replace(prelude, "")
        output_line_parts = output_line.split(" ")
        self.assertEqual(len(output_line_parts), 3)
        self.assertEqual(output_line.count("\n"), 1)
        self.assertEqual(output_line[-1], "\n")
        self.assertEqual("G1", output_line_parts[0])
        self.assertEqual("Y20.000", output_line_parts[1])
        self.assertEqual("E", output_line_parts[2][0])

    def test_changey(self):
        output = StringIO()
        t = GcodeTurtle(fd=output)
        t.sety(10)
        prelude = output.getvalue()
        t.changey(20)
        output_line = output.getvalue()
        output_line = output_line.replace(prelude, "")
        output_line_parts = output_line.split(" ")
        self.assertEqual(len(output_line_parts), 3)
        self.assertEqual(output_line[-1], "\n")
        self.assertEqual(output_line.count("\n"), 1)
        self.assertEqual("G1", output_line_parts[0])
        self.assertEqual("Y30.000", output_line_parts[1])
        self.assertEqual("E", output_line_parts[2][0])

    def test_setz(self):
        output = StringIO()
        t = GcodeTurtle(fd=output)
        prelude = output.getvalue()
        t.setz(20)
        output_line = output.getvalue()
        output_line = output_line.replace(prelude, "")
        output_line_parts = output_line.split(" ")
        self.assertEqual(len(output_line_parts), 3)
        self.assertEqual(output_line[-1], "\n")
        self.assertEqual(output_line.count("\n"), 1)
        self.assertEqual("G1", output_line_parts[0])
        self.assertEqual("Z20.000", output_line_parts[1])
        self.assertEqual("E", output_line_parts[2][0])

    def test_up(self):
        expected = u"G1 F1800.000 E0.00000\r\nG92 E0\r\nG1 Z0.700 F6000.000\r\nG1 E1.00000 F1800.000\r\nG1 F3000.000\r\n"
        output = StringIO()
        t = GcodeTurtle(fd=output)
        prelude = output.getvalue()
        t.up()
        output_line = output.getvalue()
        output_line = output_line.replace(prelude, "")
        self.assertEqual(output_line[-1], "\n")
        self.assertSequenceEqual(expected.split("\n"), output_line.split("\n"))

    def test_forward(self):
        output = StringIO()
        t = GcodeTurtle(fd=output)
        t.set_heading(0)
        t.forward(100)
        self.assertEqual(t.x, 0)
        self.assertEqual(t.y, 100)

    def test_right(self):
        output = StringIO()
        t = GcodeTurtle(fd=output)
        t.set_heading(0)
        t.right(30)
        t.forward(100)
        self.assertAlmostEqual(t.x, 50)
        self.assertAlmostEqual(t.y, 50 * (3 ** .5))

    def test_pen_up(self):
        output = StringIO()
        t = GcodeTurtle(fd=output)
        prelude = output.getvalue()
        t.pen_up()
        output_line = output.getvalue().replace(prelude, "")
        self.assertEqual(output_line, "G1 E-1.000 F6000.000\r\n")
        prelude = output.getvalue()
        t.forward(10)
        output_line = output.getvalue().replace(prelude, "")
        self.assertNotEqual(output_line.split(" ")[-1][0], "E")

    def test_pen_up_does_not_retract_twice(self):
        output = StringIO()
        t = GcodeTurtle(fd=output)
        prelude = output.getvalue()
        t.pen_up()
        t.pen_up()
        output_line = output.getvalue().replace(prelude, "")
        print output_line
        self.assertEqual(output_line, "G1 E-1.000 F6000.000\r\n")

    def test_pen_down(self):
        output = StringIO()
        t = GcodeTurtle(fd=output)
        t.pen_up()
        prelude = output.getvalue()
        t.pen_down()
        output_line = output.getvalue().replace(prelude, "")
        self.assertEqual(output_line, "G1 E1.000 F3000.000\r\n")
        prelude = output.getvalue()
        t.forward(10)
        output_line = output.getvalue().replace(prelude, "")
        self.assertEqual(output_line.split(" ")[-1][0], "E")

    def test_pen_down_does_not_retract_twice(self):
        output = StringIO()
        t = GcodeTurtle(fd=output)
        t.pen_up()
        prelude = output.getvalue()
        t.pen_down()
        t.pen_down()
        output_line = output.getvalue().replace(prelude, "")
        self.assertEqual(output_line, "G1 E1.000 F3000.000\r\n")