import rhinoscriptsyntax as rs

#CreatingBeamProcedure

#Beam = rs.GetObject("GetLine", rs.filter.curve)


#Creating Beam Function
def CreatingBeam (Crv):
    EndPt = rs.CurveEndPoint(Crv)
    StPt = rs.CurveStartPoint(Crv)
    
    DirVec = EndPt- StPt
    
    StPl = rs.PlaneFromNormal(StPt, DirVec)
    EndPl = rs.PlaneFromNormal(EndPt, DirVec)
    
    CirEd = rs.AddCircle(EndPl, 0.2)
    CirSt = rs.AddCircle(StPl, 0.2)
    
    IdsList = []
    IdsList.append( CirSt)
    IdsList.append( CirEd)
    
    BeamGeometry = rs.AddLoftSrf(IdsList)
    
    return BeamGeometry

def CreatingNodeFun(Pt, Lines, BeamRad, BeamLength):
    Beams = []
    for i in Lines:
        MidPt = rs.CurveMidPoint(i)
        DirVe = MidPt-Pt
        DirVecUni = rs.VectorUnitize(DirVe)
        TrVec = rs.VectorScale(DirVecUni, BeamLength)
        PtToMove = rs.AddPoint(pt)
        EndPt = rs.MoveObject(PtToMove, TrVec)
        Plane01 = rs.PlaneFromNormal(pt, DirVe)
        Plane02 = rs.PlaneFromNormal(PtToMove, DirVe)
        
        Ids = []
        Cir01 = rs.AddCircle(Plane01, BeamRad)
        Cir02 = rs.AddCircle(Plane02, BeamRad)
        Ids.append(Cir01)
        Ids.append(Cir02)
        
        Beam = rs.AddLoftSrf(Ids)
        Beams.append(Beam)
    return Beams
        


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
        
    


#Beam = CreatingBeam (Beam)
