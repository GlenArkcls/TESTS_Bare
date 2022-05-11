function [out] = isIDFunction(fnName)
%isIDFunction returns true of the GDS function returns a single ID
%  
out=strcmpi(fnName(1:6),"create") || strcmpi(fnName,"getParentID");
end