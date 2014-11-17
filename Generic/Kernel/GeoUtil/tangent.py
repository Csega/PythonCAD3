#
# Copyright (c) 2003, 2004 Art Haas
#
# Copyright (c) 2010 Matteo Boscolo
#
# This file is part of PythonCAD.
#
# PythonCAD is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# PythonCAD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PythonCAD; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#
# functions for handling tangent circles on multiple objects
#

import math

from Kernel.GeoEntity.cline import CLine
from Kernel.GeoEntity.ccircle import CCircle
from Kernel.exception import *

#
# common constants
#

_dtr = math.pi/180.0
_piover2 = math.pi/2.0

def _get_two_point_projection(x1, y1, x2, y2, x, y):
    """
        project a point to a segment 
    """
    _sqlen = pow((x2 - x1), 2) + pow((y2 - y1), 2)
    _rn = ((x - x1) * (x2 - x1)) + ((y - y1) * (y2 - y1))
    _r = _rn/_sqlen
    _px = x1 + _r * (x2 - x1)
    _py = y1 + _r * (y2 - y1)
    return _px, _py

def _get_angled_projection(angle, yint, x, y):
    """
        find the projection point of point (x, y) on a line
        defined by an angle and y intercept
    """
    _x1 = 0.0
    _y1 = yint
    _x2 = _x1 + math.cos(angle)
    _y2 = _y1 + math.sin(angle)
    return _get_two_point_projection(_x1, _y1, _x2, _y2, x, y)

