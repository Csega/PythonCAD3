#
# Copyright (c) 2006 Art Haas
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
# code to handle rotating objects
#

from math import hypot, fmod, atan2, sin, cos, pi

from Kernel.GeoEntity.util     import *
from Kernel.GeoEntity.point    import Point
from Kernel.GeoEntity.segment  import Segment
from Kernel.GeoEntity.arc      import Arc
from Kernel.GeoEntity.cline    import CLine
from Kernel.GeoEntity.ccircle  import CCircle
from Kernel.GeoEntity.polyline import Polyline


#from PythonCAD.Generic.segjoint import Chamfer, Fillet
#from PythonCAD.Generic.leader import Leader
#from PythonCAD.Generic.text import TextBlock
#from PythonCAD.Generic.dimension import Dimension, DimString
#from PythonCAD.Generic.dimension import LinearDimension
#from PythonCAD.Generic.dimension import AngularDimension


_twopi = (2.0 * pi)
_dtr = (pi/180.0)

def _calc_coords(pt, cx, cy, ra):
    _px, _py = pt.getCoords()
    _r = hypot((_px - cx), (_py - cy))
    _aorig = atan2((_py - cy), (_px - cx))
    _anew = fmod((_aorig + ra), _twopi)
    _nx = cx + (_r * cos(_anew))
    _ny = cy + (_r * sin(_anew))
    return (_nx, _ny)

def _xfrm_point(pt, objdict, cx, cy, ra):
    _layer = pt.getParent()
    _pid = id(pt)
    _np = None
    _x, _y = _calc_coords(pt, cx, cy, ra)
    if _can_move(pt, objdict) and objdict.get(_pid) is not False:
        pt.setCoords(_x, _y)
    else:
        _pts = _layer.find('point', _x, _y)
        if len(_pts) == 0:
            _np = Point(_x, _y)
            _layer.addObject(_np)
        else:
            _np = _most_used(_pts)
    return _np
    
def _adjust_dimensions(op, np):
    _objs = 0
    _dims = []
    _reset = True
    for _user in op.getUsers():
        if isinstance(_user, Dimension):
            _dims.append(_user)
        else:
            _objs = _objs + 1
            if _objs > 1:
                _reset = False
                break
    if _reset:
        for _dim in _dims:
            if isinstance(_dim, LinearDimension):
                _p1, _p2 = _dim.getDimPoints()
                if _p1 is op:
                    _user.setP1(np)
                elif _p2 is op:
                    _user.setP2(np)
            elif isinstance(_dim, AngularDimension):
                _vp, _p1, _p2 = _dim.getDimPoints()
                if _vp is op:
                    _user.setVertexPoint(np)
                elif _p1 is op:
                    _user.setP1(np)
                elif _p2 is op:
                    _user.setP2(np)
            else:
                raise TypeError, "Unknown dimension type: " + `type(_dim)`
    return _reset

def _most_used(plist):
    _pmax = plist.pop()
    _max = _pmax.countUsers()
    for _pt in plist:
        _count = _pt.countUsers()
        if _count > _max:
            _max = _count
            _pmax = _pt
    return _pmax

def _used_by(obj, plist):
    _objpt = None
    for _pt in plist:
        for _user in _pt.getUsers():
            if _user is obj:
                _objpt = _pt
                break
        if _objpt is not None:
            break
    return _objpt
    
def _can_move(obj, objdict):
    raise DeprecatedError,"The can move have no more relevance from Version R38"
    for _user in obj.getUsers():
        if id(_user) not in objdict:
            return False
    return True




def _rotate_polyline(obj, objdict, cx, cy, ra):
    _pts = obj.getPoints()
    _layer = obj.getParent()
    if _layer is None:
        raise RuntimeError, "Polyline parent is None"
    _move = True
    for _pt in _pts:
        if _pt.getParent() is not _layer:
            raise RuntimeError, "Polyline/point parent object conflict!"
        _move = (_can_move(_pt, objdict) and
                 (objdict.get(id(_pt)) is not False))
        if not _move:
            break
    if _move:
        for _pt in _pts:
            _x, _y = _calc_coords(_pt, cx, cy, ra)
            _pt.setCoords(_x, _y)
            _pid = id(_pt)
            objdict[_pid] = False
    else:
        for _i in range(len(_pts)):
            _pt = _pts[_i]
            if objdict.get(_pid) is True:
                _x, _y = _calc_coords(_pt, cx, cy, ra)
                _pts = _layer.find('point', _x, _y)
                if len(_pts) == 0:
                    _np = Point(_x, _y)
                    _layer.addObject(_np)
                else:
                    _np = _most_used(_pts)
                obj.setPoint(_i, _np)
                objdict[_pid] = False
                _layer.delObject(_pt)

