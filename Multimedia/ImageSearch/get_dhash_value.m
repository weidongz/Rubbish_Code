%% dhash function
function [ dhash_value ] = get_dhash_value( I )
%   From image data get dhash
%   the input ought to be cdata
%   the oughtput is dhash value

%% I = PicData;
% resize to 8*9 pixels
I_R = imresize(I, [8 9]);
I_Gray = rgb2gray(I_R);
I_DGray = [I_Gray(1:8,2:9), zeros(8,1)];
value = (I_Gray - I_DGray)>0;
value = value(1:8,1:8);
dhash_value = transpose(value(:));
end