def _two_line_tangent(x1, y1, x2, y2, x3, y3, x4, y4, x, y):
    """
        this function calculates the apprpriate tangent circle
        for two lines (x1, y1)->(x2, y2) and (x3, y3)->(x4, y4)
        using a point (x, y) to determine which tangent circle
        should be defined
    """
    _cx = _cy = _radius = None
    _denom = ((x2 - x1) * (y4 - y3)) - ((y2 - y1) * (x4 - x3))
    # print "denom: %g" % _denom
    if abs(_denom) < 1e-10:
        # print "parallel ..."
        if abs(x2 - x1) < 1e-10: # both vertical
            if x < min(x1, x3) or x > max(x1, x3):
                return None
            _cx = (x3 + x1)/2.0
            _cy = y
            _radius = abs(x3 - x1)/2.0
        elif abs(y2 - y1) < 1e-10: # both horizontal
            if y < min(y1, y3) or y > max(y1, y3):
                return None
            _cx = x
            _cy = (y3 + y1)/2.0
            _radius = abs(y3 - y1)/2.0
        else: # both at equal angles
            _ax1, _ay1 = _get_two_point_projection(x1, y1, x2, y2, x, y)
            # print "ax1: %g; ay1: %g" % (_ax1, _ay1)
            _ax2, _ay2 = _get_two_point_projection(x3, y3, x4, y4, x, y)
            # print "ax2: %g; ay2: %g" % (_ax2, _ay2)
            if (x < min(_ax1, _ax2) or
                x > max(_ax1, _ax2) or
                y < min(_ay1, _ay2) or
                y > max(_ay1, _ay2)):
                return None
            _cx = (_ax1 + _ax2)/2.0
            _cy = (_ay1 + _ay2)/2.0
            _radius = math.hypot((_ax1 - _cx), (_ay1 - _cy))
        return _cx, _cy, _radius
    #
    # the lines are not parallel, so we have to test for the
    # different combinations of horizontal/vertical/sloped lines ...
    #
    if abs(y2 - y1) < 1e-10: # horizontal line 1
        # print "horizontal line 1 ..."
        if abs(y4 - y3) < 1e-10: # this should be handled above ...
            # print "horizontal line 2 ..."
            if y < min(y1, y3) or y > max(y1, y3):
                return None
            _cx = x
            _cy = (y1 + y3)/2.0
            _radius = abs(_cy - y1)
        elif abs(x4 - x3) < 1e-10: # vertical line 2
            # print "vertical line 2 ..."
            _a1 = math.pi/4.0
            _a2 = -_a1
        else:
            _angle = math.atan2((y4 - y3), (x4 - x3))
            _a1 = _angle/2.0
            if _a1 > 0.0:
                _a2 = _a1 - _piover2
            else:
                _a2 = _a1 + _piover2
    elif abs(x2 - x1) < 1e-10: # vertical line 1
        # print "vertical line 1 ..."
        if abs(y4 - y3) < 1e-10: # horizontal line2
            # print "horizontal line 2 ..."
            _a1 = math.pi/4.0
            _a2 = -_a1
        elif abs(x4 - x3) < 1e-10: # this should be handled above ...
            if x < min(x1, x3) or x > max(x1, x3):
                return None
            _cx = (x1 + x3)/2.0
            _cy = y
            _radius = abs(_cx - x1)
        else:
            _angle = math.atan2((y4 - y3), (x4 - x3))
            if _angle > 0.0:
                _a1 = (_angle + _piover2)/2.0
                _a2 = _a1 - _piover2
            else:
                _a1 = (_angle - _piover2)/2.0
                _a2 = _a1 + _piover2
    else:
        _angle1 = math.atan2((y2 - y1), (x2 - x1))
        if abs(y4 - y3) < 1e-10: # horizontal line2
            _a1 = _angle1/2.0
            if _a1 > 0.0:
                _a2 = _a1 - _piover2
            else:
                _a2 = _a1 + _piover2
        elif abs(x4 - x3) < 1e-10: # vertical line2
            if _angle1 > 0.0:
                _a1 = (_angle1 + _piover2)/2.0
                _a2 = _a1 - _piover2
            else:
                _a1 = (_angle1 - _piover2)/2.0
                _a2 = _a1 + _piover2
        else:
            _angle2 = math.atan2((y4 - y3), (x4 - x3))
            _a1 = (_angle1 + _angle2)/2.0
            if _a1 > 0.0:
                _a2 = _a1 - _piover2
            else:
                _a2 = _a1 + _piover2
    if _cx is not None and _cy is not None and _radius is not None:
        return _cx, _cy, _radius
    #
    # handle the general case of two lines at arbitrary angles
    #
    # print "arbitrary angles ..."
    # print "a1: %g" % (_a1/_dtr)
    # print "a2: %g" % (_a2/_dtr)
    _rn = ((y1 - y3) * (x4 - x3)) - ((x1 - x3) * (y4 - y3))
    # print "rn: %g" % _rn
    _r = _rn/_denom
    # print "r: %g" % _r
    _ix = x1 + _r * (x2 - x1)
    _iy = y1 + _r * (y2 - y1)
    # print "ix: %g; iy: %g" % (_ix, _iy)
    _m1 = math.tan(_a1)
    _b1 = _iy - (_m1 * _ix)
    # print "line1: m: %g; b: %g" % (_m1, _b1)
    _m2 = math.tan(_a2)
    _b2 = _iy - (_m2 * _ix)
    # print "line2: m: %g; b: %g" %  (_m2, _b2)
    _px1, _py1 = _get_angled_projection(_a1, _b1, x, y)
    # print "px1: %g; py1: %g" % (_px1, _py1)
    _sep1 = math.hypot((_px1 - x), (_py1 - y))
    _px2, _py2 = _get_angled_projection(_a2, _b2, x, y)
    # print "px2: %g; py2: %g" % (_px2, _py2)
    _sep2 = math.hypot((_px2 - x), (_py2 - y))
    if _sep1 < _sep2:
        _cx = _px1
        _cy = _py1
    else:
        _cx = _px2
        _cy = _py2
    _px, _py = _get_two_point_projection(x1, y1, x2, y2, _cx, _cy)
    _radius = math.hypot((_px - _cx), (_py - _cy))
    return _cx, _cy, _radius


