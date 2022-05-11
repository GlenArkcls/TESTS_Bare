function [server] = connect(port)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
disp(port)
try
    server = CliConnection(port);
   
catch
    disp("was an exception")
    return;
end