def _rotate_leader(obj, objdict, cx, cy, ra):
    _layer = obj.getParent()
    if _layer is None:
        raise RuntimeError, "Leader parent is None"
    _p1, _p2, _p3 = obj.getPoints()    
    if _p1.getParent() is not _layer:
        raise RuntimeError, "Leader/P1 parent object conflict!"
    if _p2.getParent() is not _layer:
        raise RuntimeError, "Leader/P2 parent object conflict!"
    if _p3.getParent() is not _layer:
        raise RuntimeError, "Leader/P3 parent object conflict!"
    _np = _xfrm_point(_p1, objdict, cx, cy, ra)
    if _np is not None:
        obj.setP1(_np)
        if _adjust_dimensions(_p1, _np):
            _layer.delObject(_p1)
    _np = _xfrm_point(_p2, objdict, cx, cy, ra)
    if _np is not None:
        obj.setP2(_np)
        if __adjust_dimensions(_p2, _np):
            _layer.delObject(_p2)
    _np = _xfrm_point(_p3, objdict, cx, cy, ra)
    if _np is not None:
        obj.setP3(_np)
        if __adjust_dimensions(_p3, _np):
            _layer.delObject(_p3)
    _pid = id(_p1)
    if objdict.get(_pid) is not False:
        objdict[_pid] = False
    _pid = id(_p2)
    if objdict.get(_pid) is not False:
        objdict[_pid] = False
    _pid = id(_p3)
    if objdict.get(_pid) is not False:
        objdict[_pid] = False

def _adjust_endpoint(arc, pt, objdict, cx, cy, ra):
    _layer = arc.getParent()
    if pt.getParent() is not _layer:
        raise RuntimeError, "Arc/Endpoint parent object conflict!"
    _pid = id(pt)
    _users = []
    for _user in pt.getUsers():
        _users.append(_user)
    _np = None
    _x, _y = _calc_coords(pt, cx, cy, ra)    
    if len(_users) == 1 and _users[0] is arc:
        if _can_move(pt, objdict) and objdict.get(_pid) is not False:
            pt.setCoords(_x, _y)
        else:
            _pts = _layer.find('point', _x, _y)
            if len(_pts) == 0:
                _np = Point(_x, _y)
                _layer.addObject(_np)
            else:
                _np = _most_used(_pts)
    else:
        pt.freeUser(arc)
        _pts = _layer.find('point', _x, _y)
        if len(_pts) == 0:
            _np = Point(_x, _y)
            _layer.addObject(_np)
        else:
            _np = _most_used(_pts)
    if _np is not None:
        _np.storeUser(arc)
        if _adjust_dimensions(pt, _np):
            _layer.delObject(pt)
    if objdict.get(_pid) is not False:
        objdict[_pid] = False
    
def _rotate_arc(obj, objdict, cx, cy, ra):
    _layer = obj.getParent()
    if _layer is None:
        raise RuntimeError, "Arc parent is None"
    _cp = obj.getCenter()    
    if _cp.getParent() is not _layer:
        raise RuntimeError, "Arc/center parent object conflict!"
    _ep1, _ep2 = obj.getEndpoints()
    _pts = _layer.find('point', _ep1[0], _ep1[1])
    _ep = _used_by(obj, _pts)
    if _ep is None:
        raise RuntimeError, "Lost Arc first endpoint: " + str(_ep)
    _adjust_endpoint(obj, _ep, objdict, cx, cy, ra)
    _pts = _layer.find('point', _ep2[0], _ep2[1])
    _ep = _used_by(obj, _pts)
    if _ep is None:
        raise RuntimeError, "Lost Arc second endpoint: " + str(_ep)
    _adjust_endpoint(obj, _ep, objdict, cx, cy, ra)
    _np = _xfrm_point(_cp, objdict, cx, cy, ra)
    if _np is not None:
        obj.setCenter(_np)
        if _adjust_dimensions(_cp, _np):
            _layer.delObject(_cp)
    _da = ra/_dtr
    obj.setStartAngle(obj.getStartAngle() + _da)
    obj.setEndAngle(obj.getEndAngle() + _da)
    _pid = id(_cp)
    if objdict.get(_pid) is not False:
        objdict[_pid] = False

def _rotate_circ_ccirc(obj, objdict, cx, cy, ra):
    if isinstance(obj, Circle):
        _objtype = 'Circle'
    elif isinstance(obj, CCircle):
        _objtype = 'CCircle'
    else:
        raise TypeError, "Unexpected object type: " + `type(obj)`
    _layer = obj.getParent()
    if _layer is None:
        raise RuntimeError, "%s parent is None" % _objtype
    _cp = obj.getCenter()    
    if _cp.getParent() is not _layer:
        raise RuntimeError, "%s/center parent object conflict!" % _objtype
    _np = _xfrm_point(_cp, objdict, cx, cy, ra)
    if _np is not None:
        obj.setCenter(_np)
        if _adjust_dimensions(_cp, _np):
            _layer.delObject(_cp)
    _pid = id(_cp)
    if objdict.get(_pid) is not False:
        objdict[_pid] = False

