from pythoncad_qt import *
from sympy import *

w,app=getPythonCAD()
w.createSympyDocument()

p=Point(10, 10)
w.plotFromSympy([p])

w.getSympyObject()
