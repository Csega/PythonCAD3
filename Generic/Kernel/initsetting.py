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
# This  module provide all the global variable to be used from the pythoncad Application
#
#
# Command List
#
from Kernel.Command import *
from Kernel.Command.segmentcommand import SegmentCommand
from Kernel.Command.arccommand import ArcCommand
from Kernel.Command.pointcommand import PointCommand
from Kernel.Command.ellipsecommand import EllipseCommand
from Kernel.Command.polylinecommand import PolylineCommand
#from Kernel.Command.aclinecommand import ACLineCommand
from Kernel.Command.ccirclecommand import CCircleCommand
from Kernel.Command.textcommand import TextCommand
from Kernel.Command.chamfercommand import ChamferCommand
from Kernel.Command.filletcommand import FilletCommand
from Kernel.Command.bisectorcommand import BisectorCommand
from Kernel.Command.rectanglecommand import RectangleCommand
from Kernel.Command.polygoncommand import PolygonCommand
from Kernel.Command.copycommand import CopyCommand
from Kernel.Command.movecommand import MoveCommand
from Kernel.Command.mirrorcommand import MirrorCommand
from Kernel.Command.rotatecommand import RotateCommand
from Kernel.Command.trimcommand import TrimCommand
from Kernel.Command.deletecommand import DeleteCommand
#
# Entity List
#
from Kernel.GeoEntity.point import Point 
from Kernel.GeoEntity.segment import Segment 
from Kernel.GeoEntity.arc import Arc
from Kernel.GeoEntity.ellipse import Ellipse
from Kernel.GeoEntity.polyline import Polyline
from Kernel.GeoEntity.style import Style 
from Kernel.GeoEntity.cline import CLine
from Kernel.GeoEntity.ccircle import CCircle
from Kernel.GeoEntity.text import Text

from Kernel.GeoComposedEntity.chamfer import Chamfer
from Kernel.GeoComposedEntity.fillet import Fillet
from Kernel.GeoComposedEntity.bisector import Bisector
#
# db Ent
#
from Kernel.settings import *
from Kernel.entity import Entity
from Kernel.layer import Layer
from Kernel.composedentity import ComposedEntity
#
# Default LAyer
# 
MAIN_LAYER="MAIN"
#
# Max Number of recent file 
#
MAX_RECENT_FILE=5
#
# Object workflow state of the entity
#
OBJECT_STATE=['MODIFIE','RELEASED', 'DELETE']
#
# Supported entity by the Application
#
PY_CAD_ENT=['POINT',
            'SEGMENT',
            'SETTINGS',
            'LAYER',
            'STYLE', 
            'ARC', 
            'ELLIPSE', 
            'POLYLINE', 
            'CLINE', 
            'CCIRCLE', 
            'TEXT', 
            'COMPOSED_ENTITY' ]

PY_CAD_COMPOSED_ENT=['CHAMFER', 'FILLET', 'BISECTOR']
#
# Command Supported by the application
#
APPLICATION_COMMAND={'SEGMENT':SegmentCommand,
                        'ARC':ArcCommand,
                        'POINT':PointCommand,
                        'ELLIPSE':EllipseCommand,
                        'POLYLINE':PolylineCommand, 
#                        'CLINE':ACLineCommand, 
                        'CCIRCLE':CCircleCommand, 
                        'TEXT':TextCommand, 
                        'CHAMFER':ChamferCommand, 
                        'FILLET':FilletCommand, 
                        'BISECTOR':BisectorCommand, 
                        'RECTANGLE':RectangleCommand, 
                        'POLYGON':PolygonCommand, 
                        'COPY':CopyCommand, 
                        'MOVE':MoveCommand, 
                        'MIRROR':MirrorCommand, 
                        'ROTATE':RotateCommand, 
                        'TRIM':TrimCommand, 
                        'DELETE':DeleteCommand}
#
# Match object Name
#
DRAWIN_ENTITY={ Point:'POINT',
                Segment:'SEGMENT',
                Arc:'ARC', 
                Ellipse:'ELLIPSE', 
                Polyline:'POLYLINE', 
                CLine:'CLINE', 
                CCircle:'CCIRCLE', 
                Text:'TEXT', 
                ComposedEntity:'COMPOSED_ENTITY'}
                
