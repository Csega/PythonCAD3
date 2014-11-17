#
# Copyright (c) 2002, 2003, 2004, 2005 Art Haas
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
# hatching code
#

import math

from PythonCAD.Generic.Kernel.Entity.point import Point
from PythonCAD.Generic.Kernel.Entity import Segment
from PythonCAD.Generic.Kernel.Entity import Circle
from PythonCAD.Generic.Kernel.Entity import Arc
from PythonCAD.Generic.Kernel.Entity import Segjoint
from PythonCAD.Generic.Kernel.Entity import Layer
from PythonCAD.Generic.Kernel.Entity.util import *
from PythonCAD.Generic.Kernel.Entity.geometricalentity  import *

class Path(geometricalentity):
    """
        The class for maintaining a list of objects defining a hatch border.
        A Path object contains one or more objects defining the boundary
        of a hatching. If the Path length is 1, the boundary is either a
        circle or an arc where the start angle and end angle are equal.
        There is no upper limit to the number of objects in the path.
        If a Path consists of Segments, Arcs, Chamfer, or Fillets, the
        Path can only be valid if starting at any point in any object
        in the Path the connections between the objects lead back to the
        starting point.
    """
    def __init__(self, objs):
        """
            Initialize a Path.
            The required argument 'objs' is a list of objects defining
            the path. The valid objects are circles, arcs, segments,
            chamfers and fillets.
        """
        if not isinstance(objs, list):
            raise TypeError, "Unexpected list type: " + `type(objs)`
        if not len(objs):
            raise ValueError, "Invalid empty object list"
        if len(objs) == 1:
            _circular = True
            _obj = objs[0]
            if isinstance(_obj, arc.Arc):
                _sa = _obj.getStartAngle()
                _ea = _obj.getEndAngle()
                if not abs(_sa - _ea) < 1e-10:
                    raise ValueError, "Invalid single Arc path: " + str(_obj)
            elif isinstance(_obj, circle.Circle):
                self.__objs = objs[:]
                return
            else:
                raise TypeError, "Invalid single entity path: " + str(_obj)
        for _obj in objs:
            if not (isinstance(_obj, segment.Segment) or
                    isinstance(_obj, arc.Arc) or
                    isistance(_obj, segjoint.Chamfer) or
                    isinstance(_obj, segjoint.Fillet)):
                raise TypeError, "Invalid object type in list: " + `type(_obj)`
        if pathIsClosed(objs):
            self.__objs = objs[:]
        else:
            raise ValueError, "Array List mast be a closef path"

    def __len__(self):
        return len(self.__objs)

    def __str__(self):
        print "Element Path are: ["
        for _obj in self.__objs:
            print str(_obj)
        print "]"

    def isCircular(self):
        """
            Test if the Path is a Circle or closed Arc.
        """
        if len(self.__objs)==1:
            if isistance(self.__objs,(arc.Arc,circle.Circle)):
                return True
        return False
    def getPath(self):
        """
            Return the objects defining the Path.
            This method returns a list of objects.
        """
        return self.__objs[:]

    def inPath(self, x, y):
        """
            Test if a coordinate pair are inside a Path.
            This method has two required arguments:
            This method returns True if the Point is inside the
            Path, and False otherwise.
        """
        _x = util.get_float(x)
        _y = util.get_float(y)
        _inside = False
        if self.__circular:
            assert len(self.__objs) == 1, "Invalid circular path length"
            _circ = self.__objs[0]
            _cx, _cy = _circ.getCenter().getCoords()
            _sep = math.hypot((_cx - _x), (_cy - _y))
            if _sep < _circ.getRadius():
                _inside = True
        else:
            _xp = 0.0
            _yp = 0.0
            _idx = None
            for _i in range(len(self.__objs)):
                _obj = self.__objs[_i]
                if isinstance(_obj, segment.Segment):
                    _p1, _p2 = _obj.getEndpoints()
                    _p1x, _p1y = _p1.getCoords()
                    _p2x, _p2y = _p2.getCoords()
                elif isinstance(_obj, arc.Arc):
                    _ep1, _ep2 = _obj.getEndpoints()
                    _p1x, _p1y = _ep1
                    _p2x, _p2y = _ep2
                elif isinstance(_obj, (segjoint.Chamfer, segjoint.Fillet)):
                    _p1, _p2 = _obj.getMovingPoints()
                    _p1x, _p1y = _p1.getCoords()
                    _p2x, _p2y = _p2.getCoords()
                _xdiff = _p2x - _p1x
                _ydiff = _p2y - _p1y
                _sqlen = pow(_xdiff, 2) + pow(_ydiff, 2)
                _r = ((_x - _p1x)*(_xdiff) + (_y - _p1y)*(_ydiff))/_sqlen
                if 0.0 < _r < 1.0:
                    _s = ((_p1y - _y)*(_xdiff) - (_p1x - _x)*(_ydiff))/_sqlen
                    if abs(_s) > 1e-10:
                        _xp = _p1x + (_r * _xdiff)
                        _yp = _p1y + (_r * _ydiff)
                        _idx = _i
                        break
            if _idx is not None:
                _count = 1
                for _i in range(len(self.__objs)):
                    if _i == _idx:
                        continue
                    _obj = self.__objs[_i]
                    if isinstance(_obj, segment.Segment):
                        _p1, _p2 = _obj.getEndpoints()
                        _p1x, _p1y = _p1.getCoords()
                        _p2x, _p2y = _p2.getCoords()
                    elif isinstance(_obj, arc.Arc):
                        _ep1, _ep2 = _obj.getEndpoints()
                        _p1x, _p1y = _ep1
                        _p2x, _p2y = _ep2
                    elif isinstance(_obj, (segjoint.Chamfer, segjoint.Fillet)):
                        _p1, _p2 = _obj.getMovingPoints()
                        _p1x, _p1y = _p1.getCoords()
                        _p2x, _p2y = _p2.getCoords()
                    _d = ((_p2x - _p1x)*(_yp - _y)) - ((_p2y - _p1y)*(_xp - _x))
                    if abs(_d) > 1e-10:
                        _n = ((_p1y - _y)*(_xp - _x)) - ((_p1x - _x)*(_yp - _y))
                        _r = _n/_d
                        if 0.0 < _r < 1.0:
                            _count = _count + 1
                if _count % 2: # need to test if point is in an arc ...
                    _inside = True
        return _inside

