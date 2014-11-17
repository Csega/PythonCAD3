#!/usr/bin/env python
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
# This  module PROVIDE ALL GLOBAL VARIABLE NEEDE TO THE SCENE
#
from Interface.Entity.point     import Point
from Interface.Entity.segment   import Segment
from Interface.Entity.arc       import Arc
from Interface.Entity.text      import Text
from Interface.Entity.ellipse   import Ellipse
from Interface.Entity.polyline  import Polyline

from PyQt4 import QtCore

from Interface.Command.distance2point import Distance2Point

SCENE_SUPPORTED_TYPE=["SEGMENT",
                      "POINT", 
                        "ARC",
                        "TEXT", 
                        "ELLIPSE", 
                        "POLYLINE"]

SCANE_OBJECT_TYPE=dict(zip(SCENE_SUPPORTED_TYPE, 
                       (
                        Segment, 
                        Point, 
                        Arc, 
                        Text, 
                        Ellipse, 
                        Polyline
                       )))

INTERFACE_COMMAND={'DISTANCE2POINT':Distance2Point}

RESTART_COMMAND_OPTION=True

BACKGROUND_COLOR=(255, 255, 255)

KEY_MAP={
         QtCore.Qt.Key_Delete:'DELETE', 
         QtCore.Qt.Key_L:'SEGMENT', 
         QtCore.Qt.Key_P:'POLYLINE', 
         QtCore.Qt.Key_G:'MOVE', 
         QtCore.Qt.Key_C:'COPY', 
         QtCore.Qt.Key_D:'DELETE', 
         QtCore.Qt.Key_R:'ROTATE', 
         QtCore.Qt.Key_M:'MIRROR'
         }
