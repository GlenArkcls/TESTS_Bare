function [translated] = translateData(input,typecode)
input=input{1};

switch typecode
    case 'd'
        translated=double(input);
    case 's'
        translated=single(input);
    case 'i32'
        translated=int32(input);
    case 'i64'
        translated=int64(input);
    case '[d'
        translated=double(cell2mat(input));
        
    case '[s'
         translated=single(cell2mat(input));
             
    case '[i32'
        translated=int32(cell2mat(input)); 
    case '[i64'
        translated=int64(cell2mat(input));
        
    case '[[d'
        translated=double(cellArrayToMat(input));
    case '[[s'
        translated=single(cellArrayToMat(input));
    case '[[i32'
        translated=int32(cellArrayToMat(input));
    case '[[i64'
        translated=int32(cellArrayToMat(input));
    otherwise
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