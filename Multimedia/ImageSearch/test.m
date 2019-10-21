
%% store ahash top 5 picname in AHashResult
top=5;%求最接近的top张图片
dist = [];
for i=1:len
    for col=1:len
        dist(i,col) = sum(bitxor(AHashResult{1,i},AHashResult{1,col}));%Hamming distance
        %     dist(2,col) = AHashResult{2,col};%PicNamne
    end
    [dist1,index] = sort(dist(i,:));
    for tmp=1:top
        AHashResult{tmp+3,i} = AHashResult{3,index(tmp)};
    end
end

%% ahash Serach
clear
load AHashResult.mat
[FileName,FileDir] = uigetfile({'*.jpg'},'Pick an image');
% for tmp=1:size(AHashResult,2)
%     if strcmp(filename,AHashResult{2,tmp})
%         subplot(1,3,1);
%         imshow(AHashResult{3,tmp})
%         title('Original Image');
%         subplot(1,3,2);
%         imshow(AHashResult{4,tmp})
%         title('First Common Image');
%         subplot(1,3,3);
%         imshow(AHashResult{5,tmp})
%         title('Second Common Image');
%     end
% end
% FilePath = fullfile(FileDir, FileName);
FilePath = [FileDir FileName];
PicData = imread(FilePath);
AHashData = get_ahash_value(PicData);
dist = [];
for i=1:size(AHashResult,2)
        dist(i,1) = sum(bitxor(AHashResult{1,i},AHashData));%Hamming distance
        [dist1,index] = sort(dist(:,1));
end
index = index(dist1<=10);
for tmp=1:3
    subplot(1,3,tmp);
    if tmp <= length(index)
        imshow([FileDir AHashResult{3,index(tmp)}])
    else
        imshow(1)
        title("no similar image")
    end
end

%% phash Serach
clear
load PHashTable.mat
[FileName,FileDir] = uigetfile({'*.jpg'},'Pick an image');
FilePath = [FileDir FileName];
PicData = imread(FilePath);
PHashData = get_phash_value(PicData);
dist = [];
for i=1:size(PHashTable,2)
        dist(i,1) = sum(bitxor(PHashTable{1,i},PHashData));%Hamming distance
        [dist1,index] = sort(dist(:,1));%dist = 0, the same image; 1 < dist < 5, similar; dist>10, different
end

for tmp=1:3
    subplot(1,3,tmp);
    imshow([FileDir PHashTable{3,index(tmp)}])
end

%% dhash Serach
clear
load DHashTable.mat
[FileName,FileDir] = uigetfile({'*.jpg'},'Pick an image');
FilePath = [FileDir FileName];
PicData = imread(FilePath);
DHashData = get_dhash_value(PicData);
dist = [];
for i=1:size(DHashTable,2)
        dist(i,1) = sum(bitxor(DHashTable{1,i},DHashData));%Hamming distance
        [dist1,index] = sort(dist(:,1));%dist = 0, the same image; 1 < dist < 5, similar; dist>10, different
end

for tmp=1:3
    subplot(1,3,tmp);
    imshow([FileDir DHashTable{3,index(tmp)}])
end