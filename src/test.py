from IOUtils import read_gcode, write_gcode
from GCodeUtils import inc_coor


file = read_gcode("dummy.gcode")

new_lines = [str(inc_coor(line, 'X', 12)) for line in file]

write_gcode("new_dummy.gcode", new_lines)
