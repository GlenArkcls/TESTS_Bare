function [translated] = translateData(input,dtype)
input=input{1};

switch dtype
    case GSOType.tnDouble
        translated=double(input);
    case GSOType.tnFloat
        translated=single(input);
    case GSOType.tnInt32
        translated=int32(input);
    case GSOType.tnInt64
        translated=int64(input);
    case GSOType.tnVDouble
        if iscell(input{1})
           translated= double(cellArrayToMat(input));
        else
           translated=double(cell2mat(input));
        end 
    case GSOType.tnVFloat
        if iscell(input{1})
           translated= single(cellArrayToMat(input));
        else
           translated=single(cell2mat(input));
        end
    case GSOType.tnVInt32
        if iscell(input{1})
           translated=int32(cellArrayToMat(input));
        else
           translated=int32(cell2mat(input));
        end  
    otherwise
	%Strings and string arrays go straight through
        translated=input;
end
end

function mat=cellArrayToMat(cellarray)
sz0=size(cellarray);
sz1=size(cellarray{1,1});
    mat=zeros(sz0(2),sz1(2));
    for i=1:sz0(2)
        mat(i,:)=(cell2mat(cellarray{1,i}));
    end
end