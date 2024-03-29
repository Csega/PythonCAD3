# NEWS

## The project has been forked on Nov 17, 2014
* New maintainer: Csega
* New repository: https://github.com/Csega/PythonCAD3
* Goal 1: make it compatible with Python 3
* Goal 2: make it compatible with PyQt5

## Release DS1-R37, Sep  22, 2009
* New Maintainer Matteo Boscolo 
* New Repository in www.Sourceforge.net/projects/pythoncad
* New Pan & Dynamic Zoom
* New  Snap System (With One shot snap :point/tangent/perpendicular/midpoint/endpoint)
* New Dynamic Cursor shape changing with snap
* New Fillet Two lines.
* Fix wrong positions in copy&paste Command
* Bug fixes and code improvements

## Release DS1-R36, May 12, 2007
* Windows preferences saved to "env['APPDATA']/PythonCAD" directory
* Bug fixes and code improvements

## Release DS1-R35, December 19, 2006
* Global preferences now set via 'Edit'->'Preferences' menu, and
  the values are saved to $HOME/.pythoncad/prefs.py file.
* Image preferences now adjustable via 'Draw'->'Set' menu commands
* Bug fixes and code improvments

## Release DS1-R34, August 3, 2006
* Additional display speedups and redraw fixes
* Entities can now be rotated around arbitrary points
* Cairo drawing routines used for entity drawing if available
* Bug fixes and code improvements

## Release DS1-R33, July 7, 2006
* Inclusion of 'gettext' module for Native Language Support
* Reworked display code greatly improving interface responsiveness
* Interface code now relies solely on messaging system for interaction
  with core interface-neutral code
* Spanish translation provided by Miguel Angel Barcena Rodriguez
* Bug fixes and code improvements

## Release DS1-R32, May 25, 2006
* Fix autosplitting code to not rely on initial setting in preferences
  file and not disable autosplitting on a layer after first execution
  where global AUTOSPLIT is False
* Fix typo in new split code
* Bug fixes

## Release DS1-R31, May 19, 2006
* Default style values for classes now settable at runtime
* Entity splitting code reworked
* Automatic entity splitting at newly added point now available
* Bug fixes and code improvements

## Release DS1-R30, March 21, 2006
* Stop using weakref module in Subpart class
* Rework again code for transferring entities between layers
* Bug fixes and code improvements

## Release DS1-R29, March 3, 2006
* Simplified Dimension __init__() methods
* Reworked entity deletion and transfer code
* RadialDimension toggling of diameter display now available from menu
* AngularDimension inversion now availabe from menu
* Bug fixes and code improvements

## Release DS1-R28, February 2, 2006
* Reworked entity modification code allows for both 'select->act' and
  'act->select' modes of operation.
* Reworked entity movement code.
* Attributes of Dimension DimString entities can be adjusted individually,
  plus the missing ability to adjust their color has been added.
* Warning cleanup for running PythonCAD under recent PyGTK releases.
* Bug fixes and code improvements

## Release DS1-R27, December 6, 2005
* Selecting an entity will cause it to be drawn in a special color.
* Deselecting a selected entity action added to 'Edit' menu.
* Bug fixes and code improvements.

## Release DS1-R26, October 21, 2005
* Horizontal and Vertical stretch now accept keyboard input to define
  the stretch distance
* Dual x/y move operation accepts keyboard input to define distances
* Dual x/y stretch operation added
* PostScript output adjustments improving conformance to Adobe standards
* Quadtree reworking to permit storage of equivalent entities
* Menus have added mnemonics to permit menu selection via keyboard
* Bug fixes and code improvements

## Release DS1-R25, May 26, 2005
* Fix several compatibility issues for running on older PyGTK releases
* Clean up GTK event handling code to better match GTK expectations
* Bug fixes and code improvements

## Release DS1-R24, April 29, 2005
* Entity drawing improvements via draw()/erase() methods
* Use of gtk.Action and gtk.ActionGroup classes for building menus
* Bug fixes and code improvements

## Release DS1-R23, March 18, 2005
* Improve scripting and entry box evaluation
* Replace deprecated values from PyGTK
* Bug fixes and code improvements

## Release DS1-R22, January 26, 2005
* Use new gtk.ComboBox and gtk.ColorDialog widgets if available.
* Add missing ability to paste TextBlock objects
* Bug fixes and code improvements

## Release DS1-R21, January 11, 2005
* File saving and restoration of locked and visibility status
* Undo/Redo code improvements
* Bug fixes and code improvements

## Release DS1-R20, December 21, 2004
* Numerous Undo/Redo improvements
* Simplified and refined file storage code
* Bug fixes and code improvements

## Release DS1-R19, November 13, 2004
* Fix file-save bug for drawings with text entities.
* Add 'showpage' to PostScript output.

## Release DS1-R18, November 12, 2004
* Dimension printing improvements
* Undo/Redo data storage improvements
* Deleted entity re-creation improvements
* Bug fixes and code improvements
* RPM packaging contributions from D. Scott Barninger

## Release DS1-R17, October 3, 2004
* Printing!!!
* Significant improvements in modifying entities
* Undo/Redo improvements
* Greatly improved text support
* Significant code improvements in dimension and text code
* Miscellaneous bug fixes and code improvements