def _gen_cline_ccircle_tangent(radius, hy, x):
    #
    # center of ccircle : (0,0)
    # radius of ccircle : r
    # distance between ccircle and hcl: hy
    # x-coordinate of mouse: x
    #
    # center of tangent circle : (px, py)
    #
    # projection point on hcl: (px, hy)
    #
    # Projection point outside the radius of the circle gives:
    #
    # math.hypot((px - cx), (py - cy)) == math.hypot((px - px), (py - hy)) + r
    #
    # Projection point inside the radius of the circle gives:
    #
    # math.hypot((px - cx), (py - cy)) + rt = r
    #
    # rt == radius of tangent circle
    #
    # Distance from projection point to tangent circle center
    #
    # math.hypot((px - px), (py - hy)) = rt
    #
    # lots of algebra reduces to the following two cases
    #
    _cx = x
    if hy > 0.0:
        _num = pow(x, 2) - pow(hy, 2) - (2.0 * hy * radius) - pow(radius, 2)
        _den = (-2.0 * hy) - (2.0 * radius)
    else:
        _num = pow(x, 2) - pow(hy, 2) + (2.0 * hy * radius) - pow(radius, 2)
        _den = (2.0 * radius) - (2.0 * hy)
    # print "num: %g" % _num
    # print "den: %g" % _den
    _cy = _num/_den
    _radius = abs(_cy - hy)
    return _cx, _cy, _radius
#
# two-point construction line
#

def _cl_cl_tangent(cl1, cl2, x, y):
    _p1, _p2 = cl1.getKeypoints()
    _x1, _y1 = _p1.getCoords()
    _x2, _y2 = _p2.getCoords()
    _p3, _p4 = cl2.getKeypoints()
    _x3, _y3 = _p3.getCoords()
    _x4, _y4 = _p4.getCoords()
    return _two_line_tangent(_x1, _y1, _x2, _y2, _x3, _y3, _x4, _y4, x, y)

def _cl_cc_tangent(cl, cc, x, y):
    _p1, _p2 = cl.getKeypoints()
    _x1, _y1 = _p1.getCoords()
    # print "x1: %g; y1: %g" % (_x1, _y1)
    _x2, _y2 = _p2.getCoords()
    # print "x2: %g; y2: %g" % (_x2, _y2)
    _ccx, _ccy = cc.center.getCoords()
    # print "ccx: %g; ccy: %g" % (_ccx, _ccy)
    _rad = cc.radius
    #
    # transform the coords into the system where the circle center is (0,0)
    # and rotate so the CLine is horizontal
    #
    _apx, _apy = cl.getProjection(_ccx, _ccy)
    # print "apx: %g; apy: %g" % (_apx, _apy)
    _sep = math.hypot((_apx - _ccx), (_apy - _ccy))
    # print "sep: %g" % _sep
    #
    # use the line (ccx, ccy) to (apx, apy) to determine the
    # angular rotation
    #
    if abs(_apx - _ccx) < 1e-10: # cline is horizontal
        _sine = 0.0
        if _apy > _ccy: # system rotated 0.0
            _cosine = 1.0
        else: # system rotated 180.0
            _cosine = -1.0
    elif abs(_apy - _ccy) < 1e-10: # cline is vertical; system rotated -90.0
        _cosine = 0.0
        if _apx > _ccx: # system rotated 90.0
            _sine = 1.0
        else: # system rotated -90.0
            _sine = -1.0
    else:
        _angle = _piover2 - math.atan2((_apy - _ccy), (_apx - _ccx))
        # print "angle: %g" % _angle
        _sine = math.sin(_angle)
        _cosine = math.cos(_angle)
    # print "sin(angle): %g" % _sine
    # print "cos(angle): %g" % _cosine
    #
    # transform (x, y) into
    _tx1 = x - _ccx
    _ty1 = y - _ccy
    # print "tx1: %g; ty1: %g" % (_tx1, _ty1)
    #
    # transform by rotating through angle to
    # map to horizontal line
    #
    _tx = (_tx1 * _cosine) - (_ty1 * _sine)
    _ty = (_tx1 * _sine) + (_ty1 * _cosine)
    # print "tx: %g; ty: %g" % (_tx, _ty)
    _tcx, _tcy, _tcrad = _gen_cline_ccircle_tangent(_rad, _sep, _tx)
    #
    # transform result back into real coordinates
    #
    # print "tcx: %g: tcy: %g" % (_tcx, _tcy)
    _cx = ((_tcx * _cosine) + (_tcy * _sine)) + _ccx
    _cy = (-(_tcx * _sine) + (_tcy * _cosine)) + _ccy
    # print "cx: %g; cy %g" % (_cx, _cy)
    return _cx, _cy, _tcrad

