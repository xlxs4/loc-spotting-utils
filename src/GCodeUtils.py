from operator import add, sub
from typing import Union

from pygcode import GCodeLinearMove

from eltypes import gcode_line, operator
from operators import replace_op


def _apply_op_to_coor(line: gcode_line, coor: str, op: operator, val: int, only_for_val:Union[int, None]) -> gcode_line:
    gcodes = line.block.gcodes
    for gcode in gcodes:
        if type(gcode) is GCodeLinearMove:
            current_coor = getattr(gcode, coor)
            if current_coor is not None:
                if only_for_val is not None:
                    if current_coor == only_for_val:
                        setattr(gcode, coor, op(current_coor, val))
                else:
                    setattr(gcode, coor, op(current_coor, val))
    
    return line

def inc_coor(line: gcode_line, coor: str, val: int, only_for_val:int = None) -> gcode_line:
    return _apply_op_to_coor(line, coor, add, val, only_for_val)

def dec_coor(line: gcode_line, coor: str, val: int, only_for_val:int = None) -> gcode_line:
    return _apply_op_to_coor(line, coor, sub, val, only_for_val)

def replace_coor(line: gcode_line, coor: str, val: int, only_for_val:int = None) -> gcode_line:
    return _apply_op_to_coor(line, coor, replace_op, val, only_for_val)
