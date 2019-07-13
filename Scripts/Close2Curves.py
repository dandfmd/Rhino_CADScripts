
__author__ = "dfmd"
__version__ = "2019.07.12"

import rhinoscriptsyntax as rs

curves = rs.GetObjects("Select pair of curves", rs.filter.curve,True,True)

def close_curve():
    curve_a = curves[0]
    curve_b = curves[1]
    points_a = [rs.CurveStartPoint(curve_a),rs.CurveEndPoint(curve_a)]
    points_b = [rs.CurveStartPoint(curve_b),rs.CurveEndPoint(curve_b)]
    for test_point in points_a:
        closest_point = rs.PointArrayClosestPoint(points_b, test_point)
        curves.append(rs.AddLine(test_point,points_b[closest_point]))
        points_b.pop(closest_point)
    rs.JoinCurves(curves,True)    
    print "Curves closed"
    
if len(curves) == 2:
    try:
        close_curve()
    except Exception as e:
        print('Error: %s' % e)