class HatchRegion(object):
    """The class defining a hatched area.

A HatchRegion object consists of one Path object defining
the external boundary of the hatching, and a list of zero
or more Paths defining any areas inside the enclosing Path
that are not hatched.
    """
    def __init__(self, extpath, voids=[]):
        """
            Initialize a HatchRegion.
            The required argument 'extpath' is a Path object defining
            the external boundary of the hatching. The optional argument
            'voids' is a list of Path objects defining areas within the
            external Path that are not to be hatched.
        """
        if not isinstance(extpath, Path):
            raise TypeError, "Invalid external path: " + `extpath`
        if not extpath.isExternal():
            raise ValueError, "Path not defined to be an external path: " + `extpath`
        if not isinstance(voids, list):
            raise TypeError, "Invalid void list: " + `voids`
        for _void in voids:
            if not isinstance(_void, Path):
                raise TypeError, "Invalid path in void list: " + `_void`
            if _void.isExternal():
                raise ValueError, "Void area defined as external: " + `_void`
        self.__ext_path = extpath
        self.__voids = voids[:]

    def getExternalPath(self):
        """
            Return the external Path for the HatchRegion.
        """
        return self.__ext_path

    def hasVoids(self):
        """
            Test if the HatchRegion has any internal non-hatched areas.
        """
        return len(self.__voids) > 0

    def getVoids(self):
        """
            Get any internal areas in the HatchRegion.
        """
        return self.__voids[:]

def _seg_seg_touch(sega, segb):
    _touch = False
    _pa1, _pa2 = sega.getEndpoints()
    _pb1, _pb2 = segb.getEndpoints()
    if _pa1 is _pb1 or _pa1 is _pb2 or _pa2 is _pb1 or _pa2 is _pb2:
        _touch = True
    return _touch

def _seg_arc_touch(seg, a):
    _touch = False
    _p1, _p2 = seg.getEndpoints()
    _ep1, _ep2 = a.getEndpoints()
    if _p1 == _ep1 or _p1 == _ep2 or _p2 == _ep1 or _p2 == _ep2:
        _touch = True
    return _touch

def _arc_arc_touch(arca, arcb):
    _touch = False
    _aep1, _aep2 = arca.getEndpoints()
    _bep1, _bep2 = arcb.getEndpoints()
    if _aep1 == _bep1 or _aep1 == _bep2 or _aep2 == _bep1 or _aep2 == _bep2:
        _touch = True
    return _touch

def _seg_joint_touch(seg, joint):
    _touch = False
    _s1, _s2 = joint.getSegments()
    if _s1 is seg or _s2 is seg:
        _touch = True
    return _touch

