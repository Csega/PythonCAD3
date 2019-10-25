# Introduction

PythonCAD is an open-source CAD package built and designed around Python.
As such, it aims to be a fully scriptable and customizable CAD program.
It is initially designed to run under Linux, one of the BSD flavors, or Unix,
however, running it on Windows is now also possible.

Using an established, powerful, and expressive language like Python as the core
of the program saves an enormous amount of work for developers and, for users
who are already familiar with Python, you don't have to try and learn a new
language if you want to extend or customize the code. If you've never written
Python code before, there are extensive resources available for you. A good
place to start is at the Python home page ...

http://www.python.org

# Goals

The primary design goal is to provide a good CAD package. The open-source world
has been moving steadily from providing superior tools for proprietary systems
(i.e. GCC), to world-class operating systems (i.e. Linux), and has advanced
remarkably in providing complete desktop environments (GNOME and KDE). It is
hoped that PythonCAD will grow to be an excellent addition to the desktop
programs now available for users of open-source software.

A design goal with the program code is to keep the user interface completely
separated from the backend or the generic code. In doing so, it should be
possible for developers to write code porting PythonCAD to their chosen
interface with less work. The initial release is written using GTK-2.0 as the
interface (utilizing the PyGTK library). The addition of a front end utilizing
the PyObjC bindings on Mac OS X and Cocoa demonstrates that this approach of
separating the interface from the core program is a viable approach of
application design. It is hoped that interfaces for GNOME, QT, KDE, and other
packages will eventually be added to PythonCAD. Now PythonCAD is developed
using the PyQt toolkit.

A second code design goal is to write a powerful graphical program without
writing much, if any, C or C++ code. The Python language frees the programmer
from many of the difficulties that are associated with C (memory allocation,
buffer handling, etc.) or C++ code (i.e. compiler and platform issues).
No language is perfect, but it is hoped that PythonCAD can demonstrate that
choosing Python as the primary language for development provides good
performance, ease of maintenance, and a fun language to work with.

# Requirements

* Python: version 3.3+
* Sympy: version 1.4
* PyQt: known to work with PyQt5, version 5.12.2


# License

PythonCAD is distributed under the terms of the
GNU General Public License (GPL).

# Modifications

Csega is intended to modify the original module, which was written for
Python 2 and has not been maintained since two years at least, to convert
the whole source to Python 3 compatible with the additional goal to convert
from PyQt4 to PyQt5 dependency.

However, since the package is still not fully functional as of (25th October 2019), Csega is intended to do a deep revision of the whole code base using [Porting Python 2 Code to Python 3](https://docs.python.org/3/howto/pyporting.html) official guide.
