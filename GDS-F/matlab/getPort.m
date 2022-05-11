function [port] = getPort()
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
port = str2double(cell2mat(inputdlg('Please enter the port number provided by your Petrel developer plug-in','Enter Port Number')));

end