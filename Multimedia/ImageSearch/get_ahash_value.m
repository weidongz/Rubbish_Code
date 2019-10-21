%% ahash function
function [ ahash_value ] = get_ahash_value( I )

%% I = PicData;
    % resize to 8*8 pixels, use 'bicubic' method to resize
%     I_R = imresize(I, [8 8], 'bilinear');
    I_R = imresize(I, [8 8]);
    % rbg to gray
    if ndims(I_R) == 3
        I_Gray = rgb2gray(I_R);
    end
    % count average value
    I_avg = sum(sum(I_Gray))/(size(I_Gray,1)*size(I_Gray,2));
%     if pixel(i,j) > averge,it will be replaced by 1, otherwise 0
%     value = double(I_Gray) - I_avg*ones(8);
    value = (double(I_Gray) - I_avg*ones(8))>0;

    t = 1;
    for i=1:8
        for j=1:8
            ahash_value(t) = value(i,j);
            t = t + 1;
        end
    end
    
end