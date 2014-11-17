#
# Copyright (c) 2003 Art Haas
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
# NURBS curves


import array
from Kernel.GeoEntity.geometricalentity  import *

class Nurb(GeometricalEntity):
    def __init__(self, ctrlpts, knots, order):
        if not isinstance(ctrlpts, list):
            raise TypeError, "Invalid control point list: " + str(ctrlpts)
        if not isinstance(knots, list):
            raise TypeError, "Invalid knot list: " + str(knots)
        if not isinstance(order, int):
            raise TypeError, "Invalid order; " + str(order)
        if order < 2 or order > 16: # what is a good max value?
            raise ValueError, "Invalid order: %d" % order
        _ctrlpts = []
        for _pt in ctrlpts:
            if not isinstance(_pt, tuple):
                raise TypeError, "Invalid control point: " + str(_pt)
            _len = len(_pt)
            if not (1 < _len < 4):
                raise ValueError, "Invalid tuple length: " + str(_pt)
            if _len == 2:
                _x, _y = _pt
                _w = 1.0
            else:
                _x, _y, _w = _pt
            if not isinstance(_x, float):
                _x = float(_x)
            if not isinstance(_y, float):
                _y = float(_y)
            if not isinstance(_w, float):
                _w = float(_w)
            if not (_w > 0.0):
                raise ValueError, "Invalid weight: %g" % _w
            _ctrlpts.append((_x, _y, _w))
        _knots = []
        for _knot in knots:
            if not isinstance(_knot, float):
                _knot = float(_knot)
            if (_knot < 0.0 or _knot > 1.0):
                raise ValueError, "Invalid knot value: %g" % _knot
            for _val in _knots:
                if _knot < (_val - 1e-10):
                    raise (ValueError, "Invalid decreasing knot: %g < %g" %
                           (_knot, _val))
            _knots.append(_knot)
        print "knots: " + str(_knots)
        print "ctrl: " + str(_ctrlpts)
        print "order: %d" % order
        _clen = len(_ctrlpts)
        if _clen < order:
            raise ValueError, "Order greater than number of control points."
        if len(_knots) != (_clen + order):
            raise ValueError, "Knot/Control Point/Order number error."
        self.__ctrlpts = _ctrlpts
        self.__knots = _knots
        self.__order = order

    def getControlPoints(self):
        return self.__ctrlpts[:]

    def getKnots(self):
        return self.__knots[:]

    def getOrder(self):
        return self.__order

    def calculate(self, count):
        if not isinstance(count, int):
            raise TypeError, "Invalid count: " + str(count)
        _cpts = self.__ctrlpts
        _knots = self.__knots
        _dt = 1.0/float(count)
        _p = self.__order - 1
        _pts = []
        for _c in range(count):
            _t = _c * _dt
            # print "time: %g" % _t
            _nx = _ny = _nw = 0.0
            for _i in range(len(_cpts)):
                # print "using cpt %d" % _i
                _x, _y, _w = _cpts[_i]
                _Ni = self._N(_i, _p, _t)
                _nx = _nx + (_Ni * _x)
                _ny = _ny + (_Ni * _y)
                _nw = _nw + (_Ni * _w)
            # print "nw: %.3f" % _nw
            # print "nx: %.3f" % _nx
            # print "ny: %.3f" % _ny
            if abs(_nw) > 1e-10:
                _pts.append((_nx/_nw, _ny/_nw))
            else:
                print "zero weight: %f, %f" % (_nx, _ny)

        return _pts

    def _N(self, i, p, t):
        # print "_N() ..."
        _flag = False
        if abs(t - 1.0) < 1e-10 and False:
            _flag = True
        if _flag:
            print "i: %d" % i
            print "p: %d" % p
            print "t: %.3f" % t
        _knots = self.__knots
        _ki = _knots[i]
        _kin = _knots[i + 1]
        if _flag:
            print "ki: %.3f" % _ki
            print "kin: %.3f" % _kin
        if p == 0:
            if ((_ki - 1e-10) < t < _kin):
                _val = 1.0
            else:
                _val = 0.0
        else:
            _kip = _knots[i + p]
            _kipn = _knots[i + p + 1]
            if _flag:
                print "kip: %.3f" % _kip
                print "kipn: %.3f" % _kipn
            _t1 = 0.0
            _v1 = _kip - _ki
            if abs(_v1) > 1e-10:
                _v2 = t - _ki
                if abs(_v2) > 1e-10:
                    _t1 = (_v2/_v1) * self._N(i, (p - 1), t)
            _t2 = 0.0
            _v1 = _kipn - _kin
            if abs(_v1) > 1e-10:
                _v2 = _kipn - t
                if abs(_v2) > 1e-10:
                    _t2 = (_v2/_v1) * self._N((i + 1), (p - 1), t)
            _val = _t1 + _t2
        if _flag:
            print "val: %f" % _val
        return _val

    def writedata(self, count, fname):
        if not isinstance(count, int):
            raise TypeError, "Invalid count: " + str(count)
        _f = file(fname, "w")
        for _pt in self.calculate(count):
            _x, _y = _pt
            _f.write("%f %f\n" % (_x, _y))
        _f.close()
        _f = file('control_points', "w")
        for _pt in self.getControlPoints():
            _x, _y, _w = _pt # ignore weight
            _f.write("%f %f\n" % (_x, _y))
        _f.close()
        _f = file('knots', "w")
        for _knot in self.getKnots():
            _f.write("%f 0.0\n" % _knot)
        _f.close()

    def _NN(self, i, p, t):
        _cpts = self.__ctrlpts
        _cl = len(_cpts)
        _knots = self.__knots
        _kl = len(_knots) - 1
        _val = _kl * [0.0]
        #
        # calculate values for 0
        #
        for _i in range(_kl):
            if ((_knots[i] - 1e-10) < t < _knots[i + 1]):
                _val[_i] = 1.0
        #
        # calculate values up to the degree
        #
        for _j in range(1, (p + 1)):
            for _i in range(_kl - _j):
                _ki = _knots[_i]
                _kin = _knots[_i + 1]
                _kip = _knots[_i + p]
                _kipn = _knots[_i + p + 1]
                _t1 = 0.0
                _n = _val[_i]
                if abs(_n) > 1e-10:
                    _v1 = _kip - _ki
                    if abs(_v1) > 1e-10:
                        _v2 = t - _ki
                        if abs(_v2) > 1e-10:
                            _t1 = (_v2/_v1) * _n
                _t2 = 0.0
                _n = _val[_i + 1]
                if abs(_n) > 1e-10:
                    _v1 = _kipn - _kin
                    if abs(_v1) > 1e-10:
                        _v2 = _kipn - t
                        if abs(_v2) > 1e-10:
                            _t2 = (_v2/_v1) * _n
                _val[_i] = _t1 + _t2