def _rotate_seg_cline(obj, objdict, cx, cy, ra):
    if isinstance(obj, Segment):
        _p1, _p2 = obj.getEndpoints()
        _objtype = 'Segment'
    elif isinstance(obj, CLine):
        _p1, _p2 = obj.getKeypoints()
        _objtype = 'CLine'
    else:
        raise TypeError, "Unexpected object type: " + `type(obj)`
    _layer = obj.getParent()
    if _layer is None:
        raise RuntimeError, "%s parent is None" % _objtype
    if _p1.getParent() is not _layer:
        raise RuntimeError, "%s/P1 parent object conflict!" % _objtype
    if _p2.getParent() is not _layer:
        raise RuntimeError, "%s/P2 parent object conflict!" % _objtype
    _np = _xfrm_point(_p1, objdict, cx, cy, ra)
    if _np is not None:
        obj.setP1(_np)
        if _adjust_dimensions(_p1, _np):
            _layer.delObject(_p1)
    _np = _xfrm_point(_p2, objdict, cx, cy, ra)
    if _np is not None:
        obj.setP2(_np)
        if _adjust_dimensions(_p2, _np):
            _layer.delObject(_p2)
    _pid = id(_p1)
    if objdict.get(_pid) is not False:
        objdict[_pid] = False
    _pid = id(_p2)
    if objdict.get(_pid) is not False:
        objdict[_pid] = False

def _adjust_point_users(pt, objdict, da):
    _layer = pt.getParent()
    for _user in pt.getUsers():
        _uid = id(_user)
        if _uid in objdict:
            if isinstance(_user, HCLine) and _layer is not None:
                if abs(fmod(da, 180.0)) < 1e-10:
                    objdict[_uid] = False
                elif abs(fmod(da, 90.0)) < 1e-10:
                    _layer.addObject(VCLine(pt))
                    _layer.delObject(_user)
                    del objdict[_uid]
                else:
                    _layer.addObject(ACLine(pt, da))
                    _layer.delObject(_user)
                    del objdict[_uid]
            elif isinstance(_user, VCLine) and _layer is not None:
                if abs(fmod(da, 180.0)) < 1e-10:
                    objdict[_uid] = False
                elif abs(fmod(da, 90.0)) < 1e-10:
                    _layer.addObject(HCLine(pt))
                    _layer.delObject(_user)
                    del objdict[_uid]
                else:
                    _layer.addObject(ACLine(pt, da))
                    _layer.delObject(_user)
                    del objdict[_uid]
            elif isinstance(_user, ACLine) and _layer is not None:
                _user.setAngle(_user.getAngle() + da)
                objdict[_uid] = False
            else:
                if not isinstance(_user, Dimension):
                    objdict[_uid] = False
    
def rotate_objects(objs, cx, cy, angle):
    """Rotate a list of objects.

rotate_objects(objs, cx, cy, angle)

objs: A list or tuple containing the objects to move.
cx: Rotation center point 'x' coordinate
cy: Rotation center point 'y' coordinate
angle: Angular amount of rotation
    """
    if not isinstance(objs, (list, tuple)):
        raise TypeError, "Invalid object list/tuple: " + `type(objs)`
    _cx = util.get_float(cx)
    _cy = util.get_float(cy)
    _da = fmod(util.get_float(angle), 360.0)
    _ra = _da * _dtr # value in radians
    if abs(_ra) < 1e-10:
        return
    _objdict = {}
    _fillets = []
    for _obj in objs:
        if not isinstance(_obj, DimString):
            _objdict[id(_obj)] = True
    for _obj in objs:
        _oid = id(_obj)
        if _oid not in _objdict:
            continue
        if _objdict[_oid]:
            if isinstance(_obj, Point):
                _x, _y = _calc_coords(_obj, _cx, _cy, _ra)
                _obj.setCoords(_x, _y)
                _adjust_point_users(_obj, _objdict, _da)
            elif isinstance(_obj, (Segment, CLine)):
                _rotate_seg_cline(_obj, _objdict, _cx, _cy, _ra)
            elif isinstance(_obj, (Circle, CCircle)):
                _rotate_circ_ccirc(_obj, _objdict, _cx, _cy, _ra)
            elif isinstance(_obj, Arc):
                _rotate_arc(_obj, _objdict, _cx, _cy, _ra)
            elif isinstance(_obj, Leader):
                _rotate_leader(_obj, _objdict, _cx, _cy, _ra)
            elif isinstance(_obj, Polyline):
                _rotate_polyline(_obj, _objdict, _cx, _cy, _ra)
            elif isinstance(_obj, (TextBlock, Dimension)) and False:
                _obj.move(_cx, _cy)
            elif isinstance(_obj, HCLine):
                _rotate_hcline(_obj, _objdict, _cx, _cy, _ra)
            elif isinstance(_obj, VCLine):
                _rotate_vcline(_obj, _objdict, _cx, _cy, _ra)
            elif isinstance(_obj, ACLine):
                _rotate_acline(_obj, _objdict, _cx, _cy, _ra)
            elif isinstance(_obj, (Chamfer, Fillet)) and False:
                _s1, _s2 = _obj.getSegments()
                if id(_s1) not in _objdict or id(_s2) not in _objdict:
                    _layer = _obj.getParent()
                    _layer.delObject(_obj)
                if isinstance(_obj, Fillet):
                    _fillets.append(_obj)
            else:
                print "Unexpected entity type: " + `type(_obj)`
            _objdict[_oid] = False
        for _obj in _fillets:
            _obj._calculateCenter() # FIXME
