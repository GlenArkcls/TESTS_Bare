function [response] = GDSWrapper(fn,server,varargin)
% GDSWrapper forwards a call to GeoDataSync system, handling transforms of
% input and output arguments
% First we have to swap the varagin from a 1*N to an N*1
% Additionally we have to ensure everything is of the correct data type,
% which is done by getting a signature from 'signatureOf' then using the
% typecodes to translate the arguments into the appropriate data type
% using 'translateData'

args={};

if ~isempty(varargin)
    % args to GDS need to be an N*1 not 1*N cell array, so we have
    % to transpose, and each cell must also
    % potentially be translated to the right data type
    sig=signatureOf(fn);
    args=arrayfun(@(v,s)translateData(v,s),varargin,sig(1:length(varargin)),'UniformOutput',false)';
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
outsz=size(tmpOutput);
shouldRemap=iscell(tmpOutput) && outsz(2)>1 &&~isIDFunction(fn);
if shouldRemap
    %Make an N*1 cell array for output
    response=cell(outsz(1),1);
    for i=1:outsz(1)
        %And into each of these cells map an 1*M cell array
        response{i,:}=tmpOutput(i,:);
    end
else
    %structures,N*1 cell arrays and 1*N arrays that are IDs
    %go straight through
    response=tmpOutput;
end

end




