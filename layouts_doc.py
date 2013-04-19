############################################################
#
#  LAYOUTS:
#
#  window.get_layout() and window.set_layout()
#  aren't really documented in the API so I am
#  making some notes here about how they work.
#
#    * rows are the positions (from 0.0 to 1.0) that make
#      up the horizontal lines around (sides of) views.
#
#    * columns are the positions (from 0.0 to 1.0) that make
#      up the vertical lines around (top/bottom of) views
#
#    * cells are the 4 positions (left,top,right,bottom)
#      that define the positions of each view
#
#  ROWS:
#
#  0.0        -----------------
#             |    |          |
#             |    |          |
#  0.66       -----------------
#             |    |          |
#  1.0        -----------------
#
#  COLUMNS:  0.0  0.3        1.0
#
#  CELLS:
#
#    ---------
#    | 0 | 0 |
#    |0 1|1 2|
#    | 1 | 1 |
#    ---------
#    | 1 | 1 |
#    |0 1|1 2|
#    | 2 | 2 |
#    ---------
#
###########################################################