def _old_validate_path(objlist):
    """
        Test if the objects in the objlist make a closed path.
        This function is private the the hatching code.
    """
    if not isinstance(objlist, list):
        raise TypeError, "Invalid object list: " + `objlist`
    _startpt = None
    _nextpt = None
    _valid = False
    for _obj in objlist:
        print "testing object: " + `_obj`
        print "start: " + `_startpt`
        print "next: " + `_nextpt`
        if isinstance(_obj, segment.Segment):
            _p1, _p2 = _obj.getEndpoints()
            if _startpt is None:
                _startpt = _p1
                _nextpt = _p2
            else:
                if _nextpt == _p1:
                    _nextpt = _p2
                elif _nextpt == _p2:
                    _nextpt = _p1
                else:
                    break
        elif isinstance(_obj, arc.Arc):
            _ep1, _ep2 = _obj.getEndpoints()
            if _startpt is None:
                _startpt = _ep1
                _nextpt = _ep2
            else:
                if _nextpt == _ep1:
                    _nextpt = _ep2
                elif _startpt == _ep2:
                    _nextpt = _ep1
                else:
                    break
        elif isinstance(_obj, (segjoint.Chamfer, segjoint.Fillet)):
            _p1, _p2 = _obj.getMovingPoints()
            if _startpt is None:
                _startpt = _p1
                _nextpt = _p2
            else:
                if _nextpt == _p1:
                    _nextpt = _p2
                elif _nextpt == _p2:
                    _nextpt = _p1
                else:
                    break
        else:
            raise TypeError, "Invalid object in path: " + `_obj`
    if _startpt == _nextpt:
        _valid = True
    return _valid

def _can_touch(obja, objb):
    _touch = False
    if isinstance(obja, segment.Segment):
        if isinstance(objb, segment.Segment):
            _touch = _seg_seg_touch(obja, objb)
        elif isinstance(objb, arc.Arc):
            _touch = _seg_arc_touch(obja, objb)
        elif isinstance(objb, segjoint.SegJoint):
            _touch = _seg_joint_touch(obja, objb)
    elif isinstance(obja, arc.Arc):
        if isinstance(objb, segment.Segment):
            _touch = _seg_arc_touch(objb, obja)
        elif isinstance(objb, arc.Arc):
            _touch = _arc_arc_touch(obja, objb)
    elif isinstance(obja, segjoint.SegJoint):
        if isinstance(objb, segment.Segment):
            _touch = _seg_joint_touch(objb, obja)
    return _touch

def _validate_path(lyr, objlist):
    """
        Test if the objects in the objlist make a closed path.
        This function is private the the hatching code.
    """
    if not isinstance(objlist, list):
        raise TypeError, "Invalid object list: " + `objlist`
    for _obj in objlist:
        _lobj = lyr.findObject(_obj)
        if _lobj is not _obj:
            raise ValueError, "Object not in layer: " + `_obj`
    _valid = True
    for _i in range(len(objlist) - 1):
        _obja = objlist[_i]
        _objb = objlist[_i+1]
        if not _can_touch(_obja, _objb):
            _valid = False
            break
    if _valid:
        _valid = _can_touch(objlist[0], objlist[-1])
    return _valid

def point_boundaries(plist):
    _xmin = None
    _xmax = None
    _ymin = None
    _ymax = None
    _set = False
    if len(plist) > 1:
        for _pt in plist:
            _x, _y = _pt.getCoords()
            if not _set:
                _xmin = _x
                _xmax = _x
                _ymin = _y
                _ymax = _y
            else:
                if _x < _xmin:
                    _xmin = _x
                if _x > _xmax:
                    _xmax = _x
                if _y < _ymin:
                    _ymin = _y
                if _y > _ymax:
                    _ymax = _y
    return (_xmin, _ymin, _xmax, _ymax)

def point_in_path(path):
    hits = 0
    for seg in path:
        p1, p2 = seg.getEndpoints()
        p1x, p1y = p1.getEndpoints()
        p2x, p2y = p2.getEndpoints()
        xmin = min(p1x, p2x)
        xmax = max(p1x, p2x)
        ymin = min(p1y, p2y)
        ymax = max(p1y, p2y)
        # if hx < xmin or hx > max or hy > ymax:
            # continue
        hits = 1 - hits
    return hits

def draw_path(path):
    if len(path):
        print "path: ["
        for seg in path:
            print seg
        print "]"

