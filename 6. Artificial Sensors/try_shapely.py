# ----------------------pip install shapely ----------------------

from shapely.geometry import LineString

line1=LineString([(0,0),(3,3)])
line2=LineString([(2,0),(2,4)])

intersection = line1.intersection(line2)

if intersection:
    print("Lines intersect at:", intersection)
else:
    print("Lines do not intersect.")