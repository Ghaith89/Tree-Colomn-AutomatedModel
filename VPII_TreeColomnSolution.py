import rhinoscriptsyntax as rs

#CreatingBeamProcedure

#Beam = rs.GetObject("GetLine", rs.filter.curve)


#Creating Beam Function
def CreatingBeam (Crv, Rad):
    EndPt = rs.CurveEndPoint(Crv)
    StPt = rs.CurveStartPoint(Crv)
    
    DirVec = EndPt- StPt
    
    StPl = rs.PlaneFromNormal(StPt, DirVec)
    EndPl = rs.PlaneFromNormal(EndPt, DirVec)
    
    CirEd = rs.AddCircle(EndPl, Rad)
    CirSt = rs.AddCircle(StPl, Rad)
    
    IdsList = []
    IdsList.append( CirSt)
    IdsList.append( CirEd)
    
    BeamGeometry = rs.AddLoftSrf(IdsList)
    
    return BeamGeometry

#Creating Node Function
def CreatingNodeFun(Pt, Lines, BeamRad, BeamLength):
    Beams = []
    for i in Lines:
        MidPt = rs.CurveMidPoint(i)
        GuidMid = rs.AddPoint(MidPt)
        DirVe = rs.VectorCreate(GuidMid, Pt)
        DirVecUni = rs.VectorUnitize(DirVe)
        TrVec = rs.VectorScale(DirVecUni, BeamLength)
        PtToMove = rs.AddPoint(Pt)
        EndPt = rs.MoveObject(PtToMove, TrVec)
        Plane01 = rs.PlaneFromNormal(Pt, DirVe)
        Plane02 = rs.PlaneFromNormal(PtToMove, DirVe)
        
        Ids = []
        Cir01 = rs.AddCircle(Plane01, BeamRad)
        Cir02 = rs.AddCircle(Plane02, BeamRad)
        Ids.append(Cir01)
        Ids.append(Cir02)
        
        Beam = rs.AddLoftSrf(Ids)
        Beams.append(Beam)
    return Beams
        

# Excecute the Code
ListBeams = rs.GetObjects("GetLine", rs.filter.curve)

ListPts = []
for i in ListBeams:
    StPt = rs.CurveStartPoint(i)
    ListPts.append(StPt)
    EdPt = rs.CurveEndPoint(i)
    ListPts.append(EdPt)
    
if ListPts:
    ListPts= rs.CullDuplicatePoints(ListPts)
    #rs.AddPoints(ListPts)
    
    #getting Neighbour elements
    
    LstNodeBeams = []
    for n in ListPts:
        NeiBeamList = []
        for l in ListBeams:
            EndL = rs.CurveEndPoint(l)
            StEl = rs.CurveStartPoint(l)
            if rs.Distance(n, EndL)< 0.2 or rs.Distance(n, StEl)<0.2:
                NeiBeamList.append(l)
                
        LstNodeBeams.append(NeiBeamList)
        
    # Creating Nodes
    co = -1
    for Cen in ListPts:
        co = co+1
        Gr = rs.WorldXYPlane()
        DistToGr = rs.DistanceToPlane(Gr, Cen)
        if DistToGr>0:
            DistToGr = DistToGr
        else:
            DistToGr = 5
        BeLen = (1/DistToGr)*2
        BRad = BeLen/3 
        if BRad > 0.2:
            BRad = 0.2
        Axes = LstNodeBeams[co]
        Node = CreatingNodeFun(Cen, Axes, BRad, BeLen)
    
    # Creating Beams
    for Axe in ListBeams:
        Gr = rs.WorldXYPlane()
        EndPt = rs.CurveEndPoint(Axe)
        StPt = rs.CurveStartPoint(Axe)
        Dist01 = rs.DistanceToPlane(Gr, StPt)
        Dist02 = rs.DistanceToPlane(Gr, EndPt)
        
        if Dist01> Dist02:
            Height = Dist01*2 
        else:
            Height = Dist02*2
        
        Rad = (1/Height)-0.01
        
        CreatingBeam(Axe, Rad)
    



