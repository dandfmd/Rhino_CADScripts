
__author__ = "dfmd"
__version__ = "2019.07.12"

import rhinoscriptsyntax as rs

base_curve = rs.GetObject("Reference curve", rs.filter.curve,True,True)
curves = rs.GetObjects("Curves")
tol = rs.GetReal("Tolerance",1)

if base_curve and curves:
    try:
        base_area = rs.CurveArea(base_curve)
        area_curves = []
        for curve in curves:
            if rs.IsCurveClosed(curve):
                if abs(rs.CurveArea(curve)[0] - base_area[0]) < base_area[1] + tol:
                     area_curves.append(curve)
        rs.SelectObjects(area_curves)
        print "%s equal area objects found." % len(area_curves)
        
    except Exception as e:
        print('Error: %s' % e)
    