def calc_tangent_circle(obja, objb, x, y):
    _x = x
    if not isinstance(_x, float):
        _x = float(x)
    _y = y
    if not isinstance(_y, float):
        _y = float(y)
    _tandata = None
    if isinstance(obja, CLine):
        if isinstance(objb, CLine):
            _tandata = _cl_cl_tangent(obja, objb, _x, _y)
        elif isinstance(objb, CCircle):
            _cl_cc_tangent(obja, objb, _x, _y)
    elif isinstance(obja, CCircle):
        if isinstance(objb, CLine):
            _tandata = _cl_cc_tangent(objb, obja, _x, _y)
        else:
            raise NotImplementedError, "We must define the ccircle ccircle tangent"
            # CCircle/CCircle tangent circles to do later ...
    return _tandata

#
# calculate the possible tangent lines between two circles
#

def _calc_values(ax, ay, bx, by, cx, cy):
    """This function was used for debugging"""
    _den = pow((bx - ax), 2) + pow((by - ay), 2)
    _num = ((cx - ax) * (bx - ax)) + ((cy - ay) * (by - ay))
    _r = _num/_den
    # print "r: %g" % _r
    _num = ((ay - cy) * (bx - ax)) - ((ax - cx) * (by - ay))
    _s = _num/_den
    # print "s: %g" % _s
    _sep = abs(_s) * math.sqrt(_den)
    # print "sep: %g" % _sep
    # return _r, _s, _sep

def _calc_tangent_triangle(r1, r2, sep, ip):
    _sine = r1/abs(ip)
    # print "sin: %g" % _sine
    _angle = math.asin(_sine)
    # print "angle: %g" % (_angle * (180.0/math.pi))
    _tan = math.tan(_angle)
    # print "tan(angle): %g" % _tan
    _cosine = math.cos(_angle)
    # print "cos(angle): %g" % _cosine
    _tanlen = r1/_tan
    # print "tanlen: %g" % _tanlen
    if ip < 0.0: # r1 < r2 and intersection point left of r1
        assert abs(ip) > r1, "Expected ip beyond radius: %g < %g" % (ip, r1)
        _tx1 =  ip + (_tanlen * _cosine)
    else:
        _tx1 =  ip - (_tanlen * _cosine)
    # print "tx1: %g" % _tx1
    _ty1 = _tanlen * _sine
    # print "ty1: %g" % _ty1
    _dist = math.hypot(_tx1, _ty1)
    # print "dist: %g" % _dist
    assert abs(_dist - r1) < 1e-10, "Invalid tangent point for circle 1"
    _tanlen = r2/_tan
    # print "tanlen: %g" % _tanlen
    if ip < 0.0: # see above
        _tx2 = ip + (_tanlen * _cosine)
        _ty2 = _tanlen * _sine
    elif ip > (sep + r2): # only possible if r1 > r2
        _tx2 = ip - (_tanlen * _cosine)
        _ty2 = _tanlen * _sine
    else:
        _tx2 = ip + (_tanlen * _cosine)
        _ty2 = -1.0 * _tanlen * _sine
    # print "tx2: %g" % _tx2
    # print "ty2: %g" % _ty2
    _dist = math.hypot((_tx2 - sep), _ty2)
    # print "dist: %g" % _dist
    assert abs(_dist - r2) < 1e-10, "Invalid tangent point for circle 2"
    return _tx1, _ty1, _tx2, _ty2