DRAWIN_COMPOSED_ENTITY={Fillet:'FILLET', 
                        Chamfer:'CHAMFER', 
                        Bisector:'BISECTOR'}



KERNEL_ENTITY=(Style,Entity,Settings,Layer)
#
# Entity supported by the kernel
#
SUPPORTED_ENTITYS=KERNEL_ENTITY+tuple(DRAWIN_ENTITY.keys())+(ComposedEntity, )


PYTHONCAD_COLOR={
    'aliceblue'             :(240,248,255),
    'antiquewhite'          :(250,235,215),
    'aqua'                  :(0,255,255),
    'aquamarine'            :(127,255,212),
    'azure'                 :(240,255,255),
    'beige'                 :(245,245,220),
    'bisque'                :(255,228,196),
    'black'                 :(0,0,0),
    'blanchedalmond'        :(255,235,205),
    'blue'                  :(0,0,255),
    'blueviolet'            :(138,43,226),
    'brown'                 :(165,42,42),
    'burlywood'             :(222,184,135),
    'cadetblue'             :(95,158,160),
    'chartreuse'            :(127,255,0),
    'chocolate'             :(210,105,30),
    'coral'                 :(255,127,80),
    'cornflowerblue'        :(100,149,237),
    'cornsilk'              :(255,248,220),
    'crimson'               :(220,20,60),
    'cyan'                  :(0,255,255),
    'darkblue'              :(0,0,139),
    'darkcyan'              :(0,139,139),
    'darkgoldenrod'         :(184,134,11),
    'darkgray'              :(169,169,169),
    'darkgreen'             :(0,100,0),
    'darkgrey'              :(169,169,169),
    'darkkhaki'             :(189,183,107),
    'darkmagenta'           :(139,0,139),
    'darkolivegreen'        :(85,107,47),
    'darkorange'            :(255,140,0),
    'darkorchid'            :(153,50,204),
    'darkred'               :(139,0,0),
    'darksalmon'            :(233,150,122),
    'darkseagreen'          :(143,188,143),
    'darkslateblue'         :(72,61,139),
    'darkslategray'         :(47,79,79),
    'darkslategrey'         :(47,79,79),
    'darkturquoise'         :(0,206,209),
    'darkviolet'            :(148,0,211),
    'deeppink'              :(255,20,147),
    'deepskyblue'           :(0,191,255),
    'dimgray'               :(105,105,105),
    'dimgrey'               :(105,105,105),
    'dodgerblue'            :(30,144,255),
    'firebrick'             :(178,340,34),
    'floralwhite'           :(255,250,240),
    'forestgreen'           :(34,139,34),
    'fuchsia'               :(255,0,255),
    'gainsboro'             :(220,220,220),
    'ghostwhite'            :(248,248,255),
    'gold'                  :(255,215,0),
    'goldenrod'             :(218,165,32),
    'gray'                  :(128,128,128),
    'green'                 :(0,128,0),
    'greenyellow'           :(173,255,47),
    'honeydew'              :(240,255,240),
    'hotpink'               :(255,105,180),
    'indianred'             :(205,920,92),
    'indigo'                :(75,0,130),
    'ivory'                 :(255,255,240),
    'khaki'                 :(240,230,140),
    'lavender'              :(230,230,250),
    'lavenderblush'         :(255,240,245),
    'lawngreen'             :(124,252,0),
    'lemonchiffon'          :(255,250,205),
    'lightblue'             :(173,216,230),
    'lightcoral'            :(240,128,128),
    'lightcyan'             :(224,255,255),
    'lightgoldenrodyellow'  :(250,250,210),
    'lightgray'             :(211,211,211),
    'lightgreen'            :(144,238,144),
    'lightgrey'             :(211,211,211),
    'lightpink'             :(255,182,193),
    'lightsalmon'           :(255,160,122),
    'lightseagreen'         :(32,178,170),
    'lightskyblue'          :(135,206,250),
    'lightslategray'        :(119,136,153),
    'lightslategrey'        :(119,136,153),
    'lightsteelblue'        :(176,196,222),
    'lightyellow'           :(255,255,224),
    'lime'                  :(0,255,0),
    'limegreen'             :(50,205,50),
    'linen'                 :(250,240,230),
    'magenta'               :(255,0,255),
    'maroon'                :(128,0,0),
    'mediumaquamarine'      :(102,205,170),
    'mediumblue'            :(0,0,205),
    'mediumorchid'          :(186,85,211),
    'mediumpurple'          :(147,112,219),
    'mediumseagreen'        :(60,179,113),
    'mediumslateblue'       :(123,104,238),
    'mediumspringgreen'     :(0,250,154),
    'mediumturquoise'       :(72,209,204),
    'mediumvioletred'       :(199,21,133),
    'midnightblue'          :(25,25,112),
    'mintcream'             :(245,255,250),
    'mistyrose'             :(255,228,225),
    'moccasin'              :(255,228,181),
    'navajowhite'           :(255,222,173),
    'navy'                  :(0,0,128),
    'oldlace'               :(253,245,230),
    'olive'                 :(128,128,0),
    'olivedrab'             :(107,142,35),
    'orange'                :(255,165,0),
    'orangered'             :(255,69,0),
    'orchid'                :(218,112,214),
    'palegoldenrod'         :(238,232,170),
    'palegreen'             :(152,251,152),
    'paleturquoise'         :(175,238,238),
    'palevioletred'         :(219,112,147),
    'papayawhip'            :(255,239,213),
    'peachpuff'             :(255,218,185),
    'peru'                  :(205,133,63),
    'pink'                  :(255,192,203),
    'plum'                  :(221,160,221),
    'powderblue'            :(176,224,230),
    'purple'                :(128,0,128),
    'red'                   :(255,0,0),
    'rosybrown'             :(188,143,143),
    'royalblue'             :(65,105,225),
    'saddlebrown'           :(139,69,19),
    'salmon'                :(250,128,114),
    'sandybrown'            :(244,164,96),
    'seagreen'              :(46,139,87),
    'seashell'              :(255,245,238),
    'sienna'                :(160,82,45),
    'silver'                :(192,192,192),
    'skyblue'               :(135,206,235),
    'slateblue'             :(106,90,205),
    'slategray'             :(112,128,144),
    'slategrey'             :(112,128,144),
    'snow'                  :(255,250,250),
    'springgreen'           :(0,255,127),
    'steelblue'             :(70,130,180),
    'tan'                   :(210,180,140),
    'teal'                  :(0,128,128),
    'thistle'               :(216,191,216),
    'tomato'                :(255,99,71),
    'turquoise'             :(64,224,208),
    'violet'                :(238,130,238),
    'wheat'                 :(245,222,179),
    'white'                 :(255,255,255),
    'whitesmok'             :(255,255,0),
    'yellowgreen'           :(154,205,50)}

