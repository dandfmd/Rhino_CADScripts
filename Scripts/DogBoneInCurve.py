
__author__ = "dfmd"
__version__ = "2019.07.12"

import rhinoscriptsyntax as rs
import json

RADIUS_TOLERANCE = 0.2

def create_bone(point,curve,length,width,radius,extend):
    
    if not extend: extend = 0.001
    curve_surface = rs.AddPlanarSrf(curve)
    if not curve_surface:
        exp_curves = rs.ExplodeCurves(curve)
        curve_surface = rs.AddEdgeSrf(exp_curves)
        rs.DeleteObjects(exp_curves)
        print("Surface problem")
#         circle = rs.AddCircle(rs.CurveAreaCentroid(curve)[0],10000)
#         planar_surface = rs.AddPlanarSrf(circle)
#         projected_curve = rs.ProjectCurveToSurface(curve,planar_surface,(0,0,-1))
#         if not projected_curve: rs.ProjectCurveToSurface(curve,planar_surface,(0,0,1))
#         if not projected_curve: print "noooooo"
#         curve_surface = rs.AddPlanarSrf(projected_curve)
#         rs.DeleteObjects([circle,planar_surface,curve])
#         curve = rs.JoinCurves(rs.DuplicateEdgeCurves(curve_surface, select=False))
#         if not curve_surface: print "WARNING"

    main_point_param = rs.CurveClosestPoint(curve,point)
    curve_normal = rs.CurveNormal(curve)
    curve_plane = rs.CurvePlane(curve)
    tangent = rs.CurveTangent(curve,main_point_param)
    center_curve = rs.AddLine((0,0,0),rs.VectorScale(tangent,length))
    rs.RotateObject(center_curve,(0,0,0),90,curve_normal)
    rs.MoveObject(center_curve,rs.VectorCreate(point,(0,0,0)))
    if not rs.IsPointOnSurface(curve_surface,rs.CurveEndPoint(center_curve)): rs.RotateObject(center_curve,point,180,curve_normal)
    normal = rs.VectorScale(tangent,10000)
    normal_inverted = rs.VectorReverse(normal)
    side_curve = rs.OffsetCurveOnSurface(center_curve,curve_surface, width/2)
    if not side_curve: side_curve = rs.OffsetCurveOnSurface(center_curve,curve_surface, -width/2)
    side_curves = [side_curve,rs.RotateObject(side_curve, rs.CurveMidPoint(center_curve),180,rs.VectorCreate(rs.CurveStartPoint(center_curve),rs.CurveEndPoint(center_curve)), True)]
    #side_curves = [side_curve,rs.MirrorObject(side_curve,rs.CurveStartPoint(center_curve),rs.CurveEndPoint(center_curve), True)]
    #side_curves = [rs.OffsetCurveOnSurface(center_curve,curve_surface, width/2),rs.OffsetCurveOnSurface(center_curve,curve_surface, -width/2)]
    for side_curve in side_curves:
        rs.ExtendCurveLength(side_curve, 0, 0,2)
        rs.ObjectColor(side_curve,(255,0,0))
    perimeter_curve = rs.AddCurve([rs.CurveStartPoint(side_curves[0]),rs.CurveEndPoint(side_curves[0]),rs.CurveEndPoint(side_curves[1]),rs.CurveStartPoint(side_curves[1]),rs.CurveStartPoint(side_curves[0])],1)
    inside_curve = rs.OffsetCurve(perimeter_curve,rs.CurveAreaCentroid(perimeter_curve)[0],radius*.7)
    external_curve = rs.OffsetCurve(perimeter_curve,rs.CurveAreaCentroid(perimeter_curve)[0],-extend)
   
    e_points = [rs.CurvePoints(external_curve)[0],rs.CurvePoints(external_curve)[3]]
    e_perimeter_curve = rs.AddCurve([rs.CurveEndPoint(side_curves[1]),rs.CurveEndPoint(side_curves[0]),e_points[0],e_points[1],rs.CurveEndPoint(side_curves[1])],1)

    center_plane_a = rs.PlaneFromPoints(rs.CurvePoints(inside_curve)[2],rs.CurvePoints(inside_curve)[1], rs.CurvePoints(inside_curve)[3])
    center_plane_b = rs.PlaneFromPoints(rs.CurvePoints(inside_curve)[1],rs.CurvePoints(inside_curve)[0], rs.CurvePoints(inside_curve)[2])

    circles = [rs.AddCircle(center_plane_a, radius+RADIUS_TOLERANCE),rs.AddCircle(center_plane_b, radius+RADIUS_TOLERANCE)]
    
    bone_curve = rs.CurveBooleanUnion([e_perimeter_curve]+circles) if extend else rs.CurveBooleanUnion([perimeter_curve]+circles)
    rs.DeleteObjects([inside_curve,center_curve,perimeter_curve,curve_surface,e_perimeter_curve,external_curve]+side_curves+circles)
    return bone_curve


