from operator import add, sub
from types import FunctionType

from pygcode import Line, GCodeLinearMove


def _apply_op_to_coor(line: Line, coor: str, op: FunctionType, val: int) -> Line:
    gcodes = line.block.gcodes
    for gcode in gcodes:
        if type(gcode) is GCodeLinearMove:
            current_coor = getattr(gcode, coor)
            if current_coor is not None:
                setattr(gcode, coor, op(current_coor, val))
    
    return line

def inc_coor(line: Line, coor: str, val: int) -> Line:
    return _apply_op_to_coor(line, coor, add, val)

def dec_coor(line: Line, coor: str, val: int) -> Line:
    return _apply_op_to_coor(line, coor, sub, val)
