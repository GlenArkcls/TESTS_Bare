function [response] = GDSWrapper(fn,server,varargin)
% GDSWrapper forwards a call to GeoDataSync system, handling transforms of
% input and output arguments
% First we have to swap the varagin from a 1*N to an N*1
% Additionally we have to ensure everything is of the correct data type,
% which is done by getting a signature as a list of types from 'signatureOf' then using the
% types to translate the arguments into the appropriate data type using 'translateData'

args={};


if ~isInternal(fn) && ~isempty(varargin)
    % args to GDS need to be an N*1 not 1*N cell array, so we have
    % to transpose, and each cell must also
    % potentially be translated to the right data type
	sig=signatureOf(fn);
	args=arrayfun(@(v,s)translateData(v,s),varargin,sig(1:length(varargin)),'UniformOutput',false)';
else
	%this line currently only for hideErrorMessages argument
    args=varargin;
end

% Call the GDS system
tmpOutput=GeoDataSync(fn,server,args);



% Now we may need to remap the outputs
% If we have a cell array that is not 1*N or N*1 we cannot pass that back to
% Python, so we are going to pack each row into a single cell.
% We turn an N*M cell array into an N*1 array. We do this even for
% a 1*M, because it could be the only item on a return of a list of items 
% e.g. a list of IDs. However, an actual ID should not be collapsed so
% we need to check for that as a special case - other cases may arise
% and developers of the test system need to be aware of this
if iscell(tmpOutput) && size(tmpOutput,2)>1 &&~isIDFunction(fn)
    response=remapCellArray(tmpOutput);
elseif isstruct(tmpOutput)
    response=remapStruct(tmpOutput);
else
    %N*1 cell arrays and 1*N arrays that are IDs
    %go straight through
    response=tmpOutput;
end

end


function [out] =isInternal(fnName)
	%These two functions are not in the function defintions because they are
	%purely internal
    out=strcmpi('hideErrorMessages',fnName) || strcmpi('getLastError',fnName);
end
 
function [remapped]=remapStruct(inp)
    remapped=struct;
    fn=fieldnames(inp);
    for i=1:size(fn,1)
        v=inp.(fn{i});
        outsz=size(v);
        if iscell(v) && outsz(2)>1 &&~isIDField(fn{i})
            v=remapCellArray(v);
        end
        remapped.(fn{i})=v;
    end
end

function [remapped] = remapCellArray(inp)
%Make an N*1 cell array for output
    outsz=size(inp);
    remapped=cell(outsz(1),1);
    for i=1:outsz(1)
        remapped{i,:}=inp(i,:);
    end
end

function [out] = isIDFunction(fnName)
%isIDFunction returns true of the GDS function returns a single ID
%  
out=strcmpi(fnName(1:6),"create") || strcmpi(fnName,"getParentID");
if ~out
    out=strcmpi(fnName(end-4:end),"IDSel"); %&& ~strcmpi(fnName(10:15),"Inters");
end
end

function ret=isIDField(name)
    ret=strcmpi(name(end-1:end),"ID");
end


