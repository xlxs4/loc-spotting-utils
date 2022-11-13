from operator import add, sub

from pygcode import GCodeLinearMove

from eltypes import gcode_line, operator


def _apply_op_to_coor(line: gcode_line, coor: str, op: operator, val: int) -> gcode_line:
    gcodes = line.block.gcodes
    for gcode in gcodes:
        if type(gcode) is GCodeLinearMove:
            current_coor = getattr(gcode, coor)
            if current_coor is not None:
                setattr(gcode, coor, op(current_coor, val))
    
    return line

def inc_coor(line: gcode_line, coor: str, val: int) -> gcode_line:
    return _apply_op_to_coor(line, coor, add, val)

def dec_coor(line: gcode_line, coor: str, val: int) -> gcode_line:
    return _apply_op_to_coor(line, coor, sub, val)
