function [ ] = BMP2JPEG()
%% Initialize
clear all
clc

%% Load image
%tr_dir=uigetdir({},'选择文件夹');
% picstr = dir([tr_dir '\lena.bmp']);
% path = input('Please enter the filename: ');
% Gray = imread(path);
% [filename,pathname]=uigetfile({'*.bmp'},'Pick an image','C:\Users\Public\Pictures\Sample Pictures');
[filename,pathname] = uigetfile({'*.bmp'},'Pick an image');
str = [pathname filename];
img = imread(str);
 
%用于计算压缩比,压缩前height×length×Coff bytes
img_height = size(img,1);
img_width = size(img,2);
Coff = size(img,3);

% rbg to gray
if ndims(img)==3
    Gray=rgb2gray(img); %将彩色图像转换为灰度图像
else
    Gray=img;
end

%压缩系数
% Alpha = 5;
Alpha = input('输入大于1的压缩系数： ');
%% Create 8*8  DCT matrix and do FDCT
DGray = double(Gray)-127*ones(size(Gray,1),size(Gray,2));
DCTFunc = @dct2; %2D DCT transform
DCTGray = blkproc(DGray,[8 8],DCTFunc);

% T = dctmtx(8);
% DCTY=blkproc(Y,[8 8],'P1*x*P2',T,T');

%% Quantization量化
%亮度量化表
Y_Table = ...
    [16 11 10 16 24 40 51 61;
    12 12 14 19 26 58 60 55;
    14 13 16 24 40 57 69 55;
    14 17 22 29 51 87 80 62;
    18 22 37 56 68 109 103 77;
    24 35 55 64 81 104 113 92;
    49 64 78 87 103 121 120 101;
    72 92 95 98 112 100 103 99 ];

Y_Table = Y_Table.*Alpha;
% 采用细量化
QuanGray = blkproc(DCTGray, [8 8], 'round(x./P1)', Y_Table);


%% Zigzag重排
ZigZagOrder = [1 2 9 17 10 3 4 11 18 25 33 26 19 12  ...
    5 6 13 20 27 34  41 49 42 35 28 21 14 7 8  ...
    15 22 29 36 43 50 57 58 51 44 37 30 23 16 24  ...
    31 38 45 52 59 60 53 46 39 32 40 47 54 61 62  ...
    55 48 56 63 64];

% 每一列对应了一个8*8的块, 64*4096，即4096个8*8的块
ColGray = im2col(QuanGray', [8 8],   'distinct');
% ZigZag rearrange
ZigGray = ColGray(ZigZagOrder, :);

col_end = size(ZigGray,2); %4096，8×8块数
row_end = size(ZigGray,1);
%% DPCM
% DCPM编码
DZigGray = [0 ,ZigGray(1,1:(col_end-1))];
DPCM = ZigGray(1,:) - DZigGray;

% 获取中间符号的类别，计算DPCM符号所需的位数SSSDPCM
SSSDPCM = [];

for col=1:col_end
    if DPCM(col) == 0
        SSSDPCM = [SSSDPCM 0];
    else
        SSSDPCM = [SSSDPCM length(dec2bin(abs(DPCM(col))))];
    end
end

% JPEG推荐的亮度直流霍夫曼编码表
DCHuffTab = ["00" "010" "011" "100" "101" "110" "1110" "11110" "111110" "1111110" "11111110" "111111110"];
%[dc_cat, ~, dc_code] = textread('DC_Huffman_Table.txt', '%s%s%s');

% 对DC符号位数SSS编码
DCSSSVec = [];
for col=1:col_end
    DCSSSVec = [DCSSSVec DCHuffTab(SSSDPCM(col)+1)];
end

% 对DC的值DPCM编码(查VLI)
DCValueVec = [];
for col=1:col_end
    DCValue = dec2bin(abs(DPCM(col)));
    if(DPCM(col) == 0)
        DCValue = '';
    end
    if(DPCM(col)<0)
        for i=1:length(DCValue)
            if(DCValue(i)=='1')
                DCValue(i)='0';
            else
                DCValue(i)='1';
            end
        end
    end
    DCValueVec = [DCValueVec string(DCValue)];
end

%DC SSS,DPCM编码拼接
DCCodeVec = strcat(DCSSSVec,DCValueVec);

%% AC编码
ACCodeVec = [];
for col = 1:col_end
    seqCoef = ZigGray(:,col);%获取当前列数值
    NumZeros = 0;           %对0计数
    CodeAc = [];        %Ac编码
    %     CatACVec = [];    %记录AC编码类别
    for i=2:row_end
        % 如果以后的AC全是0，插入EOB（1010）
        if (sum(abs(seqCoef(i:end)))==0) %max(seq(i:end)) == 0
            CodeAc = [CodeAc '1010'];
            break
        else
            %  如果其中某个单元的0的个数超过16，则需要分成每16个一组，F/0编码为 '11111111001'
            if(NumZeros == 16)
                CodeAc = [CodeAc  '11111111001'];
                NumZeros = 0;
            else
                if (seqCoef(i)~=0)
                    % 计算AC类别
                    catAc = length(dec2bin(abs(seqCoef(i))));
                    %                     CatACVec = [CatACVec; catAc];
                    
                    % Run/Size（16进制）
                    ACrun = dec2hex(catAc);
                    ACSize = dec2hex(NumZeros);
                    runsize = [ACSize ACrun];
                    % Huffman编码
                    codeCatAc = code_category_AC(runsize);
                    
                    % 对非0值编码
                    ACValue = dec2bin(abs(seqCoef(i)));
                    if(seqCoef(i)<0)
                        for AC_index=1:length(ACValue)
                            if(ACValue(AC_index)=='1')
                                ACValue(AC_index)='0';
                            else
                                ACValue(AC_index)='1';
                            end
                        end
                    end
                    
                    %组合在一起
                    CodeAc = [CodeAc codeCatAc ACValue];
                    NumZeros = 0;
                else
                    NumZeros = NumZeros+1;
                end
            end
        end
    end
    ACCodeVec = [ACCodeVec, string(CodeAc)];
end

%% Write it to txt
% CodeVec = [];
% for i = 1:col_end
%     CodeVec(i) = strcat(DCCodeVec(i),ACCodeVec(i));
% end
CodeVec = [DCCodeVec;ACCodeVec];
%CodeVec = CodeVec';
%str2num(CodeVec)
%JPEGCode = char.empty;
%‘w’,则代表写入，它写一次数据都会覆盖之前的数据
fid = fopen('JPEGCODE.txt','w');
fprintf(fid,'%s',CodeVec);
fclose(fid);

%%计算压缩比，压缩效率，PSNR
% 压缩比
OringalSize= img_height * img_width * Coff * 8; % bits
% NumVec = str2num(CodeVec);
CompressSize = 0;
for i = 1:2
    for j=1:size(CodeVec,2)
        CompressSize = CompressSize + length( char(CodeVec(i,j)) );
    end
end
CompressRate = OringalSize/CompressSize;
fprintf('压缩比是 %.4f\n', CompressRate)

% 压缩效率
% 计算entropy(DC系数概率与AC系数概率P(i)）,L_Huf = 平均码长 
% CompressEfficiency = Entrophy/L_Huf;
% fprintf('压缩效率是 %.4f\n', CompressEfficiency)
end