def make_paths(pt, seg, sdict):
    paths = []
    print "initial segment: " + str(seg)
    sp1, sp2 = seg.getEndpoints()
    if pt is sp1:
        sp = sp1
    else:
        sp = sp2
    print "start point: " + str(sp)
    segkeys = {}
    path = []
    segkeys[seg] = pt
    path.append(seg)
    draw_path(path)
    paths.append(path)
    while(len(paths)):
        path = paths.pop()
        draw_path(path)
        seg = path[-1]
        print "path final segment: " + str(seg)
        # print "segkey: " + str(segkeys[seg])
        p1, p2 = seg.getEndpoints()
        print "p1: " + str(p1)
        if p1 in sdict and segkeys[seg] is not p1:
            if p1 is sp:
                print "complete path:"
                draw_path(path)
            else:
                for p1seg in sdict[p1]:
                    if p1seg not in path:
                        segkeys[p1seg] = p1
                        path.append(p1seg)
                        # print "new path:"
                        draw_path(path)
                        paths.append(path)
        print "p2: " + str(p2)
        if p2 in sdict and segkeys[seg] is not p2:
            if p2 is sp:
                print "complete path:"
                draw_path(path)
            else:
                for p2seg in sdict[p2]:
                    if p2seg not in path:
                        segkeys[p2seg] = p2
                        path.append(p2seg)
                        # print "new_path:"
                        draw_path(path)
                        paths.append(path)


def check_clist(ct, clist):
    xct, yct = ct.getCenter().getCoords()
    rct = ct.getRadius()
    add_flag = True
    i = 0
    while (i < len(clist)):
        _c = clist[i]
        x, y = _c.getCenter().getCoords()
        r = _c.getRadius()
        sep = math.hypot((xct - x), (yct - y))
        if sep < r: # ct center point inside _c
            if sep + rct < r:
                add_flag = False
            else:
                i = i + 1
        elif sep < rct: # _c center point inside ct
            if sep + r < rct:
                del clist[i]
            else:
                i = i + 1
        else: # two circle that may or may not overlap
            i = i + 1
        if not add_flag:
            break
    return add_flag

def get_contained_circles(l, c):
    clist = []
    xc, yc = c.getCenter().getCoords()
    rc = c.getRadius()
    for _cir in l.getLayerEntities("circle"):
        if _cir is c:
            continue
        x, y = _cir.getCenter().getCoords()
        r = _cir.getCoords()
        sep = math.hypot((xc - x), (yc - y))
        if sep + r < rc:
            if(check_clist(_cir, clist)):
                clist.append(_cir)
    return clist

