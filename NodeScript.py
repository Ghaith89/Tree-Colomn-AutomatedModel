import rhinoscriptsyntax as rs

def CreatingNodeFun(Pt, Lines, BeamRad, BeamLength):
    Beams = []
    for i in Lines:
        MidPt = rs.CurveMidPoint(i)
        GuidMid = rs.AddPoint(MidPt)
        DirVe = rs.VectorCreate(GuidMid, Pt)
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


ListLines = rs.GetObjects("Lines", rs.filter.curve)

pt = rs.GetObject("Cen", rs.filter.point)

NodeList = CreatingNodeFun(pt, ListLines, 0.2, 1)
