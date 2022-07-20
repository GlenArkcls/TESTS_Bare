function sig = signatureOf(fnName)
switch fnName
    case "hideErrorMessages"
        sig=["i32"];
    case "getSystemType"
        sig=[];
    case "getVersion"
        sig=[];
    case "getLastError"
        sig=[];
    case "getProjectName"
        sig=[];
    case "getProjectDirectory"
        sig=[];
    case "createSeismicProject"
        sig=[];
    case "createInterpretationCollection"
        sig=["[c","i32"];
        %sig=[GSOType.tnStr8,GSOType.tnInt32];
    case "getFolderIDList"
        sig=[];
    case "getParentID"
        sig=["id"];
        %sig=[GSOType.tnVStr8]
    case "createFolder"
        sig=["[c","id"];
        %sig=[GSOType.tnStr8,GSOType.tnVStr8]
    case "createSeismicCollection"
        sig=["[c"];
        %sig=[GSOType.tnStr8]
    case "create3DSeis"
        sig=["[c","id","i32","i32","i32","i32","i32","i32","d","d","d","d","d","d","d","d","d","i32"];
%         sig=[GSOType.tnStr8,...
%              GSOType.tnVStr8,...
%              GSOType,tnInt32,...
%              GSOType,tnInt32,...
%              GSOType,tnInt32,...
%              GSOType,tnInt32,...
%              GSOType,tnInt32,...
%              GSOType,tnInt32,...
%              GSOType.tnDouble,...
%              GSOType.tnDouble,...
%              GSOType.tnDouble,...
%              GSOType.tnDouble,...
%              GSOType.tnDouble,...
%              GSOType.tnDouble,...
%              GSOType.tnDouble,...
%              GSOType.tnDouble,...
%              GSOType.tnDouble,...
%              GSOType.tnInt32];
    case "getSeisColIDList"
        sig=[];
    case "get3DSeisIDList"
        sig=[];
    case "get3DSeisIDListCol"
        sig=["id"];
        %sig=[GSOType.tnVStr8];
    case "get3DSeisGeom"
        sig=["id"];
        %sig=[GSOType.tnVStr8];
    case "put3DSeisTraces"
        sig=["id","[[s","[i32","[i32","i32","i32","d"];
        %sig=[GSOType.tnVStr8,...
         %    GSOType];
    case "get3DSeisDataRange"
        sig=["id"];
    case "get3DSeisTracesAll"
        sig=["id","d","d"];
    case "get3DSeisTracesSpec"
        sig=["id","[i32","[i32","d","d"];
    case "get3DSeisTracesRange"
        sig=["id","i32","i32","i32","i32","d","d"];
    case "get3DSeisTracesInXl"
        sig=["id","i32","i32","d","d"];
    case "get3DSeisTracesTransect"
        sig=["id","d","d","d","d","d","d","i32"];
    case "delete3DSeis"
        sig=["id"];
    case "getXYFromInlineCrossline"
        sig=["id","[d","[d"];
    case "getInlineCrosslineFromXY"
        sig=["id","[d","[d"];
    case "getInlineCrosslineFromXYExact"
        sig=["id","[d","[d"];
    case "create2DSeis"
        sig=["[c","i32","[d","[d","i32","d","d","id"];
    case "get2DSeisIDList"
        sig=[];
    case "get2DSeisIDListCol"
        sig=["id"];
        %sig=[GSOType.tnVStr8];
    case "get2DSeisGeom"
        sig=["id"];
        %sig=[GSOType.tnVStr8];
    case "put2DSeisTraces"
        sig=["id","[[s"];
        %sig=[GSOType.tnVStr8,GSOType.tnVFloat];
    case "get2DSeisDataRange"
        sig=["id"];
    case "get2DSeisTracesAll"
        sig=["id"];
        %sig=[GSOType.tnVStr8];
    case "get2DSeisTracesSpec"
        sig=["id","[i32"];
        %sig=[GSOType.tnVStr8,GSOType.tnVInt32];
    case "createSurf"
        sig=["[c","i32","i32","i32","d","d","d","d","d","i32"];
%         sig=[GSOType.tnStr8,...
%              GSOType.tnInt32,...
%              GSOType.tnInt32,...
%              GSOType.tnInt32,...
%              GSOType.tnDouble,...
%              GSOType.tnDouble,...
%              GSOType.tnDouble,...
%              GSOType.tnDouble,...
%              GSOType.tnDouble,...
%              GSOType.tnInt32];
    case "getSurfGeom"
        sig=["id"];
        %sig=[GSOType.tnVStr8];
    case "putSurfVals"
        sig=["id","[s"];
        %sig=[GSOType.tnVStr8,GSOType.tnVFloat];
    case "getSurfDataRange"
        sig=["id"];
        %sig=[GSOType.tnVStr8];
    case "getSurfVals"
        sig=["id"];
        %sig=[GSOType.tnVStr8];
    case "getSurfValsRangeIlXl"
        sig=["id","id","i32","i32","i32","i32"];