def make_hatch_area(lyr, x, y):
    _x = util.get_float(x)
    _y = util.get_float(y)
    if not isinstance(lyr, layer.Layer):
        raise TypeError, "Invalid layer: " + `lyr`
    #
    # see if we're in a circle
    #
    _circle = None
    for _c in lyr.getLayerEntities("circle"):
        _xc, _yc = _c.getCenter().getCoords()
        _r = _c.getRadius()
        _sep = math.hypot((_xc - _x), (_yc - _y))
        if _sep < _r:
            if _circle is None:
                _circle = _c
            else:
                _rc = _circle.getRadius()
                if _r < _rc:
                    _circle = _c
    #
    # get the eligible points in the layer and
    # store any circles that may be fully inside
    # the bounding circle
    #
    _pts = {}
    _circle_voids = []
    if _circle is not None:
        _cx, _cy = _circle.getCenter().getCoords()
        _rad = _circle.getRadius()
        _xmin = _cx - _rad
        _ymin = _cy - _rad
        _xmax = _cx + _rad
        _ymax = _cy + _rad
        for _pt in lyr.getLayerEntities("point"):
            _x, _y = _pt.getCoords()
            if _x < _xmin or _y < _ymin or _y > _ymax:
                continue
            if _x > _xmax:
                break
            _sep = math.hypot((_cx - _x), (_cy - _y))
            if _sep < _rad:
                _addpt = True
                if lyr.countUsers(_pt) == 1:
                    _obj = lyr.usesObject(_pt)
                    if not isinstance(_obj, circle.Circle):
                        _addpt = False
                if _addpt:
                    _pts[_pt] = True
        for _circ in lyr.getLayerEntities("circle"):
            if _circ is _circle:
                continue
            _tcx, _tcy = _circ.getCenter().getCoords()
            _tr = _circ.getRadius()
            if (_tcx + _tr) > _xmax:
                break
            if ((_tcx - _tr) < _xmin or
                (_tcy - _tr) < _ymin or
                (_tcy + _tr) > _ymax):
                continue
            _sepmax = math.hypot((_cx - _tcx), (_cy - _tcy)) + _tr
            if _sepmax < _rad:
                _circle_voids.append(_circ)
    else:
        for _pt in lyr.getLayerEntities("point"):
            _addpt = True
            if lyr.countUsers(_pt) == 1:
                _obj = lyr.usesObject(_pt)
                if not isinstance(_obj, circle.Circle):
                    _addpt = False
            if _addpt:
                _pts[_pt] = True
    #
    # find the entites that can make closed paths
    #
    _objs = {}
    for _pt in _pts:
        for _user in lyr.usesObject(_pt):
            if isinstance(_user, (segment.Segment, arc.Arc,
                                  segjoint.Chamfer, segjoint.Fillet)):
                _objs[_user] = True
                if isinstance(_user, segment.Segment):
                    for _seguser in lyr.usesObject(_user):
                        _objs[_seguser] = True
    _paths = {}
    for _obj in _objs:
        _p1 = None
        _p2 = None
        if isinstance(_obj, segment.Segment):
            if _obj not in _paths:
                _paths[_obj] = []
            for _user in lyr.usesObject(_obj):
                if isinstance(_user, (segjoint.Chamfer, segjoint.Fillet)):
                    _paths[_obj].append(_user)
            _p1, _p2 = _obj.getEndpoints()
        elif isinstance(_obj, arc.Arc):
            _ep1, _ep2 = _obj.getEndpoints()
            for _pt in _pts:
                if _pt == _ep1:
                    _p1 = _pt
                elif _p2 == _ep2:
                    _p2 = _pt
                if _p1 is not None and _p2 is not None:
                    break
            if _p1 is None or _p2 is None:
                continue # only one arc endpoint in list
        else:
            _s1, _s2 = _obj.getSegments()
            if _obj not in _paths:
                _paths[_obj] = []
            _paths[_obj].append(_s1)
            _paths[_obj].append(_s2)
        if _p1 is not None:
            for _user in lyr.usesObject(_p1):
                if _user is not _obj:
                    if isinstance(_user, (segment.Segment, arc.Arc)):
                        _paths[_obj].append(_user)
        if _p2 is not None:
            for _user in lyr.usesObject(_p2):
                if _user is not _obj:
                    if isinstance(_user, (segment.Segment, arc.Arc)):
                        _paths[_obj].append(_user)
    #
    # remove any object that doesn't connect to another object
    #
    _objlist = _paths.keys()
    for _obj in _objlist:
        if len(_paths[_obj]) < 1:
            del _paths[_obj]
    #
    # try to make paths from the selected objects
    #
    _routes = {}
    _objlist = _paths.keys()
    _objcount = len(_objlist)
    for _obj in _objlist:
        _objpaths = []
        _path = [_obj]
        for _fullpath in _make_paths(_paths, _objcount, _obj, _path):
            print "path: " + str(_fullpath)
            _valid = _validate_path(lyr, _fullpath)
            if _valid:
                _objpaths.append(_fullpath)
            else:
                print "invalid path"
        _routes[_obj] = _objpaths

def _make_paths(pathdict, maxlen, tail, path):
    _paths = []
    _pathlen = len(path)
    _head = None
    if _pathlen <= maxlen and tail in pathdict:
        if _pathlen:
            _head = path[0]
        for _next in pathdict[tail]:
            if _next is _head:
                _good = True
                if _pathlen == 2:
                    if (isinstance(path[0], segment.Segment) and
                        isinstance(path[1], segment.Segment)):
                        _good = False
                if _good:
                    _paths.append(path)
            elif _next not in path:
                _path = path + [_next]
                for _newpath in _make_paths(pathdict, maxlen, _next, _path):
                    _paths.append(_newpath)
            else:
                pass
    return _paths

hpx = 3.0
hpy = 4.0

def hatchtests():
    p1 = point.Point(0,0)
    p2 = point.Point(10,0)
    p3 = point.Point(10,10)
    p4 = point.Point(0,10)
    s1 = segment.Segment(p1,p2)
    s2 = segment.Segment(p2,p3)
    s3 = segment.Segment(p3,p4)
    s4 = segment.Segment(p4,p1)
    l1 = layer.Layer('foo')
    l1.addObject(p1)
    l1.addObject(p2)
    l1.addObject(p3)
    l1.addObject(p4)
    l1.addObject(s1)
    l1.addObject(s2)
    l1.addObject(s3)
    l1.addObject(s4)
    # find_hatched_area(l1, hpx, hpy)
    p5 = point.Point(2.95, 3.95)
    l1.addObject(p5)
    c1 = circle.Circle(p5, 1)
    l1.addObject(c1)
    # find_hatched_area(l1, hpx, hpy)

if __name__ == '__main__':
    hatchtests()