PYTHONCAD_HIGLITGT_COLOR=PYTHONCAD_COLOR['tomato']
PYTHONCAD_PREVIEW_COLOR=PYTHONCAD_COLOR['steelblue']

PYTHONCAD_LINETYPE={
    'continue':             (1),
    'dash':                 (10, 10), 
    'central':              (10, 8, 1, 8)}
    
PYTHONCAD_STYLE_ATTRIBUTES=['entity_color',
                            'entity_linetype', 
                            'entity_tichness',
                            'text_font', 
                            'text_haigt',
                            'text_aling', 
                            'text_aline_to_point']
                            
PYTHONCAD_STYLE_DEFAULT_VALUE=[(0, 0, 0),
                                '1', 
                                '1',
                                'arial', 
                                '10',
                                'left'
                                'sw']

def getDefaultStyle():
    return dict(zip(PYTHONCAD_STYLE_ATTRIBUTES,PYTHONCAD_STYLE_DEFAULT_VALUE))
#
# Snap init settings
#
global SNAP_POINT_ARRAY
global ACTIVE_SNAP_POINT

SNAP_POINT_ARRAY={'ALL':0, 
                    'END':1,
                    'MID':2, 
                    'ORTO':3, 
                    'TANGENT':4, 
                    'CENTER':5,
                    'QUADRANT':6,
                    'ORIG':7, 
                    'INTERSECTION':8  
                    }

ACTIVE_SNAP_POINT=SNAP_POINT_ARRAY["ALL"]