def calc_two_circle_tangents(r1, r2, sep):
    # print "in calc_two_circle_tangents() ..."
    _r1 = r1
    if not isinstance(_r1, float):
        _r1 = float(r1)
    if not _r1 > 0.0:
        raise ValueError, "Invalid radius: %g" % _r1
    _r2 = r2
    if not isinstance(_r2, float):
        _r2 = float(r2)
    if not _r2 > 0.0:
        raise ValueError, "Invalid radius: %g" % _r2
    _sep = sep
    if not isinstance(_sep, float):
        _sep = float(sep)
    _tangents = []
    if (abs(_sep) + min(_r1, _r2)) > max(_r1, _r2): # small circle not within larger
        if abs(_r1 - _r2) < 1e-10:
            # print "same radii ..."
            _tangents.append((0.0, _r1, _sep, _r2))
            _tangents.append((0.0, -_r1, _sep, -_r2))
            if abs(_sep) > _r1 + _r2:
                _mid = _sep/2.0
                _angle = math.asin(_r1/_mid)
                _tanlen = _r1/math.tan(_angle)
                _xt = _tanlen * math.cos(_angle)
                _yt = _tanlen * math.sin(_angle)
                _tx1 = _mid - _xt
                _ty1 = _yt
                _tx2 = _mid + _xt
                _ty2 = -_yt
                _tangents.append((_tx1, _ty1, _tx2, _ty2))
                # _calc_values(_tx1, _ty1, _tx2, _ty2, 0.0, 0.0)
                # _calc_values(_tx1, _ty1, _tx2, _ty2, _sep, 0.0)
                _tangents.append((_tx1, -_ty1, _tx2, -_ty2))
                # _calc_values(_tx1, -_ty1, _tx2, -_ty2, 0.0, 0.0)
                # _calc_values(_tx1, -_ty1, _tx2, -_ty2, _sep, 0.0)
        else:
            _alpha = pow((_r1/_r2), 2)
            # print "alpha: %g" % _alpha
            _a = (1.0 - _alpha)
            # print "a: %g" % _a
            _b = (2.0 * _alpha * _sep)
            # print "b: %g" % _b
            _c = (-1.0 * _alpha * pow(_sep, 2))
            # print "c: %g" % _c
            _det = pow(_b, 2) - (4.0 * _a * _c)
            # print "det: %g" % _det
            if _det > 0.0: # can this ever be negative?
                # print "r1: %g" % _r1
                # print "r2: %g" % _r2
                # print "sep: %g" % _sep
                _denom = 2.0 * _a
                _det_sqrt = math.sqrt(_det)
                _num = (-1.0 * _b) + _det_sqrt
                _offset = _num/_denom
                # print "offset: %g" % _offset
                if (_r1 > _r2):
                    # print "r1 > r2"
                    if ((_offset > (_sep + _r2)) or
                        ((_offset > _r1) and (_offset < (_sep - _r2)))):
                        _tpts = _calc_tangent_triangle(_r1, _r2, _sep, _offset)
                        _tangents.append(_tpts)
                        _tx1, _ty1, _tx2, _ty2 = _tpts
                        # _calc_values(_tx1, _ty1, _tx2, _ty2, 0.0, 0.0)
                        # _calc_values(_tx1, _ty1, _tx2, _ty2, _sep, 0.0)
                        # _calc_values(_tx2, _ty2, _tx1, _ty1, _sep, 0.0)
                        # _calc_values(_tx2, _ty2, _tx1, _ty1, 0.0, 0.0)
                        _tpts = (_tx1, - _ty1, _tx2, -_ty2)
                        _tangents.append(_tpts)
                        # _calc_values(_tx1, -_ty1, _tx2,-_ty2, 0.0, 0.0)
                        # _calc_values(_tx1, -_ty1, _tx2, -_ty2, _sep, 0.0)
                        # _calc_values(_tx2, -_ty2, _tx1, -_ty1, _sep, 0.0)
                        # _calc_values(_tx2, -_ty2, _tx1, -_ty1, 0.0, 0.0)
                else: # _r1 < _r2
                   #  print "r1 < r2"
                    if ((_offset < -_r1) or
                        ((_offset > _r1) and (_offset < (_sep - _r2)))):
                        _tpts = _calc_tangent_triangle(_r1, _r2, _sep, _offset)
                        _tangents.append(_tpts)
                        _tx1, _ty1, _tx2, _ty2 = _tpts
                        # _calc_values(_tx1, _ty1, _tx2, _ty2, 0.0, 0.0)
                        # _calc_values(_tx1, _ty1, _tx2, _ty2, _sep, 0.0)
                        # _calc_values(_tx2, _ty2, _tx1, _ty1, _sep, 0.0)
                        # _calc_values(_tx2, _ty2, _tx1, _ty1, 0.0, 0.0)
                        _tpts = (_tx1, - _ty1, _tx2, -_ty2)
                        _tangents.append(_tpts)
                        # _calc_values(_tx1, -_ty1, _tx2,-_ty2, 0.0, 0.0)
                        # _calc_values(_tx1, -_ty1, _tx2, -_ty2, _sep, 0.0)
                        # _calc_values(_tx2, -_ty2, _tx1, -_ty1, _sep, 0.0)
                        # _calc_values(_tx2, -_ty2, _tx1, -_ty1, 0.0, 0.0)
                _num = (-1.0 * _b) - _det_sqrt
                _offset = _num/_denom
                # print "offset: %g" % _offset
                if (_r1 > _r2):
                    # print "r1 > r2"
                    if ((_offset > (_sep + _r2)) or
                        ((_offset > _r1) and (_offset < (_sep - _r2)))):
                        _tpts = _calc_tangent_triangle(_r1, _r2, _sep, _offset)
                        _tangents.append(_tpts)
                        _tx1, _ty1, _tx2, _ty2 = _tpts
                        _tpts = (_tx1, - _ty1, _tx2, -_ty2)
                        _tangents.append(_tpts)
                else: # _r1 < _r2
                    # print "r1 < r2"
                    if ((_offset < -_r1) or
                        ((_offset > _r1) and (_offset < (_sep - _r2)))):
                        _tpts = _calc_tangent_triangle(_r1, _r2, _sep, _offset)
                        _tangents.append(_tpts)
                        _tx1, _ty1, _tx2, _ty2 = _tpts
                        # _calc_values(_tx1, _ty1, _tx2, _ty2, 0.0, 0.0)
                        # _calc_values(_tx1, _ty1, _tx2, _ty2, _sep, 0.0)
                        # _calc_values(_tx2, _ty2, _tx1, _ty1, _sep, 0.0)
                        # _calc_values(_tx2, _ty2, _tx1, _ty1, 0.0, 0.0)
                        _tpts = (_tx1, - _ty1, _tx2, -_ty2)
                        _tangents.append(_tpts)
                        # _calc_values(_tx1, -_ty1, _tx2,-_ty2, 0.0, 0.0)
                        # _calc_values(_tx1, -_ty1, _tx2, -_ty2, _sep, 0.0)
                        # _calc_values(_tx2, -_ty2, _tx1, -_ty1, _sep, 0.0)
                        # _calc_values(_tx2, -_ty2, _tx1, -_ty1, 0.0, 0.0)
    return _tangents
