from operator import add, sub
from typing import Union

from pygcode import GCodeLinearMove

from eltypes import gcode_line, operator
from operators import replace_op


def _apply_op_to_coor(
    line: gcode_line, coor: str, op: operator, val: int, additive: bool,
    only_for_val: Union[int, None]
) -> gcode_line:
    found = False
    gcodes = line.block.gcodes
    for gcode in gcodes:
        if type(gcode) is GCodeLinearMove:
            current_coor = getattr(gcode, coor)
            if current_coor is not None:
                if only_for_val is not None:
                    if current_coor == only_for_val:
                        setattr(gcode, coor, op(current_coor, val))
                        if additive:
                            found = True
                else:
                    setattr(gcode, coor, op(current_coor, val))
                    if additive:
                        found = True

    return line, found


def inc_coor(
    line: gcode_line, coor: str, val: int, additive: bool,
    only_for_val: Union[int, None]
) -> gcode_line:
    return _apply_op_to_coor(line, coor, add, val, additive, only_for_val)


def dec_coor(
    line: gcode_line, coor: str, val: int, additive: bool,
    only_for_val: Union[int, None]
) -> gcode_line:
    return _apply_op_to_coor(line, coor, sub, val, additive, only_for_val)


def replace_coor(
    line: gcode_line, coor: str, val: int, additive: bool,
    only_for_val: Union[int, None]
) -> gcode_line:
    return _apply_op_to_coor(
        line, coor, replace_op, val, additive, only_for_val
    )
