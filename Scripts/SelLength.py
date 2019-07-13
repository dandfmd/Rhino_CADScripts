
__author__ = "dfmd"
__version__ = "2019.07.12"

import rhinoscriptsyntax as rs

base_curve = rs.GetObject("Reference curve", rs.filter.curve,True,True)
curves = rs.GetObjects("Curves")
tol = rs.GetReal("Tolerance",.005)

if base_curve and curves:
    try:
        base_lenght = rs.CurveLength(base_curve)
        lenght_curves = []
        for curve in curves:
            if abs(rs.CurveLength(curve) - base_lenght) < tol:
                lenght_curves.append(curve)
        rs.SelectObjects(lenght_curves)
        print "%s equal length objects found." % len(lenght_curves)
        
    except Exception as e:
        print('Error: %s' % e)
