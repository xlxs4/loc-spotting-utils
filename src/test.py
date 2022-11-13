from IOUtils import read_gcode, write_gcode
from GCodeUtils import inc_coor, replace_coor


file = read_gcode("dummy.gcode")

new_lines = [replace_coor(line, 'Z', 12) for line in file]
new_lines = [inc_coor(line, 'X', 10, only_for_val = 84) for line in new_lines]

write_gcode("new_dummy.gcode", new_lines)
