
__author__ = "dfmd"
__version__ = "2019.07.12"

import rhinoscriptsyntax as rs

def dogbone(curves,diam,diam_barrenos,tol):
    for curve in curves:
        if rs.CloseCurve(curve):
            centroid = rs.CurveAreaCentroid(curve)[0]
        else:
            centroid = rs.CurveMidPoint(curve)
        if diam_barrenos == -1:
            rs.AddPoint(centroid)
        elif diam_barrenos == 0:
            pass
        else:
            rs.AddCircle(centroid,diam_barrenos*.5)
    
        curve = rs.ConvertCurveToPolyline(curve,delete_input=True)
        tol_curve = rs.OffsetCurve(curve, centroid,-tol) if tol else curve
        ocurve = rs.OffsetCurve(tol_curve, rs.CurveAreaCentroid(curve)[0],diam*.3)
        circles = [rs.AddCircle(i,diam/2) for i in rs.CurvePoints(ocurve)]
        rs.CurveBooleanUnion(circles+[tol_curve])
        rs.DeleteObjects([ocurve,tol_curve]+circles)
        if curve: rs.DeleteObject(curve)

def Main():
    try:
        data_name = "Rect2DogBone"
        curves = rs.GetObjects("Rectangle curve",rs.filter.curve,True,True)
        diam = rs.GetInteger("DogBone circle diameter",16 if not rs.GetDocumentData(data_name,"diam_external") else float(rs.GetDocumentData(data_name,"diam_external")))
        diam_barrenos = rs.GetInteger("Circle at centroid (0=None -1=Point n=Diameter)",0 if not rs.GetDocumentData(data_name,"diam_barrenos") else float(rs.GetDocumentData(data_name,"diam_barrenos")))
        tol = float(rs.GetReal("External offset",0 if not rs.GetDocumentData(data_name,"tolerance") else float(rs.GetDocumentData(data_name,"tolerance"))))
        if curves and diam:
            rs.EnableRedraw(False)
            dogbone(curves,diam,diam_barrenos,tol)
            rs.SetDocumentData(data_name,"diam_external",str(diam))
            rs.SetDocumentData(data_name,"diam_barrenos",str(diam_barrenos))
            rs.SetDocumentData(data_name,"tolerance",str(tol))
            rs.EnableRedraw(True)
        print("%s DogBones created" % len(curves))
    
    except Exception as e:
        print("Error: %s" % e)
        
if __name__=="__main__":
    Main()