%         sig=[GSOType.tnVStr8,...
%              GSOType.tnVStr8,...
%              GSOType.tnInt32,...
%              GSOType.tnInt32,...
%              GSOType.tnInt32,...
%              GSOType.tnInt32];
    case "get3DHorzIDList"
        sig=[];
    case "create3DHorz"
        sig=["[c","i32","id","id"];
    case "get3DHorzGeom"
        sig=["id"];
    case "put3DHorzValues"
        sig=["id","[s"];
    case "get3DHorzVals"
        sig=["id"];
    case "get3DHorzValsInXl"
        sig=["id","i32","i32","i32","i32"];
    case "put3DHorzValuesSpec"
        sig=["id","[s","[d","[d"];
    case "create3DHorzProp"
        sig=["id","[c"];
    case "put3DHorzPropValues"
        sig=["id","[s"];
    case "get3DHorzPropVals"
        sig=["id"];
    case "get3DHorzPropValsInXl"
        sig=["id","i32","i32","i32","i32"];
    case "put3DHorzPropValuesSpec"
        sig=["id","[s","[d","[d"];
    case "get3DHorzDataRange"
        sig=["id"];
    case "get3DHorzPropDataRange"
        sig=["id"];
    case "getSeismicValsFromHorizon"
        sig=["id","id","i32","i32","i32","i32","d","d"];
    case "createPointSet"
        sig=["[c","id"];
    case "putPointSetData"
        sig=["id","i32","[d","[d","[d","i32"];
    case "getPointSetData"
        sig=["id"];
	case "createWellRoot"
        sig=[];
    case "createWellCollection"
        sig=["[c"];
    case "getWellCollectionIDList"
        sig=[];
    case "getWellIDList"
        sig=[];
	case "createWell"
        sig=["[c"];
	case "putWellHead"
        sig=["id","d","d"];
	case "getWellInfo"
        sig=["id"];
	case "putWellTrack"
        sig=["id","[d","[d","[d","[c","d"];
    case "getWellIDListGlobal"
        sig=[];
    case "getLogIDList"
        sig=["id"];
	case "createLog"
        sig=["id","[c"];
    case "createGlobalLog"
        sig=["[c"];
    case "getLogIDListGlobal"
        sig=[];
	case "putLogData"
        sig=["id","[s","d","d"];
    case "putLogDataExplicit"
        sig=["id","[d","[s"];
    case "getLogData"
        sig=["id"];
	case "getWellGeom"
        sig=["id"];
	case "getWellTrajectory"
        sig=["id"];
	case "getWellData"
        sig=["id"];
    case "createWellMarker"
        sig=["id","[c","d","i32"];
    case "getWellMarkers"
        sig=["id"];
    case "getFaultIDList"
        sig=[];
    case "createFault"
        sig=["[c","i32"];
    case "putFaultData"
        sig=["id","i32","[i32","[d","[d","[d"];
    case "getFaultGeom"
        sig=["id"];
    case "getWaveletIDList"
         sig=[];
    case "createWavelet"
        sig=["[c","id"];
    case "putWaveletData"
        sig=["id","d","[d"];
    case "getWaveletData"
        sig=["id"];
    case "getPolygonIDList"
        sig=[];
    case "createPolygon"
        sig=["[c","id"];
    case "putPolygonData"
        sig=["id","i32","[i32","[d","[d","[d","i32","[i32"];
    case "getPolygonData"
        sig=["id"];
    %%Interactive functions
    case "getFolderIDSel"
        sig=[];
    case "getSeis3DIntersectionIDSel"
        sig=[]
    case "get2DSeisIDSel"
        sig=[]
    case "getInterpretationCollectionIDSel"
        sig=[]
    case "get3DSeisIDSel"
        sig=[]
    case "get3DSeisColIDSel"
        sig=[]
    case "getSurfIDSel"
        sig=[]
    case "getSurfPropIDSel"
        sig=[]
    case "get3DHorzIDSel"
        sig=[]
    case "get3DHorzPropIDSel"
        sig=[]
    case "get2DHorzIDSel"
        sig=[]
    case "getWellIDSel"
        sig=[]
    case "getWellCollectionIDSel"
        sig=[]
    case "getLogIDSel"
        sig=[]
    case "getGlobalLogIDSel"
        sig=[]
    case "getWaveletIDSel"
        sig=[]
    case "getFaultIDSel"
        sig=[]
    case "getPointSetIDSel"
        sig=[]
    case "getPolygonIDSel"
        sig=[]
    otherwise
        fprintf("signature for function %s not found.\n",fnName),
        sig=[];
end


       
     