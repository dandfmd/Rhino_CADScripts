
__author__ = "dfmd"
__version__ = "2019.07.12"

import rhinoscriptsyntax as rs

curves = rs.GetObjects("Selecciona curvas",rs.filter.curve,True,True)

if curves:
    try:
        for curve in curves:
            point = rs.CurveAreaCentroid(curve)[0]
            rs.AddPoint(point)
            rs.DeleteObject(curve)
        print("%s points added." % len(curves))
        
    except Exception as e:
        print('Error: %s' % e)