## Release DS1-R16, June 16, 2004
* Fixes for Cocoa interface
* Bug fix in SegJoints for Chamfers and Fillets

## Release DS1-R15, June 15, 2004
* Added Cocoa-based front end
* Undo/Redo improvements
* Layer addition and deletion bug fixes
* Miscellaneous bug fixes

## Release DS1-R14, May 26, 2004
* Undo/Redo improvements
* Fix file save bug regression
* Fix broken handling of drawing tangent circles
* Fix quadtree errors for angled construction lines
* Miscelleanous bug fixes and code improvements

## Release DS1-R13, April 28, 2004
* Undo/Redo added
* Many deprecated methods removed
* Drawings are now stored with the background color and inactive layer color
* Point colors can be adjusted
* Bug fixes and code improvements

## Release DS1-R12, February 24, 2004
* Subpart classes now store weak references to objects
* xrange() -> range() conversion
* Many deprecated methods removed
* Conversion of most entities to a new message-sending design
  similar to that of QT's signals/slots
* New class hierarchy allows for entites to be locked and hidden
* Quadtrees used for storing most entities in a drawing.
* Bug fixes and code improvements.

## Release DS1-R11, December 30, 2003
* More Python 2.3 fixes
* Reworked file saving to avoid using mutable objects as dictionary keys
* Major improvements in with transferring objects between layers
* Bug fixes and code improvments

## Release DS1-R10, October 14, 2003
* Python 2.3 fixes
* Entity clipping changes
* DWG reading code added - no reading of DWG files yet
* Adding diameter display option for radial dimensions
* Bug fixes and code improvemnts

## Release DS1-R9, July 29, 2003
* Rework internal option handling
* Rework internal storage of colors, linetypes, linestyles
* Tangent calculation fixes
* Intersection fixes when testing for points
* Fix improper user of mutable variables as hash keys.
* Bug fixes and code improvements

## Release DS1-R8, June 24, 2003
* Intersection code changed to return intersection points as tuples.
* Leader line arrow size and dimension endpoint size now settable
  through preference dialogs and preference file
* Saving to existing files now shows a dialog to allow the operation
  to be cancelled.
* Polygon drawing tool added.
* Unified preferences dialog box and increased preference setting
  options and abilities.
* Begin the rework of drawing options internal handling.
* Bug fixes and code improvements

## Release DS1-R7, June 3, 2003
* Tangent Construction Circle creation:
	- Tangent to a single construction line or construction circle
	- Tangent to two construction lines or a construction line and
	  construction circle
* Tangent construction line creation between two construction circles
* Parallel construction line creation simplified
* First iteration of a command-line mode for working in a drawing
* File format changes to make the files easier to understand
* Large code cleanup by moving interface-neutral code to the "Generic"
  subdirectory
* Many new methods added to drawing entities (i.e. layer.bindObject())
* Reworked object splitting code - polylines can now be split
* Assorted bug fixes and code improvements

## Release DS1-R6, May 4, 2003
* Text can now be stored in a drawing
* New Polyline entity available - this is essentially a set of
  connected Segment elements.
* Mirroring objects around a construction line is now available.
* Interface neutral code moved from Interface/Gtk to Generic. More
  of this should be done in upcoming releases.
* Internal reworking of Tool objects, and the creation/modification
  of entities from the UI. The Tool changes should make the code
  clearer and simpler to write, as well as move more code from the
  interface specific directory to the generic directory.
* Assorted bug fixes and code improvements

## Release DS1-R5, March 28, 2003
* The reading of a global and user preferences file is implemented
* Many changes in anticipation of hatching - hatching itself is
  still not available though
* Several new methods added for searching for objects at a specific
  location and of a specific size.
* Dimension endpoint markers now displayed
* Added leader lines
* Filenames are now saved with a '.gz' to indicate they are gzipped
* Added adjustable sizes to dimension end points
* Assorted bug fixes and code improvements

## Release DS1-R4, February 24, 2003
* Split many Layer routines into smaller, private methods
* Bugs found and fixed in Layer due to method splitting metioned above
* Big improvements in drawing dimensions
* Linear Dimensioning added
* Angular Dimensioning added
* Saved files now only contain used colors, linetypes, styles
* Interactive feedback when creating dimensions and arcs
* Assorted bug fixes and code improvements

## Release DS1-R3, January 30, 2003
* Added drawing tangent and perpendicular construction lines
* Added splitting of segments, circles, and arcs
* Line thickness is drawn for "real" entities
* More code modified to current standards
* Added more doc strings
* Rewrote most of the intersection calculation code
* Bug fixes and code improvements

## Release DS1-R2, January 11, 2003
* Add layer deletion and clearing.
* Add setting current entity attributes from "Draw" menu.
* Fix changing attributes from "Modify" menu.
* Don't write empty placeholder tags in files.
* Many doc strings added.
* Modify a few routines to adhere to the current code standards.
* Add the ability to transfer objects between layers.
* Add a web page for keeping track of needed development features,
  enhancements, and wish list ideas.

## December 18, 2002
The first release! Basic drawing functionality works, rudimentary
editing exists, and that's about it.
