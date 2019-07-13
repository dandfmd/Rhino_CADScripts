
__author__ = "dfmd"
__version__ = "2019.07.12"

import rhinoscriptsyntax as rs

points = rs.GetObjects("Selecciona puntos",rs.filter.point,True,True)
diam = rs.GetReal("Diameter",10.0)

if points and diam:
    try:
        for point in points:
            rs.ObjectColor(rs.AddCircle(point, diam/2),(0,0,255))
            rs.DeleteObject(point)
            print("%s circles added." % len(circles))
    except Exception as e:
        print('Error: %s' % e)