def rebuild_curves(curves):
    new_curves = []
    for curve in curves:
    
        new_curves.append(curve)
#         exp_curves = rs.ExplodeCurves(curve,True)
#         curve_surface = rs.AddEdgeSrf(exp_curves)
#         dup_edges = rs.DuplicateEdgeCurves(curve_surface)
#         new_curves.append(rs.JoinCurves(dup_edges,True))
#         rs.DeleteObjects(exp_curves+[curve_surface])
        
    return new_curves

def Main():
    
    input_curves = rs.GetObjects("Curves",rs.filter.curve,True,True)
    input_points = rs.GetObjects("Points for dogboone placement",rs.filter.point)
    if not input_curves or not input_points: return
    
    #Reads, asks and writes settings to document
    data_name = "dogbone2"
    values = rs.GetDocumentData(data_name,"settings")
    values = json.loads(values)["data"] if values else ["35.0","15.0","9.525","1"]
    settings = ["Length:","With:","Diameter:","Tolerance Offset:"]
    length,width,diam,aperture = [ float(i.replace(" ","")) for i in rs.PropertyListBox(settings,values,"DogBone by dfmd","Settings:")]
    rs.SetDocumentData(data_name,"settings",json.dumps({"data":[length,width,diam,aperture]}))
   
    sorted_points = []
    clean_curves = []
    rs.EnableRedraw(False)
    for curve in input_curves:
       
        point_list = []
        for point in input_points:
            if rs.PointInPlanarClosedCurve(point,curve,rs.CurvePlane(curve)) == 2:
                point_list.append(point)
                
        if point_list:
            sorted_points.append(rs.SortPointList(point_list))
            #Clean curve
#             circle = rs.AddCircle(rs.CurveAreaCentroid(curve)[0],10000)
#             planar_surface = rs.AddPlanarSrf(circle)
#             projected_curve = rs.ProjectCurveToSurface(curve,planar_surface,(0,0,-1))
#             clean_curves.append(projected_curve)
#             rs.DeleteObjects([circle,planar_surface,curve])
            
            clean_curves.append(curve)
    
    #main_curve = rs.GetCurveObject("Selecciona curva",True)[0]
    #main_points = rs.SortPointList(rs.GetObjects("Selecciona puntos de referencia",rs.filter.point))
    #input_curves = rebuild_curves(input_curves)
   
    for main_curve in clean_curves:
        
        main_points = sorted_points[clean_curves.index(main_curve)]
        bone_curves = [create_bone(point,main_curve,length,width,diam/2,aperture) for point in main_points]
        #new_main_curve = rs.CopyObject(rs.ConvertCurveToPolyline(main_curve,False,False,True))
        new_main_curve = rs.CopyObject(main_curve)
        completed = True
        for bone_curve in bone_curves:
            
            buffer_curve = rs.CurveBooleanDifference(new_main_curve,bone_curve)
            
            if len(buffer_curve) > 1:
                rs.DeleteObjects(buffer_curve)
                rs.DeleteObject(new_main_curve)
                completed = False
                break
            
            rs.DeleteObject(new_main_curve)
            new_main_curve = buffer_curve
            
        if not completed:
            super_curve = rs.CurveBooleanUnion(bone_curves)
            rare_curves = rs.CurveBooleanDifference(main_curve, super_curve)
            if len(rare_curves) > 1:
                areas = [rs.CurveArea(i) for i in rare_curves]
                sorted_curves = [x for (y,x) in sorted(zip(areas,rare_curves))]
                rs.DeleteObjects(sorted_curves[:-1])
                
            rs.DeleteObject(super_curve)
    
        rs.DeleteObjects(bone_curves+[main_curve])

    
if __name__=="__main__":
    
    try:
        Main()
        print("Dogbone curve created succesfully")
    except Exception as e: #error as Exception:
        print("Upps still in beta... %s" % e)
    
    