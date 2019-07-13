
__author__ = "dfmd"
__version__ = "2019.07.12"

import rhinoscriptsyntax as rs

surfaces = rs.GetObjects("Surfaces", rs.filter.surface,True,True)
tol = 10
y_distance = 0

if surfaces:
    try:
        rs.EnableRedraw(False)
        for srf in surfaces:
            urolled_srf = rs.UnrollSurface(srf, explode=False)
            bounding_box = rs.BoundingBox(urolled_srf)
            y_distance += rs.Distance(bounding_box[0],bounding_box[3]) + tol
            move_vector = rs.VectorCreate((0,0,0),(0,y_distance,0))
            rs.MoveObjects(urolled_srf,move_vector)
        rs.EnableRedraw(True)
    except Exception as e:
        print('Error: %s' % e)