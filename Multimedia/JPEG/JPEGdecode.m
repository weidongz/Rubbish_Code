function [] = JPEGdecode()
%% Initialize
clear
m = input('输入宽度像素： ');
n = input('输入长度像素： ');
% n=512; %row
% m=512; %col
blocsFiles = n/8;
blocsColumnes = m/8;
JPEG_decoded = zeros(n,m); %存储解码后数据
% Alpha = 5;
Alpha = input('输入编码时的压缩系数： ');
% the previous DC coefficient.
DCPrev = 0;

Y_Table = ...
   [16 11 10 16 24 40 51 61;  
	12 12 14 19 26 58 60 55;  
	14 13 16 24 40 57 69 55;  
	14 17 22 29 51 87 80 62;  
	18 22 37 56 68 109 103 77;  
	24 35 55 64 81 104 113 92;  
	49 64 78 87 103 121 120 101;  
	72 92 95 98 112 100 103 99 ];
%亮度量化表

Y_Table = Y_Table.*Alpha;
%% load JPEGCODE.txt
% jpeg_bitstream = textscan('JPEGCODEREF.txt','%s',-1);
fileID = fopen('.\JPEGCODE.txt');
JPEG_bitstream = textscan(fileID,'%c');
fclose(fileID);

% class(jpeg_bitstream1{1})
% 从元胞数组中提取出char
JPEG_bitstream  = JPEG_bitstream{1}';

%%
for i=1:blocsFiles
    for j=1:blocsColumnes
        % DC Decodification
        seqCoef = char.empty;
        [valor, numBits] = DCdecode(JPEG_bitstream);
        JPEG_bitstream = JPEG_bitstream(numBits+1:end);
        coeficient = DCPrev + valor;
        seqCoef = coeficient;
        DCPrev = coeficient;
        
        % AC Decodification
        while (length(seqCoef)<64)
            [coef,numZeros,numBits,EndOfBlock] = ACdecode(JPEG_bitstream);
            if (EndOfBlock)
                for k=1:(64-length(seqCoef))
                    seqCoef = [seqCoef 0];
                end
                JPEG_bitstream = JPEG_bitstream(5:end);
            else
                for l=1:numZeros
                    seqCoef = [seqCoef 0];
                end
                seqCoef = [seqCoef coef];
                JPEG_bitstream = JPEG_bitstream(numBits+1:end);
            end
        end
        sequencia_decodificada{i,j}=seqCoef;
        
        bloc = izigzag(seqCoef,8,8);
        bloc = bloc.*Y_Table;
        bloc = round(idct2(bloc)+128);
        JPEG_decoded(i*8-7:i*8,j*8-7:j*8) = bloc;
    end
end

JPEG_decoded=uint8(JPEG_decoded);
%  subplot(1,2,1);
imshow(JPEG_decoded);
title('Compressed Image');
%  subplot(1,2,2);
% [filename,pathname] = uigetfile({'*.bmp'},'Pick an image');
% str = [pathname filename];
% Gray = imread(str);
%  imshow(uint8(Gray));
%  title ('Original Image');
end