#
# Color table to define a match from Autocad external format and Pythoncad internal format
#
cgcol = {
'#000000':0, 0:'#000000',
'#ff0000':1, 1:'#ff0000',
'#ffff00':2, 2:'#ffff00',
'#00ff00':3, 3:'#00ff00',
'#00ffff':4, 4:'#00ffff',
'#0000ff':5, 5:'#0000ff',
'#ff00ff':6, 6:'#ff00ff',
'#ffffff':7, 7:'#ffffff',
'#414141':8, 8:'#414141',
'#808080':9, 9:'#808080',
'#ff0000':10, 10:'#ff0000',
'#ffaaaa':11, 11:'#ffaaaa',
'#bd0000':12, 12:'#bd0000',
'#bd7e7e':13, 13:'#bd7e7e',
'#810000':14, 14:'#810000',
'#815656':15, 15:'#815656',
'#680000':16, 16:'#680000',
'#684545':17, 17:'#684545',
'#4f0000':18, 18:'#4f0000',
'#4f3535':19, 19:'#4f3535',
'#ff3f00':20, 20:'#ff3f00',
'#ffbfaa':21, 21:'#ffbfaa',
'#bd2e00':22, 22:'#bd2e00',
'#bd8d7e':23, 23:'#bd8d7e',
'#811f00':24, 24:'#811f00',
'#816056':25, 25:'#816056',
'#681900':26, 26:'#681900',
'#684e45':27, 27:'#684e45',
'#4f1300':28, 28:'#4f1300',
'#4f3b35':29, 29:'#4f3b35',
'#ff7f00':30, 30:'#ff7f00',
'#ffd4aa':31, 31:'#ffd4aa',
'#bd5e00':32, 32:'#bd5e00',
'#bd9d7e':33, 33:'#bd9d7e',
'#814000':34, 34:'#814000',
'#816b56':35, 35:'#816b56',
'#683400':36, 36:'#683400',
'#685645':37, 37:'#685645',
'#4f2700':38, 38:'#4f2700',
'#4f4235':39, 39:'#4f4235',
'#ffbf00':40, 40:'#ffbf00',
'#ffeaaa':41, 41:'#ffeaaa',
'#bd8d00':42, 42:'#bd8d00',
'#bdad7e':43, 43:'#bdad7e',
'#816000':44, 44:'#816000',
'#817656':45, 45:'#817656',
'#684e00':46, 46:'#684e00',
'#685f45':47, 47:'#685f45',
'#4f3b00':48, 48:'#4f3b00',
'#4f4935':49, 49:'#4f4935',
'#ffff00':50, 50:'#ffff00',
'#ffffaa':51, 51:'#ffffaa',
'#bdbd00':52, 52:'#bdbd00',
'#bdbd7e':53, 53:'#bdbd7e',
'#818100':54, 54:'#818100',
'#818156':55, 55:'#818156',
'#686800':56, 56:'#686800',
'#686845':57, 57:'#686845',
'#4f4f00':58, 58:'#4f4f00',
'#4f4f35':59, 59:'#4f4f35',
'#bfff00':60, 60:'#bfff00',
'#eaffaa':61, 61:'#eaffaa',
'#8dbd00':62, 62:'#8dbd00',
'#adbd7e':63, 63:'#adbd7e',
'#608100':64, 64:'#608100',
'#768156':65, 65:'#768156',
'#4e6800':66, 66:'#4e6800',
'#5f6845':67, 67:'#5f6845',
'#3b4f00':68, 68:'#3b4f00',
'#494f35':69, 69:'#494f35',
'#7fff00':70, 70:'#7fff00',
'#d4ffaa':71, 71:'#d4ffaa',
'#5ebd00':72, 72:'#5ebd00',
'#9dbd7e':73, 73:'#9dbd7e',
'#408100':74, 74:'#408100',
'#6b8156':75, 75:'#6b8156',
'#346800':76, 76:'#346800',
'#566845':77, 77:'#566845',
'#274f00':78, 78:'#274f00',
'#424f35':79, 79:'#424f35',
'#3fff00':80, 80:'#3fff00',
'#bfffaa':81, 81:'#bfffaa',
'#2ebd00':82, 82:'#2ebd00',
'#8dbd7e':83, 83:'#8dbd7e',
'#1f8100':84, 84:'#1f8100',
'#608156':85, 85:'#608156',
'#196800':86, 86:'#196800',
'#4e6845':87, 87:'#4e6845',
'#134f00':88, 88:'#134f00',
'#3b4f35':89, 89:'#3b4f35',
'#00ff00':90, 90:'#00ff00',
'#aaffaa':91, 91:'#aaffaa',
'#00bd00':92, 92:'#00bd00',
'#7ebd7e':93, 93:'#7ebd7e',
'#008100':94, 94:'#008100',
'#568156':95, 95:'#568156',
'#006800':96, 96:'#006800',
'#456845':97, 97:'#456845',
'#004f00':98, 98:'#004f00',
'#354f35':99, 99:'#354f35',
'#00ff3f':100, 100:'#00ff3f',
'#aaffbf':101, 101:'#aaffbf',
'#00bd2e':102, 102:'#00bd2e',
'#7ebd8d':103, 103:'#7ebd8d',
'#00811f':104, 104:'#00811f',
'#568160':105, 105:'#568160',
'#006819':106, 106:'#006819',
'#45684e':107, 107:'#45684e',
'#004f13':108, 108:'#004f13',
'#354f3b':109, 109:'#354f3b',
'#00ff7f':110, 110:'#00ff7f',
'#aaffd4':111, 111:'#aaffd4',
'#00bd5e':112, 112:'#00bd5e',
'#7ebd9d':113, 113:'#7ebd9d',
'#008140':114, 114:'#008140',
'#56816b':115, 115:'#56816b',
'#006834':116, 116:'#006834',
'#456856':117, 117:'#456856',
'#004f27':118, 118:'#004f27',
'#354f42':119, 119:'#354f42',
'#00ffbf':120, 120:'#00ffbf',
'#aaffea':121, 121:'#aaffea',
'#00bd8d':122, 122:'#00bd8d',
'#7ebdad':123, 123:'#7ebdad',
'#008160':124, 124:'#008160',
'#568176':125, 125:'#568176',
'#00684e':126, 126:'#00684e',
'#45685f':127, 127:'#45685f',
'#004f3b':128, 128:'#004f3b',
'#354f49':129, 129:'#354f49',
'#00ffff':130, 130:'#00ffff',
'#aaffff':131, 131:'#aaffff',
'#00bdbd':132, 132:'#00bdbd',
'#7ebdbd':133, 133:'#7ebdbd',
'#008181':134, 134:'#008181',
'#568181':135, 135:'#568181',
'#006868':136, 136:'#006868',
'#456868':137, 137:'#456868',
'#004f4f':138, 138:'#004f4f',
'#354f4f':139, 139:'#354f4f',
'#00bfff':140, 140:'#00bfff',
'#aaeaff':141, 141:'#aaeaff',
'#008dbd':142, 142:'#008dbd',
'#7eadbd':143, 143:'#7eadbd',
'#006081':144, 144:'#006081',
'#567681':145, 145:'#567681',
'#004e68':146, 146:'#004e68',
'#455f68':147, 147:'#455f68',
'#003b4f':148, 148:'#003b4f',
'#35494f':149, 149:'#35494f',
'#007fff':150, 150:'#007fff',
'#aad4ff':151, 151:'#aad4ff',
'#005ebd':152, 152:'#005ebd',
'#7e9dbd':153, 153:'#7e9dbd',
'#004081':154, 154:'#004081',
'#566b81':155, 155:'#566b81',
'#003468':156, 156:'#003468',
'#455668':157, 157:'#455668',
'#00274f':158, 158:'#00274f',
'#35424f':159, 159:'#35424f',
'#003fff':160, 160:'#003fff',
'#aabfff':161, 161:'#aabfff',
'#002ebd':162, 162:'#002ebd',
'#7e8dbd':163, 163:'#7e8dbd',
'#001f81':164, 164:'#001f81',
'#566081':165, 165:'#566081',
'#001968':166, 166:'#001968',
'#454e68':167, 167:'#454e68',
'#00134f':168, 168:'#00134f',
'#353b4f':169, 169:'#353b4f',
'#0000ff':170, 170:'#0000ff',
'#aaaaff':171, 171:'#aaaaff',
'#0000bd':172, 172:'#0000bd',
'#7e7ebd':173, 173:'#7e7ebd',
'#000081':174, 174:'#000081',
'#565681':175, 175:'#565681',
'#000068':176, 176:'#000068',
'#454568':177, 177:'#454568',
'#00004f':178, 178:'#00004f',
'#35354f':179, 179:'#35354f',
'#3f00ff':180, 180:'#3f00ff',
'#bfaaff':181, 181:'#bfaaff',
'#2e00bd':182, 182:'#2e00bd',
'#8d7ebd':183, 183:'#8d7ebd',
'#1f0081':184, 184:'#1f0081',
'#605681':185, 185:'#605681',
'#190068':186, 186:'#190068',
'#4e4568':187, 187:'#4e4568',
'#13004f':188, 188:'#13004f',
'#3b354f':189, 189:'#3b354f',
'#7f00ff':190, 190:'#7f00ff',
'#d4aaff':191, 191:'#d4aaff',
'#5e00bd':192, 192:'#5e00bd',
'#9d7ebd':193, 193:'#9d7ebd',
'#400081':194, 194:'#400081',
'#6b5681':195, 195:'#6b5681',
'#340068':196, 196:'#340068',
'#564568':197, 197:'#564568',
'#27004f':198, 198:'#27004f',
'#42354f':199, 199:'#42354f',
'#bf00ff':200, 200:'#bf00ff',
'#eaaaff':201, 201:'#eaaaff',
'#8d00bd':202, 202:'#8d00bd',
'#ad7ebd':203, 203:'#ad7ebd',
'#600081':204, 204:'#600081',
'#765681':205, 205:'#765681',
'#4e0068':206, 206:'#4e0068',
'#5f4568':207, 207:'#5f4568',
'#3b004f':208, 208:'#3b004f',
'#49354f':209, 209:'#49354f',
'#ff00ff':210, 210:'#ff00ff',
'#ffaaff':211, 211:'#ffaaff',
'#bd00bd':212, 212:'#bd00bd',
'#bd7ebd':213, 213:'#bd7ebd',
'#810081':214, 214:'#810081',
'#815681':215, 215:'#815681',
'#680068':216, 216:'#680068',
'#684568':217, 217:'#684568',
'#4f004f':218, 218:'#4f004f',
'#4f354f':219, 219:'#4f354f',
'#ff00bf':220, 220:'#ff00bf',
'#ffaaea':221, 221:'#ffaaea',
'#bd008d':222, 222:'#bd008d',
'#bd7ead':223, 223:'#bd7ead',
'#810060':224, 224:'#810060',
'#815676':225, 225:'#815676',
'#68004e':226, 226:'#68004e',
'#68455f':227, 227:'#68455f',
'#4f003b':228, 228:'#4f003b',
'#4f3549':229, 229:'#4f3549',
'#ff007f':230, 230:'#ff007f',
'#ffaad4':231, 231:'#ffaad4',
'#bd005e':232, 232:'#bd005e',
'#bd7e9d':233, 233:'#bd7e9d',
'#810040':234, 234:'#810040',
'#81566b':235, 235:'#81566b',
'#680034':236, 236:'#680034',
'#684556':237, 237:'#684556',
'#4f0027':238, 238:'#4f0027',
'#4f3542':239, 239:'#4f3542',
'#ff003f':240, 240:'#ff003f',
'#ffaabf':241, 241:'#ffaabf',
'#bd002e':242, 242:'#bd002e',
'#bd7e8d':243, 243:'#bd7e8d',
'#81001f':244, 244:'#81001f',
'#815660':245, 245:'#815660',
'#680019':246, 246:'#680019',
'#68454e':247, 247:'#68454e',
'#4f0013':248, 248:'#4f0013',
'#4f353b':249, 249:'#4f353b',
'#333333':250, 250:'#333333',
'#505050':251, 251:'#505050',
'#696969':252, 252:'#696969',
'#828282':253, 253:'#828282',
'#bebebe':254, 254:'#bebebe',
'#ffffff':255, 255:'#ffffff',
}
#descripe the text position refered to the point clicked
TEXT_POSITION=['n','ne', 'e', 'se', 's', 'sw', 'w','nw', 'c']
