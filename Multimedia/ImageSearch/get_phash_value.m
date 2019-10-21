%% phash function
function [ phash_value ] = get_phash_value( I )
%   From image data count phash value
%   the input ought to be cdata
%   the oughtput is phash value

%% I = PicData;
% resize to 32*32 pixels
I_R = imresize(I, [32 32]);
% rgb to gray
if ndims(I_R) == 3
    I_Gray = rgb2gray(I_R);
end
% DCT transform

I_DCT = dct2(I_Gray);
% I_DGray2 = double(I_Gray) - 128;
% I_DCT2 = dct2(I_DGray2);

% save low frequency
I_LF = I_DCT(1:8,1:8);

% count average value
I_avg = sum(sum(I_LF))/(size(I_LF,1)*size(I_LF,2));
value = (double(I_LF) - I_avg*ones(8))>0;

% t = 1;
% for i=1:8
%     for j=1:8
%         phash_value(t) = value(i,j);
%         t = t + 1;
%     end
% end
phash_value = transpose(value(:));

end
