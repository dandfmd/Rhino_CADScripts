
__author__ = "dfmd"
__version__ = "2019.07.12"

import rhinoscriptsyntax as rs

data_name = "OffsetAndClose"

curve = rs.GetObject("Select curve", rs.filter.curve,True,True)
dir = rs.GetPoint("Offset direction")
dist = rs.GetReal("Offset distance",5 if not rs.GetDocumentData(data_name,"dist") else float(rs.GetDocumentData(data_name,"dist")))

def offset():
    curves = [curve]
    offset_curve = rs.OffsetCurve(curve,dir,dist)
    curves.append(offset_curve)
    curves.append(rs.AddLine(rs.CurveEndPoint(offset_curve), rs.CurveEndPoint(curve)))
    curves.append(rs.AddLine(rs.CurveStartPoint(offset_curve), rs.CurveStartPoint(curve)))
    rs.JoinCurves(curves,True)
    print "Offset created."
    
if curve and dir and dist: 
    try:
        offset()
        rs.SetDocumentData(data_name,"dist",str(dist))
    except Exception as e:
        print('Error: %s' % e)