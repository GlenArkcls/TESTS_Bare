function sig = signatureOf(fnName)
switch fnName
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
    case "createPointSet"
        sig=["[c","id"];
    case "putPointSetData"
        sig=["id","i32","[d","[d","[d","i32"];
	case "createWellRoot"
        sig=[];
	case "createWell"
        sig=["[c"];
	case "putWellHead"
        sig=["id","d","d"];
	case "putWellTrack"
        sig=["id","[d","[d","[d","[c","d"];
	case "createLog"
        sig=["id","[c"];
	case "putLogData"
        sig=["id","[d","d","d"];
	case "getWellGeom"
        sig=["id"];
	case "getWellTrajectory"
        sig=["id"];
	case "getWellData"
        sig=["id"];
    otherwise
        fprintf("signature for function %s not found.\n",fnName),
        sig=[];
end


       
     